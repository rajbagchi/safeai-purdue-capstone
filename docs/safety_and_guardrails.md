# Safety and Guardrails

This document describes the safety measures implemented across every stage of the pipeline. Medical Q&A systems can cause real harm if they deliver incorrect dosing, miss danger signs, or present unverified information as authoritative. Our approach is defense-in-depth: multiple independent safety layers, each catching different categories of error.

## Safety by pipeline stage

### Stage 1: Extraction safety

**Preservation of exact values.** The extraction engine uses rule-based parsing (PyMuPDF + pdfplumber), never LLM-based interpretation. Cell values in dosing tables are preserved character-for-character. This eliminates the risk of an AI model "correcting" a dose that looks unusual but is clinically correct.

**Cross-validation (Pass 4).** Every page of extracted text is independently re-extracted with a second library (pdfplumber) and compared. Pages with <90% consistency are flagged, alerting downstream stages to potential extraction errors.

**Automatic PDF repair (2026-04-10).** Some PDFs produced by tools like Adobe InDesign use a non-standard internal page-tree structure that pdfminer/pdfplumber cannot traverse, causing pdfplumber to return 0 pages and the cross-consistency score to silently stay at 0% — a false failure. The extractor now detects this: if pdfplumber returns 0 pages, it automatically re-saves the PDF through PyMuPDF (`garbage=4, deflate=True, clean=True`) to a temporary file, which normalises the PDF structure to standard format. pdfplumber then runs on the repaired copy and produces correct results. The temporary file is deleted after cross-validation. This fix is transparent — no configuration change is needed — and makes cross-validation work correctly on any uploaded PDF.

**Table classification.** Tables are classified by clinical function (dosing, clinical management, evidence, structural, other). Misclassifying a dosing table as "other" could cause it to be paraphrased instead of preserved verbatim. The classification uses conservative keyword matching with domain-specific vocabularies from `configs/*.json`.

### Stage 2: Validation safety

Six independent validation stages catch different error categories:

| Stage | What it checks | Why it matters |
|---|---|---|
| Structure | Heading hierarchy, page numbering | Malformed structure = wrong section assignments |
| Tables | Column counts, numeric density | Corrupted tables = wrong dosing data |
| Cross-consistency | PyMuPDF vs pdfplumber agreement | Extraction failures = missing content |
| Medical content | Presence of critical clinical terms | Missing terms = incomplete extraction |
| Dosing plausibility | Weight bands, monotonicity, coverage, clinical bounds, combination ratios, empty cells | Implausible dosing = medication errors |
| Human review | Flags items needing physician attention | Catches what automated checks cannot |

**Dosing plausibility** is the most critical safety stage. It runs six sub-checks on every dosing-classified table:

1. **Weight contiguity** — no gaps between consecutive weight bands
2. **Dose monotonicity** — doses increase with weight (as expected clinically)
3. **Weight coverage** — table covers pediatric through adult ranges
4. **Clinical bounds** — per-kg doses fall within reference ranges for known drugs
5. **Combination consistency** — fixed-ratio drug combinations maintain stable ratios
6. **Positive/non-empty** — no missing values in dosing cells

### Stage 3: Chunking safety

**Preservation levels.** Every chunk is assigned a preservation level (`VERBATIM`, `HIGH`, `STANDARD`) based on its section type and table presence. This level travels with the chunk through retrieval and response generation, constraining how the content may be used.

**Metadata extraction.** Clinical metadata (drug names, weight ranges, contraindications) is extracted from every chunk. This enables the retriever and response layer to make safety-aware decisions — e.g., including contraindication chunks when a drug is mentioned.

**Related chunk linking.** Dosing tables are linked to their surrounding narrative context. When a dosing table is retrieved, the related narrative (which may contain contraindications or special population warnings) can be pulled in automatically.

### Stage 4: Clinical verification

**Physician review package.** The `ClinicalVerifier` generates a structured review package (`review_package.json` + `physician_review_report.md`) that a clinician can review before the knowledge base is used for patient care.

**5-tier triage classification:**

| Tier | Content type | Review priority |
|---|---|---|
| 1 | Validated dosing tables (passed Stage 2) | Mandatory — highest priority |
| 2 | Unvalidated dosing tables | Mandatory |
| 3 | Clinical management content | Mandatory |
| 4 | Evidence tables, high-preservation narrative | Recommended |
| 5 | Optional/background content | Optional |

**5 clinical verification checks per chunk:**

1. Dosage accuracy
2. Patient stratification correctness
3. Contraindication completeness
4. Conditional logic integrity
5. Source provenance

**SHA-256 audit hashes.** Every chunk gets a content hash. After physician review, the hash is re-verified to ensure no content was modified between review and deployment.

**Digital signatures.** Completed reviews include a digital signature (reviewer name, institution, timestamp, chunk ID, audit hash) for accountability.

**Deployment gate.** `passes_deployment_gate()` blocks any knowledge base from production use if mandatory-tier chunks (Tiers 1-3) have not been verified. This is a hard gate — there is no override.

### Stage 5: Response safety

**Two-brain architecture.** The response generator and the guardrail validator are separate, independent systems. The generator cannot suppress or modify guardrail findings.

