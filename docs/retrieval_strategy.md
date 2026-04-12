# Retrieval Strategy

**Module:** `pipeline/retriever.py` (650 lines) | **Class:** `HybridRetriever`

## What we built

A **hybrid retrieval system** combining sparse keyword search (BM25), dense semantic search (FAISS + sentence-transformers), reciprocal rank fusion (RRF), cross-encoder reranking, and metadata-aware boosting.

```
User query
  |
  +---> BM25 (sparse)               ---> top-20 by keyword match
  |                                        |
  +---> FAISS (general, MiniLM)     ---> top-20 by embedding similarity
  |                                        |
  +---> FAISS (medical, PubMedBERT) ---> top-20 by medical similarity (optional)
  |                                        |
  +---> ColPali v1.2 (visual)       ---> top-20 pages by MaxSim (optional)
  |       content-aware weight:            |
  |       table pages 2x, figure 1.5x,    |
  |       text-only 0.3x                   |
  +------- Reciprocal Rank Fusion ---------+---> top-10 fused results
  |
  +---> Cross-encoder reranking (blended) ---> re-scored top-10
  |
  +---> Metadata-aware re-ranking (4 boosts) ---> top-5 final results
```

### Why hybrid?

Neither sparse nor dense retrieval alone is sufficient for medical Q&A:

- **BM25** excels at exact drug name matches ("artemether-lumefantrine") but fails on semantic paraphrases ("anti-malarial combination therapy").
- **Dense retrieval** captures semantic similarity but can miss exact dosing values — a query for "5 mg/kg" may retrieve content about "weight-based dosing" that mentions different doses.

Combining both modalities with rank fusion consistently outperforms either alone in our testing.

## CT Health AI Integration: ColPali v1.2 Visual Retrieval

**Module:** `pipeline/colpali_retriever.py` | **Status:** Optional, auto-detected at query time

### Why visual retrieval?

Clinical PDFs frequently contain dosing tables and diagnostic flow charts rendered as images rather than text. PyMuPDF and pdfplumber can only extract text; they produce empty or placeholder output for image-based content. BM25 and FAISS have no signal for these pages. ColPali v1.2 operates directly on page images using a PaliGemma-3B vision-language backbone — it sees what a human sees, regardless of whether the PDF layer contains machine-readable text.

CT Health AI uses ColPali as its primary visual retrieval tier. We ported the same approach into SafeAI as an optional fourth tier in RRF fusion.

### How it works

**Indexing (once per PDF):**
1. Each page is rendered to a 150 DPI RGB image via `pypdfium2`
2. ColPali embeds each page as a set of 128-dim L2-normalized patch embeddings (`(n_patches, 128)` array)
3. Embeddings are saved as `.npy` files in `<kb_dir>/colpali_index/`
4. A `metadata.json` records per-page content flags (`has_tables`, `has_figures`) and chunk_ids

**Query time:**
1. The query text is embedded with ColPali's query encoder -> `(n_tokens, 128)` array
2. MaxSim late-interaction score is computed against each page:
   ```
   Score = sum_t  max_p  (query_emb[t] . page_emb[p])
   ```
   For each query token, find the most similar page patch, then sum. This captures fine-grained spatial matches — e.g., a query token "5mg/kg" matching the specific cell in an image-based dosing table.
3. Top-20 pages ranked by MaxSim score, expanded to their associated chunk_ids
4. Content-aware weighting applied before RRF:
   - Table pages: `colpali_score x 2.0` — high confidence, directly relevant
   - Figure pages: `colpali_score x 1.5` — high value for diagnostic/flow content
   - Text-only pages: `colpali_score x 0.3` — suppress noise; text search handles these better
5. ColPali ranked list enters RRF alongside BM25, FAISS general, FAISS medical

### Build the index

```bash
# Install dependencies
pip install 'colpali-engine>=0.3.8' torch torchvision pypdfium2

# Build index (run once, after run_pipeline.py)
python scripts/build_colpali_index.py --pdf /path/to/guideline.pdf --kb ./my_output

# Test on first 50 pages
python scripts/build_colpali_index.py --pdf guideline.pdf --kb ./my_output --pages 0-49

# Reduce batch size if out of memory
python scripts/build_colpali_index.py --pdf guideline.pdf --kb ./my_output --batch-size 2
```

