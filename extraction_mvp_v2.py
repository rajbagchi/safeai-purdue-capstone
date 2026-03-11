# -*- coding: utf-8 -*-
"""
Clinical Guidelines — PDF Extraction Pipeline (Stage 1)
========================================================
Features:
  - Layout-aware parsing with Docling
  - Image region extraction + OCR (RapidOCR)
  - Table linearisation to Natural Language Logic
  - Benchmark accuracy against configurable ground truth
  - Speed metrics
  - Pass / Fail report for tables AND images

Config-driven: reads document-specific settings from pipeline_config.json
    python extraction_mvp_v2.py                         # uses default config
    python extraction_mvp_v2.py --config configs/X.json # uses custom config
"""

# ─────────────────────────────────────────────────────────────────────────────
# 0.  INSTALL DEPENDENCIES  (uncomment in Colab / fresh env)
# ─────────────────────────────────────────────────────────────────────────────
# %pip install docling rapidocr-onnxruntime pillow -q

# ─────────────────────────────────────────────────────────────────────────────
# 1.  IMPORTS
# ─────────────────────────────────────────────────────────────────────────────
import os
import re
import time
import json
import hashlib
import multiprocessing
from pathlib import Path
from typing import Optional

# ── Docling ──────────────────────────────────────────────────────────────────
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.datamodel.base_models import InputFormat

# ── Image / OCR ──────────────────────────────────────────────────────────────
from PIL import Image
import numpy as np

# ── Pipeline config ──────────────────────────────────────────────────────────
from pipeline_config import (
    load_config, get_pdf_path, get_document_title, get_ground_truth,
    get_all_table_keywords, get_benchmark_pages,
)

# ─────────────────────────────────────────────────────────────────────────────
# 2.  CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────
CONFIG = load_config()
PDF_PATH = get_pdf_path(CONFIG)
BENCHMARK_PAGES = get_benchmark_pages(CONFIG)
GROUND_TRUTH = get_ground_truth(CONFIG)
OUTPUT_DIR = Path("extraction_output")
OUTPUT_DIR.mkdir(exist_ok=True)

# ── Speed optimisation settings ───────────────────────────────────────────
USE_CACHE = True          # Cache Docling conversion result to skip re-processing
PAGE_RANGES = None        # None = full PDF; list of (start, end) 1-indexed inclusive
                          # e.g. [(170, 215)] to extract only pages 170–215
N_WORKERS = 1             # 1 = sequential (default); 0 = auto (cpu_count // 2); N = N workers
CACHE_DIR = OUTPUT_DIR / "cache"
CACHE_DIR.mkdir(exist_ok=True)

# ─────────────────────────────────────────────────────────────────────────────
# 2b. SPEED OPTIMISATION HELPERS (cache / page-range / parallel)
# ─────────────────────────────────────────────────────────────────────────────

def _cache_key(pdf_path: str, page_ranges) -> str:
    """Generate a cache key from PDF identity + page-range config."""
    stat = os.stat(pdf_path)
    raw = f"{os.path.abspath(pdf_path)}|{stat.st_size}|{stat.st_mtime_ns}"
    if page_ranges:
        raw += f"|{page_ranges}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


def _derive_page_map(page_ranges):
    """Map subset page numbers (1-indexed) → original PDF page numbers.

    Returns None if page_ranges is None (full-document mode).
    """
    if not page_ranges:
        return None
    page_map = {}
    subset_page = 1
    for start, end in page_ranges:
        for orig in range(start, end + 1):
            page_map[subset_page] = orig
            subset_page += 1
    return page_map


