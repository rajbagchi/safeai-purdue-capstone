# Stage 1: Primary Extraction Strategy

**Safe AI Uganda — Clinical Data Extraction Methodology**
**Document:** Config-driven (reference: WHO Consolidated Malaria Guidelines, B09514-eng.pdf, 478 pages)
**Last updated:** 11.03.2026

---

## Executive Summary

Stage 1 is the primary extraction pass that converts the WHO Malaria Guidelines PDF into structured, machine-readable data. This is the foundation upon which all subsequent validation stages (cross-validation, automated checks, clinical review) are built.

| Metric | Value |
|---|---|
| **Accuracy (text + tables)** | 93.8% (15 of 16 ground-truth checks pass) |
| **Extraction passes required** | 1 (single-pass extraction; remaining 6.2% gap to be resolved in Stage 2 cross-validation) |
| **Total extraction time (first run)** | 23 minutes 7 seconds |
| **Total extraction time (cached re-run)** | 29 seconds |
| **Compute requirements** | CPU-only; Intel i5 (4-core), 16 GB RAM, no GPU required |

The single failure is a dosing table row (`80 + 480 mg` artemether-lumefantrine) that spans a page boundary (pp.173-174). Docling truncates the table at the page break, losing the final row. This is a known limitation of layout-based extraction and is the primary target for Stage 2 cross-validation with an independent OCR engine.

---

## 1. Extraction Architecture

Stage 1 uses a two-tool pipeline: **PyMuPDF** for low-level PDF manipulation and **Docling** (IBM) for layout-aware document understanding.

### 1.1 PDF Handling — PyMuPDF (fitz)

PyMuPDF is used for PDF-level operations that Docling does not natively support:

- **Page-range extraction**: Creates subset PDFs containing only the pages of interest (e.g., dosing tables on pp.170-215), reducing conversion time proportionally.
- **Parallel chunk splitting**: Divides the full PDF into N chunks for multi-core processing.
- **Ground-truth verification**: Scans raw page text to verify page number mappings for benchmark keywords.

PyMuPDF does **not** perform the primary extraction. It prepares the PDF for Docling.

### 1.2 Layout-Aware Extraction — Docling (IBM) v2.5.0

Docling is the primary extraction engine. It processes the PDF through a deep-learning pipeline that understands document layout:

- **Text extraction**: Converts all 478 pages to structured Markdown, preserving heading hierarchy, paragraph structure, and reading order.
- **Table structure recognition**: Uses the TableFormer model (FAST mode) to detect table boundaries, identify rows/columns/headers, and export each table as a Markdown table with cell-level fidelity.
- **Image region detection**: Identifies embedded figures and diagrams, crops them as image regions, and makes them available for downstream OCR.

**Configuration:**
- `do_ocr = False` — The PDF has selectable text; Docling extracts it directly without OCR overhead.
- `do_table_structure = True` — Enables the TableFormer deep-learning model for table parsing.
- `images_scale = 2.0` — Renders images at 2x DPI for better OCR accuracy downstream.
- `generate_picture_images = True` — Produces cropped PIL images for each detected figure.

### 1.3 Image OCR — RapidOCR (onnxruntime)

For the 2 embedded images in the PDF (a therapeutic pathway diagram on p.198 and an evidence-to-decision figure on p.450), Docling crops the image region and RapidOCR extracts any text within:

- RapidOCR runs on the ONNX Runtime backend (CPU-only, no GPU required).
- The OCR engine is initialised once as a singleton to avoid reloading the model per image.
- Images smaller than 50x50 pixels are skipped as PDF layout artifacts.

### 1.4 Table Classification and Linearisation

After extraction, each of the 207 tables is automatically classified using keyword scoring:

| Classification | Count | Description |
|---|---|---|
| **dosing** | 41 | Weight-based drug dosage tables (clinically critical) |
| **evidence** | 21 | GRADE evidence quality tables from annexes |
| **clinical_management** | 1 | Complication management tables (e.g., severe malaria) |
| **structural** | 2 | Table of contents, abbreviation lists |
| **other** | 142 | Reference tables, metadata, supplementary |

Table classification keywords are now loaded from the JSON config file (`clinical_table_keywords` field) via `pipeline_config.py`. The default 7 clinical management keywords can be expanded per-document — for example, the Uganda Clinical Guidelines config uses 33 keywords. Classification uses case-insensitive matching, and a relaxed threshold allows a single clinical keyword (with no dosing keywords present) to classify a table as `clinical_management`.