### Auto-detection

`query.py` auto-detects `colpali_index/` in the KB directory and enables visual retrieval with no extra flags. `HybridRetriever` accepts an optional `colpali_index` parameter:

```python
from pipeline.colpali_retriever import ColPaliIndex
colpali_index = ColPaliIndex(Path("./my_output/colpali_index"))
retriever = HybridRetriever(chunks, colpali_index=colpali_index)
```

If `colpali-engine` is not installed or the index does not exist, the retriever continues with BM25 + FAISS + cross-encoder. ColPali failure never blocks a query.

## CT Health AI Integration: Spelling Normalization + BM25 Heading Weighting

After comparing this codebase with CT Health AI (which uses sqlite-vec + FTS5 BM25 with explicit heading repetition weighting), two improvements were ported into this retriever:

### 1. American -> British medical spelling normalization

Medical guidelines authored outside the US use British spellings ("anaemia", "haemoglobin", "oedema"). A query for "anemia" will have zero BM25 overlap with a chunk containing "anaemia". This is a known retrieval failure mode for WHO guidelines.

`_normalize_medical_spelling(query)` applies a 30-term US->UK substitution map (e.g., `anemia -> anaemia`, `hemoglobin -> haemoglobin`, `pediatric -> paediatric`, `cesarean -> caesarean`) to the query before it reaches BM25 and dense retrieval. The map is defined in `_BRITISH_MAP` at the top of `retriever.py`.

Normalization runs automatically on every query in `retrieve()`:

```python
normalized_q = _normalize_medical_spelling(query)
# Used for BM25, dense embedding, and cross-encoder — all three modalities benefit
```

### 2. BM25 heading repetition weighting

CT Health AI weights section headings more heavily than body text in its BM25 index by repeating heading tokens proportional to their structural level. A dosing table under "Severe Malaria — Artesunate Dosing" should rank higher for a query about artesunate dosing than a table under a generic "Treatment" heading, even if both have the same body text.

`_chunk_text()` (the static method that builds the BM25 index token sequence) now applies heading repetition:

| Heading level | Repetitions |
|---|---|
| Level 1 (top section) | 5x |
| Level 2 (subsection) | 3x |
| Level 3 (sub-subsection) | 2x |
| Body text / no heading | 1x (unchanged) |

For child chunks (`contextual_content` present), extra heading repetitions are prepended as a prefix so the embedding also captures the structural signal. For parent chunks, heading tokens appear at the start, followed by body text and NLL.

This change improves precision for hierarchical medical documents where the same dosing content can appear under multiple section levels.

### BM25 (sparse search)

The BM25Okapi index is built over tokenized chunk text. Tokenization strips non-alphanumeric characters, lowercases, and removes single-character tokens. The index searches over the `contextual_content` field of child chunks, which includes the metadata header. Heading tokens are repeated proportional to structural level (see CT Health AI Integration above), and queries are normalized from American to British medical spelling before being submitted.

### Dense search (FAISS)

Chunks are embedded using `sentence-transformers/all-MiniLM-L6-v2` (384-dimensional embeddings, ~90 MB model). The FAISS `IndexFlatIP` (inner product) index stores normalized embeddings for exact cosine similarity search. The text sent to the encoder is the `contextual_content` field — the child chunk's content with its metadata header prepended — so the embedding captures both context and content.

**Model choice rationale:** `all-MiniLM-L6-v2` is a general-purpose sentence encoder trained on 1B+ sentence pairs (Apache 2.0). It is NOT a medical-domain-specific model. We chose it for its small footprint, fast inference, and strong general semantic similarity. The lack of medical-specific training is compensated by BM25's exact keyword matching and the metadata-aware re-ranking layer.