def _effective_workers() -> int:
    """Determine actual number of parallel workers."""
    if N_WORKERS == 1:
        return 1
    if N_WORKERS == 0:
        return max(2, multiprocessing.cpu_count() // 2)
    return N_WORKERS


def _create_subset_pdf(pdf_path: str, page_ranges: list) -> str:
    """Extract specific page ranges into a temporary PDF using PyMuPDF.

    Returns the path to the subset PDF (stored in CACHE_DIR).
    """
    import fitz
    src = fitz.open(pdf_path)
    dst = fitz.open()
    for start, end in page_ranges:
        dst.insert_pdf(src, from_page=start - 1, to_page=min(end, len(src)) - 1)
    subset_path = str(CACHE_DIR / "subset.pdf")
    dst.save(subset_path)
    dst.close()
    src.close()
    return subset_path


def _split_pdf_into_chunks(pdf_path: str, n_chunks: int) -> list:
    """Split a PDF into n_chunks temporary files for parallel processing.

    Returns list of dicts with chunk_id, path, page_offset (1-indexed), n_pages.
    """
    import fitz
    src = fitz.open(pdf_path)
    total = len(src)
    chunk_size = max(1, -(-total // n_chunks))  # ceiling division

    chunks = []
    for i in range(n_chunks):
        start = i * chunk_size
        end = min(start + chunk_size, total)
        if start >= total:
            break
        chunk_doc = fitz.open()
        chunk_doc.insert_pdf(src, from_page=start, to_page=end - 1)
        chunk_path = str(CACHE_DIR / f"chunk_{i}.pdf")
        chunk_doc.save(chunk_path)
        chunk_doc.close()
        chunks.append({
            "chunk_id": i,
            "path": chunk_path,
            "page_offset": start + 1,   # 1-indexed
            "n_pages": end - start,
        })
    src.close()
    return chunks


def _convert_chunk_worker(chunk_info: dict) -> dict:
    """Convert a single PDF chunk.  Runs in a spawned worker process.

    Must be a top-level function so multiprocessing can pickle it.
    """
    import time as _time
    t0 = _time.perf_counter()

    converter = build_converter()
    result = converter.convert(chunk_info["path"])
    doc = result.document
    elapsed = _time.perf_counter() - t0

    # Save DoclingDocument as JSON for the main process to load
    out_path = chunk_info["path"].replace(".pdf", "_doc.json")
    doc.save_as_json(out_path)

    # Clean up chunk PDF
    try:
        os.unlink(chunk_info["path"])
    except Exception:
        pass

    return {
        "chunk_id": chunk_info["chunk_id"],
        "doc_json_path": out_path,
        "page_offset": chunk_info["page_offset"],
        "n_pages": chunk_info["n_pages"],
        "n_tables": len(doc.tables),
        "elapsed_s": round(elapsed, 1),
    }


# ─────────────────────────────────────────────────────────────────────────────
# 3.  GROUND-TRUTH SNIPPETS  (loaded from pipeline_config.json)
#     Each entry: {"page": int, "type": "text"|"table"|"image", "must_contain": [str, ...]}
#     Page numbers are PDF page numbers (1-indexed), NOT printed page numbers.
# ─────────────────────────────────────────────────────────────────────────────
# GROUND_TRUTH is loaded from config at the top of this file.

# ─────────────────────────────────────────────────────────────────────────────
# 4.  HELPER: DOCLING CONVERTER  (with image pipeline enabled)
# ─────────────────────────────────────────────────────────────────────────────

def build_converter() -> DocumentConverter:
    """Return a DocumentConverter that extracts text, tables AND images.

    batch_size=1 is set to avoid the 'padding=True' tensor error that occurs
    when docling-ibm-models tries to batch pages of different sizes together.
    This is a known incompatibility with newer versions of transformers.
    If you upgrade: pip install transformers==4.40.2 docling-ibm-models==2.0.6
    """
    from docling.datamodel.pipeline_options import EasyOcrOptions
    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = False          # PDF has selectable text; RapidOCR handles images separately
    pipeline_options.do_table_structure = True
    pipeline_options.images_scale = 2.0      # higher DPI for OCR accuracy
    pipeline_options.generate_picture_images = True  # ← needed for image crops

    # ── batch_size=1 prevents the 'Unable to create tensor / padding=True'
    #    error caused by transformers / docling-ibm-models version mismatch
    try:
        pipeline_options.page_batch_size = 1
    except Exception:
        pass  # older docling versions may not expose this option

    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
        }
    )
    return converter


# ─────────────────────────────────────────────────────────────────────────────
# 5.  HELPER: TABLE → NATURAL LANGUAGE LOGIC
# ─────────────────────────────────────────────────────────────────────────────

def table_to_nll(table_md: str) -> str:
    """
    Convert a Markdown table to Natural Language Logic sentences so that
    LLMs can reason about it without alignment hallucinations.

    Example row:  | 5–<15 kg | 1 tablet | 2 × daily | 3 days |
    Output:       "IF body weight is 5–<15 kg, THEN the dose is 1 tablet,
                   given 2 × daily for 3 days."
    """
    lines = [l.strip() for l in table_md.strip().split("\n") if l.strip()]
    if not lines:
        return ""

    # Extract headers (first non-separator row)
    headers = []
    data_lines = []
    for line in lines:
        if "---" in line:
            continue
        cells = [c.strip() for c in line.split("|") if c.strip()]
        if not headers:
            headers = cells
        else:
            data_lines.append(cells)

    if not headers or not data_lines:
        return table_md  # fallback: return as-is

    nll_sentences = []
    for row in data_lines:
        if not row or not any(row):
            continue
        parts = []
        for h, v in zip(headers, row):
            if v:
                parts.append(f"{h} is {v}")
        if parts:
            # first part becomes the IF condition, rest become THEN clauses
            condition = parts[0]
            outcomes = ", ".join(parts[1:]) if len(parts) > 1 else ""
            sentence = f"IF {condition}"
            if outcomes:
                sentence += f", THEN {outcomes}."
            nll_sentences.append(sentence)

    return "\n".join(nll_sentences)


# ─────────────────────────────────────────────────────────────────────────────
# 5b. HELPER: TABLE CLASSIFICATION
# ─────────────────────────────────────────────────────────────────────────────

# Keywords used to classify each table into a category.
# Only dosing and clinical_management tables get NLL linearisation.

_DOSING_KEYWORDS = get_all_table_keywords(CONFIG)
_EVIDENCE_KEYWORDS = [
    "grade", "quality of evidence", "relative effect", "95% ci",
    "no. of par", "no of par", "cochrane", "rr ", "systematic review",
    "assumed risk", "corresponding risk", "trials)",
]
_STRUCTURAL_KEYWORDS = [
    "contents", "annex", "preparation of the guidelines",
    "abbreviation", "glossary", "introduction......",
]
_CLINICAL_MGMT_KEYWORDS = [
    "manifestation", "complication", "immediate management",
    "clinical feature", "danger sign", "referral", "severity",
]


def classify_table(table_md: str) -> str:
    """Classify a table as dosing | evidence | structural | clinical_management | other.

    Classification is based on keyword matches in the markdown content.
    Returns one of: 'dosing', 'evidence', 'structural', 'clinical_management', 'other'.
    """
    md_lower = table_md.lower()

    def _score(keywords):
        return sum(1 for kw in keywords if kw in md_lower)

    scores = {
        "dosing": _score(_DOSING_KEYWORDS),
        "evidence": _score(_EVIDENCE_KEYWORDS),
        "structural": _score(_STRUCTURAL_KEYWORDS),
        "clinical_management": _score(_CLINICAL_MGMT_KEYWORDS),
    }
    best = max(scores, key=scores.get)
    if scores[best] >= 2:
        return best
    return "other"


# ─────────────────────────────────────────────────────────────────────────────
# 6.  HELPER: IMAGE OCR  (RapidOCR) — engine cached as singleton
# ─────────────────────────────────────────────────────────────────────────────

_ocr_engine = None

def _get_ocr_engine():
    """Lazy-init singleton for RapidOCR to avoid re-loading the model per image."""
    global _ocr_engine
    if _ocr_engine is None:
        from rapidocr_onnxruntime import RapidOCR
        _ocr_engine = RapidOCR()
    return _ocr_engine

def ocr_image(pil_image: Image.Image) -> str:
    """Run RapidOCR on a PIL Image and return extracted text."""
    try:
        engine = _get_ocr_engine()
        img_array = np.array(pil_image.convert("RGB"))
        result, _ = engine(img_array)
        if result:
            return " ".join([line[1] for line in result])
        return ""
    except ImportError:
        return "[RapidOCR not installed — pip install rapidocr-onnxruntime]"
    except Exception as e:
        return f"[OCR error: {e}]"


# ─────────────────────────────────────────────────────────────────────────────
# 7.  CORE EXTRACTION FUNCTION
# ─────────────────────────────────────────────────────────────────────────────

def extract_document(pdf_path: str) -> dict:
    """
    Full extraction pipeline with caching, page-range, and parallel support.
    Returns a dict with: text, tables, images, nll_tables, timings.
    """
    print(f"\n{'='*70}")
    print(f"  CLINICAL GUIDELINES — EXTRACTION PIPELINE (Stage 1)")
    print(f"{'='*70}")
    print(f"  Source : {pdf_path}")
    if PAGE_RANGES:
        total_subset = sum(e - s + 1 for s, e in PAGE_RANGES)
        print(f"  Pages  : {PAGE_RANGES} ({total_subset} pages)")
    n_workers = _effective_workers()
    if USE_CACHE:
        print(f"  Cache  : enabled")
    if n_workers > 1:
        print(f"  Workers: {n_workers}")
    print()

    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    page_map = _derive_page_map(PAGE_RANGES)

    # ── Step 1: Try loading from cache ─────────────────────────────────────
    doc_pairs = None   # list of (DoclingDocument, page_offset)
    t_build = 0.0
    t_convert = 0.0

    cache_path = CACHE_DIR / f"docling_{_cache_key(pdf_path, PAGE_RANGES)}.json"

    if USE_CACHE and cache_path.exists():
        try:
            from docling.datamodel.document import DoclingDocument
            print("📦 Loading from cache…")
            t1 = time.perf_counter()
            cached_doc = DoclingDocument.load_from_json(cache_path)
            t_convert = time.perf_counter() - t1
            doc_pairs = [(cached_doc, 0)]
            print(f"   ✅ Loaded in {t_convert:.2f}s  (skipped PDF conversion)")
        except Exception as e:
            print(f"   ⚠️  Cache load failed: {e}")

    # ── Step 2: Convert if no cache hit ────────────────────────────────────
    if doc_pairs is None:
        # Page-range subset
        actual_pdf = pdf_path
        if PAGE_RANGES:
            print(f"📄 Creating page subset…")
            actual_pdf = _create_subset_pdf(pdf_path, PAGE_RANGES)
            print(f"   ✅ Subset PDF: {total_subset} pages")

        # Skip parallel for small documents (overhead > benefit)
        if n_workers > 1:
            import fitz
            with fitz.open(actual_pdf) as f:
                est_pages = len(f)
            if est_pages < 50:
                print(f"   ({est_pages} pages — sequential is faster)")
                n_workers = 1

        if n_workers > 1:
            # ── Parallel conversion ────────────────────────────────────────
            print(f"\n🔄 Parallel conversion with {n_workers} workers…")
            chunks = _split_pdf_into_chunks(actual_pdf, n_workers)
            for c in chunks:
                print(f"   Chunk {c['chunk_id']}: {c['n_pages']} pages "
                      f"(offset {c['page_offset']})")

            t1 = time.perf_counter()
            ctx = multiprocessing.get_context("spawn")
            with ctx.Pool(n_workers) as pool:
                chunk_results = pool.map(_convert_chunk_worker, chunks)
            t_convert = time.perf_counter() - t1

            # Load each chunk's document
            from docling.datamodel.document import DoclingDocument
            doc_pairs = []
            for cr in sorted(chunk_results, key=lambda x: x["chunk_id"]):
                d = DoclingDocument.load_from_json(cr["doc_json_path"])
                doc_pairs.append((d, cr["page_offset"] - 1))
                print(f"   Chunk {cr['chunk_id']}: {cr['n_tables']} tables, "
                      f"{cr['elapsed_s']}s")
                try:
                    os.unlink(cr["doc_json_path"])
                except Exception:
                    pass
        else:
            # ── Sequential conversion ──────────────────────────────────────
            print("⚙️  Building Docling converter…")
            t0 = time.perf_counter()
            converter = build_converter()
            t_build = time.perf_counter() - t0
            print(f"   ✅ Converter ready in {t_build:.2f}s")

            print(f"\n🔄 Converting PDF…  (this may take a while for large docs)")
            t1 = time.perf_counter()
            conv_result = converter.convert(actual_pdf)
            doc = conv_result.document
            t_convert = time.perf_counter() - t1
            doc_pairs = [(doc, 0)]

            # Cache the DoclingDocument
            if USE_CACHE:
                try:
                    doc.save_as_json(cache_path)
                    size_mb = cache_path.stat().st_size / (1024 * 1024)
                    print(f"   💾 Cached: {cache_path.name} ({size_mb:.1f} MB)")
                except Exception as e:
                    print(f"   ⚠️  Cache save failed: {e}")

        print(f"   ✅ Conversion complete in {t_convert:.2f}s")

        # Clean up temp subset PDF
        if PAGE_RANGES and actual_pdf != pdf_path:
            try:
                os.unlink(actual_pdf)
            except Exception:
                pass

    # ── Summary ────────────────────────────────────────────────────────────
    total_pages = sum(len(d.pages) for d, _ in doc_pairs)
    total_tables = sum(len(d.tables) for d, _ in doc_pairs)
    total_images = sum(len(d.pictures) for d, _ in doc_pairs)
    print(f"   📄 Pages : {total_pages}")
    print(f"   📊 Tables: {total_tables}")
    print(f"   🖼️  Images: {total_images}")

    # ── Export full markdown text ─────────────────────────────────────────
    print("\n📝 Exporting full document text…")
    t2 = time.perf_counter()
    full_markdown = "\n\n".join(d.export_to_markdown() for d, _ in doc_pairs)
    t_text = time.perf_counter() - t2
    print(f"   ✅ Text export: {len(full_markdown):,} chars in {t_text:.2f}s")

    # ── Extract tables + classify + NLL ────────────────────────────────────
    print("\n📊 Extracting tables, classifying, and linearising…")
    t3 = time.perf_counter()
    tables = []
    table_idx = 0
    for d, offset in doc_pairs:
        for tbl in d.tables:
            table_idx += 1
            try:
                md = tbl.export_to_markdown(doc=d)
                tbl_type = classify_table(md)

                # Page provenance — remap for page-range and parallel modes
                page_no = tbl.prov[0].page_no if tbl.prov else None
                if page_no is not None and offset:
                    page_no = page_no + offset
                if page_map and page_no in page_map:
                    page_no = page_map[page_no]

                nll = table_to_nll(md) if tbl_type in ("dosing", "clinical_management") else ""

                tables.append({
                    "index": table_idx,
                    "page_no": page_no,
                    "classification": tbl_type,
                    "num_rows": tbl.data.num_rows,
                    "num_cols": tbl.data.num_cols,
                    "markdown": md,
                    "nll": nll,
                })
            except Exception as e:
                tables.append({"index": table_idx, "error": str(e)})
    t_tables = time.perf_counter() - t3

    # Summary by classification
    class_counts = {}
    for t in tables:
        c = t.get("classification", "error")
        class_counts[c] = class_counts.get(c, 0) + 1
    print(f"   ✅ {len(tables)} tables processed in {t_tables:.2f}s")
    print(f"      Classification: {class_counts}")

    # ── Extract images + OCR ──────────────────────────────────────────────
    print("\n🖼️  Extracting image regions and running OCR…")
    t4 = time.perf_counter()
    images = []
    image_idx = 0
    for d, offset in doc_pairs:
        for pic in d.pictures:
            image_idx += 1
            entry = {"index": image_idx}

            # Page provenance — remap for page-range and parallel modes
            page_no = pic.prov[0].page_no if pic.prov else None
            if page_no is not None and offset:
                page_no = page_no + offset
            if page_map and page_no in page_map:
                page_no = page_map[page_no]
            entry["page_no"] = page_no

            try:
                entry["caption"] = pic.caption_text(d) if hasattr(pic, "caption_text") else ""
            except Exception:
                entry["caption"] = ""

            try:
                pil_img = pic.get_image(d)
                if pil_img is not None:
                    if pil_img.width < 50 or pil_img.height < 50:
                        continue
                    img_path = OUTPUT_DIR / f"image_{image_idx:03d}.png"
                    pil_img.save(img_path)
                    entry["saved_path"] = str(img_path)
                    entry["width"] = pil_img.width
                    entry["height"] = pil_img.height
                    entry["ocr_text"] = ocr_image(pil_img)
                else:
                    entry["ocr_text"] = ""
                    entry["error"] = "get_image returned None"
            except Exception as e:
                entry["ocr_text"] = ""
                entry["error"] = str(e)

            images.append(entry)

    t_images = time.perf_counter() - t4
    print(f"   ✅ {len(images)} images processed in {t_images:.2f}s")

    timings = {
        "build_converter_s": round(t_build, 3),
        "convert_pdf_s": round(t_convert, 3),
        "export_text_s": round(t_text, 3),
        "process_tables_s": round(t_tables, 3),
        "process_images_s": round(t_images, 3),
        "total_s": round(t_build + t_convert + t_text + t_tables + t_images, 3),
    }

    return {
        "full_markdown": full_markdown,
        "tables": tables,
        "images": images,
        "timings": timings,
        "page_count": total_pages,
    }


# ─────────────────────────────────────────────────────────────────────────────
# 8.  BENCHMARK:  ACCURACY (dosing pp.173-178, severe malaria p.212)
# ─────────────────────────────────────────────────────────────────────────────

def compute_accuracy(extraction: dict) -> dict:
    """
    Check each ground-truth item against the extracted content.
    Returns pass/fail counts + per-item details.
    """
    print(f"\n{'='*70}")
    bp_label = f"Pages {BENCHMARK_PAGES[0]}–{BENCHMARK_PAGES[-1]}" if BENCHMARK_PAGES else "all ground truth"
    print(f"  ACCURACY BENCHMARK  ({bp_label})")
    print(f"{'='*70}")

    full_text_lower = extraction["full_markdown"].lower()
    tables_text     = " ".join(t.get("markdown", "") for t in extraction["tables"]).lower()
    images_text     = " ".join(
        (img.get("caption", "") + " " + img.get("ocr_text", ""))
        for img in extraction["images"]
    ).lower()

    results = []
    for gt in GROUND_TRUTH:
        gt_type = gt["type"]
        keywords = [kw.lower() for kw in gt["must_contain"]]

        if gt_type == "text":
            search_space = full_text_lower
        elif gt_type == "table":
            search_space = tables_text
        elif gt_type == "image":
            search_space = images_text
        else:
            search_space = full_text_lower

        found = [kw for kw in keywords if kw in search_space]
        missing = [kw for kw in keywords if kw not in search_space]
        passed = len(missing) == 0

        results.append({
            "page": gt["page"],
            "type": gt_type,
            "passed": passed,
            "found": found,
            "missing": missing,
        })

        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status}  Page {gt['page']:>3}  [{gt_type:5}]  "
              f"found={found}  missing={missing}")

    n_pass = sum(1 for r in results if r["passed"])
    n_fail = len(results) - n_pass
    accuracy_pct = (n_pass / len(results) * 100) if results else 0.0

    print(f"\n  Passes : {n_pass} / {len(results)}")
    print(f"  Fails  : {n_fail} / {len(results)}")
    print(f"  Accuracy: {accuracy_pct:.1f}%")

    return {
        "accuracy_pct": round(accuracy_pct, 1),
        "n_pass": n_pass,
        "n_fail": n_fail,
        "details": results,
    }


