# Setup and Usage Guide

This guide walks through installing dependencies, configuring PDF paths, running the pipeline, and interacting with the Q&A system in your terminal.

## Non-technical users (Mac): start.command

If you are not comfortable with the command line, use the **`start.command`** launcher included in the project root. It handles all setup automatically.

**One-time setup (Terminal, run once):**

```bash
chmod +x /path/to/safeai-purdue-capstone-main/start.command
```

After that, **double-click `start.command`** in Finder every time. It will:

1. Create a Python virtual environment (`safeai-env/`) on first run
2. Install all dependencies automatically (2-5 minutes on first run)
3. Open a native Mac file picker to select your guideline PDF (first run only)
4. Process the PDF into a knowledge base (first run only, 5-15 minutes)
5. Launch the conversational assistant: "What can I help you with today?"

Every subsequent run: just double-click and the assistant opens in seconds.

## Prerequisites

- **Python 3.9+**
- **A clinical guideline PDF** (WHO Malaria or Uganda Clinical Guidelines, or any medical PDF)

## Installation

```bash
# Clone the repository
git clone https://github.com/rajbagchi/safeai-purdue-capstone.git
cd safeai-purdue-capstone

# Install dependencies
pip install -r requirements-pipeline.txt
```

### Key dependencies

| Package | Purpose |
|---|---|
| `pymupdf` | Primary PDF text and table extraction (Pass 1, 2) -- fallback when Docling unavailable |
| `pdfplumber` | Secondary extraction for cross-validation (Pass 4) |
| `rank-bm25` | Sparse keyword retrieval |
| `sentence-transformers` | Dense embedding (`all-MiniLM-L6-v2`) and cross-encoder reranking (`ms-marco-MiniLM-L-6-v2`) |
| `faiss-cpu` | Approximate nearest-neighbor search |
| `rapidfuzz` | Fuzzy text matching for cross-validation |
| `numpy>=1.26` | numpy 2.x used on Python 3.13 (pre-built wheels); 1.26.x on older Python |

> **Note:** `sentence-transformers`, `faiss-cpu`, and `chromadb` are optional. If unavailable, the pipeline falls back to BM25-only retrieval.

### Optional: Docling + TableFormer ACCURATE (recommended for production)

For best table extraction accuracy (especially borderless or multi-column dosing tables), install Docling:

```bash
pip install 'docling>=2.64.0'
```

When installed, Docling's TableFormer transformer model is used as the primary table extractor. PyMuPDF remains the fallback. Docling adds ~2 GB of PyTorch vision model dependencies but achieves near-perfect table recall on clinical PDFs. See [docs/extraction_strategy.md](extraction_strategy.md) for details.

To disable Docling even if installed, set `use_docling_tables=False` in `ExtractionConfig`.

### Optional: ColPali v1.2 visual retrieval (recommended for image-heavy PDFs)

Some clinical PDFs contain dosing tables and flow charts rendered as images rather than text. These pages are invisible to BM25 and FAISS. ColPali v1.2 (PaliGemma-3B) embeds page images as patch vectors and uses MaxSim late-interaction scoring to find visually relevant pages.

```bash
# Install dependencies
pip install 'colpali-engine>=0.3.8' torch torchvision pypdfium2

# Run the pipeline first to build the knowledge base
python run_pipeline.py --pdf /path/to/guideline.pdf --output-dir ./my_output

# Then build the ColPali index (one-time, per PDF)
python scripts/build_colpali_index.py --pdf /path/to/guideline.pdf --kb ./my_output

# query.py auto-detects the index -- no extra flags needed
python query.py "ACT dosing by weight" --kb ./my_output
```

ColPali is fully optional. If not installed or the index is not present, the retriever continues with BM25 + FAISS + cross-encoder. See [docs/retrieval_strategy.md](retrieval_strategy.md) for details on the MaxSim scoring and content-aware weighting.

## Configuring PDF paths

The pipeline needs to know where your PDF lives. There are three ways to specify it:

### Option 1: Command-line argument (recommended)

```bash
python run_pipeline.py --preset who-malaria --pdf /path/to/Bookshelf_NBK588130.pdf
```

### Option 2: Environment variables

```bash
# WHO Malaria
export MALARIA_PDF="/path/to/Bookshelf_NBK588130.pdf"
python run_pipeline.py --preset who-malaria

# Uganda Clinical Guidelines
export UGANDA_PDF="/path/to/Uganda_Clinical_Guidelines_2023.pdf"
python run_pipeline.py --preset uganda
```

### Option 3: Any PDF (no preset)

```bash
python run_pipeline.py --pdf /path/to/any_guideline.pdf
```

This creates a generic `ExtractionConfig` with no document-specific keywords.

## Running the pipeline

### With a preset

Presets load document-specific keywords, drug vocabularies, and classification rules from `configs/*.json`:

```bash
# WHO Malaria Guidelines
python run_pipeline.py --preset who-malaria --pdf /path/to/malaria.pdf

# Uganda Clinical Guidelines 2023
python run_pipeline.py --preset uganda --pdf /path/to/uganda.pdf
```

### With a custom output directory

```bash
python run_pipeline.py --preset who-malaria \
    --pdf /path/to/malaria.pdf \
    --output-dir ./my_output
```

### What happens during a run

The pipeline executes 5 steps in sequence:

```
STEP 1: MULTI-PASS EXTRACTION
  Pass 0 - Document analysis (page count, table detection)
  Pass 1 - Text extraction with structure
  Pass 2 - Table extraction + page-boundary stitching (Pass 2b)
  Pass 4 - Cross-validation (pdfplumber vs PyMuPDF)
  Pass images - Embedded image extraction + OCR

STEP 2: VALIDATION
  Stage 1 - Structure checks
  Stage 2 - Table quality
  Stage 3 - Cross-validation consistency
  Stage 4 - Medical content presence
  Stage 6 - Dosing plausibility (6 checks per table)
  Stage 5 - Human review flagging

STEP 3: SMART CHUNKING
  Semantic parent chunks + parent-child splitting + search index

STEP 4: CLINICAL VERIFICATION PACKAGE
  Physician review package + deployment gate

STEP 5: GUARDRAIL BRAIN INITIALIZATION
  Knowledge base saved, system ready for Q&A
```

### Output directory structure

After a successful run, your output directory will contain:

```
my_output/
  cache/                     # Pickled extraction cache (speeds up re-runs)
  images/                    # Extracted embedded images (PNG)
  tables/                    # Individual table markdown files
  validation/                # Timestamped JSON validation reports
  chunks.json                # All semantic chunks with metadata
  knowledge_base.json        # Full extraction + validation + chunks
  review_package.json        # Clinical verification items for physician review
  physician_review_report.md # Markdown physician review document
  image_inventory.json       # Image metadata (OCR text, captions)
  tables_nll.txt             # Natural language descriptions of dosing tables
```

The RAG retrieval artifacts (benchmark results, child chunks, brain1 mobile package) are stored separately in [`rag_output/`](../rag_output/). See [`rag_output/README.md`](../rag_output/README.md) for the full directory guide.

## Verbatim query interface (no LLM)

`query.py` provides a standalone query CLI that returns verbatim passages from a processed knowledge base -- no LLM, no synthesis, no paraphrasing. Every result includes the section heading, page number, preservation level, and the exact source text.

```bash
# Basic query (auto-detects KB directory)
python query.py "What is the treatment for malaria in children?"

# Specify result count
python query.py "ACT dosing by weight" --top-k 3

# Specify KB directory explicitly
python query.py "Danger signs requiring referral" --kb ./medical_kb_who_malaria

# Show only the matching child chunk (not full parent context)
python query.py "Amoxicillin dose for pneumonia" --child-only
```

The query pipeline: normalize spelling -> hybrid BM25 + FAISS + cross-encoder -> return verbatim parent chunk text. The KB directory must contain a `knowledge_base.json` (preferred) or `chunks.json` file, produced by `run_pipeline.py`.

### Auto-detected KB directories

`query.py` checks these paths automatically when `--kb` is not specified:
- `./medical_kb_who_malaria`
- `./medical_kb_uganda_clinical_2023`
- `./medical_knowledge_base`

## Interactive Q&A mode

After the pipeline finishes, it drops into an interactive prompt:

```
======================================================================
INTERACTIVE Q&A MODE
Type 'quit' to exit, 'status' for system status
======================================================================

--------------------------------------------------
Your question: What is the recommended treatment for uncomplicated malaria?
```

### Commands

| Input | Action |
|---|---|
| Any question | Retrieves relevant chunks and generates a guardrail-validated response |
| `status` | Shows chunk count, validation confidence, and human review status |
| `quit` / `exit` / `q` | Exits the Q&A session |

### Example session

```
Your question: What is the dosing for artemether-lumefantrine in children?

======================================================================
Based on the WHO guidelines, artemether-lumefantrine (AL) is dosed by
body weight for children with uncomplicated P. falciparum malaria...

Triage Level: GREEN
Immediate Actions: ...
Citations: Page 173, Page 174
======================================================================
```

## Re-running with a cached knowledge base

On the first run, the pipeline extracts and processes the full PDF. On subsequent runs with the same output directory, it loads the cached knowledge base and skips directly to Q&A:

```
MEDICAL Q&A SYSTEM - COMPLETE PIPELINE
Loading existing knowledge base from ./my_output/knowledge_base.json
System ready!
```

To force a full re-extraction, delete the output directory or use a new `--output-dir`.

## Running the test suite

```bash
# Run all 444 tests
python -m pytest tests/ -q

# Run a specific test file
python -m pytest tests/test_dosing_plausibility.py -v

# Run with coverage
python -m pytest tests/ --cov=pipeline --cov-report=term-missing
```

## Generating reports

Two report scripts are included in `scripts/`:

```bash
# Full pipeline report (extraction + validation + Q&A for 25 queries)
python scripts/who_malaria_pipeline_report.py

# Response layer validation (guardrail pass rates across 50 queries)
python scripts/response_layer_validation_report.py
```

Reports are written to the `reports/` directory.

## Troubleshooting

| Issue | Solution |
|---|---|
| `ModuleNotFoundError: No module named 'sentence_transformers'` | Install: `pip install sentence-transformers`. Pipeline will fall back to BM25-only if missing. |
| `numpy` build failure during install | Python 3.13 cannot build numpy 1.x from source. The requirement is now `numpy>=1.26` which installs pre-built numpy 2.x wheels on Python 3.13. Delete your venv and reinstall. |
| PDF not found | Set the env var (`MALARIA_PDF` or `UGANDA_PDF`) or pass `--pdf /absolute/path` |
| Slow first run | The first run downloads embedding models (~90 MB). Subsequent runs use the cached model. |
| `EOFError` in scripts | The Q&A loop handles EOF gracefully. Use `Ctrl+C` or pipe `echo quit` for non-interactive runs. |
