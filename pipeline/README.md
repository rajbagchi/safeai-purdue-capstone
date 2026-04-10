# Pipeline Developer Guide

This document is for developers who want to understand, extend, or debug the pipeline code.

For strategy/rationale docs, see the [`docs/`](../docs/) folder. For setup and usage, see [docs/setup_and_usage.md](../docs/setup_and_usage.md).

## Module map

The pipeline consists of 10 modules executed in sequence by the orchestrator:

```
cli.py               CLI entry point (argparse, preset selection)
  |
orchestrator.py      Pipeline coordinator (MedicalQASystem)
  |
  +-- config.py                  Configuration dataclass + preset factories
  +-- extractor.py               Multi-pass PDF extraction (MultiPassExtractor)
  |     uses docling_table_extractor.py when use_docling_tables=True
  +-- docling_table_extractor.py Optional Docling+TableFormer table extraction
  +-- colpali_retriever.py       Optional ColPali v1.2 visual retrieval (page-level MaxSim)
  +-- validator.py               6-stage extraction validation (ExtractionValidator)
  +-- chunker.py                 Semantic chunking + metadata (SmartChunker)
  +-- clinical_verifier.py       Physician review + deployment gate (ClinicalVerifier)
  +-- retriever.py               Hybrid BM25+dense+RRF retrieval (HybridRetriever)
  +-- guardrail.py               Medical safety validation (MedicalGuardrailBrain)
  +-- response.py                Structured response formatting (ResponseOrchestrator, VHTResponseFormatter)
```

### Execution flow

```python
# 1. CLI parses args, selects preset, creates ExtractionConfig
cfg = extraction_config_who_malaria_nih(pdf_path="...")

# 2. Orchestrator initializes and builds knowledge base
qa = MedicalQASystem(cfg.pdf_path, cfg.output_dir, cfg)
qa.initialize()
#    -> MultiPassExtractor.run()          # 6 passes
#    -> ExtractionValidator.validate_all() # 6 stages
#    -> SmartChunker.chunk_by_headings()   # parent chunks
#    -> SmartChunker.create_child_chunks() # child chunks
#    -> SmartChunker.create_search_index() # BM25 index
#    -> ClinicalVerifier.generate()        # review package
#    -> HybridRetriever(chunks)            # dense index
#    -> MedicalGuardrailBrain(chunks)      # guardrail init

# 3. Q&A loop
result = qa.answer(query)
#    -> HybridRetriever.retrieve(query)    # top-k chunks
#    -> MedicalGuardrailBrain.validate()   # safety check
#    -> ResponseOrchestrator.create()      # structured response
#    -> VHTResponseFormatter.format()      # output formatting
```

## Chunk schema

Every chunk is a dictionary with these fields:

```python
{
    # Core content
    "text": str,                    # Raw text content
    "page": int,                    # Source page number
    "heading": str,                 # Section heading

    # Classification
    "section_type": str,            # dosing | contraindication | diagnosis | treatment | background
    "preservation_level": str,      # VERBATIM | HIGH | STANDARD
    "content_type": str,            # narrative | table | image_ocr | image_placeholder
    "is_table_only": bool,          # True if chunk contains only table data

    # Tables
    "tables": [                     # Embedded tables (may be empty)
        {
            "classification": str,  # dosing | clinical_management | evidence | other
            "nll": str,             # Natural language description
            "headers": [str],
            "data": [dict],
            "markdown": str,
            "num_rows": int,
        }
    ],

    # Clinical metadata (17 fields)
    "clinical_metadata": {
        "condition": str | None,
        "drug_name": str | None,
        "dosage_summary": str | None,
        "patient_weight_min_kg": float | None,
        "patient_weight_max_kg": float | None,
        "patient_age_min": str | None,
        "patient_age_max": str | None,
        "route": str | None,
        "frequency": str | None,
        "duration": str | None,
        "contraindications": [str],
        "special_populations": [str],
        "level_of_care": str | None,
        "clinical_features": [str],
        "danger_signs": [str],
        "referral_criteria": [str],
        "clinical_section_type": str | None,
    },

    # Relationships
    "related_chunks": {
        "prev_sibling": int | None,
        "next_sibling": int | None,
        "preceding_narrative": int | None,
        "following_narrative": int | None,
        "context_for_tables": [int],
        "section_siblings": [int],
    },

    # Child chunk fields (only present on child chunks)
    "parent_chunk_id": int,         # Index of parent chunk
    "contextual_content": str,      # Content with metadata header prepended
    "child_strategy": str,          # proposition | recursive_paragraph | nll_child

    # Retrieval fields (added by retriever)
    "score": float,                 # Fused/reranked relevance score
    "retrieval_rank": int,          # 1-based rank in result set
}
```

