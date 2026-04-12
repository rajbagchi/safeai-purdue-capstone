"""
Multi-pass PDF extraction engine.
"""

import os
import json
import re
import hashlib
import pickle
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import asdict

import fitz  # PyMuPDF
import numpy as np
import pandas as pd
from rapidfuzz import fuzz

from .config import (
    ExtractionConfig,
    DOSING_TABLE_KEYWORDS,
    EVIDENCE_TABLE_KEYWORDS,
    STRUCTURAL_TABLE_KEYWORDS,
    CLINICAL_TABLE_KEYWORDS,
)

try:
    import camelot
    CAMELOT_AVAILABLE = True
except ImportError:
    CAMELOT_AVAILABLE = False

from .docling_table_extractor import (
    extract_tables_with_docling,
    DOCLING_AVAILABLE,
)

try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False

try:
    import tabulate  # noqa: F401 — pandas uses for DataFrame.to_markdown
    TABULATE_AVAILABLE = True
except ImportError:
    TABULATE_AVAILABLE = False

try:
    import pytesseract as _pytesseract
    from PIL import Image as _PIL_Image
    _PYTESSERACT_AVAILABLE = True
except ImportError:
    _pytesseract = None  # type: ignore[assignment]
    _PIL_Image = None    # type: ignore[assignment]
    _PYTESSERACT_AVAILABLE = False

try:
    import easyocr as _easyocr
    _EASYOCR_AVAILABLE = True
except ImportError:
    _easyocr = None  # type: ignore[assignment]
    _EASYOCR_AVAILABLE = False

# Lazy-initialised easyocr Reader (expensive to construct; share across images).
_easyocr_reader = None

# Regex for identifying figure/chart caption text near an image.
_CAPTION_PREFIX_RE = re.compile(
    r"^\s*(figure|fig\.?|plate|chart|diagram|photograph|photo|image)\s*\d*\.?\s*",
    re.IGNORECASE,
)


def _ocr_image_file(path: str) -> str:
    """Run OCR on an image file and return the extracted text.

    Tries pytesseract first, then easyocr.  Falls back gracefully to an
    empty string if neither engine is installed or the call fails.
    """
    global _easyocr_reader

    if _PYTESSERACT_AVAILABLE:
        try:
            img = _PIL_Image.open(path)
            return _pytesseract.image_to_string(img, lang="eng").strip()
        except Exception:
            pass

    if _EASYOCR_AVAILABLE:
        try:
            if _easyocr_reader is None:
                _easyocr_reader = _easyocr.Reader(["en"], gpu=False, verbose=False)
            result = _easyocr_reader.readtext(path, detail=0)
            return " ".join(str(r) for r in result).strip()
        except Exception:
            pass

    return ""


def _extract_image_caption(page: Any, xref: int) -> str:
    """Attempt to extract a caption from page text near the image.

    Uses PyMuPDF to find the image's bounding box on the page, then
    searches text blocks in an 80 pt band immediately below the image
    for caption-like text (Figure X, Fig., Chart, Plate, …).

    Returns the caption string (max 300 chars) or empty string.
    """
    try:
        rects = page.get_image_rects(xref)
        if not rects:
            return ""
        img_rect = rects[0]
        band_bottom = img_rect.y1 + 80

        best: str = ""
        for block in page.get_text("blocks"):
            bx0, by0, bx1, by1, text, *_ = block
            if not isinstance(text, str) or not text.strip():
                continue
            text = text.strip()
            # Block must start below (or at) the image bottom and within the band.
            if by0 >= img_rect.y1 - 5 and by0 <= band_bottom:
                # Prefer explicit caption patterns; otherwise take first match.
                if _CAPTION_PREFIX_RE.match(text) or not best:
                    best = text
        return best[:300]
    except Exception:
        return ""


def _normalise_for_crossval(text: str) -> str:
    """Normalise text before cross-validation comparison.

    Removes differences that are artefacts of the extractor (whitespace,
    soft hyphens, line-break hyphens) rather than genuine content divergence.
    """
    # Strip soft-hyphen line-break joins: "treat-\nment" → "treatment"
    text = re.sub(r"-\s*\n\s*", "", text)
    # Collapse all whitespace (tabs, newlines, multiple spaces) to single space
    text = re.sub(r"\s+", " ", text)
    # Remove non-printable characters
    text = re.sub(r"[^\x20-\x7E]", "", text)
    return text.strip().lower()


def _dataframe_to_markdown(df) -> str:
    """Prefer pandas to_markdown (needs tabulate); fall back to CSV-like text."""
    if hasattr(df, "to_markdown"):
        try:
            return df.to_markdown(index=False)
        except Exception:
            pass
    return df.to_string(index=False)


