# Extraction Pipeline Overview

**Safe AI Uganda — Purdue Capstone Project**
**Document:** WHO Consolidated Malaria Guidelines (B09514-eng.pdf, 478 pages)
**Last updated:** 05.03.2026

---

## What This Document Is

This is the master reference for the clinical data extraction pipeline. It explains the full end-to-end flow from raw WHO PDF to physician-verified, deployment-ready chunks — what each stage does, what it reads, what it writes, and how data flows between stages.

For detailed implementation notes on any individual stage, see the corresponding strategy document listed in Section 6.

---

## Where Extraction Fits in the Safe AI System

The extraction pipeline is the **foundational upstream process** that feeds the entire Safe AI system. Nothing downstream works without it.

```
┌─────────────────────────────────────────────────────────────────┐
│                    SAFE AI SYSTEM ARCHITECTURE                  │
│                                                                 │
│  ┌──────────────────────────────┐                               │
│  │  WHO/MoH Clinical Guidelines │  (PDF — human-readable only)  │
│  └──────────────┬───────────────┘                               │
│                 │                                                │
│                 ▼                                                │
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
  │                  WHO PDF (B09514-eng.pdf)                   │
  │                     478 pages                               │
  └────────────────────────┬────────────────────────────────────┘
                           │
                           ▼
  ┌─────────────────────────────────────────────────────────────┐
  │  STAGE 1: Primary Extraction            (~23 min first run) │
  │  extraction_mvp_v2.py (1,104 lines)                         │
  │                                                             │
  │  • Docling layout-aware PDF parsing                         │
  │  • PyMuPDF for PDF manipulation                             │
  │  • Table detection, classification, NLL generation          │
  │  • 93.8% accuracy (15/16 ground-truth checks pass)          │
  │                                                             │
  │  OUT: full_extraction.md (2.2 MB)                           │
  │       table_inventory.json (207 tables)                     │
  │       tables_nll.txt (43 tables with NLL)                   │
  └────────────────────────┬────────────────────────────────────┘
                           │
                           ▼
  ┌─────────────────────────────────────────────────────────────┐
  │  STAGE 2: Cross-Validation                         (~8.5s)  │
  │  stage2_cross_validation.py (1,056 lines)                   │
  │                                                             │
  │  • Independent PyMuPDF extraction for cell-level comparison │
  │  • Table reclassification: 41 → 29 true dosing tables       │
  │  • Page-boundary stitching: recovers ≥35 kg row (p.173-174)│
  │  • 12 tables reclassified (dosing → structural/other)       │
  │                                                             │
  │  OUT: cross_validation_report.json                          │
  │       (updates tables_nll.txt with stitched table)          │
  └────────────────────────┬────────────────────────────────────┘
                           │
                           ▼
  ┌─────────────────────────────────────────────────────────────┐
  │  STAGE 3: Automated Plausibility Checks            (~0.2s)  │
  │  stage3_automated_checks.py (899 lines)                     │
  │                                                             │
  │  • 6 automated checks on dosing tables:                     │
  │    Weight contiguity, dose monotonicity, weight coverage,   │
  │    clinical bounds, combination consistency, positive/empty  │
  │  • 8 tables pass all 6 checks (7 individual + 1 stitched)  │
  │  • 22 tables skipped (no weight column — not true dosing)   │
  │                                                             │
  │  OUT: plausibility_report.json                              │
  └────────────────────────┬────────────────────────────────────┘
                           │
                           ▼
  ┌─────────────────────────────────────────────────────────────┐
  │  STAGE 4a: Chunking + Metadata                     (~1.1s)  │
  │  stage4a_chunking.py (1,640 lines)                          │
  │                                                             │
  │  • Splits 2.2 MB markdown into 1,478 discrete chunks        │
  │  • Safety preservation levels: verbatim / high / standard   │
  │  • Clinical metadata: drug names, weight ranges, conditions │
  │  • Section hierarchy reconstruction + related-chunk linking │
  │  • 207/207 inventory tables matched (100%)                  │
  │                                                             │
  │  OUT: chunks.json (1,478 chunks, 10.6 MB)                  │
  └────────────────────────┬────────────────────────────────────┘
                           │
                           ▼
  ┌─────────────────────────────────────────────────────────────┐
  │  STAGE 4b: Clinical Verification Framework         (~0.4s)  │
  │  stage4b_review_package.py (1,461 lines)                    │
  │                                                             │
  │  • 5-tier triage: 31 mandatory, 325 recommended, 1,122 skip│
  │  • 5 Clinical Verification Checks per item                  │
  │  • SHA-256 audit hashes for tamper detection                │
  │  • Physician-readable markdown report by tier               │
  │  • Ingest mode: validates reviews, computes signatures      │
  │                                                             │
  │  OUT: review_package.json (356 items, 1.8 MB)              │
  │       physician_review_report.md (1.0 MB)                  │
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

| Stage | Reads | Writes | Key Metric |
|---|---|---|---|
| **1. Primary Extraction** | `B09514-eng.pdf` | `full_extraction.md`, `table_inventory.json`, `tables_nll.txt` | 207 tables, 93.8% accuracy |
| **2. Cross-Validation** | PDF + `table_inventory.json` + `full_extraction.md` | `cross_validation_report.json`, updated `tables_nll.txt` | 12 reclassifications, 1 stitch |
| **3. Plausibility Checks** | `table_inventory.json` + `cross_validation_report.json` + `tables_nll.txt` | `plausibility_report.json` | 8/29 pass all 6 checks |
| **4a. Chunking** | `full_extraction.md` + all 3 reports above | `chunks.json` | 1,478 chunks, 207/207 matched |
| **4b. Verification** | `chunks.json` | `review_package.json`, `physician_review_report.md` | 356 items, 31 mandatory |

### How Tables Flow Through the Pipeline

```
Stage 1:  207 tables extracted from PDF
            │
            ├── 41 classified as "dosing"
            ├── 21 classified as "evidence"
            ├──  2 classified as "structural"
            ├──  1 classified as "clinical"
            └── 142 classified as "other"
            │
