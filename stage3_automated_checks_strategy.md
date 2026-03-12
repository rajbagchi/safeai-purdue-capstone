# Stage 3: Automated Plausibility Checks Strategy

**Safe AI Uganda — Clinical Data Extraction Methodology**
**Document:** Config-driven (reference: WHO Consolidated Malaria Guidelines, B09514-eng.pdf, 478 pages)
**Last updated:** 11.03.2026

---

## Executive Summary

Stage 3 validates the clinical plausibility of extracted dosing tables using six automated checks. It operates on the refined table set produced by Stages 1 and 2, and resolves the remaining known parsing failure (DHA-piperaquine weight bands on p.176). Stage 3 also reveals that only 7 of the 29 tables still classified as "dosing" after Stage 2 are actually weight-based dosing tables — the other 22 are GRADE evidence, abbreviation, and narrative tables that contain drug name keywords but no weight-based dosing structure.

| Metric | Value |
|---|---|
| **Dosing tables from Stage 2** | 29 |
| **Weight-based dosing tables (checked)** | 7 |
| **Non-weight-based (skipped, recommend reclassify)** | 22 |
| **Tables passing all 6 checks** | 7 of 7 (100%) |
| **Stitched table (pp.173–174)** | Passes all 6 checks |
| **Stage 1 parsing failures resolved** | 1 (DHA-piperaquine weight bands `60 < 80`, `>80`) |
| **Total time** | ~6 seconds |
| **Compute requirements** | CPU-only; Intel i5 (4-core), 16 GB RAM, no GPU required |

All 7 true weight-based dosing tables — covering the five first-line ACTs (artemether-lumefantrine, artesunate-amodiaquine, artesunate-mefloquine, artesunate-SP, DHA-piperaquine), primaquine, and a second-line treatment table — pass every plausibility check with zero issues. No false positives.

---

## 1. Plausibility Check Architecture

### 1.1 Data Pipeline

Stage 3 loads data from both previous stages before running checks:

1. **Table inventory** (`table_inventory.json`) — 207 tables with index, page, classification, dimensions
2. **Stage 2 reclassifications** (`cross_validation_report.json`) — 12 tables reclassified from "dosing" to "structural", reducing the set from 41 → 29
3. **Docling cache** (`cache/docling_*.json`) — full table markdown for cell-level parsing
4. **Stage 2 stitched table** (`cross_validation_report.json`) — the complete 4-row AL dosing table (pp.173–174) with the recovered `≥ 35 kg: 80 + 480` row

Additionally, Stage 3 loads disease-specific parameters from the pipeline config JSON via `pipeline_config.py`, including dose reference ranges for clinical bounds checking.

