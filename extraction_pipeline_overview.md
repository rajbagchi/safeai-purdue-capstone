# Extraction Pipeline Overview

**Safe AI Uganda — Purdue Capstone Project**
**Documents:** Config-driven — validated on WHO Malaria Guidelines (478 pp.) and Uganda Clinical Guidelines 2023 (1,161 pp.)
**Last updated:** 12.03.2026

---

## What This Document Is

This is the master reference for the clinical data extraction pipeline. It explains the full end-to-end flow from raw clinical guidelines PDF to physician-verified, deployment-ready chunks — what each stage does, what it reads, what it writes, and how data flows between stages. The pipeline is **config-driven** and supports multiple documents via per-document JSON configs (see `configs/` directory). Metrics shown here cover both validated documents: WHO Malaria Guidelines (478 pages) and Uganda Clinical Guidelines 2023 (1,161 pages).

For detailed implementation notes on any individual stage, see the corresponding strategy document listed in Section 6.

---

## Where Extraction Fits in the Safe AI System

The extraction pipeline is the **foundational upstream process** that feeds the entire Safe AI system. Nothing downstream works without it.

```
┌─────────────────────────────────────────────────────────────────┐
│                    SAFE AI SYSTEM ARCHITECTURE                  │
│                                                                 │
│  ┌──────────────────────────────┐  ┌────────────────────────┐   │
│  │  WHO/MoH Clinical Guidelines │  │  Config JSON            │   │
│  │  (PDF — human-readable only) │  │  (configs/*.json)       │   │
│  └──────────────┬───────────────┘  └───────────┬────────────┘   │
│                 │                               │                │
│                 └───────────┬───────────────────┘                │
│                             ▼                                    │
│  ┌──────────────────────────────┐                               │
│  │   EXTRACTION PIPELINE        │  ◄── YOU ARE HERE             │
│  │   (Stages 1 → 4b)           │                               │
│  │   Offline, one-time process  │                               │
│  └──────────────┬───────────────┘                               │
│                 │                                                │
│                 ▼                                                │
│  ┌──────────────────────────────┐                               │
│  │   DEPLOYMENT GATE            │  Layer 1: Retrieval Scope     │
│  │   verified_by + audit_hash   │  Limitation (Guardrail)       │
│  └──────────────┬───────────────┘                               │
│                 │                                                │
│                 ▼                                                │
│  ┌──────────────────────────────┐                               │
│  │   BRAIN 1: KNOWLEDGE LAYER   │  RAG vector database          │
│  │   (Verified clinical chunks) │  of physician-signed content  │
│  └──────────────┬───────────────┘                               │
│                 │                                                │
│                 ▼                                                │
│  ┌──────────────────────────────┐                               │
│  │   BRAIN 2: REASONING LAYER   │  LLM-powered clinical        │
│  │   + 7-Layer Guardrails       │  recommendations for VHTs     │
│  └──────────────┬───────────────┘                               │
│                 │                                                │
│                 ▼                                                │
│  ┌──────────────────────────────┐                               │
│  │   VHT MOBILE APPLICATION     │  Field deployment in Uganda   │
│  └──────────────────────────────┘                               │
└─────────────────────────────────────────────────────────────────┘
```

### Why Extraction Is a Non-Negotiable

1. **Feeding Brain 1**: MoH guidelines are published as presentation-formatted PDFs with nested tables, algorithms, and flow charts. They cannot be searched or reasoned over by an AI. The extraction pipeline translates these into structured, machine-readable chunks that are embedded into Brain 1's RAG vector database.

2. **Offline Pre-processing**: Extraction is entirely divorced from the real-time operation of the system in the field. It runs once (or periodically when guidelines are updated) in a controlled engineering environment using cloud compute and human reviewers. The output becomes a "static knowledge base" packaged and deployed to VHT workers' mobile devices.

