# Benchmarking and Validation

This document covers the validation stages, dosing plausibility checks, clinical verification, and end-to-end benchmarking results for both target PDFs.

## Validation framework

**Module:** `pipeline/validator.py` (880 lines) | **Class:** `ExtractionValidator`

The validator runs six stages after extraction, each producing a confidence score (0.0 to 1.0) and a pass/fail determination. The overall confidence is the mean of all stage confidences.

### Stage 1: Structure validation

Checks heading hierarchy and page numbering. A single heading-level skip (e.g., H1 to H3, common in medical PDFs) costs 10% confidence. Passing threshold: 80%.

### Stage 2: Table quality

Verifies that extracted tables have at least 2 columns and that tables containing dosing keywords have sufficient numeric values. Confidence = fraction of valid tables.

### Stage 3: Cross-consistency

Compares Pass 1 (PyMuPDF) text with Pass 4 (pdfplumber) text using fuzzy string matching. Text is normalized before comparison (whitespace collapsed, soft hyphens removed, lowercased). Passing threshold: 90%.

### Stage 4: Medical content presence

Checks that critical medical terms from the config appear in the extracted text. Confidence = fraction of terms found. Passing threshold: 80%.

### Stage 5: Human review flagging

Identifies items requiring physician attention. Only flags dosing tables that failed Stage 6 checks (not every table mentioning "mg"). Includes contraindication pages and OCR-required pages. Capped at 50 items to keep the list actionable. Confidence is proportional to the number of flagged items.

### Stage 6: Dosing plausibility

The most critical stage. Runs six sub-checks on every dosing-classified table:

#### Check 1: Weight contiguity
No gaps >1 kg between consecutive weight bands. Only fires on tables with explicit weight-band structure (header contains "weight" and at least one row parses to a weight range).

#### Check 2: Dose monotonicity
Each dose component must be non-decreasing across ascending weight bands. Only fires on tables with weight-band structure.

#### Check 3: Weight coverage
Tables should cover from pediatric (<=10 kg) through adult (>=35 kg) ranges. Only fires on tables with weight-band structure.

#### Check 4: Clinical bounds
Per-kg doses are compared against reference ranges for known drugs (artemether 1-4 mg/kg, lumefantrine 6-16 mg/kg, etc.). A 2.5x tolerance factor accommodates clinical variation.

#### Check 5: Combination consistency
For fixed-ratio combination drugs (identified by "/" or "+" in column headers), the component ratio should be stable across all weight bands. Requires at least 3 multi-component rows and a combo-drug header hint.

#### Check 6: Positive/non-empty
All weight and dose cells should be non-empty and positive. Cells containing explicit "not applicable" markers (-, --, n/a, nil, etc.) are treated as intentional rather than missing.

### Agnostic design

All checks are document-agnostic. There are no hardcoded page numbers, drug lists, or table indices. The checks work on any clinical guideline PDF — the quality of results depends on the config's `drug_keywords` and `dosing_keywords` vocabulary.

## Clinical verification

**Module:** `pipeline/clinical_verifier.py` (1,227 lines) | **Class:** `ClinicalVerifier`

### Review package generation

The verifier generates a JSON review package and a Markdown physician review report containing:

- Every chunk classified into a 5-tier priority system (Tier 1 = validated dosing, Tier 5 = optional)
- Applicable clinical verification checks for each chunk
- SHA-256 audit hashes for integrity verification
- Pre-filled review items with decision fields (verified / needs-revision / rejected)

### Physician review workflow

1. Pipeline generates `review_package.json` and `physician_review_report.md`
2. Physician reviews each item and fills in decision + notes
3. Completed review is ingested via `ClinicalVerifier.ingest()`
4. System validates: audit hash integrity, reviewer identity, ISO timestamps, mandatory decisions
5. Verified status and digital signatures are applied to chunks
6. Deployment gate check determines production readiness