**Dosing** and **clinical_management** tables are converted to Natural Language Logic (NLL) — a linearised IF/THEN format that enables LLMs to reason about tabular data without alignment hallucinations:

```
IF Body weight is 5 to < 15 kg, THEN Dose is 20 + 120 mg, given twice daily for 3 days.
IF Body weight is 15 to < 25 kg, THEN Dose is 40 + 240 mg, given twice daily for 3 days.
```

---

## 2. Scoring and Accuracy Benchmarking

### 2.1 Ground-Truth Design

Accuracy is measured against 16 hand-verified ground-truth checks spanning three content types:

| Content type | Checks | Pass | Fail | Accuracy |
|---|---|---|---|---|
| **Text** | 8 | 8 | 0 | 100% |
| **Table** | 7 | 6 | 1 | 85.7% |
| **Image** | 1 | 1 | 0 | 100% |
| **Total** | **16** | **15** | **1** | **93.8%** |

Ground-truth entries are defined as JSON objects with a page number, content type, and a list of keywords that must be present in the extracted output. Ground-truth entries are loaded from the `ground_truth` field in the pipeline config JSON file (e.g., `configs/malaria_who_2025.json`). This allows each document to define its own benchmark checks without modifying the extraction script.

```json
{"page": 173, "type": "table", "must_contain": ["20 + 120"]}
```

The benchmark focuses on the clinically critical sections: ACT dosing tables (pp.173-178), severe malaria management (p.212), and the therapeutic pathway figure (p.198).

### 2.2 How Scoring Works

The scorecard operates in three search spaces:

1. **Text checks** search the full Markdown export (~2.26 million characters).
2. **Table checks** search the concatenated Markdown of all 207 tables.
3. **Image checks** search the concatenated OCR text and captions from all extracted images.

Each ground-truth keyword is matched case-insensitively. A check **passes** only if every keyword in its `must_contain` list is found. The final accuracy is the percentage of checks that pass.

### 2.3 Known Failure

The single failure is the artemether-lumefantrine dosing table (Table 13-14, pp.173-174). This table has 4 weight bands, but the final row (`>= 35 kg: 80 + 480 mg`) falls on page 174 while the table header and first 3 rows are on page 173. Docling treats each page's table fragment independently, resulting in a 3-row table on p.173 and a 1-row fragment on p.174 that is not linked back to its header.

**Resolution path:** Stage 2 cross-validation with PaddleOCR or Pixtral will independently re-extract this table and flag the discrepancy for reconciliation.

### 2.4 Additional Quality Checks

Beyond the ground-truth scorecard, Stage 1 also runs:

- **Table structural quality** (174 pass / 33 fail): Checks for empty cells, missing headers, and preserved special characters. Failures are primarily in GRADE annex tables (pp.415-473) that are misclassified as dosing.
- **Dosing plausibility** (41 checked, 1 issue): Validates weight-band contiguity, dose monotonicity, and positive values across all dosing tables. One issue found: DHA-piperaquine table (p.176) has a weight-band parsing edge case.

---

## 3. Extraction Acceleration

Three optimisation strategies reduce extraction time for iterative development and re-processing:

### 3.1 Conversion Result Caching

| | First run | Cached re-run |
|---|---|---|
| **PDF conversion** | 1,352 seconds | 1.8 seconds |
| **Total pipeline** | 1,387 seconds | 29 seconds |
| **Speedup** | — | **~47x faster** |

After Docling converts the PDF, the entire `DoclingDocument` object is serialised to a JSON cache file (16.5 MB) using Docling's built-in `save_as_json()` method. On subsequent runs, the cache is loaded in under 2 seconds via `load_from_json()`, completely bypassing the 22-minute conversion.

The cache key is a SHA-256 hash of the PDF's absolute path, file size, and modification timestamp. If the PDF changes, the cache is automatically invalidated and a fresh conversion is triggered.

### 3.2 Page-Range Extraction

For targeted extraction of specific sections (e.g., only the dosing tables on pp.170-215), PyMuPDF creates a subset PDF containing only the requested pages before passing it to Docling. This reduces conversion time proportionally:

- Full PDF (478 pages): ~22 minutes
- Dosing section only (46 pages): ~2 minutes (estimated)

Page numbers in the extraction output are automatically remapped to their original PDF page numbers, so downstream consumers always see correct provenance.

### 3.3 Parallel Chunk Processing

For first-run conversion of the full PDF without a cache, the document is split into N chunks (one per CPU core) using PyMuPDF. Each chunk is converted in a separate process via Python's `multiprocessing` module using the `spawn` context (safe for PyTorch model loading). Results are merged after all workers complete.