3. **Layer 1 of the Guardrail System**: Extraction forms the basis of Layer 1: Retrieval Scope Limitation in the system's seven-layer guardrail architecture. The mandatory physician verification gate (Stage 4b) ensures the knowledge base only contains verified, MoH-approved content — preventing the ingestion of corrupted or adversarial data.

4. **Error Propagation Risk**: If a parsing error occurs during extraction (e.g., misaligning a dosing table), that error propagates through the entire Two-Brain system, potentially generating incorrect dosing recommendations. This is why the pipeline has 5 stages of validation, not just one.

---

## Pipeline Diagram

```
  ┌─────────────────────────────────────────────────────────────┐
  │           Source PDF + Config JSON (configs/*.json)          │
  │        Validated: Malaria WHO (478 pp), Uganda CG (1161 pp) │
  └────────────────────────┬────────────────────────────────────┘
                           │
                           ▼
  ┌─────────────────────────────────────────────────────────────┐
  │  STAGE 1: Primary Extraction                                │
  │  extraction_mvp_v2.py (1,104 lines)                         │
  │                                                             │
  │  • Docling layout-aware PDF parsing                         │
  │  • PyMuPDF for PDF manipulation                             │
  │  • Table detection, classification (config-driven keywords) │
  │  • NLL generation, image OCR extraction                     │
  │  • Malaria: 93.8% accuracy, 207 tables, 29s (cached)       │
  │  • Uganda:  87.5% accuracy, 899 tables, ~83 min             │
  │                                                             │
  │  OUT: full_extraction.md, table_inventory.json,             │
  │       tables_nll.txt, image_inventory.json                  │
  └────────────────────────┬────────────────────────────────────┘
                           │
                           ▼
  ┌─────────────────────────────────────────────────────────────┐
  │  STAGE 2: Cross-Validation                                  │
  │  stage2_cross_validation.py (1,056 lines)                   │
  │                                                             │
  │  • Independent PyMuPDF extraction for cell-level comparison │
  │  • Table reclassification + page-boundary stitching         │
  │  • Malaria: 12 reclassified, 1 stitch, 100% combined acc.  │
  │  • Uganda:  96 reclassified, 3 stitches, 87.5% combined    │
  │                                                             │
  │  OUT: cross_validation_report.json                          │
  │       (updates tables_nll.txt with stitched tables)         │
  └────────────────────────┬────────────────────────────────────┘
                           │
                           ▼
  ┌─────────────────────────────────────────────────────────────┐
  │  STAGE 3: Automated Plausibility Checks                     │
  │  stage3_automated_checks.py (899 lines)                     │
  │                                                             │
  │  • 6 automated checks on dosing tables:                     │
  │    Weight contiguity, dose monotonicity, weight coverage,   │
  │    clinical bounds, combination consistency, positive/empty  │
  │  • Malaria: 29 dosing tables, 1 stitched (PASS)            │
  │  • Uganda:  385 dosing tables, 1 stitched (FAIL)            │
  │                                                             │
  │  OUT: plausibility_report.json                              │
  └────────────────────────┬────────────────────────────────────┘
                           │
                           ▼
  ┌─────────────────────────────────────────────────────────────┐
  │  STAGE 4a: Chunking + Metadata                              │
  │  stage4a_chunking.py (1,640 lines)                          │
  │                                                             │
  │  • Splits markdown into discrete chunks with metadata       │
  │  • Safety preservation levels: verbatim / high / standard   │
  │  • 17-field clinical metadata (drug, condition, LOC, etc.)  │
  │  • Image OCR enrichment from image_inventory.json           │
  │  • Malaria: 1,478 chunks (31 verbatim / 324 high / 1,123)  │
  │  • Uganda:  3,735 chunks (18 verbatim / 227 high / 3,490)  │
  │                                                             │
  │  OUT: chunks.json                                           │
  └────────────────────────┬────────────────────────────────────┘
                           │
                           ▼
  ┌─────────────────────────────────────────────────────────────┐
  │  STAGE 4b: Clinical Verification Framework                  │
  │  stage4b_review_package.py (1,461 lines)                    │
  │                                                             │
  │  • 5-tier triage for physician review prioritization        │
  │  • 5 Clinical Verification Checks (images via OCR content)  │
  │  • SHA-256 audit hashes for tamper detection                │
  │  • Malaria: 355 review items, 31 mandatory                 │
  │  • Uganda:  245 review items, 3 mandatory                  │
  │                                                             │
  │  OUT: review_package.json, physician_review_report.md       │
  └────────────────────────┬────────────────────────────────────┘
                           │
                           ▼
  ┌─────────────────────────────────────────────────────────────┐
  │  PHYSICIAN REVIEW (Human Step)                              │
  │                                                             │
  │  • IDI physician reviews 31 mandatory chunks (~62 min)      │
  │  • 5 checks: Dosage, Stratification, Contraindications,    │
  │    Conditional Logic, Provenance                            │
  │  • Decisions: Approved / Flagged / Corrected                │
  │  • Returns completed review_package.json                    │
  └────────────────────────┬────────────────────────────────────┘
                           │
                           ▼
  ┌─────────────────────────────────────────────────────────────┐
  │  DEPLOYMENT GATE                                            │
  │                                                             │
  │  stage4b_review_package.py --ingest completed_review.json   │
  │                                                             │
  │  • Validates audit hashes (no content tampering)            │
  │  • Computes digital signatures per chunk                    │
  │  • Updates chunks.json with verified_by fields              │
  │  • SAFETY RULE: No content proceeds to Brain 1 without      │
  │    verified_by signature + audit_hash                       │
  └─────────────────────────────────────────────────────────────┘
```

