# Stage 4a: Chunking + Metadata Strategy

**Safe AI Uganda — Clinical Data Extraction Methodology**
**Document:** WHO Consolidated Malaria Guidelines (B09514-eng.pdf, 478 pages)
**Last updated:** 04.03.2026

---

## Executive Summary

Stage 4a transforms the 2.2 MB full extraction markdown into discrete, metadata-rich chunks that serve as atomic units for RAG retrieval and physician review (Stage 4b). Each chunk carries structured clinical metadata, a safety preservation level (to prevent LLM paraphrasing of dosages), and a verified-by placeholder for clinical sign-off.

**Key insight: Physicians only need to review ~31 chunks (2.1% of total), not all 1,478.** The preservation level triage focuses physician effort on the safety-critical dosing and clinical management content while allowing the remaining 97.9% to proceed without manual review.

| Metric | Value |
|---|---|
| **Total chunks produced** | 1,478 |
| **Narrative chunks** | 1,235 |
| **Table chunks** | 207 (all inventory tables matched) |
| **Image chunks** | 35 |
| **Stitched table chunk** | 1 (pp.173–174 AL dosing, from Stage 2) |
| **Dosing table chunks** | 30 (including stitched) |
| **Physician mandatory review (verbatim)** | **31 chunks (2.1%)** — dosing tables, clinical tables |
| **Physician recommended review (high)** | **325 chunks (22.0%)** — evidence tables, dosing narratives |
| **No physician review needed (standard)** | **1,122 chunks (75.9%)** — general narrative, structural |
| **Dosing tables with drug_name populated** | 27 / 30 (90%) |
| **Dosing tables with weight range populated** | 14 / 30 (47%) |
| **All chunks verified_by status** | "unverified" (ready for Stage 4b) |
| **Total time** | ~1.1 seconds |
| **Compute requirements** | CPU-only; no dependencies beyond Python stdlib |

---

## 1. Chunking Architecture

### 1.1 Data Pipeline

Stage 4a loads outputs from all three previous stages:

1. **Full extraction markdown** (`full_extraction.md`) — 2.2 MB, 15,248 lines, 1,547 sections
2. **Table inventory** (`table_inventory.json`) — 207 tables with index, page, classification
3. **Cross-validation report** (`cross_validation_report.json`) — 12 reclassifications, 1 stitched table, NLL regeneration
4. **Plausibility report** (`plausibility_report.json`) — Stage 3 validation results for 29 dosing tables
5. **NLL text** (`tables_nll.txt`) — Natural Language Logic representations for 43 tables

### 1.2 Markdown Parsing

The markdown is split into sections on `## ` headings (1,547 sections). Each section's content is further decomposed into three element types:

- **Narrative** — continuous text between headings, tables, and images
- **Table** — lines starting with `|` (markdown table format)
- **Image** — `<!-- image -->` placeholders

Page footers (`N of 478`) and repeated WHO header lines are stripped during parsing.

### 1.3 Section Hierarchy

WHO guidelines use section numbering (e.g., `5.2.1.1.2 Dosing of ACTs`) embedded in the heading text. The parser maintains a depth stack based on dot-delimited numbering to reconstruct the full hierarchy path. Unnumbered headings (e.g., "Remark:", "Strong recommendation for") inherit their parent's hierarchy.

### 1.4 Table Matching

Each of the 207 inline markdown tables is matched back to its `table_inventory.json` entry using:

1. **Page resolution** — each table element's global line number is mapped to a PDF page via the page footer markers
2. **Page-based matching** — inventory entries on the same page are consumed in positional order
3. **Adjacent page fallback** — if no exact match, tries ± 1 page (handles page-boundary cases)

Result: 207/207 tables matched (100%).

### 1.5 Narrative Chunk Splitting

Oversized narrative chunks (> 1,500 estimated tokens) are split on paragraph boundaries (`\n\n`). Tiny trailing fragments (< 200 tokens) are merged back into the preceding sub-chunk. Target range: 200–1,500 tokens per narrative chunk.

---

## 2. Per-Chunk Schema

Every chunk includes the following fields:

| Field | Type | Description |
|---|---|---|
| `chunk_id` | string | Unique identifier (e.g., `narrative-0042`, `dosing_table-0013`, `stitched_table-S1`) |
| `chunk_type` | enum | `narrative`, `dosing_table`, `evidence_table`, `structural_table`, `clinical_table`, `other_table`, `image` |
| `source_pages` | int[] | PDF page number(s) |
| `section_hierarchy` | string[] | Full heading path from document root |
| `section_number` | string | Section number (e.g., `5.2.1.1.2`) |
| `section_title` | string | Section heading text |
| `content` | string | Chunk text/markdown |
| `content_type` | enum | `markdown`, `markdown_table`, `image_placeholder` |
| `nll` | string\|null | NLL representation (dosing tables only) |
| `table_index` | int\|null | Inventory table index |
| `table_classification` | object\|null | Stage 1 + Stage 2 classification cascade |
| `validation` | object\|null | Stage 3 plausibility check results |
| `clinical_domain` | string\|null | Most specific clinical topic from section hierarchy |
| `safety` | object | Preservation level + reasoning |
| `verified_by` | object | Physician review placeholder |
| `clinical_metadata` | object | Structured clinical fields |
| `related_chunks` | object | Links to sibling, narrative, and section chunks |
| `word_count` | int | Word count |
| `token_estimate` | int | Estimated token count (words × 1.3) |

---

## 3. Safety Metadata — Preservation Levels

Each chunk is assigned a preservation level that controls how a downstream RAG/LLM system may handle the content:

| Level | Applies to | Count | Meaning for RAG/LLM |
|---|---|---|---|
| **verbatim** | Dosing tables, clinical management tables | 31 | **No paraphrasing allowed.** Dosage values, weight bands, drug names are safety-critical. Content must be returned exactly as extracted. |
| **high** | Evidence tables, narratives containing dosing/contraindication keywords | 325 | **Minimal paraphrasing.** Key clinical facts must be preserved. Numbers, drug names, and clinical thresholds must be exact. |
| **standard** | General narrative, structural/other tables, images | 1,122 | Standard RAG behavior — summarization and paraphrasing acceptable. |

### Assignment Logic

1. Dosing tables (final classification = "dosing") → **verbatim**
2. Clinical management tables → **verbatim**
3. Evidence tables → **high**
4. Narrative chunks containing keywords (`mg/kg`, `contraindicated`, `do not give`, `recommended dose`, `severe malaria`, etc.) → **high**
5. All other chunks → **standard**

---

## 4. Verified-By — Physician Review Framework

### 4.1 Review Triage: Physicians Do NOT Review All 1,478 Chunks

The preservation level creates a priority-based triage that dramatically reduces physician workload:

| Priority | Preservation | Chunks | % of Total | What it contains | Physician action |
|---|---|---|---|---|---|
| **1 — Critical** | `verbatim` | **31** | **2.1%** | Dosing tables, clinical management tables — drug dosages that patients receive | **Must verify** — a wrong number could cause patient harm |
| **2 — Important** | `high` | **325** | **22.0%** | Evidence tables + narratives with dosing keywords, contraindications, danger signs | **Should review** — contains clinical thresholds and safety information |
| **3 — Low** | `standard` | **1,122** | **75.9%** | General narrative, structural tables, abbreviations, images | **Can skip** — no safety-critical content |

**In practice, the IDI physician reviews ~31 chunks as mandatory (the verbatim dosing/clinical tables), then triages among the 325 high-priority chunks based on clinical relevance. The remaining 1,122 standard chunks do not require physician review.**

The Stage 4b review workflow should:
1. **Filter by `safety.preservation_level == "verbatim"`** — present these 31 chunks first
2. **Then filter by `safety.preservation_level == "high"`** — present these for secondary review
3. **Skip `standard`** chunks unless the physician explicitly requests to see them

### 4.2 Verified-By Schema

Every chunk carries a `verified_by` block initialized as a null placeholder:

```json
{
  "status": "unverified",
  "reviewer_name": null,
  "reviewer_role": null,
  "institution": null,
  "digital_signature": null,
  "verified_at": null,
  "comments": null
}
```

### 4.3 Review Workflow (Stage 4b)

In Stage 4b, the IDI physician will:
1. Review the 31 verbatim chunks (dosing tables, clinical management tables)
2. Review high-priority narrative chunks containing contraindications and dosing recommendations
3. Update `status` to `"verified"` or `"flagged"` for each reviewed chunk
4. Fill in `reviewer_name`, `reviewer_role`, `institution`, and `digital_signature`
5. Add `comments` for any clinical corrections or flags

This creates a traceable audit trail: **extraction → automated validation → physician sign-off**, where the physician's effort is focused on the 2% of chunks that are safety-critical rather than the entire document.

---

## 5. Clinical Metadata Extraction

### 5.1 Dosing Table Chunks

For dosing tables, the following fields are extracted automatically:

| Field | Source | Coverage |
|---|---|---|
| `drug_name` | Table header text (e.g., "artemether + lumefantrine" from "Dose (mg) of artemether + lumefantrine...") | 27/30 (90%) |
| `patient_weight_min_kg` | First weight band lower bound, parsed with Stage 3's 8-format weight parser | 14/30 (47%) |
| `patient_weight_max_kg` | Last weight band upper bound (null if open-ended ≥ N) | 14/30 |
| `condition` | Inferred from section hierarchy (e.g., "5.2.1 Treating uncomplicated malaria" → "Uncomplicated malaria") | 30/30 |
| `frequency` | Extracted from header text (e.g., "twice daily") | Where present |
| `duration` | Extracted from header text (e.g., "3 days") | Where present |
| `route` | Default "oral" for ACTs | All dosing |
| `dosage_summary` | Composed from frequency + duration | Where present |

### 5.2 Narrative Chunks

For narrative chunks, the following are scanned via regex:

| Field | Source |
|---|---|
| `condition` | Inferred from section hierarchy |
| `patient_age_min/max` | Age patterns (e.g., "children under 5 years", "infants < 6 months") |
| `patient_weight_min/max` | Weight mentions (e.g., "weighing < 25 kg") |
| `contraindications` | Keyword scanning ("contraindicated in", "do not give to", "not recommended in") |
| `special_populations` | Pattern scanning (pregnant women, children < N kg, G6PD deficiency, HIV patients) |

---

## 6. Related-Chunk Linking

Three passes establish bidirectional relationships:

| Pass | Links created | Purpose |
|---|---|---|
| Sequential | `prev_sibling`, `next_sibling` | Document order traversal |
| Table ↔ Narrative | `preceding_narrative`, `following_narrative`, `context_for_tables` | Links each table to the narrative that introduces it and follows it |
| Section grouping | `section_siblings` | Groups all chunks within the same section hierarchy |

These links enable a RAG system to retrieve not just the matching chunk, but its surrounding clinical context.

---

## 7. Chunk Type Distribution

| Chunk Type | Count | Description |
|---|---|---|
| `narrative` | 1,235 | Clinical guidance text, recommendations, remarks |
| `dosing_table` | 30 | Weight-based dosing tables (incl. stitched) |
| `evidence_table` | 21 | GRADE evidence summary tables |
| `other_table` | 142 | Miscellaneous tables (abbreviations, criteria, etc.) |
| `image` | 35 | Image placeholders (flowcharts, diagrams) |
| `structural_table` | 14 | Table of contents, document structure |
| `clinical_table` | 1 | Clinical management reference |

---

## 8. Time Breakdown

| Phase | Time |
|---|---|
| Load stage data | 0.01s |
| Build enrichment lookups | <0.01s |
| Parse markdown | 0.04s |
| Create chunks | 0.15s |
| Enrich safety + clinical metadata | 0.83s |
| Link related chunks | 0.02s |
| Validate | 0.06s |
| **Total** | **~1.1s** |

---

## 9. Output Artefacts

| File | Size | Contents |
|---|---|---|
| `extraction_output/chunks.json` | ~10.6 MB | 1,478 chunks with full metadata envelope |

The JSON envelope includes:
- `pipeline_version`: "4a"
- `source_document`: WHO guidelines identifier
- `chunk_type_counts`: per-type tallies
- `stages_loaded`: confirmation that all 3 upstream stages contributed
- `validation_summary`: matching stats, preservation level distribution, clinical metadata coverage
- `timings`: per-phase execution times

---

## 10. What's Not Covered (Deferred to Stage 4b or Later)

| Gap | Reason / Mitigation |
|---|---|
| **Physician verification** | `verified_by` block is a placeholder; Stage 4b will implement the review workflow |
| **Embedding generation** | chunks.json is ready for embedding but vectors are not computed in Stage 4a |
| **Cross-chunk deduplication** | Some tables appear in both the "Summary of recommendations" (ToC area) and the main content; not deduplicated |
| **Image OCR in chunks** | Image chunks are placeholders; Stage 2 verified one image via OCR but full image chunking is deferred |
| **PDF-agnostic adaptation** | The script uses configurable constants (page footer regex, structural heading patterns) that can be adjusted per WHO PDF; formal generalization across WHO guideline PDFs is deferred to a future update of all strategy documents |
| **Drug name coverage gap** | 3/30 dosing tables lack `drug_name` due to non-standard header formats; can be resolved with physician annotation in Stage 4b |