- Documents under 50 pages automatically fall back to sequential mode (startup overhead exceeds benefit).
- Default: sequential (`N_WORKERS = 1`). Set to `0` for auto-detection or a specific number for manual control.

---

## 4. Time Breakdown by Stage

*As of 03.03.2026 — full 478-page extraction on Intel i5-8257U, 16 GB RAM, macOS.*

### 4.1 First Run (No Cache)

| Stage | Time | % of Total | Description |
|---|---|---|---|
| Build converter | 0.0s | 0.0% | Docling initialisation (models already downloaded) |
| **PDF conversion** | **1,352.5s** | **97.5%** | Layout analysis + TableFormer on 478 pages |
| Text export | 2.2s | 0.2% | Markdown generation from document model |
| Table processing | 25.5s | 1.8% | Classification + NLL linearisation of 207 tables |
| Image OCR | 6.5s | 0.5% | RapidOCR on 2 extracted images |
| **Total** | **1,386.6s** | **100%** | **~23 minutes 7 seconds** |

PDF conversion dominates at 97.5% of total time. This is the deep-learning layout analysis step (TableFormer, reading-order detection) running on CPU. All other stages combined take under 35 seconds.

### 4.2 Cached Re-Run

| Stage | Time | % of Total | Description |
|---|---|---|---|
| Cache load | 1.8s | 6.1% | Load serialised DoclingDocument from JSON |
| Text export | 1.9s | 6.4% | Markdown generation |
| Table processing | 20.0s | 68.3% | Classification + NLL linearisation |
| Image OCR | 5.6s | 19.2% | RapidOCR on 2 images |
| **Total** | **29.3s** | **100%** | **~29 seconds** |

With caching, the bottleneck shifts to table processing (68.3%), which involves classifying 207 tables and generating NLL for 42 of them.

---

## 5. Output Artefacts

All outputs are written to the `extraction_output/` directory. Each file serves a specific role in the extraction and validation pipeline.

### 5.1 `extraction_summary.json` (9.9 KB)

**What it is:** A single JSON file containing the complete scorecard from the extraction run.

**What it contains:**
- Ground-truth accuracy results (per-check pass/fail with found and missing keywords)
- Table quality report (pass/fail counts, list of flagged dosing tables with specific issues)
- Image quality report
- Dosing plausibility check results (weight-band gaps, dose monotonicity violations)
- Timing breakdown for each pipeline stage
- Overall counts (pages, tables, images)

**Why it is necessary:** This is the primary artefact for auditing and tracking extraction quality over time. It enables automated comparison between extraction runs and provides the data for the executive summary metrics (accuracy %, time, counts). The `as of` date and detailed per-check results support traceability requirements for clinical data.

### 5.2 `cache/docling_*.json` (16.5 MB)

**What it is:** A serialised copy of the full Docling document model, stored as JSON with base64-encoded image data.

**What it contains:** The complete internal representation of the 478-page document, including all text content, table structures, image regions, page layouts, and provenance metadata.

**Why it is necessary:** Eliminates the 22-minute PDF conversion step on subsequent runs. This is essential for iterative development — changing classification logic, NLL formatting, or plausibility checks can be tested in ~30 seconds instead of ~23 minutes. The cache auto-invalidates if the source PDF is modified.

### 5.3 `full_extraction.md` (2.2 MB, 15,248 lines)

**What it is:** The complete document content exported as Markdown.

**What it contains:** All text, headings, lists, and inline table representations from the 478-page PDF, preserving the document's hierarchical structure and reading order.

**Why it is necessary:** Serves as the human-readable reference for the extracted content. Used by Stage 2 cross-validation as the baseline to compare against independent OCR output. Also serves as the input for any downstream chunking strategy (semantic search, RAG, LLM context windows).

### 5.4 `table_inventory.json` (28 KB, 207 entries)

**What it is:** A structured index of every table detected in the document.

**What it contains:** For each of the 207 tables: index number, source page number, classification (dosing/evidence/structural/clinical_management/other), dimensions (rows x columns), and whether NLL linearisation was generated.

**Why it is necessary:** Enables targeted review of specific table types without loading the full extraction. Clinicians reviewing Stage 4 can filter to only dosing tables. The classification data also feeds into the table quality report — only dosing tables are checked for empty cells and special characters, avoiding false positives on evidence annex tables where merged cells are expected.

### 5.5 `tables_nll.txt` (74 KB, 374 lines)