---

## Data Flow Summary

### What Each Stage Reads and Writes

| Stage | Reads | Writes | Malaria Key Metric | Uganda Key Metric |
|---|---|---|---|---|
| **1. Primary Extraction** | Source PDF + `configs/*.json` | `full_extraction.md`, `table_inventory.json`, `tables_nll.txt`, `image_inventory.json` | 207 tables, 93.8% accuracy | 899 tables, 87.5% accuracy |
| **2. Cross-Validation** | PDF + `table_inventory.json` + `full_extraction.md` + config | `cross_validation_report.json`, updated `tables_nll.txt` | 12 reclassified, 1 stitch, 100% combined | 96 reclassified, 3 stitches, 87.5% combined |
| **3. Plausibility Checks** | `table_inventory.json` + `cross_validation_report.json` + `tables_nll.txt` + config | `plausibility_report.json` | 29 dosing, stitched PASS | 385 dosing, stitched FAIL |
| **4a. Chunking** | `full_extraction.md` + all 3 reports above + `image_inventory.json` + config | `chunks.json` | 1,478 chunks, 207/207 matched | 3,735 chunks |
| **4b. Verification** | `chunks.json` + config | `review_package.json`, `physician_review_report.md` | 355 items, 31 mandatory | 245 items, 3 mandatory |

### How Tables Flow Through the Pipeline

**Malaria WHO Guidelines (478 pages)**

```
Stage 1:  207 tables extracted
            ├── 41 dosing │ 21 evidence │ 2 structural │ 1 clinical │ 142 other
Stage 2:  41 dosing re-examined → 29 confirmed + 12 reclassified + 1 stitched (pp.173–174)
Stage 3:  30 dosing checked → 29 skipped (no weight col) + 1 stitched PASS
Stage 4a: 1,478 chunks (1,235 narrative + 30 dosing + 21 evidence + 14 structural + 1 clinical + 142 other + 35 image)
Stage 4b: 355 review items → T1: 1 │ T2: 29 │ T3: 1 │ T4: 324 │ T5: 1,123 → 31 mandatory
```

**Uganda Clinical Guidelines (1,161 pages)**

