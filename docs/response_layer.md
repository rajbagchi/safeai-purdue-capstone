# Response Layer Strategy

**Modules:** `pipeline/response.py` (500 lines), `pipeline/guardrail.py` (145 lines) | **Classes:** `ResponseOrchestrator`, `VHTResponseFormatter`, `MedicalGuardrailBrain`

## What we built

A **two-brain response system** designed for Village Health Team (VHT) workers in low-resource clinical settings. Retrieved chunks are assembled into structured, guardrail-validated responses in multiple output formats.

```
Retrieved chunks
  |
  +---> ResponseOrchestrator
  |       - Infer triage level (RED / YELLOW / GREEN)
  |       - Extract actions from PDF chunk text (bullet/numbered lists)
  |       - Extract monitoring from chunk clinical_metadata (danger_signs)
  |       - Extract referral criteria from chunk clinical_metadata
  |       - Fall back to hardcoded templates only when PDF yields nothing
  |       - Extract VERBATIM dosing blocks
  |       - Generate family education message
  |       - Calculate confidence score from retrieval quality
  |
  +---> MedicalGuardrailBrain (validation)
  |       - Validate triage level against danger signs
  |       - Detect dangerous advice patterns
  |       - Verify citation page references
  |       - Check required response sections
  |
  +---> VHTResponseFormatter (output)
          - VHT_STANDARD: full structured response
          - VHT_QUICK: minimal triage summary
          - CLINICIAN: clinical detail focus
          - REFERRAL: structured referral note
```

### Why a two-brain architecture?

The "generating brain" (ResponseOrchestrator) assembles the response. The "validating brain" (MedicalGuardrailBrain) independently checks it for safety violations. This separation ensures that the generation logic cannot bypass safety checks — the guardrail brain has no knowledge of how the response was assembled, only whether the final output is safe.

### Triage inference

Every response starts with a triage classification:

| Level | Criteria | Response behavior |
|---|---|---|
| **RED** | Danger signs detected (convulsions, unconscious, unable to drink, severe bleeding, haemorrhage, eclampsia, sepsis, etc.) | Emergency header, immediate referral, no home treatment |
| **YELLOW** | Clinical concern without danger signs | Urgent actions, monitoring checklist, referral criteria |
| **GREEN** | Routine clinical question | Standard guidance, monitoring, when-to-refer list |

Triage level drives fallback template selection when PDF chunks do not yield extractable content. When chunks contain relevant list items or clinical metadata, those are used instead (see PDF-first content extraction below).

**Updated 2026-04-10 — Expanded keyword list + typo tolerance.**

`infer_triage_from_query()` now has 24 danger-sign entries (was 8). Partial-prefix matching is used instead of full-word matching: "bleed" matches bleeding/bleeds/bled; "haemorrhag" matches both British and American spellings; "eclampsi" matches eclampsia/pre-eclampsia. Added obstetric emergencies (antepartum/postpartum haemorrhage, eclampsia, placenta previa/praevia, abruption, cord prolapse, obstructed labour), systemic emergencies (sepsis, "in shock", not breathing), and expanded neurological signs (fits, not waking).

Fuzzy matching via `rapidfuzz` is applied as a second pass when exact matching finds nothing: each word in the query is compared to 6 canonical danger-sign phrases at >=80% similarity. This catches common typos ("leeding" -> "bleeding" at 82% similarity) without false-positives on normal clinical vocabulary.

### RED triage response gating

**Added 2026-04-10.** For RED-triage responses, two additional safety gates apply on top of the standard pipeline:

1. **Family message validation** (`_generate_family_message`): PDF-extracted caregiver sentences are rejected for RED triage if they contain "at home", "home treatment", or "home management" language — a GREEN-context sentence extracted from the guidelines must not appear in an emergency response. The sentence is also rejected unless it contains emergency language ("refer", "health facility", "hospital", "urgent", "immediately"). Rejected sentences fall through to the hardcoded RED template ("This is a serious condition. The patient needs to go to the health facility immediately.").

2. **Action label and filter** (`chat.py _format_response`): For RED triage, any action item containing "at home" / "home treatment" / "manage at home" is removed from the list. The section header changes from "What to do:" to "Steps while arranging referral:" to make clear these are pre-transport instructions, not home management steps.

### Preservation-level-aware formatting

The response formatter respects the preservation level assigned during chunking:

- **VERBATIM** chunks (dosing tables): Rendered as exact text blocks with no modification. The `_dosing_block()` method extracts these and presents them in a clearly demarcated section.
- **HIGH** chunks (contraindications, treatment protocols): Presented with minimal formatting changes.
- **STANDARD** chunks (background, diagnosis): May be paraphrased and summarized.

