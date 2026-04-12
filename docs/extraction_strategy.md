# Extraction Strategy

**Module:** `pipeline/extractor.py` (979 lines) | **Class:** `MultiPassExtractor`

## What we built

A **multi-pass extraction engine** that runs six passes over each PDF to maximize coverage and cross-validate accuracy. Each pass targets a different content type, and later passes build on the output of earlier ones.

```
Pass 0  Document profiling       (page count, table density, scan detection)
Pass 1  Text + headings          (PyMuPDF with layout coordinates)
Pass 2  Table extraction         (PyMuPDF find_tables + classification)
Pass 2b Page-boundary stitching  (reconnects tables split across pages)
Pass 4  Cross-validation         (pdfplumber re-extraction + fuzzy comparison)
Images  Embedded image capture   (rasterization + OCR + caption extraction)
```

### Why multi-pass?

Medical PDFs are not flat text. A single extraction pass misses tables, conflates headings with body text, and cannot verify its own accuracy. By dedicating separate passes to structure analysis, text, tables, and cross-validation, we catch content that any single extractor would miss.

### Key design decisions

**1. PyMuPDF as the primary engine**

PyMuPDF (`fitz`) provides fast, memory-efficient access to both text blocks (with `y_pos` coordinates for layout ordering) and a built-in `find_tables()` API. It handles the 1,161-page Uganda PDF in under 2 minutes.

**2. Full-document table scan**

Pass 0 samples only 20 pages. Early experiments showed this missed tables on later pages. We added `full_document_table_scan=True` (default) to scan every page, which increased table recall from ~60% to ~100% on the Uganda PDF (950 tables detected).

**3. Page-boundary table stitching (Pass 2b)**

Many dosing tables span two pages. Without stitching, each half is a separate (incomplete) table. Pass 2b identifies continuation fragments by matching column counts and header patterns, then concatenates them. This stitched 77 tables in the malaria PDF and 170 in Uganda.

**4. Table classification taxonomy**

Every extracted table is classified into one of five types based on header and cell content analysis:

| Type | Description | Preservation |
|---|---|---|
| `dosing` | Drug dosing by weight/age | VERBATIM |
| `clinical_management` | Treatment protocols, symptom management | HIGH |
| `evidence` | Study results, meta-analysis summaries | STANDARD |
| `structural` | Table of contents, index | Excluded |
| `other` | Anything unclassifiable | STANDARD |

Classification drives downstream decisions: preservation level, chunking strategy, validation checks, and clinical verification tier.

**5. Cross-validation (Pass 4)**

Re-extracting text with pdfplumber and computing `fuzz.ratio` similarity against Pass 1 catches silent extraction failures. Text is normalized before comparison (whitespace collapsed, soft hyphens stripped, lowercased) to avoid false divergence from formatting differences. The Uganda PDF scores 94% consistency; malaria scores 83% (lower due to dense evidence tables with complex layouts).

**PDF compatibility fix (2026-04-10):** Some PDFs produced by tools like Adobe InDesign use a non-standard internal page-tree structure that pdfminer/pdfplumber cannot traverse directly, returning 0 pages and causing a false 0% consistency score. The extractor now detects this automatically: if pdfplumber returns 0 pages, the PDF is re-saved through PyMuPDF (`garbage=4, clean=True`) to a temporary file, which normalises the structure to standard PDF. pdfplumber then runs on the repaired copy. The temporary file is deleted after cross-validation. This makes cross-validation work on any uploaded PDF regardless of how it was produced.

**6. Image OCR and caption extraction**

Embedded images are rasterized to PNG. If `pytesseract` or `easyocr` is available, OCR text is extracted. Captions are located by searching for text blocks in an 80px band below the image bounding box, preferring blocks starting with "Figure", "Chart", "Diagram", etc.

## CT Health AI Integration: Docling + TableFormer ACCURATE

**Module:** `pipeline/docling_table_extractor.py` | **Status:** Optional, default enabled when `use_docling_tables=True`

After comparing this codebase with the CT Health AI pipeline (which uses IBM Docling 2.64 + TableFormer ACCURATE as its primary table extractor), we integrated Docling as an optional primary table extraction method. The integration is backwards-compatible: PyMuPDF remains the fallback when Docling is unavailable or when `use_docling_tables=False`.

### Why Docling + TableFormer?