# ─────────────────────────────────────────────────────────────────────────────
# 9.  TABLE & IMAGE QUALITY REPORT
# ─────────────────────────────────────────────────────────────────────────────

def table_quality_report(tables: list) -> dict:
    """Run classification-aware structural validation checks on all extracted tables."""
    print(f"\n{'='*70}")
    print(f"  TABLE QUALITY REPORT  ({len(tables)} tables)")
    print(f"{'='*70}")

    passed = failed = skipped = 0
    flagged_for_review = []

    for tbl in tables:
        idx = tbl["index"]
        if "error" in tbl:
            print(f"  ⚠️  Table {idx:>3}: skipped (error: {tbl['error'][:60]})")
            skipped += 1
            continue

        md = tbl.get("markdown", "")
        tbl_type = tbl.get("classification", "other")
        page = tbl.get("page_no", "?")
        issues = []

        # Check 1: Has content
        if len(md.strip()) < 10:
            issues.append("nearly empty")

        # Check 2: Has headers
        lines = [l for l in md.split("\n") if "|" in l]
        if len(lines) < 2:
            issues.append("missing header row")

        # Check 3: Empty cells — only flag for dosing tables where every cell matters.
        # Evidence and structural tables legitimately have merged/empty cells.
        if tbl_type == "dosing":
            data_lines = [l for l in lines if "---" not in l][1:]
            empty_cell_rows = []
            for r_i, row in enumerate(data_lines, 1):
                cells = [c.strip() for c in row.split("|")[1:-1]]
                if any(c == "" for c in cells):
                    empty_cell_rows.append(r_i)
            if empty_cell_rows:
                issues.append(f"empty cells in rows {empty_cell_rows[:5]}")

        # Check 4: Special characters preserved (dosing tables only)
        if tbl_type == "dosing":
            has_special = any(ch in md for ch in ["≥", "≤", "<", ">", "±"])
            if not has_special:
                issues.append("dosing table may be missing special chars (≥ ≤ < >)")

        label = f"[{tbl_type:^20}] p.{page}"
        if issues:
            print(f"  ❌ FAIL Table {idx:>3} {label} ({tbl['num_rows']}r×{tbl['num_cols']}c): {'; '.join(issues)}")
            failed += 1
            if tbl_type == "dosing":
                flagged_for_review.append({"table_index": idx, "page": page, "issues": issues})
        else:
            print(f"  ✅ PASS Table {idx:>3} {label} ({tbl['num_rows']}r×{tbl['num_cols']}c)")
            passed += 1

    print(f"\n  Passes : {passed}")
    print(f"  Fails  : {failed}")
    print(f"  Skipped: {skipped}")
    if flagged_for_review:
        print(f"\n  ⚠️  {len(flagged_for_review)} DOSING tables flagged for clinical review:")
        for f in flagged_for_review:
            print(f"     Table {f['table_index']} (p.{f['page']}): {f['issues']}")

    return {
        "table_pass": passed,
        "table_fail": failed,
        "table_skip": skipped,
        "dosing_flagged": flagged_for_review,
    }