```
Stage 1:  899 tables extracted (all classified as "other" or "dosing" by keyword match)
Stage 2:  481 dosing re-examined → 385 confirmed + 96 reclassified + 3 stitched
Stage 3:  385 dosing checked → 385 skipped (no weight col) + 1 stitched FAIL
Stage 4a: 3,735 chunks (2,686 narrative + 3 dosing + 899 other + 147 image)
Stage 4b: 245 review items → T1: 0 │ T2: 3 │ T3: 0 │ T4: 242 │ T5: 3,490 → 3 mandatory
```

---

## Issue Resolution Across Stages

The pipeline is designed so that each stage resolves issues identified by the previous stage:

| Issue | Identified | Resolved | How |
|---|---|---|---|
| Page-boundary table truncation (≥35 kg row lost) | Stage 1 | Stage 2 | PyMuPDF independent extraction + stitching |
| 12 tables misclassified as "dosing" (actually GRADE evidence, abbreviations) | Stage 1 | Stage 2 | Keyword-based reclassification (no numeric weight bands or dose values) |
| DHA-piperaquine complex weight format (e.g., "60 < 80 kg") | Stage 1 | Stage 3 | Enhanced 8-format weight parser |
| Dose monotonicity (does dose increase with weight?) | Not visible in raw extraction | Stage 3 | Automated plausibility check |
| Weight band contiguity (are there gaps between bands?) | Not visible in raw extraction | Stage 3 | Automated plausibility check |
| Clinical metadata extraction (drug, condition, LOC, danger signs, referral) | Not available in raw markdown | Stage 4a | Regex-based extraction from table headers + section hierarchy + OCR text |
| Image content lost in chunking (empty `<!-- image -->` placeholders) | Stage 4a (original) | Stage 4a (v2.1) | OCR text from `image_inventory.json` enriches image chunks |
| Content integrity for deployment | Not addressed pre-4b | Stage 4b | SHA-256 audit hashes + digital signatures |

---

## How to Run the Pipeline

### Prerequisites

- Python 3.9+
- `pip install docling pymupdf` (Stages 1 and 2 only)
- Stages 3–4b: **no external dependencies** (Python stdlib only)
- Source PDF in the path specified by the config JSON
- A config JSON file for the document (see `configs/` directory)

### Onboarding a New Document

To onboard a new clinical guidelines PDF, use the config generator:

```bash
python config_generator.py --pdf path/to/new_guidelines.pdf --output configs/new_guidelines.json
```

This generates an AI-assisted config JSON with document-specific keywords, ground-truth checks, and dose reference ranges. Review and edit the generated config before running the pipeline.

### Full Pipeline Execution

Each config JSON includes an `output_dir` field that determines where outputs are written (e.g., `"output_dir": "extraction_output_malaria"`). This allows multiple documents to be processed without overwriting each other.

```bash
# --- Example: Malaria WHO Guidelines ---
python extraction_mvp_v2.py --config configs/malaria_who_2025.json
python stage2_cross_validation.py --config configs/malaria_who_2025.json
python stage3_automated_checks.py --config configs/malaria_who_2025.json
python stage4a_chunking.py --config configs/malaria_who_2025.json
python stage4b_review_package.py --config configs/malaria_who_2025.json

# --- Example: Uganda Clinical Guidelines ---
python extraction_mvp_v2.py --config configs/uganda_clinical_2023.json
python stage2_cross_validation.py --config configs/uganda_clinical_2023.json
python stage3_automated_checks.py --config configs/uganda_clinical_2023.json
python stage4a_chunking.py --config configs/uganda_clinical_2023.json
python stage4b_review_package.py --config configs/uganda_clinical_2023.json

# --- HUMAN STEP: Physician reviews physician_review_report.md ---
# --- Physician fills in review_package.json decisions ---

# Stage 4b (ingest): Apply physician review to chunks
python stage4b_review_package.py --config configs/malaria_who_2025.json --ingest extraction_output_malaria/completed_review.json
```