CT Health AI's pipeline achieves **27/27 tables linearized with 0 skipped**, compared to SafeAI's original PyMuPDF approach which could miss or misparse complex borderless or nested tables. TableFormer is a transformer-based table structure recognition model trained on PubTables-1M — it predicts cell boundaries and spanning relationships without relying on visible grid lines, which is critical for clinical dosing tables that often use borderless formatting.

### How the integration works

```python
# ExtractionConfig (config.py)
use_docling_tables: bool = True   # new field — enables Docling as primary

# extractor.py — modified extract_all() table section:
if config.use_docling_tables and DOCLING_AVAILABLE:
    docling_tables = extract_tables_with_docling(pdf_path, output_dir, table_mode="accurate")
    # PyMuPDF still runs as cross-check (count logged), but Docling tables are used
    # Pass 2b stitching is skipped for Docling tables (it handles cross-page layout natively)
    # SafeAI's _classify_table() and _generate_nll() are applied to Docling table dicts
else:
    # original PyMuPDF path runs unchanged
```

The `extract_tables_with_docling()` function in `docling_table_extractor.py` returns table dicts matching SafeAI's existing format:

```python
{
    "page": int,           # 0-based page number
    "method": "docling",   # provenance
    "source": "docling",
    "data": List[dict],    # row dicts keyed by column header
    "headers": List[str],
    "markdown": str,       # full markdown table string
    "num_rows": int,
    "num_cols": int,
    "bbox": [x0, y0, x1, y1],
    "confidence": 0.97,    # fixed high-confidence marker
    "stitched": False,     # Docling handles layout natively
    "classification": "",  # filled by SafeAI's _classify_table()
    "nll": "",             # filled by SafeAI's _generate_nll()
}
```

### Installation

Docling is an optional dependency. To enable:

```bash
pip install 'docling>=2.64.0'
```

If Docling is not installed, `DOCLING_AVAILABLE = False` and the pipeline transparently falls back to PyMuPDF. No code changes needed.

### Disabling Docling (use PyMuPDF only)

```python
from pipeline.config import ExtractionConfig
cfg = ExtractionConfig(pdf_path="...", use_docling_tables=False)
```

## Alternatives we considered

### Single-pass extraction (rejected)

Using only PyMuPDF text extraction is fast but misses table structure entirely. Tables render as space-separated values with no column alignment. For medical dosing tables where column membership determines whether "500" means "500 mg" or "500 mL", this is unacceptable.

### Docling / Unstructured.io (original evaluation — now integrated)

We originally evaluated both document intelligence frameworks and rejected them for the following reasons:
- **Docling** provides excellent table detection but adds significant dependencies (PyTorch vision models, ~2 GB) and was slower than PyMuPDF on our 1,161-page PDF.
- **Unstructured.io** had similar overhead and its table extraction quality was comparable to PyMuPDF's built-in `find_tables()` for our structured medical PDFs.

Since our PDFs are digitally-authored (not scanned), the simpler PyMuPDF approach provided equivalent quality with fewer dependencies and faster runtime.

**Update:** After benchmarking CT Health AI's Docling integration, we reversed the Docling decision for table extraction specifically. TableFormer ACCURATE (the transformer-based table model in Docling) outperforms `find_tables()` on complex borderless tables. Docling is now the **optional primary** path, with PyMuPDF as fallback. See the CT Health AI Integration section above.

### Camelot for table extraction (partially adopted)

Camelot excels at borderless tables using its lattice/stream detection. We included it as a fallback for tables that PyMuPDF's `find_tables()` misses (typically borderless formatting tables). However, Camelot requires Ghostscript and is significantly slower per-page, so it runs only on pages where PyMuPDF detection fails.

### OCR-first pipeline (rejected)

Some medical NLP systems OCR every page regardless of content type. Our document profiling (Pass 0) showed that both target PDFs are digitally-authored with no scanned pages. Running OCR on 1,600+ pages would add minutes of processing time with no quality benefit. Instead, OCR runs only on pages flagged as scanned or image-heavy.

### LLM-based extraction (rejected)

Using an LLM to parse tables from raw text would provide semantic understanding but introduces hallucination risk for dosing values. A model that "corrects" `50 mg` to `500 mg` based on contextual expectation could cause medication errors. Our rule-based extraction preserves exact cell values without modification — a critical requirement for safety-critical medical content.

## Output

The extraction engine produces a structured dictionary containing per-page text blocks, classified tables with markdown and structured data, cross-validation scores, and image inventory. This output feeds directly into the [validation stage](benchmarking_and_validation.md) and [chunking stage](chunking_strategy.md).

See also: [pipeline/README.md](../pipeline/README.md) for module-level documentation.