### Deployment gate

`passes_deployment_gate()` requires that all mandatory-tier chunks (Tiers 1-3) have `verified_by.status == "verified"` and a valid `audit_hash`. Any unverified mandatory chunk blocks deployment.

## Raw data

The benchmark data files are tracked in the repository under [`rag_output/`](../rag_output/):

- **[`retrieval_test_results.json`](../rag_output/retrieval_test_results.json)** — per-query results for all 30 clinical test queries (12 original + 18 expanded) with P@3, P@5, MRR, per-result relevance, source pages, content previews, and per-category breakdown
- **[`build_report.json`](../rag_output/build_report.json)** — corpus stats, timing, aggregate metrics, model configuration
- **[`brain1_package/`](../rag_output/brain1_package/)** — the deployable mobile package (24.11 MB)

See [`rag_output/README.md`](../rag_output/README.md) for the full directory guide.

## Benchmark results

### WHO Malaria Guidelines (478 pages, 203 tables)

| Stage | Score | Status |
|---|---|---|
| 1. Structure | 80% | PASS |
| 2. Tables | 100% | PASS |
| 3. Cross-consistency | 83% | FAIL (below 90% threshold) |
| 4. Medical content | 100% | PASS |
| 6. Dosing plausibility | 42% (8/19 tables) | FAIL |
| 5. Human review | 50 items flagged | — |
| **Overall confidence** | **~68%** | |

**Stage 3 analysis:** The 83% cross-consistency score reflects genuine text divergence on the malaria PDF's dense evidence tables (pages 314-476), where PyMuPDF and pdfplumber render complex multi-column layouts differently. The clinical content on these pages is still correctly extracted — the divergence is in formatting, not substance.

**Stage 6 analysis:** 11 of 19 dosing tables fail because the WHO malaria guidelines deliberately use non-contiguous weight bands for some drugs (e.g., separate tables for infants and adults) and include evidence comparison tables that are classified as "dosing" due to drug name mentions.

### Uganda Clinical Guidelines (1,161 pages, 950 tables)

| Stage | Score | Status |
|---|---|---|
| 1. Structure | 80% | PASS |
| 2. Tables | 100% | PASS |
| 3. Cross-consistency | 94% | PASS |
| 4. Medical content | 100% | PASS |
| 6. Dosing plausibility | 99% (479/484 tables) | PASS |
| 5. Human review | 43 items flagged | — |
| **Overall confidence** | **~79%** | |

The Uganda PDF performs significantly better because:
- Its table layouts are more uniform (consistent 2-3 column structures)
- Its 212 drug keywords provide richer classification vocabulary
- Its dosing tables use standard weight-band formats

**2026-04-10 — Cross-validation fix:** Uganda's cross-consistency (Stage 3) was originally reported as 0% in earlier re-runs because the Uganda Clinical Guidelines 2023 PDF is produced by Adobe InDesign using a non-standard internal page-tree structure that pdfminer/pdfplumber cannot traverse — pdfplumber returned 0 pages. The extractor now detects this automatically: if pdfplumber returns 0 pages, it re-saves the PDF through PyMuPDF (`garbage=4, deflate=True, clean=True`) to a temporary file that normalises the structure, then runs pdfplumber on the repaired copy. This restores Uganda's cross-consistency to the correct 94% and makes cross-validation work on any PDF regardless of how it was produced. The dosing plausibility update from 97% (495/509) to 99% (479/484) also reflects the corrected re-run results.

### Response layer validation

Both presets were tested with 25 queries each (50 total):

| Metric | WHO Malaria | Uganda |
|---|---|---|
| Queries tested | 25 | 25 |
| Guardrail pass rate | 100% | 100% |
| Triage level consistency | All GREEN | All GREEN |
| Response confidence | 0.79 (range: 0.64–0.95) | 0.89 (range: 0.68–1.00) |
| VHT response length | 1,439-1,578 chars | 1,422-1,597 chars |