## Adding a new preset

1. Create a JSON config in `configs/` (see [configs/README.md](../configs/README.md))
2. Add a factory function in `config.py`:

```python
def extraction_config_my_guideline(
    pdf_path: Optional[str] = None,
    output_dir: Optional[str] = None,
) -> ExtractionConfig:
    json_cfg = _load_json_config(_CONFIGS_DIR / "my_guideline.json")
    # ... merge keywords, set defaults
    return ExtractionConfig(...)
```

3. Register in `cli.py`:

```python
if args.preset == "my-guideline":
    cfg = extraction_config_my_guideline(pdf_path=args.pdf, output_dir=args.output_dir)
```

## Adding a new validation check

1. Add a static method to `ExtractionValidator` in `validator.py`
2. Call it from `_validate_dosing_plausibility()` or create a new stage in `validate_all()`
3. Add tests in `tests/test_dosing_plausibility.py`

## Key constants

| Constant | Location | Value | Purpose |
|---|---|---|---|
| `_CHILD_MAX_TOKENS` | chunker.py | 512 | Max child chunk size (STANDARD) |
| `_CHILD_OVERLAP_TOKENS` | chunker.py | 50 | Overlap between consecutive children |
| `_RRF_K_DEFAULT` | retriever.py | 60 | RRF fusion constant |
| `_CE_BLEND_ALPHA` | retriever.py | 0.6 | Weight for RRF in cross-encoder blend (1-alpha for CE) |
| `DEFAULT_EMBED_MODEL` | retriever.py | all-MiniLM-L6-v2 | Primary embedding (general-purpose, 384-dim) |
| `MEDICAL_EMBED_MODEL` | retriever.py | pubmedbert-base-embeddings | Medical embedding (optional, 768-dim, disabled by default) |
| `DEFAULT_RERANK_MODEL` | retriever.py | ms-marco-MiniLM-L-6-v2 | Cross-encoder reranker (general-purpose) |
| `MEDICAL_RERANK_MODEL` | retriever.py | MedCPT-Cross-Encoder | Medical cross-encoder alternative (Public Domain) |
| `_DRUG_MATCH_BOOST` | retriever.py | 1.35 | Score multiplier for drug-name match |
| `_DOSING_TYPE_BOOST` | retriever.py | 1.25 | Score multiplier for dosing_table in dosing queries |
| `_NLL_BOOST` | retriever.py | 1.15 | Score multiplier for NLL children in dosing queries |
| `_EVIDENCE_TABLE_DEMOTE` | retriever.py | 0.85 | Score demote for evidence_table in dosing queries |
| `_CONDITION_MATCH_BOOST` | retriever.py | 1.20 | Score multiplier for condition metadata match |
| `_DOMAIN_MATCH_BOOST` | retriever.py | 1.10 | Score multiplier for clinical_domain match |
| `_RATIO_TOLERANCE` | validator.py | 0.35 | Max combo drug ratio deviation |
| `_COVERAGE_PEDIATRIC_LOW` | validator.py | 10.0 kg | Expected minimum weight coverage |
| `_COVERAGE_ADULT_HIGH` | validator.py | 35.0 kg | Expected minimum adult coverage |
| `_DOSE_BOUNDS_TOLERANCE` | validator.py | 2.5x | Clinical bounds tolerance factor |
| `_BRITISH_MAP` | retriever.py | 30-term dict | US→UK medical spelling normalization map |
| `DOCLING_AVAILABLE` | docling_table_extractor.py | bool | True if `docling>=2.64.0` installed |
| `COLPALI_AVAILABLE` | colpali_retriever.py | bool | True if `colpali-engine` + `torch` installed |
| `_COLPALI_TABLE_WEIGHT` | colpali_retriever.py | 2.0 | RRF weight multiplier for table pages |
| `_COLPALI_FIGURE_WEIGHT` | colpali_retriever.py | 1.5 | RRF weight multiplier for figure pages |
| `_COLPALI_TEXT_WEIGHT` | colpali_retriever.py | 0.3 | RRF weight multiplier for text-only pages |