This prevents the response layer from inadvertently altering dosing values — the most dangerous category of error in medical Q&A.

### Structured response sections

The VHT_STANDARD format includes:

1. **Emergency header** (RED triage only) — bold alert box
2. **Quick summary** — one-sentence triage decision
3. **Step-by-step actions** — numbered, concrete instructions
4. **Monitoring checklist** — what to watch for, when to escalate
5. **Danger signs** — when to refer immediately
6. **Family education message** — plain-language explanation for caregivers
7. **VHT reminders** — documentation, follow-up timing
8. **Dosing blocks** — VERBATIM dosing information
9. **Citations** — page references with preservation level labels

### Medical jargon translation

A built-in translation dictionary converts clinical terminology to VHT-friendly language:

```
"lethargic"  →  "very weak"
"dyspnea"    →  "difficulty breathing"
"febrile"    →  "fever"
"emesis"     →  "vomiting"
```

### PDF-first content extraction

**Changed 2026-04-09.** Actions, monitoring items, and referral criteria are now extracted directly from the retrieved guideline PDF chunks rather than selected from hardcoded template lists.

**Why:** The previous implementation used hardcoded keyword-matched templates (e.g. always showing the same 6 "convulsions" steps regardless of what the PDF said). This meant the response content did not actually reflect the loaded guideline — the same fixed text was returned for any document. The fix grounds every response in the actual source material.

**How it works:**

- **Actions** (`_extract_list_items_from_chunks`): Scans the text of each retrieved chunk for bullet-point and numbered-list items using regex, action-verb lines (Give, Check, Refer, Monitor, Administer, ...), and bold markdown items (`**...**`). Items between 10 and 250 characters are collected, deduplicated, and returned (up to 6). These come verbatim from the PDF.
- **Monitoring** (`_collect_metadata_field` -> `danger_signs`): Reads the `danger_signs` list from each chunk's `clinical_metadata`, which the chunker (`pipeline/chunker.py`) already extracts from the PDF text using `_DANGER_SIGN_RE`. Formatted as "Watch for: ...".
- **Referral criteria** (`_collect_metadata_field` -> `referral_criteria`): Reads the `referral_criteria` list from chunk `clinical_metadata`, extracted from the PDF using `_REFERRAL_RE`.

All three methods fall back to the hardcoded templates only when the PDF chunks yield nothing extractable (e.g. chunks are purely tabular with no prose lists).

**Updated 2026-04-10:** Four additional improvements:

- **Triage escalation from chunk content** (`_escalate_triage_from_chunks`): After query-based triage inference, scans `clinical_metadata.danger_signs` across retrieved chunks. If RED-level danger signs are found and the query has patient-clinical context, triage is escalated to RED. If a severity keyword is present and chunk danger signs are non-empty, GREEN is escalated to YELLOW. Conservative design: only uses metadata (not raw chunk text) and requires patient-context signals in the query to prevent informational queries from being falsely escalated.

- **PDF-first danger signs section**: `VHTResponseFormatter._danger_signs_section()` now accepts chunk danger signs from `ResponseContent.danger_signs` and renders them instead of the hardcoded 7-sign list. Falls back to the hardcoded list only when chunks yield nothing.

- **PDF-first family message**: `_generate_family_message()` scans retrieved chunk text for caregiver-education sentences (matching Tell/Explain/Advise/Counsel/Inform patterns) before falling back to templates.

- **Cross-section deduplication** (`_deduplicate_sections`): Actions, monitoring, and referral criteria share a deduplication pass so the same item never appears in two sections of the same response.

**Updated 2026-04-10 (content leakage fix):** Relevance-score filtering for content extraction.

**Why:** The retriever returns 5 chunks sorted by relevance score. In practice, chunks ranked 4th and 5th often score 0.2--0.3 — they are from tangentially related guideline sections (e.g., a general malaria background section retrieved alongside a specific treatment protocol). Because `_extract_list_items_from_chunks` and `_collect_metadata_field` iterated over all 5 chunks equally, bullet points and metadata from these low-relevance chunks leaked into the actions, monitoring, and referral output, producing steps from unrelated parts of the guidelines.

**Fix:** New `_relevant_chunks()` helper filters to chunks with `score >= 0.40` and caps at the top 3. All three selection methods (`_select_actions`, `_select_monitoring`, `_select_referral_criteria`) and the danger-signs collector in `create()` now pre-filter through `_relevant_chunks()`. Fallback: always includes at least the top-1 chunk so extraction is never empty. Citations and dosing blocks continue to use the full retrieved set.

```
_CONTENT_SCORE_THRESHOLD = 0.40   # chunks below this are excluded from content extraction
_CONTENT_MAX_CHUNKS = 3           # never pull from more than 3 chunks for list/metadata extraction
```

### Confidence scoring

