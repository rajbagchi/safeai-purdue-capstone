# Medical Pipeline Package

Modular production pipeline for WHO Malaria Guidelines: multi-pass extraction, validation, chunking, and two-brain Q&A.

## Source documents (config presets)

`ExtractionConfig` accepts any `pdf_path` string (Windows absolute paths, spaces, etc.). For the two validated PDFs on disk:

| Preset | Default PDF | Output dir (default) |
|--------|-------------|----------------------|
| `extraction_config_who_malaria_nih()` | `C:\temp\capstone\Bookshelf_NBK588130.pdf` | `C:\temp\capstone\medical_kb_who_malaria` |
| `extraction_config_uganda_clinical_2023()` | `C:\temp\capstone\Uganda Clinical Guidelines 2023.pdf` | `C:\temp\capstone\medical_kb_uganda_clinical_2023` |

Each preset sets `document_title` and `critical_content_terms` so Stage 4 medical-term checks are appropriate (malaria-specific vs. broad clinical). Paths are normalized in `ExtractionConfig.__post_init__` via `pathlib.Path.expanduser().resolve()`.

CLI:

```bash
python run_pipeline.py --preset who-malaria
python run_pipeline.py --preset uganda
python run_pipeline.py --pdf "D:\other\guide.pdf" --output-dir ./my_kb
```

Markdown reports (stages + 25 searches):

```bash
python scripts/who_malaria_pipeline_report.py --preset who-malaria
python scripts/who_malaria_pipeline_report.py --preset uganda --reuse-kb
```

## Structure

| Module | Purpose |
|--------|---------|
| `config.py` | `ExtractionConfig`, `ValidationReport`, `TriageLevel`, `DangerSign` |
| `extractor.py` | `MultiPassExtractor` — PDF analysis, text/table/OCR extraction, cross-validation |
| `validator.py` | `ExtractionValidator` — structure, tables, cross-consistency, medical content, human-review flags |
| `chunker.py` | `SmartChunker` — semantic chunks by headings, BM25 search index |
| `guardrail.py` | `MedicalGuardrailBrain` — triage, dangerous advice, citations |
| `orchestrator.py` | `MedicalQASystem` — runs pipeline, saves/loads KB, `answer()` |
| `cli.py` | Interactive Q&A entry point |
| `__main__.py` | Enables `python -m pipeline` |

## Usage

From project root:

```bash
# Run interactive Q&A (builds or loads knowledge base)
python run_pipeline.py

# Or
python -m pipeline
```

In code:

```python
from pipeline import MedicalQASystem, ExtractionConfig

qa = MedicalQASystem("path/to/guidelines.pdf", output_dir="./medical_knowledge_base")
qa.initialize()
result = qa.answer("What is the dose for severe malaria in children?")
```

## Dependencies

Install from repo root:

```bash
pip install -r requirements-pipeline.txt
```

Includes: **PyMuPDF**, **numpy**, **pandas**, **rank-bm25**, **rapidfuzz**, **tabulate** (for `DataFrame.to_markdown` on tables), **pdfplumber** (cross-validation vs. Pass 1 text). Optional: **camelot** for borderless tables.

Extractor behavior:

- **Full-document table scan** (`ExtractionConfig.full_document_table_scan`, default `true`) finds all pages with PyMuPDF tables (not only the first 20 sampled in Pass 0).
- **Embedded images** saved under `{output_dir}/images/` as PNG plus `image_inventory.json` when `enable_image_extraction` is true.