Stage 2:  41 dosing tables re-examined
            │
            ├── 29 confirmed as true dosing tables
            ├── 12 reclassified to structural/other (no dose values)
            └──  1 stitched table recovered (pp.173–174, ≥35 kg row)
            │
            │   NOTE: 29 confirmed + 1 stitched = 30 dosing table chunks
            │
Stage 3:  30 dosing tables checked (29 individual + 1 stitched)
            │
            ├──  8 pass all 6 plausibility checks (7 individual + 1 stitched)
            └── 22 skipped (no weight column — GRADE evidence, abbreviations)
            │
Stage 4a: 207 tables + 1 stitched = 208 table chunks
          (plus 1,235 narrative + 35 image = 1,478 total chunks)
            │
            ├── 30 dosing_table chunks (preservation: verbatim)
            ├── 21 evidence_table chunks
            ├── 14 structural_table chunks
            ├──  1 clinical_table chunk (preservation: verbatim)
            └── 142 other_table chunks
            │
Stage 4b: 356 review items generated (Tiers 1–4)
            │
            ├── Tier 1:   8 validated dosing tables (MANDATORY)
            ├── Tier 2:  22 unvalidated dosing tables (MANDATORY)
            ├── Tier 3:   1 clinical management table (MANDATORY)
            ├── Tier 4: 325 evidence + high-priority narratives (RECOMMENDED)
            └── Tier 5: 1,122 standard chunks (EXCLUDED from review)
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
| Clinical metadata extraction (drug name, condition, contraindications) | Not available in raw markdown | Stage 4a | Regex-based extraction from table headers + section hierarchy |
| Content integrity for deployment | Not addressed pre-4b | Stage 4b | SHA-256 audit hashes + digital signatures |

---

## How to Run the Pipeline

### Prerequisites

- Python 3.9+
- `pip install docling pymupdf` (Stages 1 and 2 only)
- Stages 3–4b: **no external dependencies** (Python stdlib only)
- Source PDF: `B09514-eng.pdf` in the working directory

### Full Pipeline Execution

```bash
# Stage 1: Primary extraction (~23 min first run, ~29s cached)
python extraction_mvp_v2.py

# Stage 2: Cross-validation (~8.5s)
python stage2_cross_validation.py

# Stage 3: Automated plausibility checks (~0.2s)
python stage3_automated_checks.py

# Stage 4a: Chunking + metadata (~1.1s)
python stage4a_chunking.py

# Stage 4b: Generate physician review package (~0.4s)
python stage4b_review_package.py

# --- HUMAN STEP: Physician reviews physician_review_report.md ---
# --- Physician fills in review_package.json decisions ---

# Stage 4b (ingest): Apply physician review to chunks
python stage4b_review_package.py --ingest extraction_output/completed_review.json
```

### Total Automated Runtime