**What it is:** Natural Language Logic linearisations of all dosing and clinical management tables.

**What it contains:** IF/THEN sentences derived from 42 tables (41 dosing + 1 clinical management), annotated with table index, page number, and classification. Example:

```
### Table 13 (p.173, dosing) ###
IF Body weight is < 15 kg, THEN Dose (mg) is 20 + 120.
IF Body weight is 15 to < 25 kg, THEN Dose (mg) is 40 + 240.
IF Body weight is 25 to < 35 kg, THEN Dose (mg) is 60 + 360.
```

**Why it is necessary:** Standard Markdown tables are prone to LLM alignment hallucinations — models may misattribute values to the wrong columns when tables have many columns or merged cells. NLL converts tabular relationships into explicit natural language that LLMs can reason about reliably. This format is specifically designed for the downstream RAG pipeline where an LLM must answer dosing queries accurately.

### 5.6 `image_*.png` (2 clinically relevant + 33 smaller elements)

**What it is:** Cropped image regions extracted from the PDF by Docling's image detection pipeline.

**What it contains:** 35 total image regions detected, of which 2 are clinically meaningful:
- `image_001.png` (36 KB): Therapeutic pathway diagram for P. vivax anti-relapse treatment (p.198)
- `image_032.png` (278 KB): Evidence-to-decision framework figure (p.450)

The remaining 33 are smaller PDF layout elements (logos, decorative elements, small charts).

**Why it is necessary:** Clinical pathway diagrams contain decision logic that is not captured in text or tables. The OCR output from these images feeds into the ground-truth benchmark (the p.198 image must contain "G6PD" and "primaquine") and will be cross-validated in Stage 2.

### 5.7 `image_inventory.json` (per-image OCR metadata)

**What it is:** A JSON array of all images extracted from the PDF, with their OCR text and metadata.

**What it contains:** For each image: index, source page number, caption text (from Docling), OCR text (from RapidOCR), saved PNG path, and image dimensions (width, height).

**Why it is necessary:** Stage 4a uses this file to enrich image chunks with OCR text content and clinical metadata, instead of creating empty placeholder chunks. This ensures that clinical flowcharts, diagnostic algorithms, and severity classification diagrams contribute their text content to the RAG knowledge base.

---

## Changelog

### v2.0 — PDF-Agnostic Config-Driven Architecture (tag: v2.0-pdf-agnostic)

**Before:** All disease-specific constants were hardcoded: 7 clinical management keywords, 16 malaria ground-truth checks, a single PDF path (`B09514-eng.pdf`), drug keywords, dosing keywords, and dose reference ranges — all embedded directly in `extraction_mvp_v2.py`.

**After:** All disease-specific constants externalized to JSON config files in `configs/` directory (e.g., `malaria_who_2025.json`, `uganda_clinical_2023.json`). Shared config loader `pipeline_config.py` provides accessor functions. All stages accept a `--config` CLI flag to select the document config. New `config_generator.py` script enables AI-assisted onboarding of new clinical PDFs — it scans a PDF and generates a draft config with drug keywords, ground truth, dosing pages, and condition patterns.

### v2.1 — Broader Clinical Content + Image OCR Enhancement

**Before:** `classify_table()` used exact-case keyword matching with a strict score threshold. Image OCR text was extracted by RapidOCR in memory but NOT persisted to disk — Stage 4a only saw empty `<!-- image -->` placeholder markers.

**After:** Table classification uses case-insensitive matching with a relaxed threshold: a single clinical keyword (with no dosing keywords) is sufficient for `clinical_management` classification. Config field `clinical_table_keywords` expanded to 33 keywords for Uganda Clinical Guidelines. New `image_inventory.json` output persists per-image OCR text, caption, page number, PNG path, and dimensions to disk, enabling Stage 4a to enrich image chunks with actual clinical content.

---

## 6. What Stage 1 Does Not Cover

The following are explicitly deferred to subsequent stages:

| Gap | Resolution Stage |
|---|---|
| Page-boundary table truncation (80 + 480 mg row) | Stage 2: Cross-validation with PaddleOCR/Pixtral |
| Abbreviation tables misclassified as dosing (pp.27, 29) | Stage 2: Classification refinement |
| DHA-piperaquine weight-band parsing edge case | Stage 3: Enhanced plausibility rules |
| Clinical correctness of extracted dosing values | Stage 4: IDI physician review |
| Content chunking for RAG/LLM pipeline | **Implemented** — Stage 4a chunking + metadata strategy |