class MultiPassExtractor:
    """
    Intelligent multi-pass extraction engine.
    Adapts strategy based on document content.
    """

    def __init__(self, config: ExtractionConfig):
        self.config = config
        self.passes: List[Dict] = []
        self.document_profile: Dict = {}

        # Create directories
        os.makedirs(config.output_dir, exist_ok=True)
        os.makedirs(config.cache_dir, exist_ok=True)
        os.makedirs(os.path.join(config.output_dir, "images"), exist_ok=True)
        os.makedirs(os.path.join(config.output_dir, "tables"), exist_ok=True)
        os.makedirs(os.path.join(config.output_dir, "validation"), exist_ok=True)

    def analyze_document(self) -> Dict:
        """Quick first pass to understand document structure."""
        print("\n🔍 [Pass 0] Analyzing document structure...")

        doc = fitz.open(self.config.pdf_path)

        profile: Dict[str, Any] = {
            "total_pages": len(doc),
            "has_tables": False,
            "has_images": False,
            "has_scanned_pages": False,
            "page_types": [],
            "estimated_tables": 0,
            "language": "unknown",
            "page_samples": [],
        }

        sample_pages = min(20, len(doc))

        for page_num in range(sample_pages):
            page = doc[page_num]
            text = page.get_text()
            text_len = len(text.strip())

            page_info: Dict[str, Any] = {
                "page": page_num + 1,
                "text_length": text_len,
                "has_images": len(page.get_images()) > 0,
                "has_vector_graphics": len(page.get_drawings()) > 0,
            }

            if self.config.enable_table_detection:
                try:
                    tabs = page.find_tables()
                    if tabs and tabs.tables:
                        page_info["has_tables"] = True
                        page_info["table_count"] = len(tabs.tables)
                        profile["has_tables"] = True
                        profile["estimated_tables"] += len(tabs.tables)
                except Exception:
                    pass

            if text_len < 100 and page_info["has_images"]:
                page_info["likely_scanned"] = True
                profile["has_scanned_pages"] = True

            if page_info["has_images"]:
                profile["has_images"] = True

            profile["page_types"].append(page_info)

        doc.close()

        self.document_profile = profile
        self.passes.append({
            "pass": 0,
            "strategy": "analysis",
            "profile": profile,
        })

        print(f"  Document: {profile['total_pages']} pages")
        print(f"  Tables detected: {profile['estimated_tables']}")
        print(f"  Scanned pages: {'Yes' if profile['has_scanned_pages'] else 'No'}")
        print(f"  Images present: {'Yes' if profile['has_images'] else 'No'}")

        return profile

    def pass1_text_extraction(self) -> List[Dict]:
        """Pass 1: Extract text with structure preservation."""
        print("\n📄 [Pass 1] Text extraction with structure...")

        doc = fitz.open(self.config.pdf_path)
        pages = []

        for page_num in range(len(doc)):
            page = doc[page_num]
            text_dict = page.get_text("dict")
            text_blocks = self._extract_text_blocks(text_dict)
            headings = self._extract_headings(text_dict)

            pages.append({
                "page": page_num + 1,
                "text_blocks": text_blocks,
                "headings": headings,
                "raw_text": page.get_text("text"),
                "extraction_method": "pymupdf_text",
            })

        doc.close()

        self.passes.append({
            "pass": 1,
            "strategy": "text_extraction",
            "pages": len(pages),
        })

        return pages

    def _extract_text_blocks(self, text_dict: Dict) -> List[Dict]:
        """Extract text blocks with position and formatting."""
        blocks = []

        for block in text_dict.get("blocks", []):
            if "lines" in block:
                for line in block["lines"]:
                    line_text = ""
                    line_fonts = []

                    for span in line["spans"]:
                        line_text += span["text"]
                        line_fonts.append({
                            "font": span.get("font", ""),
                            "size": span.get("size", 0),
                            "flags": span.get("flags", 0),
                        })

                    if line_text.strip():
                        blocks.append({
                            "text": line_text.strip(),
                            "y_pos": block.get("bbox", [0, 0, 0, 0])[1],
                            "fonts": line_fonts,
                            "is_bold": any(f["flags"] & 2**4 for f in line_fonts),
                            "is_italic": any(f["flags"] & 2**1 for f in line_fonts),
                        })

        blocks.sort(key=lambda x: x["y_pos"])
        return blocks

    def _extract_headings(self, text_dict: Dict) -> List[Dict]:
        """Identify headings based on font size and style."""
        headings = []

        for block in text_dict.get("blocks", []):
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"].strip()
                        if text and len(text) < 100:
                            font_size = span.get("size", 0)
                            is_bold = span.get("flags", 0) & 2**4

                            if font_size > 12 or is_bold:
                                level = 1 if font_size > 16 else 2 if font_size > 14 else 3
                                headings.append({
                                    "text": text,
                                    "level": level,
                                    "y_pos": block.get("bbox", [0, 0, 0, 0])[1],
                                    "font_size": font_size,
                                    "is_bold": is_bold,
                                })

        headings.sort(key=lambda x: x["y_pos"])
        return headings

    def _scan_all_pages_for_tables(self) -> List[int]:
        """Find every 1-based page index that has at least one PyMuPDF-detected table."""
        pages_out: List[int] = []
        doc = fitz.open(self.config.pdf_path)
        try:
            for i in range(len(doc)):
                page = doc[i]
                try:
                    tabs = page.find_tables()
                    if tabs and tabs.tables:
                        pages_out.append(i + 1)
                except Exception:
                    continue
        finally:
            doc.close()
        return pages_out

    @staticmethod
    def _classify_table(
        table: Dict,
        extra_dosing_keywords: List[str],
        extra_clinical_keywords: List[str],
    ) -> str:
        """
        Classify a table as one of five types:
          dosing | evidence | clinical_management | structural | other

        Classification is keyword-scored against the combined header + cell text.
        Priority order: structural → evidence → dosing → clinical_management → other.
        This matches the cascade used in the original stage2_cross_validation.py.
        """
        header_text = " ".join(str(h) for h in table.get("headers", [])).lower()
        data_text = " ".join(
            str(v)
            for row in table.get("data", [])
            for v in (row.values() if isinstance(row, dict) else row)
        ).lower()
        combined = header_text + " " + data_text

        # --- structural check (abbreviation lists, ToC) ---
        # Two or more structural signals override dosing patterns (handles abbreviation
        # tables that define drug names with doses, e.g. "AL = 80+480 mg").
        # A single structural signal is still blocked by dose/weight patterns to avoid
        # misclassifying dosing tables that happen to define one abbreviation.
        struct_hits = sum(1 for kw in STRUCTURAL_TABLE_KEYWORDS if kw in combined)
        if struct_hits >= 2:
            return "structural"
        if struct_hits == 1 and not re.search(r"\b\d+\s*mg\b|\bkg\b|\bbody weight\b", combined):
            return "structural"

        # --- evidence / GRADE quality tables ---
        evidence_hits = sum(1 for kw in EVIDENCE_TABLE_KEYWORDS if kw in combined)
        if evidence_hits >= 2:
            return "evidence"

        # --- dosing tables: base keywords + document-specific drug names ---
        all_dosing_kws = DOSING_TABLE_KEYWORDS + extra_dosing_keywords
        dosing_hits = sum(1 for kw in all_dosing_kws if kw in combined)
        has_weight_pattern = bool(
            re.search(
                r"\b\d+\s*(to\s*<?|<|>|–|-)\s*\d+\s*kg\b"
                r"|\bkg\b"
                r"|\bbody weight\b"
                r"|\bweight\s*\(",
                combined,
            )
        )
        has_dose_value = bool(
            re.search(r"\b\d+\s*\+\s*\d+\s*mg\b|\b\d+\s*mg\b|\b\d+\s*mg/kg\b", combined)
        )
        if dosing_hits >= 2 or (dosing_hits >= 1 and (has_weight_pattern or has_dose_value)):
            return "dosing"

        # --- clinical management tables ---
        all_clinical_kws = CLINICAL_TABLE_KEYWORDS + extra_clinical_keywords
        clinical_hits = sum(1 for kw in all_clinical_kws if kw in combined)
        if clinical_hits >= 1:
            return "clinical_management"

        # --- weak dosing signal (single keyword or pattern only) ---
        if dosing_hits >= 1 or has_weight_pattern or has_dose_value:
            return "dosing"

        return "other"

    @staticmethod
    def _generate_nll(table: Dict) -> str:
        """
        Convert a classified dosing or clinical_management table into Natural
        Language Logic (NLL) sentences to prevent LLM alignment hallucinations
        when reasoning about tabular dosing data.

        Each row becomes one IF/THEN sentence:
          IF <first_column_header> is <value>, THEN <col2_header> is <val2>, ...

        Only called for dosing and clinical_management tables; returns "" for
        evidence, structural, and other types.

        Example output for an AL dosing table row:
          IF body weight is 5–<15 kg, THEN dose is 1 tablet, frequency is twice
          daily, duration is 3 days.
        """
        classification = table.get("classification", "other")
        if classification not in ("dosing", "clinical_management"):
            return ""

        headers = [str(h).strip() for h in table.get("headers", []) if str(h).strip()]
        data = table.get("data", [])

        if not headers or not data:
            return ""

        sentences: List[str] = []
        for row in data:
            if isinstance(row, dict):
                values = [str(row.get(h, "")).strip() for h in headers]
            else:
                values = [str(v).strip() for v in row]

            pairs = [(h, v) for h, v in zip(headers, values) if v]
            if not pairs:
                continue

            condition_h, condition_v = pairs[0]
            sentence = f"IF {condition_h} is {condition_v}"

            if len(pairs) > 1:
                outcomes = ", ".join(
                    f"{h} is {v}" for h, v in pairs[1:]
                )
                sentence += f", THEN {outcomes}."
            else:
                sentence += "."

            sentences.append(sentence)

        return "\n".join(sentences)

    def pass_images_extraction(self) -> List[Dict[str, Any]]:
        """
        Rasterize embedded images per page to PNG under output_dir/images/.
        Returns an inventory list (paths relative to output_dir where useful).
        """
        print("\n🖼️ [Pass images] Extracting embedded images...")
        img_dir = os.path.join(self.config.output_dir, "images")
        os.makedirs(img_dir, exist_ok=True)
        inventory: List[Dict[str, Any]] = []
        doc = fitz.open(self.config.pdf_path)
        min_pixels = 400  # skip tiny icons / bullets (~20x20)
        try:
            for page_index in range(len(doc)):
                page = doc[page_index]
                page_no = page_index + 1
                for img_index, img in enumerate(page.get_images(full=True)):
                    xref = img[0]
                    try:
                        pix = fitz.Pixmap(doc, xref)
                        if pix.width * pix.height < min_pixels:
                            pix = None
                            continue
                        if pix.n - pix.alpha > 3:
                            pix = fitz.Pixmap(fitz.csRGB, pix)
                        fname = f"page{page_no}_img{img_index + 1}.png"
                        out_path = os.path.join(img_dir, fname)
                        img_width, img_height = pix.width, pix.height
                        pix.save(out_path)
                        pix = None
                        caption = _extract_image_caption(page, xref)
                        ocr_text = _ocr_image_file(out_path)
                        inventory.append({
                            "page": page_no,
                            "image_index": img_index + 1,
                            "xref": xref,
                            "width": img_width,
                            "height": img_height,
                            "file": out_path,
                            "ocr_text": ocr_text,
                            "caption": caption,
                        })
                    except Exception as e:
                        print(f"  Warning: image xref {xref} page {page_no}: {e}")
        finally:
            doc.close()

        images_with_ocr = sum(1 for i in inventory if i.get("ocr_text"))
        images_with_caption = sum(1 for i in inventory if i.get("caption"))
        self.passes.append({
            "pass": "images",
            "strategy": "embedded_raster",
            "images_saved": len(inventory),
            "images_with_ocr": images_with_ocr,
            "images_with_caption": images_with_caption,
            "ocr_engine": (
                "pytesseract" if _PYTESSERACT_AVAILABLE
                else ("easyocr" if _EASYOCR_AVAILABLE else "none")
            ),
        })
        print(
            f"  Saved {len(inventory)} image(s) to {img_dir} "
            f"({images_with_ocr} with OCR text, {images_with_caption} with caption)"
        )
        return inventory

    def pass2_table_extraction(self, pages_with_tables: List[int]) -> List[Dict]:
        """Pass 2: Specialized table extraction with classification."""
        print(f"\n📊 [Pass 2] Table extraction on {len(pages_with_tables)} pages...")

        extra_dosing = self.config.dosing_table_keywords or []
        extra_clinical = self.config.clinical_table_keywords or []

        tables = []
        doc = fitz.open(self.config.pdf_path)

        for page_num in pages_with_tables:
            page = doc[page_num - 1]

            try:
                tabs = page.find_tables()
                if tabs and tabs.tables:
                    for i, table in enumerate(tabs.tables):
                        df = table.to_pandas().fillna("")

                        table_file = os.path.join(
                            self.config.output_dir,
                            "tables",
                            f"page{page_num}_table{i+1}.csv",
                        )
                        df.to_csv(table_file, index=False)

                        raw_table = {
                            "page": page_num,
                            "table_id": i,
                            "method": "pymupdf",
                            "data": df.to_dict(orient="records"),
                            "headers": df.columns.tolist(),
                            "markdown": _dataframe_to_markdown(df),
                            "num_rows": len(df),
                            "num_cols": len(df.columns),
                            "file": table_file,
                            "confidence": 0.9,
                            "bbox": tuple(table.bbox),
                        }
                        raw_table["classification"] = self._classify_table(
                            raw_table, extra_dosing, extra_clinical
                        )
                        raw_table["nll"] = self._generate_nll(raw_table)
                        tables.append(raw_table)
            except Exception as e:
                print(f"  Warning: Table extraction on page {page_num} failed: {e}")

            if CAMELOT_AVAILABLE and len(tables) == 0:
                try:
                    temp_pdf = os.path.join(self.config.cache_dir, f"temp_page_{page_num}.pdf")
                    with open(temp_pdf, "wb") as f:
                        f.write(page.get_pdf_output())

                    lattice_tables = camelot.read_pdf(temp_pdf, pages="1", flavor="lattice")
                    for table in lattice_tables:
                        df = table.df
                        t = {
                            "page": page_num,
                            "method": "camelot_lattice",
                            "data": df.to_dict(orient="records"),
                            "headers": df.iloc[0].tolist(),
                            "markdown": _dataframe_to_markdown(df),
                            "confidence": 0.95,
                        }
                        t["classification"] = self._classify_table(t, extra_dosing, extra_clinical)
                        t["nll"] = self._generate_nll(t)
                        tables.append(t)

                    stream_tables = camelot.read_pdf(temp_pdf, pages="1", flavor="stream")
                    for table in stream_tables:
                        df = table.df
                        t = {
                            "page": page_num,
                            "method": "camelot_stream",
                            "data": df.to_dict(orient="records"),
                            "headers": df.iloc[0].tolist(),
                            "markdown": _dataframe_to_markdown(df),
                            "confidence": 0.85,
                        }
                        t["classification"] = self._classify_table(t, extra_dosing, extra_clinical)
                        t["nll"] = self._generate_nll(t)
                        tables.append(t)

                    if os.path.exists(temp_pdf):
                        os.remove(temp_pdf)
                except Exception:
                    pass

        doc.close()

        # Summarise classification distribution for the pass log
        classification_counts: Dict[str, int] = {}
        for t in tables:
            c = t.get("classification", "other")
            classification_counts[c] = classification_counts.get(c, 0) + 1

        self.passes.append({
            "pass": 2,
            "strategy": "table_extraction",
            "tables_found": len(tables),
            "classification_counts": classification_counts,
        })
        print(f"  Classifications: {classification_counts}")

        return tables

    def pass2b_stitch_page_boundary_tables(self, tables: List[Dict]) -> List[Dict]:
        """Pass 2b: Detect and stitch tables split across page boundaries.

        For each PyMuPDF table whose bottom edge exceeds 90% of its page height,
        searches the next page for a table starting within the top 10% with a
        matching column count.  Matching fragments are merged into a single stitched
        table dict (method='pymupdf_stitched') and the two originals are removed.

        Edge cases handled:
          - 0-row continuation: PyMuPDF puts the data into column headers — those
            headers are converted into a data row before merging.
          - Duplicate header row: some PDFs repeat the header on continuation pages —
            the duplicate first row is stripped from the bottom fragment.
        """
        BOTTOM_THRESHOLD = 0.90
        TOP_THRESHOLD = 0.10

        # Only PyMuPDF tables carry reliable bbox; Camelot tables are passed through.
        pymupdf_tables = [t for t in tables if t.get("method") == "pymupdf" and "bbox" in t]
        other_tables = [t for t in tables if not (t.get("method") == "pymupdf" and "bbox" in t)]

        by_page: Dict[int, List[Dict]] = {}
        for t in pymupdf_tables:
            by_page.setdefault(t["page"], []).append(t)

        extra_dosing = self.config.dosing_table_keywords or []
        extra_clinical = self.config.clinical_table_keywords or []

        doc = fitz.open(self.config.pdf_path)
        stitched_tables: List[Dict] = []
        fragment_ids: set = set()  # (page, table_id) pairs consumed by stitching

        for page_num in sorted(by_page.keys()):
            page_height = doc[page_num - 1].rect.height

            for top_tbl in by_page[page_num]:
                if (top_tbl["page"], top_tbl.get("table_id")) in fragment_ids:
                    continue

                bbox = top_tbl["bbox"]
                if bbox[3] / page_height < BOTTOM_THRESHOLD:
                    continue

                next_page_tables = by_page.get(page_num + 1, [])
                if not next_page_tables:
                    continue

                next_page_height = doc[page_num].rect.height  # 0-indexed: page_num+1-1

                for bot_tbl in next_page_tables:
                    if (bot_tbl["page"], bot_tbl.get("table_id")) in fragment_ids:
                        continue

                    next_bbox = bot_tbl["bbox"]
                    if next_bbox[1] / next_page_height > TOP_THRESHOLD:
                        continue

                    if top_tbl["num_cols"] != bot_tbl["num_cols"]:
                        print(
                            f"  Pass 2b: column mismatch page {page_num}→{page_num+1} "
                            f"({top_tbl['num_cols']} vs {bot_tbl['num_cols']}) — skipping"
                        )
                        continue

                    try:
                        df_top = pd.DataFrame(top_tbl["data"])
                        df_bot = pd.DataFrame(bot_tbl["data"])

                        # 0-row continuation: headers are actually the data row
                        if len(df_bot) == 0 and bot_tbl["headers"]:
                            header_vals = [str(h) for h in bot_tbl["headers"]]
                            df_bot = pd.DataFrame(
                                [header_vals],
                                columns=df_top.columns[: len(header_vals)],
                            )

                        # Remove duplicate header repeated at top of continuation
                        top_headers = [str(h).strip().lower() for h in df_top.columns]
                        if len(df_bot) > 0:
                            first_row = [str(v).strip().lower() for v in df_bot.iloc[0]]
                            if first_row == top_headers:
                                df_bot = df_bot.iloc[1:]

                        # Skip if continuation fragment is empty after header removal
                        if len(df_bot) == 0 or len(df_bot.columns) == 0:
                            continue

                        # Align columns and concatenate
                        df_bot.columns = df_top.columns[: len(df_bot.columns)]
                        df_stitched = pd.concat([df_top, df_bot], ignore_index=True)

                        def _clean(val: Any) -> str:
                            s = str(val).replace("\n", " ").replace("<br>", " ")
                            return re.sub(r"\s+", " ", s).strip()

                        md_lines = [
                            "| " + " | ".join(_clean(h) for h in df_stitched.columns) + " |",
                            "| " + " | ".join("---" for _ in df_stitched.columns) + " |",
                        ]
                        for _, row in df_stitched.iterrows():
                            md_lines.append("| " + " | ".join(_clean(v) for v in row) + " |")

                        stitched: Dict[str, Any] = {
                            "page": page_num,
                            "pages": [page_num, page_num + 1],
                            "method": "pymupdf_stitched",
                            "data": df_stitched.to_dict(orient="records"),
                            "headers": [str(h) for h in df_stitched.columns],
                            "markdown": "\n".join(md_lines),
                            "num_rows": len(df_stitched),
                            "num_cols": len(df_stitched.columns),
                            "stitched": True,
                            "stitched_from_rows": [top_tbl["num_rows"], bot_tbl["num_rows"]],
                            "confidence": min(
                                top_tbl.get("confidence", 0.9),
                                bot_tbl.get("confidence", 0.9),
                            ),
                        }
                        stitched["classification"] = self._classify_table(
                            stitched, extra_dosing, extra_clinical
                        )
                        stitched["nll"] = self._generate_nll(stitched)

                        stitched_tables.append(stitched)
                        fragment_ids.add((top_tbl["page"], top_tbl.get("table_id")))
                        fragment_ids.add((bot_tbl["page"], bot_tbl.get("table_id")))

                        print(
                            f"  ✅ Pass 2b: stitched pages {page_num}+{page_num+1} — "
                            f"{top_tbl['num_rows']}+{len(df_bot)}={len(df_stitched)} rows "
                            f"[{stitched['classification']}]"
                        )
                        break  # one continuation per top fragment

                    except Exception as e:
                        print(f"  ⚠️  Pass 2b: stitch failed pages {page_num}+{page_num+1}: {e}")

        doc.close()

        remaining = [
            t for t in pymupdf_tables
            if (t["page"], t.get("table_id")) not in fragment_ids
        ]
        result = remaining + stitched_tables + other_tables

        self.passes.append({
            "pass": "2b",
            "strategy": "page_boundary_stitching",
            "stitched_count": len(stitched_tables),
            "fragments_removed": len(fragment_ids),
        })

        if stitched_tables:
            print(f"\n  📎 Pass 2b: {len(stitched_tables)} table(s) stitched across page boundaries")
        else:
            print("\n  Pass 2b: no page-boundary tables detected")

        return result

    def pass3_ocr_extraction(self, scanned_pages: List[int]) -> List[Dict]:
        """Pass 3: OCR for scanned/image-heavy pages."""
        print(f"\n🖼️ [Pass 3] OCR extraction on {len(scanned_pages)} scanned pages...")

        ocr_results = []
        for page_num in scanned_pages:
            ocr_results.append({
                "page": page_num,
                "method": "ocr_needed",
                "status": "requires_manual_review",
                "note": "Page appears scanned - manual verification recommended",
            })

        self.passes.append({
            "pass": 3,
            "strategy": "ocr",
            "pages_processed": len(scanned_pages),
        })

        return ocr_results

    def pass4_cross_validation(self, extracted_data: Dict) -> Dict:
        """Pass 4: Cross-validate with different extraction tool."""
        print("\n🔄 [Pass 4] Cross-validation extraction...")

        if not PDFPLUMBER_AVAILABLE:
            print("  PDFPlumber not available, skipping cross-validation")
            return {"method": "skipped", "reason": "pdfplumber_not_available"}

        validation_results: Dict[str, Any] = {
            "method": "pdfplumber",
            "page_matches": [],
            "consistency_score": 0.0,
        }

        try:
            import pdfplumber
            import tempfile

            # Some PDFs (e.g. Adobe InDesign output) use internal page-tree
            # structures that pdfminer/pdfplumber cannot traverse directly,
            # returning 0 pages. Re-saving through PyMuPDF normalises the
            # structure so pdfplumber can read any document.
            pdf_path_for_plumber = self.config.pdf_path
            tmp_file = None
            with pdfplumber.open(pdf_path_for_plumber) as probe:
                if len(probe.pages) == 0:
                    print("  PDF structure not readable by pdfplumber — repairing via PyMuPDF...")
                    import fitz
                    src = fitz.open(self.config.pdf_path)
                    tmp_file = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
                    tmp_file.close()
                    src.save(tmp_file.name, garbage=4, deflate=True, clean=True)
                    src.close()
                    pdf_path_for_plumber = tmp_file.name
                    print(f"  Repaired PDF written to temp file — retrying cross-validation")

            with pdfplumber.open(pdf_path_for_plumber) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    text = page.extract_text() or ""

                    pass1_text = ""
                    for p in extracted_data.get("pass1", []):
                        if p.get("page") == page_num:
                            pass1_text = p.get("raw_text", "")
                            break

                    if pass1_text and text:
                        similarity = fuzz.ratio(
                            _normalise_for_crossval(pass1_text),
                            _normalise_for_crossval(text),
                        ) / 100.0
                        validation_results["page_matches"].append({
                            "page": page_num,
                            "similarity": similarity,
                        })

            if tmp_file:
                import os as _os
                _os.unlink(tmp_file.name)

            if validation_results["page_matches"]:
                validation_results["consistency_score"] = float(np.mean([
                    m["similarity"] for m in validation_results["page_matches"]
                ]))

        except Exception as e:
            print(f"  Cross-validation failed: {e}")

        self.passes.append({
            "pass": 4,
            "strategy": "cross_validation",
            "results": validation_results,
        })

        return validation_results

    def _write_nll_file(self, tables: List[Dict]) -> None:
        """Write tables_nll.txt — one NLL block per dosing/clinical_management table."""
        nll_path = os.path.join(self.config.output_dir, "tables_nll.txt")
        nll_tables = [t for t in tables if t.get("nll")]
        if not nll_tables:
            return
        with open(nll_path, "w", encoding="utf-8") as f:
            for i, t in enumerate(nll_tables, 1):
                pages = t.get("pages", [t.get("page", "?")])
                f.write(f"--- Table {i} | page(s) {pages} | {t.get('classification', '')} ---\n")
                f.write(t["nll"])
                f.write("\n\n")
        print(f"  📝 NLL written: {len(nll_tables)} table(s) → {nll_path}")

    def extract_all(self) -> Dict:
        """Orchestrate multi-pass extraction."""
        print("=" * 70)
        print("MULTI-PASS EXTRACTION ENGINE")
        print("=" * 70)

        cache_key = self._get_cache_key()
        cache_file = os.path.join(self.config.cache_dir, f"{cache_key}.pkl")

        if os.path.exists(cache_file):
            print("\n📦 Loading cached extraction results...")
            with open(cache_file, "rb") as f:
                return pickle.load(f)

        print(
            f"  Dependencies: tabulate={'yes' if TABULATE_AVAILABLE else 'NO (install for table markdown)'}, "
            f"pdfplumber={'yes' if PDFPLUMBER_AVAILABLE else 'NO'}"
        )

        profile = self.analyze_document()
        pages = self.pass1_text_extraction()

        scanned_pages = []
        for page_info in profile["page_types"]:
            if page_info.get("likely_scanned", False):
                scanned_pages.append(page_info["page"])

        if self.config.enable_table_detection and self.config.full_document_table_scan:
            print("\n📋 Scanning all pages for tables (full-document scan)...")
            pages_with_tables = self._scan_all_pages_for_tables()
            print(f"  Pages with tables: {len(pages_with_tables)}")
        else:
            pages_with_tables = []
            for page_info in profile["page_types"]:
                if page_info.get("has_tables", False):
                    pages_with_tables.append(page_info["page"])

        tables = []
        if pages_with_tables and self.config.enable_table_detection:
            use_docling = self.config.use_docling_tables and DOCLING_AVAILABLE
            if use_docling:
                # --- Primary: Docling + TableFormer ACCURATE ---
                # Docling reconstructs multi-page tables natively; pass2b
                # stitching is skipped.  Classification and NLL are applied
                # below via the same helpers used for PyMuPDF tables.
                print("\n[Docling] Using Docling as primary table extractor...")
                extra_dosing = self.config.dosing_table_keywords or []
                extra_clinical = self.config.clinical_table_keywords or []
                docling_tables = extract_tables_with_docling(
                    self.config.pdf_path,
                    self.config.output_dir,
                )
                # Apply SafeAI's classification and NLL to Docling tables
                for t in docling_tables:
                    t["classification"] = self._classify_table(
                        t, extra_dosing, extra_clinical
                    )
                    t["nll"] = self._generate_nll(t)
                tables = docling_tables
                # --- Secondary: PyMuPDF for cross-check ---
                # PyMuPDF tables are extracted but used only as a secondary
                # cross-validation baseline; they are not added to `tables`.
                pymupdf_tables = self.pass2_table_extraction(pages_with_tables)
                docling_count = len(docling_tables)
                pymupdf_count = len(pymupdf_tables)
                print(
                    f"  [Docling vs PyMuPDF] Docling: {docling_count} tables, "
                    f"PyMuPDF: {pymupdf_count} tables"
                )
                self.passes.append({
                    "pass": "docling_vs_pymupdf",
                    "docling_tables": docling_count,
                    "pymupdf_tables": pymupdf_count,
                    "primary": "docling",
                })
            else:
                # --- Legacy: PyMuPDF + stitching ---
                if not DOCLING_AVAILABLE and self.config.use_docling_tables:
                    print(
                        "  [Warning] use_docling_tables=True but Docling is not "
                        "installed. Falling back to PyMuPDF. "
                        "Install with: pip install 'docling>=2.64.0'"
                    )
                tables = self.pass2_table_extraction(pages_with_tables)
                tables = self.pass2b_stitch_page_boundary_tables(tables)
            self._write_nll_file(tables)

        ocr_data = []
        if scanned_pages and self.config.enable_ocr:
            ocr_data = self.pass3_ocr_extraction(scanned_pages)

        cross_validation = self.pass4_cross_validation({
            "pass1": pages,
            "pass2": tables,
        })

        images: List[Dict[str, Any]] = []
        if self.config.enable_image_extraction:
            images = self.pass_images_extraction()

        extraction_result = {
            "metadata": {
                "pdf_path": self.config.pdf_path,
                "extraction_date": datetime.now().isoformat(),
                "config": asdict(self.config),
                "document_profile": profile,
                "passes_completed": len(self.passes),
            },
            "pages": pages,
            "tables": tables,
            "images": images,
            "ocr_data": ocr_data,
            "cross_validation": cross_validation,
            "extraction_log": self.passes,
        }

        with open(cache_file, "wb") as f:
            pickle.dump(extraction_result, f)

        inv_path = os.path.join(self.config.output_dir, "image_inventory.json")
        try:
            with open(inv_path, "w", encoding="utf-8") as f:
                json.dump(images, f, indent=2, default=str)
        except OSError:
            pass

        return extraction_result

    def _get_cache_key(self) -> str:
        """Generate cache key based on file and config."""
        file_stat = os.stat(self.config.pdf_path)
        file_hash = hashlib.md5(
            f"{self.config.pdf_path}_{file_stat.st_size}_{file_stat.st_mtime}".encode()
        ).hexdigest()[:8]

        config_hash = hashlib.md5(
            json.dumps(asdict(self.config), sort_keys=True).encode()
        ).hexdigest()[:8]

        return f"extraction_{file_hash}_{config_hash}"