All 50 queries passed guardrail validation with no warnings or errors.

**2026-04-09 — Confidence scoring fix:** Prior to this date, `_calculate_confidence()` used a fixed baseline of `0.95` (RED triage) or `0.90` (all other queries), adjusted only for guardrail warnings. This meant every query — regardless of retrieval quality — received the same score. The WHO Malaria `0.90` value in the original table was this hardcoded constant, not a measured signal.

The confidence values above reflect the real computed values after the fix. The formula combines three signals:

```
confidence = 0.6 × retrieval_score + 0.4 × coverage − penalty
```

- **Retrieval score (60%)** — mean of top-3 retrieved chunk scores (normalized to [0,1] by the hybrid retriever after RRF + cross-encoder blending)
- **Coverage (40%)** — fraction of the 5 requested chunks that were actually found
- **Guardrail penalty (subtracted)** — −0.05 per warning, −0.15 per error, −0.10 if guardrail failed

This makes the confidence score a genuine measure of how well the retrieved evidence supports the response.

**2026-04-09 — PDF-first response content:** Actions, monitoring instructions, and referral criteria are now extracted verbatim from retrieved PDF chunks using regex (bullet points, numbered lists, `danger_signs` and `referral_criteria` from chunk `clinical_metadata`), rather than returned from hardcoded keyword-matched templates. Hardcoded templates remain as fallback only when the PDF chunks contain no extractable items. This ensures every response reflects the actual uploaded document.

## Retrieval benchmark results

The retrieval pipeline uses alpha-blended cross-encoder scoring (`blended = alpha * norm(RRF) + (1-alpha) * norm(CE)` with `_CE_BLEND_ALPHA = 0.6`) followed by metadata-aware re-ranking.

### 12-query benchmark (original)

| Metric | Value |
|--------|-------|
| Mean P@3 | 0.750 |
| Mean MRR | 0.944 |
| Perfect P@3 (= 1.0) | 5 / 12 queries |

Notable per-query result: Q01 (artemether-lumefantrine dose) improved from 0.333 (baseline) to 0.667 with blended scoring.

**Benchmark label caveat:** The original 12-query labels were created from the archived retriever's output (all returned chunks marked relevant). The P@3 gap vs. the archived baseline (0.750 vs. 0.944) is partly due to incomplete label coverage -- the new retriever returns different but relevant chunks not present in the original label set.

### 30-query expanded benchmark

The benchmark was expanded from 12 to 30 queries to reduce overfitting risk and better represent real clinical use. The 18 new queries span 8 categories (diagnostic, prevention, treatment_protocol, population_specific, procedural, safety, evidence, operational) with **independently created relevance labels** — labels were generated by searching chunk content with regex patterns, NOT by running the retriever.

| Metric | Value |
|--------|-------|
| Mean P@3 | 0.489 |
| Mean MRR | 0.686 |
| Perfect P@3 | 5 / 30 queries |

**Per-category P@3 breakdown:**

| Category | Queries | Mean P@3 | Perfect | Notes |
|----------|---------|----------|---------|-------|
| original (dosing/treatment) | 12 | 0.750 | 5/12 | Strong — keyword-heavy queries |
| procedural | 2 | 0.667 | 0/2 | |
| population_specific | 2 | 0.500 | 0/2 | |
| treatment_protocol | 4 | 0.417 | 0/4 | |
| evidence | 2 | 0.333 | 0/2 | |
| prevention | 2 | 0.167 | 0/2 | Weak |
| safety | 2 | 0.167 | 0/2 | Weak |
| operational | 2 | 0.167 | 0/2 | Weak |
| diagnostic | 2 | 0.000 | 0/2 | Failed |