**Dual-embedding support:** The retriever supports an optional second embedding model via the `medical_embed_model_name` parameter (default `None`). When set (e.g., to `NeuML/pubmedbert-base-embeddings`), the retriever builds a second FAISS index and merges results via 3-way RRF (BM25 + general dense + medical dense). Model constants are defined in `retriever.py`: `DEFAULT_EMBED_MODEL`, `MEDICAL_EMBED_MODEL`, `DEFAULT_RERANK_MODEL`, `MEDICAL_RERANK_MODEL`.

### Reciprocal Rank Fusion (RRF)

RRF merges the BM25 and dense ranked lists using:

```
RRF_score(doc) = sum( 1 / (k + rank_i(doc)) )  for each ranked list i
```

With `k=60` (standard), this gives balanced weight to both modalities. A document ranked #1 in both lists gets score `2/61 = 0.033`; a document ranked #1 in one and #20 in the other gets `1/61 + 1/80 = 0.029`. The gap is small, which is intentional — we want documents that appear in both lists to rank highest, not just documents that dominate one list.

### Cross-encoder reranking (optional)

The top-10 fused results are re-scored using `cross-encoder/ms-marco-MiniLM-L-6-v2` with **alpha-blended scoring**. Rather than fully replacing RRF scores with cross-encoder scores, the system blends them:

```
blended = alpha * norm(RRF) + (1 - alpha) * norm(CE)
```

where `_CE_BLEND_ALPHA = 0.6` (i.e., 60% weight on RRF, 40% on cross-encoder). Both score vectors are min-max normalized to [0, 1] before blending. This preserves the medical-keyword signals from BM25 (carried through RRF) while benefiting from the cross-encoder's semantic understanding. The optimal alpha range was found via sweep: 0.60-0.80 all produce equivalent results; 0.60 was chosen as the sweet spot giving maximum cross-encoder influence without degrading keyword precision.

**Model choice rationale:** `cross-encoder/ms-marco-MiniLM-L-6-v2` is a general-purpose cross-encoder trained on MS MARCO web search data (Apache 2.0). Like the embedding model, it has NO medical-domain-specific training, which is why blending (not replacing) RRF scores is important — a full replacement lets the cross-encoder overpower medical keyword signals from BM25.

**MedCPT cross-encoder support:** The `_load_cross_encoder()` method auto-detects MedCPT vs. sentence-transformers models. For MedCPT (`ncbi/MedCPT-Cross-Encoder`), it uses `AutoModelForSequenceClassification` with safetensors instead of the sentence-transformers `CrossEncoder` wrapper. This is the only biomedical cross-encoder available on HuggingFace, trained on 18M PubMed query-article pairs (Public Domain license).

Reranking is non-fatal: if the cross-encoder model fails to load (e.g., no internet on first run), the system falls back to RRF-only results with a warning.

### Metadata-aware re-ranking (v2)

After cross-encoder reranking, a metadata-aware post-processing step applies four multiplicative boost signals using clinical metadata already present on every chunk. This never removes results — only re-orders them.

**Boost 1 — Drug-name match (x1.35):** Drug names are extracted from the query using the config's `drug_keywords` list. Chunks whose content or `drug_name` metadata field contains a matching drug receive a 35% score boost. This fixes the Q01 failure where artesunate content outranked the correct artemether-lumefantrine dosing table.

**Boost 2 — Chunk-type for dosing queries (x1.25 / x1.15 / x0.85):** When the query contains dosing-intent signals ("dose", "mg/kg", "tablet", "schedule"), `dosing_table` and `verbatim` chunks receive a 25% boost, NLL children (semantic bridges to tables) receive 15%, and `evidence_table` chunks are demoted by 15%. This ensures that for dosing questions, the actual dosing table ranks above narrative paragraphs that happen to mention similar weights.

**Boost 3 — Condition match (x1.20):** The query is matched against condition patterns from the config (regex-based, e.g., `severe\s+malaria` -> "Severe malaria") or a built-in keyword map. Chunks whose `condition` metadata matches receive a 20% boost.