## RAG output artifacts

The retrieval benchmark results and deployable mobile package are tracked in [`rag_output/`](../rag_output/). Key files: `retrieval_test_results.json` (12-query benchmark), `build_report.json` (corpus stats and metrics), `child_chunks.json` (1,695 chunks), and `brain1_package/` (24 MB mobile export). Binary indices (FAISS, numpy) are gitignored and regenerated by `retriever.py`. See [`rag_output/README.md`](../rag_output/README.md) for details.

## Recent changes

### 2026-04-10 — `chat.py` + `pipeline/orchestrator.py`: CE threshold calibration + synonym expansion

**Problem:** Queries whose terminology differs from the document vocabulary (e.g. "appendicitis" when the guideline uses "acute abdomen") were triggering the "No matching guidelines found" message even though the content was present. The CE threshold of -1.5 was too aggressive for `ms-marco-MiniLM-L-6-v2`, which was trained on general web-search text, not medical language.

**Fix 1 — CE threshold in `chat.py` raised to -4.0.** Genuinely out-of-domain queries (weather, sports) score -5 to -8. Medical vocabulary mismatches score -1.5 to -3. Using -4.0 avoids false "no match" rejections while still suppressing truly irrelevant queries.

**Fix 2 — Synonym list in `orchestrator._preprocess_query()` expanded from 15 to 35 entries.** New groups include: appendicitis → "acute abdomen surgical abdomen right iliac fossa", stroke → "cerebrovascular accident CVA", meningitis → "meningism neck stiffness", TB, anaemia, typhoid, sickle cell, HIV, sepsis, wound/injury, and more. This ensures retrieval finds the right guideline section even when the user's term and the document's term differ.

### 2026-04-10 — `pipeline/orchestrator.py`: Offline query rewriting (`_preprocess_query`)

New `_preprocess_query(query)` static method runs before every retrieval call. It strips conversational framing ("A lady has…", "My child is…", "I have a patient who…") so the retriever sees clinical terms instead of pronouns and filler. It then appends medical synonyms for 35 term groups (e.g. "bleed" → appends "bleeding haemorrhage hemorrhage"; "fit" → "convulsions seizures"; "appendicitis" → "acute abdomen surgical abdomen right iliac fossa"). Original query is kept for triage inference, display, and response text — only the retrieval call receives the enriched query. No internet access, no models — pure regex and a static synonym dictionary.

### 2026-04-10 — `pipeline/retriever.py` + `chat.py`: No-match detection

**Problem:** Min-max normalisation maps the best retrieved chunk to score 1.0 regardless of absolute relevance. A query about the weather would still return a chunk scoring 1.0 relative to the others in the KB, and the system would generate a response using those chunks.

**Fix:** After computing cross-encoder logits and before min-max normalisation, the max raw CE score (`_ce_best_raw`) is stored on the first result chunk. CE logit > 0 = model believes query and chunk are related; < 0 = not related. In `chat.py`, if `_ce_best_raw < -1.5` (clearly off-topic), the response is suppressed and "No matching guidelines found for this query" is displayed instead. Queries between −1.5 and 0 still show the response but with the existing low-confidence warning. Falls back silently when the cross-encoder is not installed (BM25-only mode).

### 2026-04-10 — `pipeline/response.py` + `chat.py`: RED triage safety gating

**Problem:** For RED-triage (emergency) responses, the response could include:
1. A family message extracted verbatim from a GREEN-context PDF chunk containing "manage at home" language
2. Actions labeled "What to do:" that read as home management steps rather than pre-transport steps

**Fix (response.py):** `_generate_family_message()` now validates PDF-extracted sentences against triage level. For RED triage, sentences containing "at home", "home treatment", or "home management" are rejected. Only sentences containing "refer", "health facility", "hospital", "urgent", or "immediately" are accepted; all others fall through to the hardcoded RED template.

