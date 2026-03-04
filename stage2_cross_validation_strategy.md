# Stage 2: Cross-Validation Strategy

**Safe AI Uganda — Clinical Data Extraction Methodology**
**Document:** WHO Consolidated Malaria Guidelines (B09514-eng.pdf, 478 pages)
**Last updated:** 04.03.2026

---

## Executive Summary

Stage 2 is the cross-validation pass that independently re-extracts clinically critical content using PyMuPDF and compares it against the Stage 1 Docling output. Its primary purpose is to catch extraction failures — particularly content lost at page boundaries — and to refine the table classification from Stage 1.

| Metric | Value |
|---|---|
| **Combined accuracy (text + tables + images)** | 100% (16 of 16 ground-truth checks pass) |
| **Stage 1 accuracy before cross-validation** | 93.8% (15 of 16) |
| **Stage 1 failures resolved** | 1 (80 + 480 mg AL dosing row recovered via page-boundary stitching) |
| **Cross-validation engine** | PyMuPDF (fitz) — zero new dependencies |
| **Average cell-level agreement (Docling vs PyMuPDF)** | 92.7% across 6 dosing table pairs |
| **Tables reclassified** | 12 (misclassified "dosing" tables corrected to "structural") |
| **Total cross-validation time** | 33 seconds |
| **Compute requirements** | CPU-only; Intel i5 (4-core), 16 GB RAM, no GPU required |

The Stage 1 failure — a dosing table row (`80 + 480 mg` artemether-lumefantrine for body weight ≥ 35 kg) spanning the page boundary between pp.173–174 — is fully resolved by Stage 2's page-boundary table stitching. Additionally, 12 tables in the GRADE annexes (pp.417–473) that Stage 1 misclassified as "dosing" are correctly reclassified as "structural."

---

## 1. Cross-Validation Architecture

Stage 2 uses **PyMuPDF** (fitz) as its sole extraction engine. This was chosen over PaddleOCR and Pixtral based on a trade-off analysis:

| Approach | New dependencies | Install risk (macOS) | Page-boundary fix? | Speed |
|---|---|---|---|---|
| **PyMuPDF (chosen)** | None (already installed) | None | Yes (via stitching) | Milliseconds |
| PaddleOCR | ~1.5 GB (paddlepaddle + paddleocr) | High (known macOS hangs/segfaults) | No (per-image) | Seconds–minutes |
| Pixtral-12B (local) | ~25 GB model | Infeasible (requires GPU) | N/A | N/A |
| Claude API Vision | None (API call) | None | Yes (sees full page) | Seconds (future Tier 2) |

PyMuPDF provides two fully independent extraction methods that differ fundamentally from Docling's deep-learning approach:

1. **`page.get_text()`** — Extracts raw text directly from the PDF's text stream, with no layout analysis or ML model. This is the most basic and reliable way to confirm that content physically exists on a given page.
2. **`page.find_tables()`** — Uses a rule-based algorithm to detect table structures from the PDF's internal geometry (lines, cells, coordinates). This is completely independent of Docling's TableFormer neural network.

### 1.1 Why Two Independent Engines Matter

Docling (Stage 1) uses the TableFormer deep-learning model to infer table structure. PyMuPDF (Stage 2) uses rule-based geometric analysis. Because these approaches have different failure modes, discrepancies between them reliably flag extraction errors:

- **Docling's failure mode**: Page-boundary truncation — TableFormer analyses each page independently and cannot link table fragments across page breaks.
- **PyMuPDF's failure mode**: Complex merged cells — rule-based detection struggles with irregular table layouts that neural models handle well.

When both engines agree on a value, confidence is high. When they disagree, the discrepancy is flagged for review.

---

## 2. Cross-Validation Layers

Stage 2 runs seven sequential validation layers, each building on the previous.

### 2.1 Raw Text Verification (Layer A)

For every ground-truth check (the same 16 entries used in Stage 1), the raw text is extracted from the corresponding PDF page using `page.get_text()` and each keyword is verified.

| Content type | Checks | Pass | Fail | Accuracy |
|---|---|---|---|---|
| **Text** | 8 | 8 | 0 | 100% |
| **Table** | 7 | 7 | 0 | 100% |
| **Image** | 1 | 1 | 0 | 100% |
| **Total** | **16** | **16** | **0** | **100%** |

The critical result: the keyword `80 + 480` **passes** on p.174. This confirms the content exists in the PDF's text layer — Docling's table parser simply failed to associate it with the table structure on p.173. Raw text verification caught what layout-aware extraction missed.

### 2.2 Independent Table Extraction (Layer B)

PyMuPDF's `find_tables()` is run on all clinically critical pages (pp.173–178 dosing tables + p.212 severe malaria).

| Page | Tables found | Dimensions | Notes |
|---|---|---|---|
| 173 | 1 | 3r × 2c | AL dosing table (truncated — missing ≥ 35 kg row) |
| 174 | 2 | 0r × 2c, 4r × 2c | Continuation fragment + artesunate-amodiaquine table |
| 175 | 2 | 4r × 2c, 4r × 3c | Artesunate-mefloquine + artesunate-SP tables |
| 176 | 1 | 8r × 2c | DHA-piperaquine table (all 8 weight bands) |
| 177 | 0 | — | No tables (narrative text on QT interval warnings) |
| 178 | 1 | 3r × 2c | Primaquine single-dose table |
| 212 | 1 | 9r × 2c | Severe malaria complications management |
| **Total** | **8** | | **Across 7 pages** |