### Total Automated Runtime

See the **Elapsed Time** table in [Key Metrics — Dual-Document Comparison](#key-metrics--dual-document-comparison) for per-stage timings for both the Malaria WHO and Uganda CG documents.

---

## Output Files Reference

Each document's outputs are written to its own directory, configured via the `output_dir` field in the config JSON (e.g., `extraction_output_malaria/`, `extraction_output_uganda/`).

| File | Stage | Description |
|---|---|---|
| `full_extraction.md` | 1 | Complete markdown extraction of all PDF pages |
| `table_inventory.json` | 1 | Tables with classifications, page numbers, and column metadata |
| `tables_nll.txt` | 1+2 | Natural Language Logic for dosing tables (incl. stitched from Stage 2) |
| `image_inventory.json` | 1 | Per-image OCR text, caption, page number, PNG path, and dimensions |
| `cross_validation_report.json` | 2 | Reclassification decisions, cell-level comparison results, stitch records |
| `plausibility_report.json` | 3 | Per-table results for 6 automated checks (pass/fail/skipped per table) |
| `chunks.json` | 4a | All chunks with full metadata: safety, 17-field clinical metadata, verified_by, related_chunks |
| `review_package.json` | 4b | Review items with audit hashes, templates, and context for physician review |
| `physician_review_report.md` | 4b | Human-readable review report organized by tier with checklists and decision fields |

---

## Per-Chunk Schema (Stage 4a Output)

Every chunk in `chunks.json` carries 20+ metadata fields, including 17 clinical metadata subfields (expanded from 12 in v2.1 to cover Level of Care, danger signs, referral criteria, clinical features, and clinical section type). The fields most relevant to downstream systems (Brain 1, guardrails) are:

| Field | Purpose for Brain 1 / Guardrails |
|---|---|
| `content` | The text to embed in the RAG vector database |
| `chunk_type` | Routing logic (dosing tables need special handling) |
| `safety.preservation_level` | `verbatim` = must be returned exactly (no LLM paraphrasing); `high` = minimal paraphrasing; `standard` = paraphrasing OK |
| `clinical_metadata` | Structured fields for filtering (drug_name, condition, patient_weight_min/max, contraindications) |
| `section_hierarchy` | Provides context for retrieval ranking |
| `related_chunks` | Enables "context expansion" — when a dosing table is retrieved, also fetch surrounding narratives |
| `source_pages` | Provenance for citation in VHT-facing responses |
| `nll` | Pre-computed natural language explanation of dosing logic; can be served directly instead of having the LLM interpret the table |
| `verified_by` | Deployment gate check — only chunks with `status: "verified"` proceed to Brain 1 |
| `audit_hash` | Integrity check — ensures content in Brain 1 matches what the physician reviewed |

---

## Safety Architecture

### The Integrity Chain

```
PDF Content → Docling Extraction → PyMuPDF Cross-Check → 6 Plausibility Checks
    → Clinical Metadata Enrichment → SHA-256 Audit Hash → Physician 5-Check Review
    → Digital Signature → Deployment Gate → Brain 1 RAG Database
```

Every link in this chain is designed to catch errors before they reach patients:

| Layer | What it catches | Stage |
|---|---|---|
| Docling extraction | Layout/structure parsing (93.8% malaria / 87.5% Uganda) | 1 |
| PyMuPDF cross-check | Cell-level extraction errors, page boundary truncation | 2 |
| Table reclassification | Misclassified non-dosing tables that could pollute dosing retrieval | 2 |
| Weight contiguity check | Missing weight bands (e.g., no dose for 25–35 kg children) | 3 |
| Dose monotonicity check | Illogical dose patterns (e.g., dose decreasing with weight) | 3 |
| Clinical bounds check | Biologically implausible values (e.g., dose > 2.5x population mean) | 3 |
| Preservation levels | LLM paraphrasing of exact dosages ("80+480 mg" → "about 500 mg") | 4a |
| Audit hash | Post-extraction content tampering | 4b |
| Physician 5-check review | All of the above + clinical judgment (contraindications, referral logic) | 4b |
| Digital signature | Non-repudiable proof that a specific physician verified specific content | 4b |
| Deployment gate | Prevents unverified content from reaching patients | 4b ingest |

### The Preservation Level System

This system prevents the most dangerous failure mode in clinical AI — an LLM paraphrasing exact medical dosages:

| Level | Malaria | Uganda | LLM Behavior | Example |
|---|---|---|---|---|
| **verbatim** | 31 | 18 | Must return content exactly as extracted. No paraphrasing, no summarization. | Dosing tables, clinical tables, narratives/images with danger signs or referral criteria |
| **high** | 324 | 227 | Minimal paraphrasing. Core clinical facts must be preserved word-for-word. | Evidence tables, narratives/images with dosing or contraindication keywords |
| **standard** | 1,123 | 3,490 | Paraphrasing acceptable. General narrative and structural content. | Background epidemiology, structural content, non-clinical images |

**Clinical rationale:** If an LLM paraphrases "80+480 mg" as "approximately 500 mg" or "480+80 mg", a VHT may administer the wrong dosage. The `verbatim` tag is an instruction to the RAG retrieval layer and the LLM prompt engineering to return this content exactly — never rephrase, never summarize, never round.

---

## Strategy Documents Reference

Each stage has its own detailed strategy document:

| Stage | Document | Lines | Key Contents |
|---|---|---|---|
| 1 | `stage1_primary_extraction_strategy.md` | ~120 | Extraction architecture, accuracy metrics, known limitations |
| 2 | `stage2_cross_validation_strategy.md` | 258 | Cross-validation methodology, reclassification rules, stitching |
| 3 | `stage3_automated_checks_strategy.md` | 247 | 6 plausibility checks, pass/fail criteria, edge cases |
| 4a | `stage4a_chunking_strategy.md` | 271 | Chunking architecture, schema, safety metadata, physician triage |
| 4b | `stage4b_clinical_verification_strategy.md` | 287 | 5 clinical checks, review tiers, audit hash + digital signature |
| — | **`extraction_pipeline_overview.md`** (this document) | — | End-to-end pipeline, architecture context, data flow |

---

## Codebase Summary

| Script | Lines | Dependencies | Purpose |
|---|---|---|---|
| `extraction_mvp_v2.py` | 1,104 | docling, pymupdf | Stage 1: PDF → markdown + table inventory + NLL + image inventory |
| `stage2_cross_validation.py` | 1,056 | pymupdf | Stage 2: Independent extraction, reclassification, stitching |
| `stage3_automated_checks.py` | 899 | stdlib only | Stage 3: 6 plausibility checks on dosing tables |
| `stage4a_chunking.py` | 1,640 | stdlib only | Stage 4a: Markdown → 1,478 metadata-rich chunks (image OCR enrichment) |
| `stage4b_review_package.py` | 1,461 | stdlib only | Stage 4b: Review package generation + ingestion |
| `pipeline_config.py` | ~90 | stdlib only | Shared config loader — validates and exposes config fields to all stages |
| `config_generator.py` | ~400 | stdlib only | AI-assisted onboarding tool for new PDF documents |
| `configs/` | — | — | Per-document JSON configs (e.g., `malaria_who_2025.json`, `uganda_clinical_2023.json`) |
| **Total** | **~6,650** | | **7 scripts + config directory, 2 external dependencies** |

---

## Key Metrics — Dual-Document Comparison

### Accuracy

| Metric | Malaria WHO 2025 | Uganda CG 2023 |
|---|---|---|
| Source PDF pages | 478 | 1,161 |
| **Stage 1 accuracy (ground truth)** | **93.8%** (15/16) | **87.5%** (7/8) |
| — Text checkpoints | 8/8 (100%) | 7/7 (100%) |
| — Table checkpoints | 6/7 (85.7%) | 0/1 (0%) |
| — Image checkpoints | 1/1 (100%) | — (no image checkpoints) |
| **Stage 2 combined accuracy** | **100%** (16/16) | **87.5%** (7/8) |
| Stage 2 text verification | 100% (16/16) | 100% (8/8) |
| Cell-level agreement (Stage 2) | 86.7%–100% (avg 92.7%) | 6.7%–100% (avg 34.8%) |
| Extraction passes to reach final accuracy | 1 pass (100% after Stage 2 recheck) | 1 pass (87.5% — table checkpoint unresolved) |

### Tables & Images

| Metric | Malaria WHO 2025 | Uganda CG 2023 |
|---|---|---|
| Tables extracted | 207 (174 pass / 33 fail) | 899 (450 pass / 449 fail) |
| Reclassifications (Stage 2) | 12 | 96 |
| True dosing tables (after reclassification) | 29 + 1 stitched = 30 | 385 |
| Weight-based dosing tables checked (Stage 3) | 0 (29 skipped — no weight column) | 0 (385 skipped — no weight column) |
| Stitched tables | 1 (PASS — all 6 checks) | 1 (FAIL — no weight column) |
| Images extracted | 2 | 77 |

### Chunks

| Metric | Malaria WHO 2025 | Uganda CG 2023 |
|---|---|---|
| **Total chunks** | **1,478** | **3,735** |
| — Narrative | 1,235 | 2,686 |
| — Dosing table | 30 | 3 |
| — Evidence table | 21 | 0 |
| — Clinical table | 1 | 0 |
| — Structural table | 14 | 0 |
| — Other table | 142 | 899 |
| — Image | 35 | 147 |
| Verbatim preservation | 31 | 18 |
| High preservation | 324 | 227 |
| Standard preservation | 1,123 | 3,490 |
| Drug name coverage (dosing tables) | 27/30 (90%) | 0/3 (0%) |
| Weight range coverage (dosing tables) | 14/30 (47%) | 1/3 (33%) |

### Physician Review

| Metric | Malaria WHO 2025 | Uganda CG 2023 |
|---|---|---|
| Total review items (Tiers 1–4) | 355 | 245 |
| Tier 1 — Validated dosing (mandatory) | 1 | 0 |
| Tier 2 — Unvalidated dosing (mandatory) | 29 | 3 |
| Tier 3 — Clinical management (mandatory) | 1 | 0 |
| Tier 4 — Evidence + high-priority (recommended) | 324 | 242 |
| Tier 5 — Standard (excluded) | 1,123 | 3,490 |
| **Mandatory review** | **31 (2.1%)** | **3 (0.08%)** |
| Estimated review time (all tiers) | ~224 min | ~127 min |

### Elapsed Time

| Stage | Malaria WHO 2025 | Uganda CG 2023 |
|---|---|---|
| Stage 1 — Primary Extraction | 29.3 s | 4,979.3 s (~83 min) |
| Stage 2 — Cross-Validation | 33.2 s | 275.4 s (~4.6 min) |
| Stage 3 — Plausibility Checks | 0.006 s | 0.014 s |
| Stage 4a — Chunking + Metadata | 1.4 s | 1.9 s |
| Stage 4b — Review Package | 0.5 s | 0.3 s |
| **Total pipeline** | **~64 s (~1.1 min)** | **~5,257 s (~87.6 min)** |

*Note: Malaria times reflect cached Docling conversion (first run ~23 min). Uganda times reflect first run on 1,161 pages.*

### Compute Requirements

| Requirement | Detail |
|---|---|
| GPU | Not required — all stages are CPU-only |
| Stages 1–2 dependencies | `docling`, `pymupdf` (pip install) |
| Stages 3–4b dependencies | Python stdlib only — no external packages |
| Python version | 3.9+ |
| Runtime scales with | PDF page count (Stage 1 dominates: ~4.3 s/page for Uganda, ~0.06 s/page for malaria cached) |
| Total codebase | ~6,650 lines across 7 scripts + config directory |

---

## Git History

| Commit | PR / Tag | Description |
|---|---|---|
| `e5d653c` | — | Stage 1: Primary extraction pipeline and strategy document |
| `0407a30` | PR #1 | Stage 2: Cross-validation with PyMuPDF |
| `6fe057c` | PR #2 | Stage 3: Automated plausibility checks |
| `dee03ae` | PR #3 | Stage 4a: Chunking and metadata strategy |
| `1b57e73` | PR #4 | Stage 4b: Clinical verification framework |
| `30c39bb` | **Tag: `v2.0-pdf-agnostic`** | Config-driven architecture — all disease-specific constants externalized to JSON configs |
| `acb5272` | PR #6 | Broader clinical content extraction, image OCR enrichment, documentation updates |
| — | (pending) | Per-document output directories + dual-document stats |

Repository: [github.com/rajbagchi/safeai-purdue-capstone](https://github.com/rajbagchi/safeai-purdue-capstone)

---

## Changelog

### v2.0 — PDF-Agnostic Config-Driven Architecture (tag: v2.0-pdf-agnostic)

**Before:** Single-document pipeline hardcoded to the WHO malaria PDF. No config files — each script had its own hardcoded constants (drug keywords, ground-truth checks, dose reference ranges, dosing page numbers). Running the pipeline on a different PDF required editing multiple Python files.

**After:** Config-driven architecture. A `configs/` directory holds per-document JSON configs (e.g., `malaria_who_2025.json`, `uganda_clinical_2023.json`). A shared loader (`pipeline_config.py`, ~90 lines) validates and exposes config fields to all stages. `config_generator.py` (~400 lines) provides AI-assisted onboarding for new PDFs. All scripts accept `--config` to select the active document configuration. Two reference configs ship with the pipeline.

### v2.2 — Dual-Document Validation + Per-Document Output Directories

**Before:** Pipeline output was hardcoded to `extraction_output/`. Running a second document would overwrite the first. Metrics in the overview only covered the malaria WHO PDF.

**After:** Each config JSON now includes an `output_dir` field (e.g., `"extraction_output_malaria"`, `"extraction_output_uganda"`), wired through all 5 stage scripts via `pipeline_config.get_output_dir()`. The overview now features a comprehensive dual-document comparison covering accuracy (text, table, image), cell-level agreement, elapsed times per stage, compute requirements, chunk breakdowns, and physician review tiers for both the WHO Malaria Guidelines (478 pages) and Uganda Clinical Guidelines 2023 (1,161 pages).

### v2.1 — Broader Clinical Content + Image OCR Enhancement

**Before:** `clinical_metadata` had 12 fields (drug, condition, dosage, weight, age, route, frequency, duration, contraindications, special_populations, age_min, age_max). No image OCR persistence — images were empty placeholders in chunks (`content: "<!-- image -->"`, `preservation_level: "standard"`, `word_count: 0`). No clinical content expansion for Level of Care, danger signs, referral criteria, or clinical features. Stage 4b treated all images as Tier 5 (excluded).

**After:** `clinical_metadata` now has 17 fields (+`level_of_care`, `clinical_features`, `danger_signs`, `referral_criteria`, `clinical_section_type`). Stage 1 persists `image_inventory.json` with per-image OCR text, captions, page numbers, PNG paths, and dimensions. Stage 4a loads the image inventory, matches images to chunks by page, and enriches them with OCR content (`content_type: "image_ocr"`) and full clinical metadata extraction. Safety Rules 4 and 5 now apply to images (danger signs/referral → verbatim; clinical keywords → high). Stage 4b includes enriched images in Tier 4 review when they have high/verbatim preservation. Three new metadata extractors: clinical table, image, and enhanced narrative (LOC, danger signs, referral, clinical features, section type).