**Fix (chat.py):** For RED triage, actions are filtered to remove any item matching "at home" / "home treatment" / "manage at home". The section label changes from "What to do:" to "Steps while arranging referral:" to make clear these are pre-transport actions.

### 2026-04-10 — `pipeline/response.py`: Triage keyword expansion + typo tolerance

**Problem:** The triage keyword list had only 8 entries with exact matching. A query like "vaginal leeding" (typo for "bleeding") returned GREEN triage; obstetric emergencies ("haemorrhage", "eclampsia", "placenta previa") were not recognised.

**Fix:** Expanded `danger_kw` from 8 to 24 entries using partial-prefix matching (e.g. "bleed" catches bleeding/bleeds/bled; "haemorrhag" catches British haemorrhage). Added obstetric emergency keywords: haemorrhage, hemorrhage, eclampsia, antepartum, postpartum, placenta previa/praevia, abruption, cord prolapse, obstructed labour, sepsis, "in shock". Added fuzzy matching via `rapidfuzz.fuzz.ratio` as a second pass: if exact matching finds nothing, each word in the query is compared to 6 canonical danger-sign phrases; ≥80% similarity triggers RED (catches typos like "leeding" matching "bleeding" at 82%).

### 2026-04-10 — `chat.py`: Extended table artifact filter in `_clean_list_items`

Added patterns to drop table-cell fragments that were leaking into the "When to refer:" section:
- `~` — tilde character used as a cell separator in the Uganda guidelines
- `mg(or` — dose column concatenation artifact
- `)(` — adjacent merged cells
- `con-, ` — word broken across table cells
- Lines starting with "hospital is" — referral column fragment

### 2026-04-10 — `pipeline/response.py`: Content leakage fix (`_relevant_chunks`)

**Problem:** `_extract_list_items_from_chunks` and `_collect_metadata_field` iterated over all 5 retrieved chunks equally. Chunks ranked 4th/5th often score 0.2–0.3 (tangentially related sections), so their bullet points and metadata leaked into actions, monitoring, and referral output — producing steps from unrelated parts of the guidelines.

**Fix:** New `_relevant_chunks(chunks, threshold=0.40, max_chunks=3)` static method filters to chunks above the relevance threshold, capped at 3. Falls back to the top-1 chunk if nothing exceeds the threshold. `_select_actions`, `_select_monitoring`, `_select_referral_criteria`, and the `create()` danger-signs collector all pre-filter through `_relevant_chunks`. Citations and dosing blocks use the full set unchanged.

Constants added: `_CONTENT_SCORE_THRESHOLD = 0.40`, `_CONTENT_MAX_CHUNKS = 3`.

### 2026-04-10 — `requirements-pipeline.txt`: numpy Python 3.13 fix

Changed `numpy>=1.20,<2` → `numpy>=1.26`. numpy 1.x has no pre-built wheel for Python 3.13; pip attempts a C++ source build that fails (`type_traits` header missing). `numpy>=1.26` resolves to numpy 2.x on Python 3.13 which ships pre-built wheels, while still allowing numpy 1.26.x on older Python versions.

### 2026-04-10 — `start.command`: Mac double-click launcher

New shell script for non-technical users. Double-clicking the file in Finder opens a Terminal window that: creates `safeai-env/` virtual environment if absent, installs all dependencies via `pip install -r requirements-pipeline.txt`, opens a native Mac file picker (via `osascript`) to select the guideline PDF, runs `run_pipeline.py` to build the knowledge base on first use, then launches `chat.py`. All subsequent runs skip to `chat.py` immediately. Requires one-time `chmod +x start.command` from Terminal.

### 2026-04-10 — `chat.py`: Conversational interface

New entry point for plain-language interaction. Run with `python3 chat.py` from the project root — no flags needed. Auto-detects available knowledge bases, prompts "What can I help you with today?", routes every query through Brain 1 → Brain 2, and displays clean terminal output (triage header, numbered actions, monitoring, referral criteria, source citations). Strips markdown formatting, deduplicates near-identical list items, and filters truncated/table-derived fragments for clean display.

### 2026-04-10 — `pipeline/response.py`: Brain 1 — 5 improvements