def image_quality_report(images: list) -> dict:
    """Check whether image regions were successfully extracted and OCR'd."""
    print(f"\n{'='*70}")
    print(f"  IMAGE QUALITY REPORT  ({len(images)} images)")
    print(f"{'='*70}")

    passed = failed = 0
    for img in images:
        idx = img["index"]
        issues = []

        if "error" in img:
            issues.append(img["error"][:80])

        ocr = img.get("ocr_text", "")
        if not ocr or len(ocr.strip()) < 5:
            issues.append("no OCR text extracted")

        w = img.get("width", 0)
        h = img.get("height", 0)
        if w < 50 or h < 50:
            issues.append(f"very small ({w}×{h}px)")

        caption = img.get("caption", "")
        if not caption:
            issues.append("no caption found")

        if issues:
            print(f"  ❌ FAIL Image {idx:>3}: {'; '.join(issues)}")
            failed += 1
        else:
            print(f"  ✅ PASS Image {idx:>3} ({w}×{h}px) caption='{caption[:50]}'")
            passed += 1

    print(f"\n  Passes : {passed}")
    print(f"  Fails  : {failed}")
    return {"image_pass": passed, "image_fail": failed}


# ─────────────────────────────────────────────────────────────────────────────
# 9b. DOSING TABLE PLAUSIBILITY CHECKS (Stage 3 — Automated Checks)
# ─────────────────────────────────────────────────────────────────────────────