Only the 29 tables still classified as "dosing" after Stage 2 enter the validation pipeline. Of these, 7 have a parseable weight column (true dosing tables) and 22 do not (GRADE evidence tables and abbreviation lists that matched drug name keywords in Stage 1's classification).

### 1.2 Enhanced Weight-Band Parser

Stage 1's `_parse_weight_range()` failed on two formats found in the DHA-piperaquine table (p.176): `"60 < 80"` and `">80"`. Stage 3 rewrites the parser to handle all weight-band formats found across the WHO guidelines:

| Format | Example | Parsed as |
|---|---|---|
| `< N` | `< 15` | (0, 15) |
| `N to < M` | `15 to < 25` | (15, 25) |
| `N to M` | `50 to 100` | (50, 100) |
| `> N to ≤ M` | `> 10 to ≤ 20` | (10, 20) |
| `N < M` | `60 < 80` | (60, 80) |
| `≥ N` or `>= N` | `≥ 35` | (35, None) |
| `> N` or `>N` | `>80` | (80, None) |
| `N to < M a` | `5 to < 25 a` | (5, 25) — footnote marker stripped |

The parser also normalises Unicode characters (≥ → >=, ≤ → <=, en-dash → hyphen) before matching. This directly resolves the Stage 1 DHA-piperaquine parsing failure.

### 1.3 Enhanced Dose Parser

Stage 1 extracted only the first numeric value from a dose cell. Stage 3 extracts **all** numeric components, enabling combination drug validation:

| Cell value | Stage 1 parse | Stage 3 parse |
|---|---|---|
| `20 + 120` | `[20.0]` | `[20.0, 120.0]` |
| `250 / 12.5` | `[250.0]` | `[250.0, 12.5]` |
| `25 mg` | `[25.0]` | `[25.0]` |
| `3.75` | `[3.75]` | `[3.75]` |

---

## 2. The Six Plausibility Checks

### 2.1 Check 1: Weight-Band Contiguity

**Purpose:** Verify no gaps exist between consecutive weight bands in a dosing table.

**Method:** For each pair of adjacent weight bands, check that the upper bound of band N equals (±0.5 kg) the lower bound of band N+1. Open-ended bands (≥, >) are allowed only as the final row.

**Stage 1 result:** 40/41 pass, 1 fail (Table 17 DHA-piperaquine due to parser bug)
**Stage 3 result:** 7/7 pass — Table 17 now passes with the fixed parser

| Table | Page | Drug | Bands | Contiguity |
|---|---|---|---|---|
| 13 | 173 | Artemether-lumefantrine | 3 | Pass |
| 14 | 174 | Artesunate-amodiaquine | 4 | Pass |
| 15 | 175 | Artesunate-mefloquine | 4 | Pass |
| 16 | 175 | Artesunate-SP | 4 | Pass |
| **17** | **176** | **DHA-piperaquine** | **8** | **Pass (was fail in Stage 1)** |
| 18 | 178 | Primaquine | 2 | Pass |
| 22 | 203 | Second-line treatment | 2 | Pass |

### 2.2 Check 2: Dose Monotonicity (Combination-Aware)

**Purpose:** Verify that doses increase (or stay equal) as body weight increases, for every component of a combination drug.

**Method:** For each dose column, extract all numeric components. For a cell like `"20 + 120"`, check that both 20 (artemether) and 120 (lumefantrine) are individually non-decreasing across rows. This is an enhancement over Stage 1, which only checked the first component.

**Result:** 7/7 pass — all components of all combination drugs increase monotonically with weight.

### 2.3 Check 3: Weight-Band Coverage Completeness (New)

**Purpose:** Verify that each dosing table covers the full pediatric-through-adult weight spectrum expected by WHO guidelines.

**Method:** Parse the first and last weight bands of each table and check:
- **Pediatric coverage:** Table starts at ≤ 10 kg (covering infants/young children)
- **Adult coverage:** Table reaches ≥ 35 kg or has an open-ended final band (≥ or >)

**Result:** 7/7 pass

| Table | Page | Weight range | Pediatric start | Adult end |
|---|---|---|---|---|
| 13 | 173 | 0–35 kg | 0 kg (< 15) | 35 kg (25 to < 35) |
| 14 | 174 | 0–open | 0 kg (< 9) | ≥ 36 kg (open-ended) |
| 15 | 175 | 0–open | 0 kg (< 9) | ≥ 30 kg (open-ended) |
| 16 | 175 | 0–open | 0 kg (< 10) | ≥ 50 kg (open-ended) |
| 17 | 176 | 0–open | 0 kg (< 8) | > 80 kg (open-ended) |
| 18 | 178 | 5–50 kg | 5 kg | 50 kg (50 to 100) |
| 22 | 203 | 10–35 kg | 10 kg (> 10 to ≤ 20) | 35 kg (> 20 to ≤ 35) |

All first-line ACT tables begin at < 10 kg (covering infants from ~3 months), and all reach adult weights via open-ended final bands.

### 2.4 Check 4: Clinical Dose Bounds (New)

**Purpose:** Catch extraction errors that produce impossible dosing values (e.g., an OCR error turning "20 + 120" into "200 + 120").

**Method:** For each row, divide the dose by the midpoint of the weight band to compute a per-kg dose. Compare this against WHO reference ranges for each drug, with a 2.5x tolerance to avoid false positives:

| Drug | Reference range (mg/kg) | Flagging bounds (with 2.5x tolerance) |
|---|---|---|
| Artemether | 1–5 | 0.4–12.5 |
| Lumefantrine | 5–30 | 2.0–75.0 |
| Artesunate | 1.5–15 | 0.6–37.5 |
| Amodiaquine | 5–20 | 2.0–50.0 |
| Mefloquine | 3–15 | 1.2–37.5 |
| DHA | 1.5–10 | 0.6–25.0 |
| Piperaquine | 10–32 | 4.0–80.0 |
| Sulfadoxine | 15–35 | 6.0–87.5 |
| Pyrimethamine | 0.5–2 | 0.2–5.0 |
| Primaquine | 0.05–1 | 0.02–2.5 |

These reference ranges are loaded from the `dose_reference_ranges` field in the pipeline config JSON. For documents without predefined dose ranges (e.g., when the config field is empty), this check is gracefully skipped.

The wide tolerance ensures only gross errors are flagged — this check is a safety net for extraction failures, not a clinical accuracy audit.

**Result:** 7/7 pass — all per-kg dose values fall within expected bounds. No false positives.

### 2.5 Check 5: Combination Drug Consistency (New)

**Purpose:** Verify that the ratio between components of a fixed-dose combination is stable across weight bands.

**Method:** For combination drugs like "20 + 120" (artemether + lumefantrine, ratio 1:6), compute the ratio (component 2 ÷ component 1) for each row. Compare each ratio to the median. Flag any row where the ratio deviates more than 35% from the median.

**Rationale:** In a correctly extracted table, the component ratio should be approximately constant because fixed-dose combinations maintain consistent proportions. A large deviation suggests a parsing error (e.g., one component was extracted from the wrong column or a digit was misread).

**Result:** 7/7 pass — all combination drug ratios are stable across weight bands.

### 2.6 Check 6: Positive Values and Empty Cells

**Purpose:** Verify all dose values are positive and no dosing table has empty cells in weight or dose columns.

**Method:** For each row, check that the weight cell is non-empty and all dose cells contain at least one positive numeric value. Any zero, negative, or missing values are flagged.

**Result:** 7/7 pass — all cells populated with positive values.

---

## 3. Scoring Summary

### 3.1 Check-Level Results

| Check | Pass | Fail | What it catches |
|---|---|---|---|
| **Weight Contiguity** | 7 | 0 | Gaps between weight bands (parsing errors) |
| **Dose Monotonicity** | 7 | 0 | Non-increasing doses (extraction errors) |
| **Weight Coverage** | 7 | 0 | Missing pediatric or adult bands |
| **Clinical Bounds** | 7 | 0 | Impossible dose values (OCR errors) |
| **Combination Consistency** | 7 | 0 | Misaligned drug components |
| **Positive / No Empty** | 7 | 0 | Missing or zero values |
| **Total** | **42** | **0** | **42 checks across 7 tables, 0 failures** |

### 3.2 Stage 1 Issue Resolution

| Issue | Stage 1 status | Stage 3 status |
|---|---|---|
| DHA-piperaquine weight bands (`60 < 80`, `>80`) | Fail (parser bug) | **Resolved** (enhanced parser) |
| DHA-piperaquine weight gap (band 6→7) | Reported as issue | **Resolved** (bands now parse correctly) |

### 3.3 Classification Cascade

Stage 3 further refines the table classification established in Stages 1 and 2:

| Stage | "Dosing" tables | Method |
|---|---|---|
| **Stage 1** | 41 | Keyword scoring (drug names, dose terms) |
| **Stage 2** | 29 | Reclassified 12 with no weight/dose patterns |
| **Stage 3** | **7** | Identified 22 more with no weight column (GRADE evidence, abbreviations) |

The 22 tables skipped by Stage 3 are recommended for reclassification as "evidence" or "other." They include:
- **Table 3 (p.27):** Abbreviation list
- **Tables 23–24 (pp.204–206):** Evidence-to-decision framework (values, preferences, equity)
- **Tables 141–190 (pp.415–460):** GRADE evidence summaries (outcome timeframes, relative risk, certainty)
- **Table 204 (p.473):** GRADE evidence summary

---

## 4. Time Breakdown

*As of 04.03.2026 — plausibility checks on Intel i5-8257U, 16 GB RAM, macOS.*

| Stage | Time | % of Total | Description |
|---|---|---|---|
| **Data loading** | **5.7s** | **97.2%** | Load Docling cache (16.5 MB) + inventory + reclassifications |
| Validate 7 tables | 0.003s | 0.1% | Run 6 checks on each of 7 tables |
| Validate stitched table | 0.000s | 0.0% | Run 6 checks on stitched AL table |
| **Total** | **5.7s** | **100%** | **~6 seconds** |

Data loading dominates because the Docling cache (16.5 MB serialised document model) must be deserialised to access table markdown. The actual plausibility computations are negligible (3 milliseconds for all 7 tables, all 6 checks).

---

## 5. Output Artefacts

### 5.1 `plausibility_report.json`

**What it is:** A single JSON file containing the complete Stage 3 plausibility results.

**What it contains:**
- Overall counts (29 from Stage 2, 7 checked, 22 skipped, 7 passed all)
- Skipped table list (22 tables with index, page, and reason)
- Per-check aggregate statistics (pass/fail counts with detail lists)
- Per-table results (each of the 7 checked tables with all 6 check results, parsed weight bands, row counts)
- Stitched table validation result (same 6 checks applied to the pp.173–174 merged table)
- Timing breakdown

**Why it is necessary:** This report provides the auditable evidence that all weight-based dosing tables in the document have been validated for clinical plausibility. It also documents which tables were skipped and why, supporting the classification refinement recommendations for downstream stages.

---

## Changelog

### v2.0 — PDF-Agnostic Config-Driven Architecture (tag: v2.0-pdf-agnostic)

**Before:** Dose reference ranges were hardcoded in a Python dictionary (artemether 1.0–5.0 mg/kg, lumefantrine 6.0–18.0 mg/kg, etc.). Only malaria-specific drugs were covered.

**After:** Dose reference ranges loaded from the `dose_reference_ranges` field in the pipeline config JSON. When the field is empty (e.g., for a general clinical guidelines document), the clinical bounds check is gracefully skipped rather than failing. All stages accept `--config` for document-specific configuration.

---

## 6. What Stage 3 Does Not Cover

The following are explicitly deferred to subsequent stages or future work:

| Gap | Resolution |
|---|---|
| Clinical correctness of actual dosing values (e.g., is 80 + 480 mg the right dose for ≥ 35 kg?) | Stage 4: IDI physician review |
| Reclassification of the 22 skipped tables | Future: update Stage 2 classification rules or add a Stage 3 reclassification pass |
| Validation of non-dosing tables (evidence, structural, clinical management) | Out of scope for plausibility checks (no clinical dose values to validate) |
| Content chunking for RAG/LLM pipeline | **Implemented** — Stage 4a chunking + metadata strategy |
| Cross-referencing dosing tables against narrative text (e.g., verifying that body text matches table values) | Future: text-table concordance check |