1. **Triage escalation from chunks** (`_escalate_triage_from_chunks`): upgrades triage level when `clinical_metadata.danger_signs` in retrieved chunks signal danger signs not present in the query. Uses metadata only (not raw text) with patient-context filter to avoid false positives.
2. **PDF-first danger signs section**: `VHTResponseFormatter._danger_signs_section()` accepts chunk danger signs and renders them instead of a hardcoded list. `ResponseContent` gains a `danger_signs` field.
3. **PDF-first family message**: `_generate_family_message()` scans chunks for caregiver-education sentences before falling back to templates.
4. **Broader list extraction**: `_extract_list_items_from_chunks()` now also captures action-verb lines (Give, Check, Refer, …) and bold markdown items.
5. **Cross-section deduplication**: `_deduplicate_sections()` ensures the same item never appears in both actions and monitoring/referral.

### 2026-04-10 — `pipeline/guardrail.py` + `pipeline/orchestrator.py`: Brain 2 — 5 improvements

1. **Triage from evidence**: `_collect_danger_signs()` scans query + chunk `clinical_metadata.danger_signs`. `validate_response()` accepts `retrieved_chunks`; orchestrator.py updated at both call sites.
2. **10 dangerous advice patterns** (was 4): added double-dosing, stopping courses early, dosing without weight, home treatment for emergencies, metronidazole in first trimester, ibuprofen in infants.
3. **Dosing value grounding** (`_validate_dosing_values`): every dosing quantity in the response is verified against retrieved source chunk text.
4. **Contraindication cross-check** (`_check_contraindications`): patient context in query matched against chunk `clinical_metadata.contraindications`.
5. **Section completeness** (`_check_completeness`): minimum content thresholds per section; citations must include page references.

### 2026-04-09 — `pipeline/response.py`: Confidence scoring + PDF-first content extraction

**`ResponseOrchestrator._calculate_confidence()`** — previously returned a hardcoded baseline of `0.95` (RED triage) or `0.90` (all other queries), adjusted only for guardrail warnings. Every query, regardless of retrieval quality, received the same score. Now computes from real retrieval signals:

```
confidence = 0.6 × retrieval_score + 0.4 × coverage − penalty
```

- Retrieval score = mean of top-3 retrieved chunk scores (normalized [0,1] by the hybrid retriever)
- Coverage = fraction of 5 requested chunks actually found
- Penalty = −0.05 per guardrail warning, −0.15 per error, −0.10 if guardrail failed overall

**`ResponseOrchestrator._select_actions()`, `_select_monitoring()`, `_select_referral_criteria()`** — previously returned hardcoded text selected by keyword-matching on the query string (~5 possible action sequences regardless of which PDF was loaded). Now use two new helper methods:

- `_extract_list_items_from_chunks(chunks)` — scans retrieved chunk text for bullet-point and numbered-list items using regex, returns them verbatim from the PDF (up to 6, deduplicated)
- `_collect_metadata_field(chunks, field_name)` — reads `danger_signs` and `referral_criteria` from chunk `clinical_metadata` extracted by the chunker

Hardcoded templates remain as fallback only when PDF chunks contain no extractable items. This means every response now reflects the actual uploaded document, not a fixed generic template.

### 2026-04-10 — `pipeline/extractor.py`: Cross-validation PDF repair for all PDF types

**`MultiPassExtractor.pass4_cross_validation()`** — previously failed silently on PDFs produced by tools like Adobe InDesign, which use a non-standard internal page-tree structure that pdfminer/pdfplumber cannot traverse. pdfplumber returned 0 pages, causing the cross-consistency score to stay at 0% — a false failure even when extraction itself was correct.

Now probes pdfplumber first: if 0 pages are returned, re-saves the PDF through PyMuPDF (`garbage=4, deflate=True, clean=True`) to a temporary file that normalises the structure to standard PDF, then runs pdfplumber on the repaired copy. The temporary file is deleted after cross-validation. No configuration change is needed — this repair is automatic and transparent for any uploaded PDF.

## Testing

```bash
# All tests
python -m pytest tests/ -q

# Specific module
python -m pytest tests/test_dosing_plausibility.py -v

# With output
python -m pytest tests/ -v --tb=short
```

Tests use `unittest.mock` extensively to avoid requiring real PDFs, OCR engines, or embedding models.