**Boost 4 — Clinical domain match (x1.10):** Domain-relevant keywords are extracted from the query and soft-matched against each chunk's `clinical_domain` field (99.7% fill rate). The boost scales with the fraction of matched keywords, up to 10%.

All four boosts stack multiplicatively. A dosing table chunk matching on drug name + dosing type + condition + domain can receive up to ~2x the original score, while an irrelevant evidence table is demoted.

### Graceful degradation

The retriever adapts to available dependencies:

| Available | Behavior |
|---|---|
| BM25 + FAISS + cross-encoder + metadata | Full hybrid + reranking + metadata boosts |
| BM25 + FAISS + cross-encoder | Full hybrid + reranking (no metadata boosts) |
| BM25 + FAISS | Hybrid with RRF, no reranking |
| BM25 only | Sparse keyword search only |

Metadata re-ranking is enabled by default and requires no additional dependencies — it uses metadata fields already present on chunks. It can be disabled via `enable_metadata_reranking=False` on the `HybridRetriever` constructor.

This means the pipeline works on machines without GPU or without `sentence-transformers` / `faiss-cpu` installed — it just falls back to BM25.

## Model evaluation

We evaluated 6 embedding models and 1 cross-encoder for medical domain retrieval. Both current production models are general-purpose (not medical-trained).

### Embedding candidates

| Model | Training Data | License | Dims | Drop-in? | Verdict |
|-------|--------------|---------|------|----------|---------|
| `NeuML/pubmedbert-base-embeddings` | PubMed title-abstract pairs | Apache 2.0 | 768 | Yes | Best medical option -- benchmarks 95.62 vs 93.46 on PubMed tasks |
| `FremyCompany/BioLORD-2023` | UMLS/SNOMED-CT ontologies | MIT | 768 | Yes | Ontology-grounded; UMLS license nuance |
| `ncbi/MedCPT-Query-Encoder` + `Article-Encoder` | 255M PubMed search logs | Public Domain | 768 | No (dual encoder) | Best retrieval benchmarks but needs pipeline refactor |
| `lokeshch19/ModernPubMedBERT` | PubMed (contrastive) | MIT | 768 | Yes | 2048-token context; new, limited benchmarks |
| `pritamdeka/S-PubMedBert-MS-MARCO` | PubMedBERT + MS MARCO | CC-BY-NC | 768 | Yes | Non-commercial license -- unusable for production |
| `gsarti/biobert-nli` | BioBERT + NLI | unclear | 768 | Yes | REJECTED: underperforms general-purpose |

### Cross-encoder candidates

| Model | Training Data | License | Verdict |
|-------|--------------|---------|---------|
| `ncbi/MedCPT-Cross-Encoder` | 18M PubMed query-article pairs | Public Domain | Only biomedical cross-encoder on HuggingFace |

### Configuration benchmark (12-query, original)

| Config | Embedding | Cross-Encoder | P@3 | MRR | Perfect | Build Time |
|--------|-----------|--------------|------|------|---------|------------|
| Baseline (archived) | MiniLM | none | 0.944 | 0.944 | 11/12 | -- |
| **A: gen+gen blend** | MiniLM | ms-marco (alpha=0.6) | **0.750** | **0.944** | **5/12** | ~70s |
| B: med+med | PubMedBERT | MedCPT (alpha=0.6) | 0.722 | 0.958 | 4/12 | ~890s |
| C: gen+med | MiniLM | MedCPT (alpha=0.6) | 0.694 | 0.938 | 4/12 | ~67s |
| D: CE off | MiniLM | none | 0.611 | 0.896 | 2/12 | ~70s |
| E: dual+med | MiniLM+PubMedBERT | MedCPT (alpha=0.6) | 0.694 | 0.958 | 3/12 | ~780s |

Config A chosen because: highest P@3 on 12-query benchmark, 13x faster build than Config B, wide alpha plateau (0.60-0.80).

Config C (gen embed + med CE) failed because MiniLM's candidate set doesn't contain medically relevant chunks for MedCPT CE to promote. Config E (dual-embed) failed because MiniLM's noise diluted PubMedBERT's medical signal in 3-way RRF.