def _parse_weight_range(cell: str) -> tuple:
    """Try to parse a weight band like '5 to < 15' or '≥ 35' into (low, high).

    Returns (low, high) as floats, where high=None means open-ended (≥).
    Returns None if the cell is not a weight range.
    """
    cell = cell.strip().replace("≥", ">=").replace("≤", "<=").replace("–", "-")
    # Pattern: "5 to < 15" or "5 to <15"
    m = re.match(r"([\d.]+)\s*(?:to|[-–])\s*<?=?\s*([\d.]+)", cell)
    if m:
        return (float(m.group(1)), float(m.group(2)))
    # Pattern: ">= 35" or "≥ 35" or ">35"
    m = re.match(r"[>≥]=?\s*([\d.]+)", cell)
    if m:
        return (float(m.group(1)), None)
    # Pattern: "< 5" (upper bound only)
    m = re.match(r"<?=?\s*([\d.]+)", cell)
    if m and "<" in cell:
        return (0.0, float(m.group(1)))
    return None


def _parse_dose_value(cell: str) -> Optional[float]:
    """Extract the first numeric dose value from a cell like '20 + 120' or '25 mg'."""
    m = re.search(r"([\d.]+)", cell)
    return float(m.group(1)) if m else None


def validate_dosing_tables(tables: list) -> dict:
    """Run clinical plausibility checks on dosing tables.

    Checks:
      1. Weight band contiguity — no gaps between consecutive ranges
      2. Dose monotonicity — doses should generally increase with weight
      3. Positive values — all doses must be > 0
    """
    print(f"\n{'='*70}")
    print(f"  DOSING TABLE PLAUSIBILITY CHECKS")
    print(f"{'='*70}")

    dosing_tables = [t for t in tables if t.get("classification") == "dosing" and "error" not in t]
    if not dosing_tables:
        print("  No dosing tables found.")
        return {"checked": 0, "issues": []}

    all_issues = []

    for tbl in dosing_tables:
        idx = tbl["index"]
        page = tbl.get("page_no", "?")
        md = tbl.get("markdown", "")
        tbl_issues = []

        # Parse rows
        lines = [l.strip() for l in md.strip().split("\n") if l.strip() and "---" not in l]
        if len(lines) < 2:
            continue

        # Get header and data
        header_cells = [c.strip() for c in lines[0].split("|") if c.strip()]
        data_rows = []
        for line in lines[1:]:
            cells = [c.strip() for c in line.split("|") if c.strip()]
            if cells:
                data_rows.append(cells)

        if not data_rows:
            continue

        # Find the weight column (usually first) and dose column(s)
        weight_col = None
        dose_cols = []
        for ci, h in enumerate(header_cells):
            h_lower = h.lower()
            if any(kw in h_lower for kw in ["body weight", "weight (kg)", "weight"]) and weight_col is None:
                weight_col = ci
            elif any(kw in h_lower for kw in ["dose", "mg", "tablet"]):
                dose_cols.append(ci)

        if weight_col is None:
            continue

        # --- Check 1: Weight band contiguity ---
        weight_ranges = []
        for row in data_rows:
            if weight_col < len(row):
                wr = _parse_weight_range(row[weight_col])
                if wr:
                    weight_ranges.append(wr)

        for i_wr in range(len(weight_ranges) - 1):
            current_high = weight_ranges[i_wr][1]
            next_low = weight_ranges[i_wr + 1][0]
            if current_high is not None and next_low is not None:
                if abs(current_high - next_low) > 0.5:
                    tbl_issues.append(
                        f"Weight gap: band {i_wr+1} ends at {current_high}, "
                        f"band {i_wr+2} starts at {next_low}"
                    )

        # --- Check 2: Dose monotonicity (first dose column) ---
        if dose_cols:
            dc = dose_cols[0]
            doses = []
            for row in data_rows:
                if dc < len(row):
                    dv = _parse_dose_value(row[dc])
                    if dv is not None:
                        doses.append(dv)

            for i_d in range(len(doses) - 1):
                if doses[i_d + 1] < doses[i_d]:
                    tbl_issues.append(
                        f"Dose not monotonic: row {i_d+1} has {doses[i_d]}, "
                        f"row {i_d+2} has {doses[i_d+1]}"
                    )

            # --- Check 3: All doses positive ---
            for i_d, dv in enumerate(doses):
                if dv <= 0:
                    tbl_issues.append(f"Non-positive dose in row {i_d+1}: {dv}")

        if tbl_issues:
            print(f"  ⚠️  Table {idx} (p.{page}): {len(tbl_issues)} issue(s)")
            for iss in tbl_issues:
                print(f"      - {iss}")
            all_issues.append({"table_index": idx, "page": page, "issues": tbl_issues})
        else:
            print(f"  ✅ Table {idx} (p.{page}): plausibility OK")

    print(f"\n  Dosing tables checked : {len(dosing_tables)}")
    print(f"  Tables with issues   : {len(all_issues)}")
    return {"checked": len(dosing_tables), "issues": all_issues}


