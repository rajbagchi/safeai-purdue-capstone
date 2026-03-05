# Stage 4b: Clinical Verification Framework

**Safe AI Uganda — Clinical Data Extraction Methodology**
**Document:** WHO Consolidated Malaria Guidelines (B09514-eng.pdf, 478 pages)
**Last updated:** 04.03.2026

---

## Executive Summary

Stage 4b generates a physician review package from Stage 4a's 1,478 chunks, enabling an IDI physician to verify safety-critical clinical content against the source PDF. The framework implements the **5 Clinical Verification Checks** (Dosage Accuracy, Stratification, Contraindications, Conditional Logic, Provenance) and produces both a structured JSON review package and a human-readable markdown report.

**Key insight: Physicians review only 31 mandatory chunks (2.1%), not all 1,478.** A 5-tier triage system prioritizes the 8 validated dosing tables (Tier 1), 22 unvalidated dosing tables (Tier 2), and 1 clinical management table (Tier 3) as mandatory, while 325 evidence + high-priority narrative chunks (Tier 4) are recommended. The remaining 1,122 standard chunks are excluded from the review package entirely.

**Safety rule: No content proceeds to Phase B (Deployment) without a `verified_by` signature and `audit_hash`.**

| Metric | Value |
|---|---|
| **Total chunks in pipeline** | 1,478 |
| **Review items generated** | 356 (Tiers 1–4) |
| **Mandatory review (Tiers 1–3)** | **31 chunks (2.1%)** |
| **Recommended review (Tier 4)** | 325 chunks (22.0%) |
| **Optional — excluded from package** | 1,122 chunks (75.9%) |
| **Tier 1 — Validated dosing tables** | 8 (passed all 6 Stage 3 checks) |
| **Tier 2 — Unvalidated dosing tables** | 22 (Stage 3 skipped) |
| **Tier 3 — Clinical management tables** | 1 |
| **Tier 4 — Evidence + high narratives** | 325 |
| **Dosing tables with NLL** | 30/30 (100%) |
| **Audit hashes computed** | 356/356 (100%) |
| **Est. mandatory review time** | ~62 min |
| **Est. total review time (all tiers)** | ~225 min |
| **Total execution time** | ~0.4 seconds |
| **Compute requirements** | CPU-only; no dependencies beyond Python stdlib |

---

## 1. The 5 Clinical Verification Checks

Every reviewed chunk is assessed against these 5 criteria by the IDI physician:

| # | Check | What the physician verifies | Primary for |
|---|---|---|---|
| 1 | **Dosage Accuracy** | Dose values match source PDF exactly (e.g., "80+480 mg", "1 tablet") | Dosing tables |
| 2 | **Stratification** | Age/weight ranges are preserved — no merged or missing rows | Dosing tables |
| 3 | **Contraindications** | Warnings are present (e.g., "Do not use in first trimester") | Narratives, clinical tables |
| 4 | **Conditional Logic** | IF/THEN referral logic is intact (e.g., NLL dosing rules, danger sign criteria) | Dosing tables (via NLL) |
| 5 | **Provenance** | Source page number and section citation are correctly cited | All chunk types |

### Check Applicability by Chunk Type

Not all 5 checks apply equally to all chunk types. The review package marks which checks are applicable for each item:

| Check | Dosing Tables | Clinical Tables | Evidence Tables | High Narratives |
|---|:---:|:---:|:---:|:---:|
| Dosage Accuracy | ✅ Primary | ✅ | — | ✅ if doses mentioned |
| Stratification | ✅ Primary | ✅ | — | ✅ if ranges mentioned |
| Contraindications | ✅ | ✅ | — | ✅ Primary |
| Conditional Logic | ✅ (via NLL) | ✅ | — | ✅ if IF/THEN present |
| Provenance | ✅ | ✅ | ✅ | ✅ |

For narrative chunks, applicability is determined dynamically: the script scans for dosing keywords (mg/kg, tablet, dose), stratification terms (weight, age, infant, child), contraindication language (contraindicated, do not give, avoid), and conditional logic patterns (if/then, refer, danger sign).

---

## 2. Review Priority Tiers

The framework uses a 5-tier triage system that is more granular than Stage 4a's preservation levels:

| Tier | Description | Chunks | Requirement | Rationale | Est. Time |
|---|---|---|---|---|---|
| **1** | Validated dosing tables — passed all 6 Stage 3 checks | **8** | **Mandatory** | Highest confidence; physician confirms automated validation | ~16 min |
| **2** | Unvalidated dosing tables — Stage 3 skipped (no weight column) | **22** | **Mandatory** | No automated checks; physician must verify carefully | ~44 min |
| **3** | Clinical management tables | **1** | **Mandatory** | Safety-critical clinical management content | ~2 min |
| **4** | Evidence tables + high-preservation narratives | **325** | **Recommended** | Clinical thresholds, dosing keywords, contraindications | ~2.7 hrs |
| **5** | Standard chunks (general narrative, structural, images) | **1,122** | **Optional** | No safety-critical content; excluded from review package |  |

### Tier Classification Logic

1. **Tier 1**: `chunk_type == "dosing_table"` AND `validation.status == "pass"` (including stitched table)
2. **Tier 2**: `chunk_type == "dosing_table"` AND validation was skipped or absent
3. **Tier 3**: `chunk_type == "clinical_table"`
4. **Tier 4**: `chunk_type == "evidence_table"` OR (`chunk_type == "narrative"` AND `safety.preservation_level == "high"`)
5. **Tier 5**: Everything else

### Physician Review Workflow

1. **Start with Tier 1** (8 chunks): These dosing tables passed all 6 automated checks. The physician confirms the extraction matches the source PDF.
2. **Proceed to Tier 2** (22 chunks): These dosing tables had no automated validation. Extra scrutiny required.
3. **Review Tier 3** (1 chunk): Clinical management table — verify all management recommendations are correct.
4. **Optionally review Tier 4** (325 chunks): Evidence tables and narratives containing dosing/contraindication keywords. Grouped by section for efficient review.
5. **Skip Tier 5**: 1,122 standard chunks have no safety-critical content and are not included in the review package.

---

## 3. Review Decisions

For each item, the physician records one of three decisions:

| Decision | Meaning | Action |
|---|---|---|
| **Approved** | All applicable checks pass; content is accurate | `verified_by.status` → `"verified"` |
| **Flagged** | One or more checks fail; requires attention before deployment | `verified_by.status` → `"flagged"` |
| **Corrected** | Content was incorrect; corrections noted | `verified_by.status` → `"flagged"` + corrections recorded |

---

## 4. Audit Hash & Digital Signature

### Audit Hash

Each review item carries an `audit_hash` — the SHA-256 hash of the chunk's `content` field. This hash is:

- **Computed at generation time** when the review package is created
- **Verified at ingestion time** when the completed review is processed
- **Purpose**: Ensures the physician reviewed the exact content that was extracted — if the content was tampered with between generation and review, the hash mismatch triggers a rejection

### Digital Signature

When the completed review is ingested, a `digital_signature` is computed for each reviewed chunk:

```
digital_signature = SHA-256(reviewer_name | institution | chunk_id | audit_hash | reviewed_at)
```

This creates a **tamper-evident** link between the reviewer's identity and the specific review action. Changing any field (name, institution, chunk, content, or timestamp) invalidates the signature.

### Integrity Chain

The full integrity chain from extraction to deployment:

```
Stage 1 (extraction) → Stage 2 (cross-validation) → Stage 3 (plausibility)
    → Stage 4a (chunking + metadata)
    → Stage 4b (audit_hash computed)
    → Physician review (5 checks × N chunks)
    → Stage 4b --ingest (digital_signature computed, verified_by updated)
    → Deployment gate: verified_by.status == "verified" AND audit_hash matches
```

---

## 5. Output Artefacts

### Generate Mode (default)

| File | Size | Contents |
|---|---|---|
| `extraction_output/review_package.json` | ~1.8 MB | 356 review items with audit hashes, clinical metadata, NLL, context, and empty review templates |
| `extraction_output/physician_review_report.md` | ~1.0 MB | Human-readable markdown with full content, checklists, and decision fields organized by tier |

### Ingest Mode (`--ingest`)

| File | Action | Contents |
|---|---|---|
| `extraction_output/chunks.json` | **Updated** | `verified_by` fields populated with reviewer info, digital signatures, and `audit_hash` added to each reviewed chunk |

---

## 6. Review Package Schema

### Per-Review-Item Fields