### Expanded benchmark (30 queries)

The benchmark was expanded from 12 to 30 queries to reduce overfitting risk and test diverse clinical scenarios. 18 new queries span 8 categories with independently created relevance labels (searched chunk content directly, not retriever output).

Config A results on 30 queries: **P@3=0.489, MRR=0.686, Perfect=5/30**

| Category | Queries | P@3 | Notes |
|----------|---------|------|-------|
| original (dosing/treatment) | 12 | 0.750 | Strong -- keyword-heavy |
| procedural | 2 | 0.667 | |
| population_specific | 2 | 0.500 | |
| treatment_protocol | 4 | 0.417 | |
| evidence | 2 | 0.333 | |
| prevention | 2 | 0.167 | Weak |
| safety | 2 | 0.167 | Weak |
| operational | 2 | 0.167 | Weak |
| diagnostic | 2 | 0.000 | Failed |

**Key insight:** The original 12-query benchmark was biased toward drug-dosing lookups. Broader clinical queries (diagnostic, prevention, safety) need medical-domain models. Next step: retest Config B (PubMedBERT + MedCPT) on the 30-query benchmark.

## Offline query preprocessing (2026-04-10)

Before retrieval, `orchestrator._preprocess_query()` rewrites the user's query into a retrieval-optimised form. This runs entirely offline — no API calls, no internet.

**Step 1 — Strip conversational framing.** VHT workers typically describe scenarios: "A lady has vaginal bleeding" or "My child is not eating". The retriever performs better on the clinical core. A regex removes the leading subject phrase, leaving "vaginal bleeding after 28 weeks of pregnancy" for retrieval.

**Step 2 — Medical synonym expansion.** 4 term groups are expanded at query time. The original term stays; synonyms are appended only if not already present:

| Query term | Appended synonyms |
|---|---|
| bleed/bleeding | haemorrhage hemorrhage |
| vomit/vomiting | emesis nausea |
| fit/fits | convulsions seizures |
| fever | febrile pyrexia temperature |
| diarrhoea/diarrhea | loose stool |
| pregnant/pregnancy | antenatal obstetric |
| weak/weakness | lethargic |
| appendicitis | acute abdomen surgical abdomen right iliac fossa |
| stroke | cerebrovascular accident CVA weakness |
| meningitis | meningism neck stiffness |
| diabetes/diabetic | blood sugar glucose |
| tuberculosis/TB | respiratory TB |
| anaemia/anemia | haemoglobin low blood count |
| typhoid | enteric fever |
| sickle cell | sickle-cell anaemia haemolytic |
| HIV/AIDS | antiretroviral immunocompromised |
| sepsis | septicaemia bacteraemia blood poisoning |
| wound/injury/trauma | laceration abrasion cut |
| ... (4 groups total) | |

The original query is preserved for triage inference, family message, and all display text. Only the retrieval call uses the enriched form.

## No-match detection (2026-04-10)

Min-max normalisation in the cross-encoder blend always maps the best-ranked chunk to score 1.0, regardless of absolute relevance. A query completely outside the loaded guidelines (e.g. "What is the weather today?") would still return chunks with high normalised scores and generate a fabricated response.

**Fix:** The raw cross-encoder logit is captured **before** normalisation as `_ce_best_raw` on the top result chunk. CE logits are unbounded:
- Positive logit -> model believes the query and chunk are related
- Negative logit -> model believes they are unrelated

In `chat.py`, if `_ce_best_raw < -4.0`, the response is suppressed and "No matching guidelines found for this query" is displayed. The threshold is set conservatively at -4.0 rather than a tighter value because `ms-marco-MiniLM-L-6-v2` was trained on general web-search data, not medical text — a vocabulary mismatch (e.g. a query using "appendicitis" against a document that says "acute abdomen") routinely scores around -1.5 to -3, which does not mean the query is out-of-domain. Genuinely unrelated queries (weather, sports, etc.) score -5 to -8. Using -4.0 avoids false "no match" rejections for legitimate medical queries whose terminology differs from the document vocabulary. Queries scoring between -4.0 and 0 receive the response with the existing low-confidence warning. When the cross-encoder is not installed (BM25-only mode), `_ce_best_raw` is None and this check is skipped.