**Guardrail checks (updated 2026-04-10):**
- Triage level must match danger signs detected in query + retrieved chunk metadata
- Dangerous advice patterns are regex-detected and blocked (10 patterns)
- All five required sections must be present with meaningful content
- Citations must reference real pages in the knowledge base
- Dosing values in the response must appear verbatim in at least one retrieved source chunk
- Drug contraindications from chunk metadata are cross-checked against patient context in the query

**Guardrail improvements (2026-04-10):** Five new checks added to `MedicalGuardrailBrain`:

1. **Triage validation from evidence** — `_collect_danger_signs()` scans query text and `clinical_metadata.danger_signs` from retrieved chunks (not raw chunk text, which is too noisy). If danger signs are found and the response is not RED, the check fails. `validate_response()` now accepts `retrieved_chunks` as an optional parameter — both call sites in `orchestrator.py` pass the retrieved chunks.

2. **Expanded dangerous advice patterns** — 4 → 10 patterns. New: double-dosing, stopping treatment course early, dosing without weight check, home treatment for emergencies, metronidazole in first trimester, ibuprofen in infants.

3. **Dosing value grounding** — `_validate_dosing_values()`: every dosing quantity in the response (mg, ml, mcg, etc.) is checked against the verbatim text and table markdown of all retrieved source chunks. A value absent from all chunks is flagged — it may have been paraphrased or invented.

4. **Contraindication cross-check** — `_check_contraindications()`: patient-context signals in the query (pregnant, infant, renal, liver, breastfeeding) are matched against `contraindications` in retrieved chunk `clinical_metadata`. Any contraindication that applies to the detected patient context raises a warning.

5. **Section completeness** — `_check_completeness()`: required sections must contain content above minimum character thresholds (not just a bare header). Citations section must include at least one page reference.

**Triage keyword hardening (2026-04-10):** `infer_triage_from_query()` expanded from 8 to 24 danger-sign entries covering obstetric emergencies (haemorrhage, eclampsia, antepartum/postpartum, abruption, placenta previa, cord prolapse, obstructed labour), systemic emergencies (sepsis, shock, not breathing), and partial-prefix matching to catch inflected forms. Fuzzy matching via `rapidfuzz` (>=80% similarity) added as a second pass to catch misspelled danger signs -- a query like "vaginal leeding" now correctly triggers RED triage.

**RED triage response gating (2026-04-10):** Two gates prevent home-management language from appearing in emergency responses:
- `_generate_family_message()` rejects PDF-extracted sentences containing "at home"/"home treatment" for RED triage; only accepts sentences with hospital/refer/emergency language.
- `chat.py` filters actions matching "at home"/"manage at home" for RED triage and relabels the section "Steps while arranging referral:" so instructions are clearly pre-transport, not home care.

**No-match detection (2026-04-10):** When a query has no relevant content in the loaded guidelines, the system now responds "No matching guidelines found" instead of fabricating a response from loosely related chunks. The raw cross-encoder logit (before min-max normalisation) is captured as `_ce_best_raw` on the top result. CE logit < -1.5 indicates no reliable match; the response is suppressed entirely. This is a safety improvement: a fabricated response based on wrong-section chunks is more dangerous than a clear "not found" message.

**Offline query rewriting (2026-04-10):** Before retrieval, `orchestrator._preprocess_query()` strips conversational framing and expands medical synonyms using a 15-group offline dictionary. This improves the chance that the retriever finds the correct guideline section, reducing the risk of responses based on wrong-section content.

**Preservation-level enforcement.** VERBATIM content (dosing tables) is rendered exactly as extracted -- the response formatter cannot paraphrase or summarize it.

**Confidence scoring (updated 2026-04-09).** Every response includes a numeric confidence (0.0-1.0) computed from three real retrieval signals:

```
confidence = 0.6 * retrieval_score + 0.4 * coverage - penalty
```

- **Retrieval score (60%)** -- mean score of the top-3 retrieved chunks, normalized to [0,1] after RRF + cross-encoder blending
- **Coverage (40%)** -- fraction of the 5 requested chunks that were actually returned
- **Guardrail penalty (subtracted)** -- -0.05 per warning, -0.15 per error, -0.10 if guardrail failed

Prior to this change, the score was a hardcoded constant (0.90 for all non-RED queries) adjusted only for guardrail warnings -- meaning a query backed by weak evidence received the same score as one with five highly-relevant passages. The score now carries real information about how well the retrieved evidence supports the response.

## Defense-in-depth summary

```
PDF Input
  |
  [Extraction] --- exact value preservation, no LLM interpretation
  |
  [Cross-validation] --- dual-extractor consistency check
  |
  [Validation] --- 6 stages, 6 dosing sub-checks
  |
  [Chunking] --- preservation levels, metadata extraction
  |
  [Clinical verification] --- physician review, audit hashes, deployment gate
  |
  [Retrieval] --- metadata-aware, not just embedding similarity
  |
  [Response generation] --- PDF-first content extraction, VERBATIM dosing blocks
  |
  [Guardrail validation] --- independent safety checks
  |
  [Confidence score] --- numeric safety signal to user
  |
  Response Output
```

No single layer is relied upon exclusively. Each layer catches different failure modes, and the deployment gate ensures that unverified content cannot reach patients.

See also: [Benchmarking and validation](benchmarking_and_validation.md) for quantitative safety metrics.