| Field | Type | Description |
|---|---|---|
| `chunk_id` | string | Unique chunk identifier |
| `review_priority` | enum | `mandatory` / `recommended` / `optional` |
| `review_tier` | int | 1–5 |
| `tier_label` | string | Human-readable tier description |
| `preservation_level` | enum | `verbatim` / `high` / `standard` |
| `chunk_type` | string | From Stage 4a |
| `source_pages` | int[] | PDF page numbers |
| `section_path` | string | Full section hierarchy |
| `clinical_domain` | string | Inferred clinical topic |
| `content` | string | Full extracted content |
| `audit_hash` | string | SHA-256 of content |
| `content_hash` | string | SHA-256 of full chunk JSON |
| `clinical_metadata` | object | Drug name, weight ranges, condition, etc. |
| `validation_summary` | string | Human-readable Stage 3 result |
| `nll` | string/null | Natural Language Logic (dosing tables) |
| `context` | object | Preceding/following narrative previews |
| `applicable_checks` | object | Which of the 5 checks apply, with guidance |
| `review` | object | Empty template for physician to fill |

### Review Template (to be completed by physician)

```json
{
  "checks": {
    "dosage_accuracy": {"status": null, "notes": null},
    "stratification": {"status": null, "notes": null},
    "contraindications": {"status": null, "notes": null},
    "conditional_logic": {"status": null, "notes": null},
    "provenance": {"status": null, "notes": null}
  },
  "overall_decision": null,
  "corrections": null,
  "reviewer_name": null,
  "reviewer_role": null,
  "institution": null,
  "reviewed_at": null,
  "digital_signature": null
}
```

---

## 7. Two Modes of Operation

### Generate Mode (default)

```
python stage4b_review_package.py
```

1. Loads `chunks.json` (1,478 chunks)
2. Classifies every chunk into tiers 1–5
3. Computes SHA-256 audit hash for each chunk's content
4. Determines which of the 5 checks apply to each item
5. Retrieves context (preceding/following narrative previews)
6. Assembles `review_package.json` with 356 items (tiers 1–4)
7. Generates `physician_review_report.md` organized by tier
8. Prints scorecard

### Ingest Mode

```
python stage4b_review_package.py --ingest path/to/completed_review.json
```

1. Loads original `chunks.json` and the completed review
2. Validates 6 integrity checks:
   - All mandatory chunks have a decision
   - All applicable check statuses are filled
   - Audit hashes match (no content tampering)
   - Reviewer identity is present
   - Timestamps are valid ISO datetimes
   - Flagged/corrected items have notes
3. Computes digital signatures for each reviewed chunk
4. Updates `chunks.json` with `verified_by` fields and `audit_hash`
5. Prints ingestion scorecard

---

## 8. Physician-Readable Report Structure

The markdown report (`physician_review_report.md`) is organized for efficient physician review:

1. **Header** — Document title, pipeline version, safety rule
2. **Instructions** — How to use the document, the 5 checks, the 3 decisions
3. **Summary table** — Tier breakdown with chunk counts, priorities, and estimated review times
4. **TIER 1** — Each validated dosing table with:
   - Full extracted content in code block
   - NLL representation
   - Clinical context (preceding/following narrative previews)
   - Extracted clinical metadata (drug, weight range, dosage, condition)
   - 5-check verification checklist with specific guidance
   - Decision checkboxes + notes field
5. **TIER 2** — Unvalidated dosing tables (same format, marked as "no automated validation")
6. **TIER 3** — Clinical management table
7. **TIER 4** — Evidence tables + high-priority narratives (grouped by section for efficiency)
8. **Appendix** — Reviewer sign-off form, glossary of terms

---

## 9. Time Breakdown

| Phase | Time |
|---|---|
| Load chunks.json | 0.16s |
| Classify into tiers | <0.01s |
| Assemble review package | 0.19s |
| Generate markdown report | <0.01s |
| Save outputs | 0.06s |
| **Total** | **~0.4s** |

---

## 10. What's Not Covered (Deferred to Stage 4b Ingestion or Later)

| Gap | Reason / Mitigation |
|---|---|
| **Actual physician review** | This stage generates the package; the physician reviews offline. Ingestion mode processes completed reviews. |
| **Automated pre-filling of check statuses** | All check statuses start as null; the physician fills them in. Future work could auto-suggest based on Stage 3 validation results. |
| **Web-based review UI** | The review is conducted via JSON + markdown files. A web UI (e.g., Streamlit) could be built on top of `review_package.json` in a future iteration. |
| **Multi-reviewer support** | Current schema supports one reviewer per chunk. Multiple reviewers would require extending the `verified_by` schema to an array. |
| **Chunk correction workflow** | When a physician marks an item as "corrected", the correction text is stored but not automatically applied to the chunk content. Manual application is required. |
| **Cross-chunk consistency checks** | The review is per-chunk; cross-referencing between related chunks (e.g., dosing table vs. preceding narrative) is left to the physician's clinical judgment. |