## Alternatives we considered

### Dense-only retrieval (rejected)

Using only embedding similarity (no BM25). We tested this and found it frequently missed exact drug name matches. A query for "primaquine dosing" would retrieve general "anti-malarial dosing" content instead of the specific primaquine table. BM25's exact keyword matching catches these cases reliably.

### BM25-only retrieval (rejected as default)

BM25 is fast and requires no model download, but it fails on semantic queries. "How should I treat a child who can't keep medicine down?" has no keyword overlap with "vomiting within 30 minutes of oral dose — repeat administration" — yet this is exactly the relevant content. Dense retrieval captures this semantic bridge.

### ChromaDB as the vector store (rejected)

ChromaDB provides a managed vector store with built-in embedding and persistence. We tested it but found that for our corpus size (3,800-4,000 chunks), FAISS `IndexFlatIP` is faster, uses less memory, and has no external process dependency. ChromaDB's advantages (persistence, filtering, multi-tenancy) don't apply to our single-document, in-memory use case.

### HNSW approximate search (rejected)

FAISS supports approximate nearest-neighbor search via HNSW or IVF indexes, which trade accuracy for speed. With only ~4,000 vectors, exact search (`IndexFlatIP`) completes in <1ms per query. There is no performance justification for approximate search at this scale.

### ColBERT / late-interaction models (rejected)

ColBERT stores per-token embeddings and computes fine-grained query-document interaction at search time. This provides better relevance than bi-encoder similarity but requires significantly more storage (384 dims x ~100 tokens per chunk vs. 384 dims x 1 embedding) and slower query time. For our corpus size and latency requirements, the bi-encoder + cross-encoder reranker achieves comparable quality at lower cost.

### Query expansion / HyDE (rejected)

Hypothetical Document Embeddings (HyDE) generates a synthetic answer to the query and uses its embedding for retrieval. This requires an LLM call per query, adding latency and cost. Our hybrid BM25 + dense approach already handles the vocabulary mismatch that HyDE addresses, without the LLM dependency.

## Parameters

| Parameter | Default | Purpose |
|---|---|---|
| `top_k_initial` | 20 | Candidates per modality before fusion |
| `top_k_fused` | 10 | Candidates after RRF before reranking |
| `rrf_k` | 60 | RRF fusion constant |
| `enable_reranking` | True | Enable cross-encoder reranking |
| `_CE_BLEND_ALPHA` | 0.6 | Weight for RRF in cross-encoder blend (1-alpha for CE) |
| `enable_metadata_reranking` | True | Enable metadata-aware boost layer |
| `drug_keywords` | From config | Drug names for query-time extraction |
| `condition_patterns` | From config | Regex->label pairs for condition matching |

## Output

The retriever returns a list of chunk dictionaries enriched with `score` (fused/reranked relevance) and `retrieval_rank` (1-based position). These feed into the [response layer](response_layer.md) for answer generation.

## Benchmark data

The retrieval benchmark artifacts are tracked in [`rag_output/`](../rag_output/):

- **[`retrieval_test_results.json`](../rag_output/retrieval_test_results.json)** — 30-query clinical benchmark (12 original + 18 expanded) with per-result relevance, rankings, source pages, and per-category breakdown
- **[`build_report.json`](../rag_output/build_report.json)** — aggregate metrics (Mean P@3 = 0.489, MRR = 0.686, Perfect P@3 = 5/30 on 30-query expanded benchmark), corpus stats, and model configuration
- **[`child_chunks.json`](../rag_output/child_chunks.json)** — all 1,695 child chunks used for retrieval
- **[`brain1_package/`](../rag_output/brain1_package/)** — mobile-ready export (24.11 MB)

See [`rag_output/README.md`](../rag_output/README.md) for the full directory guide and how to cross-reference results against the source PDFs.

See also: [Chunking strategy](chunking_strategy.md) for how chunks are prepared for retrieval.