| Stage | Time | Cumulative |
|---|---|---|
| Stage 1 (first run) | ~23 min | 23 min |
| Stage 1 (cached) | ~29s | 29s |
| Stage 2 | ~8.5s | 38s |
| Stage 3 | ~0.2s | 38s |
| Stage 4a | ~1.1s | 39s |
| Stage 4b | ~0.4s | 40s |
| **Total (cached)** | | **~40 seconds** |

---

## Output Files Reference

All outputs are written to `extraction_output/`.

| File | Stage | Size | Description |
|---|---|---|---|
| `full_extraction.md` | 1 | 2.2 MB | Complete markdown extraction of all 478 PDF pages |
| `table_inventory.json` | 1 | 28 KB | 207 tables with classifications, page numbers, and column metadata |
| `tables_nll.txt` | 1+2 | 76 KB | Natural Language Logic for 43 tables (42 from Stage 1 + 1 stitched from Stage 2) |
| `cross_validation_report.json` | 2 | 28 KB | Reclassification decisions, cell-level comparison results, stitch records |
| `plausibility_report.json` | 3 | 13 KB | Per-table results for 6 automated checks (pass/fail/skipped per table) |
| `chunks.json` | 4a | 10.6 MB | 1,478 chunks with full metadata: safety, clinical metadata, verified_by, related_chunks |
| `review_package.json` | 4b | 1.8 MB | 356 review items with audit hashes, templates, and context for physician review |
| `physician_review_report.md` | 4b | 1.0 MB | Human-readable review report organized by tier with checklists and decision fields |

---

## Per-Chunk Schema (Stage 4a Output)

Every chunk in `chunks.json` carries 16+ metadata fields. The fields most relevant to downstream systems (Brain 1, guardrails) are:

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
| Docling extraction | Layout/structure parsing (93.8% accuracy) | 1 |
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

| Level | Count | LLM Behavior | Example |
|---|---|---|---|
| **verbatim** | 31 | Must return content exactly as extracted. No paraphrasing, no summarization. | "80 + 480 mg artemether-lumefantrine twice daily for 3 days" |
| **high** | 325 | Minimal paraphrasing. Core clinical facts must be preserved word-for-word. | "Lumefantrine exposure is decreased in pregnant women" |
| **standard** | 1,122 | Paraphrasing acceptable. General narrative and structural content. | Background on malaria epidemiology |

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
| `extraction_mvp_v2.py` | 1,104 | docling, pymupdf | Stage 1: PDF → markdown + table inventory + NLL |
| `stage2_cross_validation.py` | 1,056 | pymupdf | Stage 2: Independent extraction, reclassification, stitching |
| `stage3_automated_checks.py` | 899 | stdlib only | Stage 3: 6 plausibility checks on dosing tables |
| `stage4a_chunking.py` | 1,640 | stdlib only | Stage 4a: Markdown → 1,478 metadata-rich chunks |
| `stage4b_review_package.py` | 1,461 | stdlib only | Stage 4b: Review package generation + ingestion |
| **Total** | **6,160** | | **5 scripts, 2 external dependencies** |

---

## Key Metrics at a Glance

| Metric | Value |
|---|---|
| Source PDF pages | 478 |
| Total tables extracted | 207 |
| True dosing tables (after reclassification) | 29 + 1 stitched = 30 |
| Dosing tables passing all automated checks | 8 (7 individual + 1 stitched) |
| Total chunks | 1,478 |
| Chunks requiring mandatory physician review | 31 (2.1%) |
| Chunks requiring recommended review | 325 (22.0%) |
| Estimated mandatory review time | ~62 minutes |
| Extraction accuracy (ground truth) | 93.8% |
| Cell-level agreement (Stage 2) | 86.7%–100% |
| Drug name extraction coverage | 27/30 (90%) |
| Weight range extraction coverage | 14/30 (47%) |
| Total pipeline runtime (cached) | ~40 seconds |
| External dependencies | 2 (docling, pymupdf — Stages 1–2 only) |
| Total codebase | 6,160 lines across 5 scripts |

---

## Git History

| Commit | PR | Description |
|---|---|---|
| `e5d653c` | — | Stage 1: Primary extraction pipeline and strategy document |
| `0407a30` | PR #1 | Stage 2: Cross-validation with PyMuPDF |
| `6fe057c` | PR #2 | Stage 3: Automated plausibility checks |
| `dee03ae` | PR #3 | Stage 4a: Chunking and metadata strategy |
| `1b57e73` | PR #4 | Stage 4b: Clinical verification framework |

Repository: [github.com/rajbagchi/safeai-purdue-capstone](https://github.com/rajbagchi/safeai-purdue-capstone)