**Key insight:** The original 12-query benchmark was biased toward drug-dosing lookups where BM25 keyword matching excels. Broader clinical queries (diagnostic, prevention, safety, operational) score much lower — these would benefit most from medical-domain embeddings like PubMedBERT. See [retrieval_strategy.md § Model evaluation](retrieval_strategy.md#model-evaluation) for the full model comparison.

**Benchmark script:** `scripts/rerun_retrieval_benchmark.py` — run with `--original` for 12-query only, or no flag for the full 30-query expanded benchmark. The script always loads ground-truth labels from git commit `e32337e` for the original 12 queries (to avoid cascading label loss), and generates labels at runtime for the expanded queries.

### Cross-encoder blending decision

| Approach | P@3 | MRR | Outcome |
|----------|-----|-----|---------|
| Full-replace (CE scores only) | 0.694 | -- | CE overpowers medical keyword signals |
| Disabled (no CE) | 0.611 | -- | Loses semantic understanding entirely |
| **Blended alpha=0.6** | **0.750** | **0.944** | **Best of both worlds** |

Both models are general-purpose, NOT medical-domain-specific:
- **Embedding:** `sentence-transformers/all-MiniLM-L6-v2` -- trained on 1B+ general sentence pairs (Apache 2.0)
- **Cross-encoder:** `cross-encoder/ms-marco-MiniLM-L-6-v2` -- trained on MS MARCO web search data (Apache 2.0)

Neither model has medical-specific training, which is why blending (preserving BM25's medical keyword signals through RRF) outperforms full cross-encoder replacement.

## Metadata-aware re-ranking (v2)

After cross-encoder blending, a metadata-aware post-processing layer applies four multiplicative score boosts using clinical metadata already present on chunks:

1. **Drug-name match (x1.35)** -- extracted from query via config `drug_keywords`
2. **Chunk-type boost (x1.25 dosing / x0.85 evidence)** -- for dosing-intent queries
3. **Condition match (x1.20)** -- condition metadata matched against query signals
4. **Domain match (x1.10)** -- clinical_domain soft-matched against query keywords

These boosts stack multiplicatively. In the Q01 case, the correct AL dosing table (originally ranked 3rd with score 0.9) jumps to rank 1 (score ~1.52) while the irrelevant artesunate narrative drops due to lacking drug-name match on "artemether" / "lumefantrine".

See [retrieval_strategy.md](retrieval_strategy.md) for full implementation details and boost constants.

## Test suite

444 unit tests cover all pipeline modules:

| Test file | Tests | Coverage |
|---|---|---|
| `test_classify_table.py` | Table classification taxonomy | 244 lines |
| `test_clinical_metadata.py` | Metadata extraction | 366 lines |
| `test_clinical_verifier.py` | Review package, deployment gate | 609 lines |
| `test_config_presets.py` | Config factory functions | 324 lines |
| `test_colpali_retriever.py` | ColPali v1.2 index, MaxSim, mocked search | 280 lines |
| `test_dosing_plausibility.py` | All 6 dosing checks | 391 lines |
| `test_hybrid_retriever.py` | BM25 + dense + RRF + ColPali integration | 265 lines |
| `test_image_ocr_enrichment.py` | Image OCR in chunker | 267 lines |
| `test_image_ocr_extractor.py` | Image extraction + OCR | 407 lines |
| `test_nll_generation.py` | Natural language table descriptions | 230 lines |
| `test_parent_child_chunking.py` | Parent-child splitting | 420 lines |
| `test_preservation_level.py` | Preservation level inference | 264 lines |
| `test_related_chunk_linking.py` | Related chunk linking | 312 lines |
| `test_stitch_tables.py` | Page-boundary table stitching | 313 lines |

Run the full suite:

```bash
python -m pytest tests/ -q
# 444 passed in ~55s
```

See also:
- [Safety and guardrails](safety_and_guardrails.md) for how these validation results enforce safety decisions
- [`rag_output/README.md`](../rag_output/README.md) for cross-referencing benchmark results against the source PDFs