# ─────────────────────────────────────────────────────────────────────────────
# 10.  SPEED REPORT
# ─────────────────────────────────────────────────────────────────────────────

def speed_report(timings: dict, page_count: int):
    print(f"\n{'='*70}")
    print(f"  SPEED REPORT")
    print(f"{'='*70}")
    for k, v in timings.items():
        label = k.replace("_", " ").replace(" s", "").title()
        print(f"  {label:<30}: {v:>8.3f} s")
    if page_count > 0:
        spp = timings["convert_pdf_s"] / page_count
        print(f"  {'Seconds Per Page':<30}: {spp:>8.3f} s")


# ─────────────────────────────────────────────────────────────────────────────
# 11.  SAVE OUTPUTS
# ─────────────────────────────────────────────────────────────────────────────

def save_outputs(extraction: dict, accuracy: dict, tbl_report: dict,
                 img_report: dict, dosing_plausibility: dict):
    # Full markdown
    md_path = OUTPUT_DIR / "full_extraction.md"
    md_path.write_text(extraction["full_markdown"], encoding="utf-8")
    print(f"\n💾 Saved: {md_path}")

    # NLL tables — only write tables that actually have NLL content
    nll_path = OUTPUT_DIR / "tables_nll.txt"
    with open(nll_path, "w", encoding="utf-8") as f:
        for t in extraction["tables"]:
            nll = t.get("nll", "")
            if nll.strip():
                page = t.get("page_no", "?")
                cls = t.get("classification", "?")
                f.write(f"\n### Table {t['index']} (p.{page}, {cls}) ###\n")
                f.write(nll + "\n")
    print(f"💾 Saved: {nll_path}")

    # Table inventory — per-table classification + page for traceability
    inventory = []
    for t in extraction["tables"]:
        inventory.append({
            "index": t["index"],
            "page_no": t.get("page_no"),
            "classification": t.get("classification"),
            "num_rows": t.get("num_rows"),
            "num_cols": t.get("num_cols"),
            "has_nll": bool(t.get("nll", "").strip()),
        })
    inv_path = OUTPUT_DIR / "table_inventory.json"
    inv_path.write_text(json.dumps(inventory, indent=2), encoding="utf-8")
    print(f"💾 Saved: {inv_path}")

    # JSON summary
    summary = {
        "accuracy": accuracy,
        "table_quality": tbl_report,
        "image_quality": img_report,
        "dosing_plausibility": dosing_plausibility,
        "timings": extraction["timings"],
        "page_count": extraction["page_count"],
        "table_count": len(extraction["tables"]),
        "image_count": len(extraction["images"]),
    }
    json_path = OUTPUT_DIR / "extraction_summary.json"
    json_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"💾 Saved: {json_path}")

    return summary