**Changed 2026-04-09.** The confidence score is now computed from actual retrieval signals rather than a hardcoded baseline.

**Why:** The previous implementation started at a fixed `0.9` (or `0.95` for RED triage) regardless of retrieval quality. This meant the score was not a real measure — queries that retrieved weakly matched chunks received the same confidence as queries with strong evidence. The README benchmark table showed `0.90` as a result, but it was simply the hardcoded constant.

**How it works (three signals):**

| Signal | Weight | Source |
|---|---|---|
| Retrieval quality | 60% | Mean score of the top-3 retrieved chunks. Scores are normalized to [0, 1] by the hybrid retriever after RRF + cross-encoder blending. |
| Coverage | 40% | Fraction of the 5 requested chunks that were actually found (`len(chunks) / 5`). |
| Guardrail penalty | subtracted | -0.05 per guardrail warning (max 4), -0.15 per error (max 2), -0.10 if guardrail failed overall. |

`confidence = 0.6 * retrieval_score + 0.4 * coverage - penalty`, clamped to [0.0, 1.0].

A query that retrieves 5 highly-relevant chunks with no guardrail issues will score close to 1.0. A query that retrieves weakly-matched chunks or triggers guardrail warnings will score proportionally lower.

## Guardrail validation

The `MedicalGuardrailBrain` runs seven independent checks on every response (updated 2026-04-10):

### 1. Required sections check

Verifies that all five required sections are present: Triage Level, Immediate Actions, Next Steps / Monitoring, When to Refer, Citations.

### 2. Triage validation (updated 2026-04-10)

Scans query text and `clinical_metadata.danger_signs` from retrieved chunks (not raw chunk text). If danger signs are found and the response triage is not RED, the check is flagged as critical. `validate_response()` now accepts `retrieved_chunks` to enable evidence-grounded validation.

### 3. Dangerous advice detection (updated 2026-04-10)

10 regex patterns detect high-risk recommendations (was 4):

- Prescribing medication without mentioning referral
- Suggesting delayed referral when danger signs are present
- Recommending home treatment for emergency conditions
- Aspirin in children (Reye syndrome risk)
- Double-dosing
- Stopping a treatment course early
- Dosing without weight check
- Home treatment for severe/emergency conditions
- Metronidazole in first trimester
- Ibuprofen in infants under 3 months

### 4. Citation validation

Extracts page references from the response and checks that each referenced page exists in the knowledge base.

### 5. Dosing value grounding (new 2026-04-10)

Every explicit dosing quantity in the response (mg, ml, mcg, etc.) is checked against the verbatim text and table markdown of all retrieved source chunks. A value absent from all chunks is flagged — it may have been paraphrased or invented.

### 6. Contraindication cross-check (new 2026-04-10)

Patient-context signals in the query (pregnant, infant, renal impairment, liver disease, breastfeeding) are matched against `contraindications` in retrieved chunk `clinical_metadata`. Applicable contraindications are surfaced as warnings.

### 7. Section completeness check (new 2026-04-10)

Required sections must contain meaningful content above minimum character thresholds (not just a bare header). Citations section must include at least one page reference.

## Rationale

### Why PDF-first action selection over pure templates?

**Changed 2026-04-09.** The original rationale for template-based actions was that clinically-reviewed fixed text is safer than generated prose. This remains valid for the fallback case. However, pure template selection meant the response never adapted to the actual loaded guideline — a document-specific instruction ("Complete 3-day ACT course even if fever resolves on day 1") would never appear unless it happened to be in a hardcoded template.

The current approach extracts bullet and numbered list items verbatim from the PDF, which are already clinically reviewed (they come from WHO or national guidelines). Templates remain as fallback when chunks contain no extractable lists. This preserves the safety rationale while grounding responses in the actual source document.

### Why not use an LLM for response generation?

Several reasons specific to our use case:

1. **Hallucination risk:** An LLM might generate plausible-sounding but incorrect dosing information. Our template + VERBATIM approach never invents dosing data.
2. **Offline operation:** VHTs may work in areas without reliable internet. The pipeline runs entirely locally with no API calls.
3. **Reproducibility:** The same query with the same knowledge base always produces the same response. LLM-based generation is stochastic.
4. **Auditability:** Every piece of information in the response traces back to a specific page in the source document via citations.

### Why four output formats?

Different users need different levels of detail:

- **VHT_QUICK**: For triage decisions in the field — just the level and one action
- **VHT_STANDARD**: For full patient encounters — complete guidance
- **CLINICIAN**: For clinical officers reviewing VHT work — more technical detail
- **REFERRAL**: For handoff between care levels — structured note format

See also: [Safety and guardrails](safety_and_guardrails.md) for how safety is enforced across all pipeline stages.