The 0-row table on p.174 is the page-boundary continuation fragment — PyMuPDF detected it but stored the data (`≥ 35 | 80 + 480`) as column headers rather than as a data row. This edge case is handled by the stitching layer.

### 2.3 Page-Boundary Table Stitching (Layer C)

This is the core innovation of Stage 2. The algorithm:

1. **Detect bottom-truncated tables**: For each page, check if any table's bounding box extends past 90% of the page height.
2. **Find continuation fragments**: On the next page, check if any table starts within the top 10% of the page height.
3. **Validate column compatibility**: The two fragments must have the same column count.
4. **Handle edge cases**: If the continuation has 0 data rows (data stored as headers), convert headers to a data row.
5. **Merge**: Append the continuation's data rows to the original table, discarding duplicate headers if present.

**Result for the AL dosing table (pp.173–174):**

| Body weight (kg) | Dose (mg) of artemether + lumefantrine given twice daily for 3 days |
|---|---|
| < 15 | 20 + 120 |
| 15 to < 25 | 40 + 240 |
| 25 to < 35 | 60 + 360 |
| **≥ 35** | **80 + 480** |

The stitched table has all 4 weight bands. The recovered row (`≥ 35 kg: 80 + 480 mg`) directly resolves the Stage 1 failure.

### 2.4 Cell-Level Comparison (Layer D)

For each dosing table that appears in both Docling and PyMuPDF output, cells are compared after normalisation (whitespace, Unicode special characters, line breaks).

| Page | Docling table | Total cells | Matching | Agreement |
|---|---|---|---|---|
| 173 | Table 13 (AL) | 8 | 7 | 87.5% |
| 174 | Table 14 (AS+AQ) | 10 | 10 | 100% |
| 175 | Table 15 (AS+MQ) | 10 | 10 | 100% |
| 175 | Table 16 (AS+SP) | 15 | 13 | 86.7% |
| 176 | Table 17 (DHA+PQP) | 18 | 17 | 94.4% |
| 178 | Table 18 (PQ) | 8 | 7 | 87.5% |
| **Average** | | **69** | **64** | **92.7%** |

All discrepancies are **formatting-only**, not data errors:
- **Line breaks in headers**: PyMuPDF preserves `<br>` tags from multi-line header text; Docling normalises them to spaces. Example: `"given twice daily for\n3 days"` vs `"given twice daily for 3 days"`.
- **Footnote marker spacing**: `"5 to < 25 a"` (Docling) vs `"5 to < 25a"` (PyMuPDF).

No actual dosing values differ between the two engines.

### 2.5 Classification Refinement (Layer E)

Stage 1 classified 41 tables as "dosing" using keyword scoring. Stage 2 applies a secondary check: does the table actually contain numeric weight-band patterns and dose values?

Tables are verified at two levels:
1. **Header-level**: Does the first row contain keywords like "Body weight", "Dose (mg)", "mg base", "daily for N days"?
2. **Cell-level**: Do the data cells contain numeric ranges (e.g., "5 to < 15") and dose values (e.g., "20 + 120", "250 mg")?

| Result | Count | Description |
|---|---|---|
| **Confirmed dosing** | 29 | Verified weight bands + dose values or dosing headers |
| **Reclassified → structural** | 12 | No weight/dose patterns (GRADE annex tables, abbreviation lists) |
| **Total reviewed** | 41 | All tables classified as "dosing" by Stage 1 |

Key reclassifications:
- **Table 5 (p.29)**: Abbreviation list — reclassified from "dosing" to "structural" (matched drug name keywords but contains no numeric data).
- **Tables 143–150 (pp.417–423)**: GRADE evidence-to-decision framework tables in the annexes — contain drug names in narrative text but no weight bands or dosing values.
- **Table 19 (p.185)**: Treatment failure criteria — reclassified to "structural."

After reclassification, the true dosing table count is **29** (down from 41).

### 2.6 Accuracy Re-Check (Layer F)

The same 16 ground-truth checks are re-run using the combined PyMuPDF table output (including stitched tables) as the search space.

| Metric | Stage 1 (Docling only) | Stage 2 (with stitching) | Change |
|---|---|---|---|
| **Text checks** | 8/8 (100%) | 8/8 (100%) | — |
| **Table checks** | 6/7 (85.7%) | 7/7 (100%) | +1 resolved |
| **Image checks** | 1/1 (100%) | 1/1 (100%) | — |
| **Combined accuracy** | **15/16 (93.8%)** | **16/16 (100%)** | **+6.2%** |

### 2.7 NLL Regeneration (Layer G)

For the stitched AL dosing table, a new NLL linearisation is generated with the recovered row:

```
IF Body weight (kg) is < 15, THEN Dose (mg) of artemether + lumefantrine given twice daily for 3 days is 20 + 120.
IF Body weight (kg) is 15 to < 25, THEN Dose (mg) of artemether + lumefantrine given twice daily for 3 days is 40 + 240.
IF Body weight (kg) is 25 to < 35, THEN Dose (mg) of artemether + lumefantrine given twice daily for 3 days is 60 + 360.
IF Body weight (kg) is ≥ 35, THEN Dose (mg) of artemether + lumefantrine given twice daily for 3 days is 80 + 480.
```

This is appended to `tables_nll.txt`, ensuring the downstream RAG pipeline receives the complete 4-row dosing table.

---

## 3. Scoring and Discrepancy Summary

Stage 2 identified **17 total discrepancies** between Stage 1 and the independent PyMuPDF extraction:

| Discrepancy type | Count | Severity | Details |
|---|---|---|---|
| **Page-boundary resolution** | 1 | Critical (resolved) | AL dosing table ≥ 35 kg row recovered |
| **Cell formatting mismatches** | 4 | Low (cosmetic) | Line breaks in headers, footnote spacing |
| **Table reclassifications** | 12 | Medium (corrective) | Non-dosing tables correctly relabelled |
| **Total** | **17** | | |

None of the discrepancies represent data-level errors in actual dosing values. The single critical discrepancy (the page-boundary failure) is fully resolved.

---

## 4. Time Breakdown by Stage

*As of 04.03.2026 — cross-validation of 7 pages on Intel i5-8257U, 16 GB RAM, macOS.*

| Stage | Time | % of Total | Description |
|---|---|---|---|
| Raw text verification | 0.2s | 0.7% | PyMuPDF `get_text()` on 16 ground-truth pages |
| PyMuPDF table extraction | 6.9s | 20.8% | `find_tables()` on 7 clinical pages |
| Page-boundary stitching | 0.01s | 0.0% | Detect + merge 1 page-boundary table |
| **Cell comparison** | **26.0s** | **78.4%** | Load Docling cache + compare 6 table pairs |
| Classification refinement | 0.02s | 0.1% | Re-check 41 dosing tables |
| Accuracy re-check | 0.0s | 0.0% | Re-run 16 ground-truth checks |
| NLL regeneration | 0.0s | 0.0% | Generate NLL for 1 stitched table |
| **Total** | **33.2s** | **100%** | **~33 seconds** |

Cell comparison dominates at 78.4%, primarily due to loading the 16.5 MB Docling cache file. The actual PyMuPDF extraction and stitching operations complete in under 7 seconds.

---

## 5. Output Artefacts

All outputs are written to the `extraction_output/` directory alongside Stage 1 outputs.

### 5.1 `cross_validation_report.json`

**What it is:** A single JSON file containing the complete Stage 2 cross-validation results.

**What it contains:**
- Raw text verification results (per-check pass/fail for all 16 ground-truth items)
- PyMuPDF table extractions (per-page markdown, row/column counts, bounding boxes, cell data)
- Page-boundary stitch results (merged table markdown, row counts from each fragment)
- Cell-level comparison results (per-table agreement percentages, specific cell differences)
- Classification refinements (list of reclassified tables with old/new classification and reason)
- Accuracy re-check results (combined Stage 1 + Stage 2 accuracy)
- NLL regeneration output (linearised stitched tables)
- Discrepancy summary (all flagged differences between Docling and PyMuPDF)
- Timing breakdown per stage

**Why it is necessary:** This is the primary audit trail for the cross-validation pass. It provides traceable evidence that the Stage 1 failure was detected and resolved, that dosing tables were independently verified, and that classification errors were corrected. The per-cell comparison data supports the claim that no actual dosing values differ between the two extraction engines.

### 5.2 `tables_nll.txt` (updated — appended)

**What changed:** A new section is appended to the existing NLL file with the stitched page-boundary table:

```
# ── Stage 2: Stitched page-boundary tables ──────────────
### Stitched Table (pp.173–174, dosing) ###
IF Body weight (kg) is < 15, THEN Dose is 20 + 120.
...
IF Body weight (kg) is ≥ 35, THEN Dose is 80 + 480.
```

**Why it is necessary:** The Stage 1 NLL for this table only had 3 rows (missing the ≥ 35 kg band). The appended stitched NLL provides the complete 4-row version for the downstream RAG pipeline. Both versions are preserved — Stage 1's original (for audit trail) and Stage 2's corrected version (for production use).

---

## 6. What Stage 2 Does Not Cover

The following are explicitly deferred to subsequent stages:

| Gap | Resolution Stage |
|---|---|
| Clinical correctness of dosing values (e.g., is 80 + 480 mg the right dose for ≥ 35 kg?) | Stage 4: IDI physician review |
| DHA-piperaquine weight-band parsing edge case (p.176) | Stage 3: Enhanced plausibility rules |
| Full-document cross-validation (only 7 pages checked) | Future: expand to all 207 tables if needed |
| Content chunking for RAG/LLM pipeline | Post-extraction chunking strategy (TBD) |
| Vision-model cross-validation (Claude API Tier 2) | Future: targeted verification of ambiguous tables |