# ─────────────────────────────────────────────────────────────────────────────
# 12.  MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    # ── Run extraction ────────────────────────────────────────────────────
    extraction = extract_document(PDF_PATH)

    # ── Accuracy benchmark ────────────────────────────────────────────────
    accuracy = compute_accuracy(extraction)

    # ── Table quality ──────────────────────────────────────────────────────
    tbl_report = table_quality_report(extraction["tables"])

    # ── Dosing plausibility (Stage 3 — automated checks) ──────────────────
    dosing_plausibility = validate_dosing_tables(extraction["tables"])

    # ── Image quality ──────────────────────────────────────────────────────
    img_report = image_quality_report(extraction["images"])

    # ── Speed ──────────────────────────────────────────────────────────────
    speed_report(extraction["timings"], extraction["page_count"])

    # ── Save everything ────────────────────────────────────────────────────
    summary = save_outputs(extraction, accuracy, tbl_report, img_report, dosing_plausibility)

    # ── Final scorecard ────────────────────────────────────────────────────
    print(f"\n{'='*70}")
    print(f"  FINAL SCORECARD")
    print(f"{'='*70}")
    print(f"  Accuracy (ground truth) : {accuracy['accuracy_pct']}%")
    print(f"  Table  Pass/Fail/Skip   : {tbl_report['table_pass']} / {tbl_report['table_fail']} / {tbl_report['table_skip']}")
    print(f"  Dosing plausibility     : {dosing_plausibility['checked']} checked, {len(dosing_plausibility['issues'])} with issues")
    print(f"  Image  Pass/Fail        : {img_report['image_pass']} / {img_report['image_fail']}")
    print(f"  Total pipeline time     : {extraction['timings']['total_s']}s")
    print(f"{'='*70}\n")

    return summary


if __name__ == "__main__":
    main()
