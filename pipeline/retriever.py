"""
Hybrid retrieval: dense (FAISS) + sparse (BM25) + RRF + optional cross-encoder
+ metadata-aware re-ranking.

Falls back gracefully to BM25-only when sentence-transformers or faiss are
not installed.

Metadata re-ranking (v2) applies four boost signals after cross-encoder
reranking, using clinical metadata already present on every chunk:

  1. Drug-name boost   — query drug names matched against chunk content/metadata
  2. Chunk-type boost  — dosing_table / NLL chunks boosted for dosing queries
  3. Condition boost   — condition field matched against query condition signals
  4. Domain boost      — clinical_domain field matched against query intent
"""

from __future__ import annotations

import re
from collections import defaultdict
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np
from rank_bm25 import BM25Okapi

# Optional heavy dependencies — graceful fallback when not installed.
try:
    from sentence_transformers import SentenceTransformer
    _SBERT_AVAILABLE = True
except ImportError:
    _SBERT_AVAILABLE = False

try:
    import faiss
    _FAISS_AVAILABLE = True
except ImportError:
    _FAISS_AVAILABLE = False

try:
    from sentence_transformers import CrossEncoder
    _CROSS_ENCODER_AVAILABLE = True
except ImportError:
    _CROSS_ENCODER_AVAILABLE = False

# MedCPT cross-encoder uses transformers directly (not sentence-transformers).
try:
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    import torch as _torch
    _TRANSFORMERS_CE_AVAILABLE = True
except ImportError:
    _TRANSFORMERS_CE_AVAILABLE = False

# ColPali visual retrieval — optional fourth tier (requires colpali-engine + torch).
# When the index is not present or colpali-engine is not installed, the retriever
# continues with BM25 + FAISS + cross-encoder as normal.
try:
    from .colpali_retriever import (
        ColPaliIndex,
        colpali_search,
        load_colpali_model,
        _COLPALI_TABLE_WEIGHT,
        _COLPALI_FIGURE_WEIGHT,
        _COLPALI_TEXT_WEIGHT,
    )
    _COLPALI_MODULE_AVAILABLE = True
except ImportError:
    _COLPALI_MODULE_AVAILABLE = False


# ---------------------------------------------------------------------------
# Default model names
# ---------------------------------------------------------------------------
# Primary embedding: general-purpose MiniLM (Apache 2.0).  Fast (22M params,
# 384-dim), strong keyword-level semantic similarity, good for table content.
# Chosen over medical models after evaluation on 12-query benchmark — see
# docs/retrieval_strategy.md § Model Evaluation for full comparison.
DEFAULT_EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Medical embedding (optional, for dual-embedding retrieval): PubMedBERT
# (Apache 2.0) trained on PubMed title-abstract pairs.  768-dim, 110M params.
# Understands medical concept relationships ("treatment failure" ↔
# "recrudescence") but 13× slower to build and didn't improve P@3 on
# current 12-query benchmark.  Set to None to disable; enable when
# validated on a larger benchmark.
MEDICAL_EMBED_MODEL = "NeuML/pubmedbert-base-embeddings"

# Cross-encoder reranker: general-purpose ms-marco (Apache 2.0).  Scores are
# alpha-blended with RRF (not replacing), preserving BM25 keyword signals.
# P@3=0.750 on current benchmark — best of all configurations tested.
DEFAULT_RERANK_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"

# Medical cross-encoder alternative: MedCPT (Public Domain), trained on 18M
# PubMed query-article pairs.  Better MRR (0.958) on conceptual queries but
# lower P@3 (0.722) overall.  Uses AutoModelForSequenceClassification.
MEDICAL_RERANK_MODEL = "ncbi/MedCPT-Cross-Encoder"
_RRF_K_DEFAULT = 60

# ---------------------------------------------------------------------------
# American → British medical spelling map (CT Health AI)
# ---------------------------------------------------------------------------
# Uganda and other Commonwealth clinical guidelines use British spelling.
# Normalising query terms before BM25/FAISS search prevents missed matches
# when users type American English (e.g. "diarrhea" vs "diarrhoea").
_BRITISH_MAP: Dict[str, str] = {
    "diarrhea": "diarrhoea",
    "diarrheal": "diarrhoeal",
    "diarrheas": "diarrhoeas",
    "anemia": "anaemia",
    "anemic": "anaemic",
    "anemias": "anaemias",
    "pediatric": "paediatric",
    "pediatrics": "paediatrics",
    "pediatrician": "paediatrician",
    "hemoglobin": "haemoglobin",
    "hemorrhage": "haemorrhage",
    "hemorrhagic": "haemorrhagic",
    "hemorrhages": "haemorrhages",
    "esophagus": "oesophagus",
    "esophageal": "oesophageal",
    "leukemia": "leukaemia",
    "leukocyte": "leucocyte",
    "leukocytes": "leucocytes",
    "feces": "faeces",
    "fecal": "faecal",
    "edema": "oedema",
    "orthopedic": "orthopaedic",
    "gynecology": "gynaecology",
    "gynecological": "gynaecological",
    "cesarean": "caesarean",
    "sulfate": "sulphate",
    "sulfur": "sulphur",
    "estrogen": "oestrogen",
}


def _normalize_medical_spelling(query: str) -> str:
    """Normalize American English medical spelling to British English.

    Applied to queries before BM25 and dense search so that US-spelled
    queries match Commonwealth-guideline content without missing results.

    Example: "treat diarrhea in children" →
             "treat diarrhoea in children"
    """
    result = query
    for us, uk in _BRITISH_MAP.items():
        # Replace whole-word occurrences (case-insensitive, preserve case structure)
        pattern = r"\b" + re.escape(us) + r"\b"
        # Lower-case replacement
        result = re.sub(pattern, uk, result, flags=re.IGNORECASE)
        # Title-case replacement (e.g. "Diarrhea" → "Diarrhoea")
        result = re.sub(
            r"\b" + re.escape(us.title()) + r"\b",
            uk.title(),
            result,
        )
    return result

# Cross-encoder blending weight.  When cross-encoder is enabled, the final
# score = alpha * norm(RRF) + (1-alpha) * norm(CE).  A value of 0.6 means
# 60% of the signal comes from the keyword/vector fusion (RRF), keeping the
# medical-terminology advantage of BM25 while still benefiting from the
# cross-encoder's semantic re-ranking.
_CE_BLEND_ALPHA = 0.6  # weight for RRF score; (1 - alpha) for cross-encoder

# ---------------------------------------------------------------------------
# Metadata re-ranking constants
# ---------------------------------------------------------------------------

# Boost multipliers applied to fused/reranked scores.  Values > 1.0 promote;
# < 1.0 demote.  Multipliers stack multiplicatively.
_DRUG_MATCH_BOOST = 1.35          # chunk mentions a drug the query asks about
_DOSING_TYPE_BOOST = 1.25         # chunk is a dosing_table for a dosing query
_NLL_BOOST = 1.15                 # chunk is an NLL child (semantic bridge to table)
_EVIDENCE_TABLE_DEMOTE = 0.85     # evidence_table for a dosing query (comparison, not prescribing)
_CONDITION_MATCH_BOOST = 1.20     # condition metadata matches query condition signal
_DOMAIN_MATCH_BOOST = 1.10        # clinical_domain matches query intent

# Dosing-intent signal words detected in the query.
_DOSING_QUERY_SIGNALS = frozenset([
    "dose", "doses", "dosing", "dosage", "mg", "mg/kg", "tablet", "tablets",
    "how much", "how many", "weight", "kg", "schedule", "regimen",
])

# Condition signal words -> canonical condition labels (used when config
# condition_patterns are not available).
_DEFAULT_CONDITION_MAP: Dict[str, str] = {
    "severe": "Severe malaria",
    "uncomplicated": "Uncomplicated malaria",
    "pregnancy": "Malaria in pregnancy",
    "pregnant": "Malaria in pregnancy",
    "vivax": "P. vivax malaria",
    "falciparum": "P. falciparum malaria",
    "prevention": "Malaria prevention",
    "chemoprevention": "Malaria chemoprevention",
    "recurrent": "Recurrent malaria",
    "diagnosis": "Malaria diagnosis",
    "vector": "Vector control",
}


def _query_has_dosing_intent(query_lower: str) -> bool:
    """Return True if the query is asking about dosing."""
    tokens = set(re.findall(r"[a-z/]+", query_lower))
    return bool(tokens & _DOSING_QUERY_SIGNALS)


def _extract_drug_names(
    query_lower: str,
    drug_keywords: Optional[Sequence[str]] = None,
) -> List[str]:
    """Extract drug name keywords present in the query."""
    if not drug_keywords:
        return []
    return [d for d in drug_keywords if d.lower() in query_lower]


def _detect_condition(
    query_lower: str,
    condition_patterns: Optional[List[List[str]]] = None,
) -> Optional[str]:
    """Return the canonical condition label if the query matches a condition pattern."""
    # Try config-provided regex patterns first.
    if condition_patterns:
        for entry in condition_patterns:
            if len(entry) >= 2:
                pattern, label = entry[0], entry[1]
                if re.search(pattern, query_lower, re.IGNORECASE):
                    return label
    # Fall back to built-in keyword map.
    for keyword, label in _DEFAULT_CONDITION_MAP.items():
        if keyword in query_lower:
            return label
    return None


def _detect_domain_keywords(query_lower: str) -> List[str]:
    """Extract domain-relevant keywords from the query for soft matching."""
    # Domain keywords that appear in clinical_domain strings.
    domain_signals = [
        "dosing", "act", "treatment", "chemoprevention", "pregnancy",
        "severe", "diagnosis", "vaccine", "vector", "prevention",
        "relapse", "vivax", "referral", "artesunate", "artemether",
        "primaquine", "quinine", "hiv", "infant", "children",
    ]
    return [kw for kw in domain_signals if kw in query_lower]


def metadata_rerank(
    scored_ids: List[Tuple[str, float]],
    id_to_chunk: Dict[str, Dict[str, Any]],
    query: str,
    *,
    drug_keywords: Optional[Sequence[str]] = None,
    condition_patterns: Optional[List[List[str]]] = None,
) -> List[Tuple[str, float]]:
    """
    Apply metadata-aware score boosts to a ranked list.

    This is a post-processing step that adjusts scores from RRF or cross-encoder
    reranking using four metadata signals.  It never removes results — only
    re-orders by adjusting scores multiplicatively.

    Parameters
    ----------
    scored_ids : ranked list of (chunk_id, score) from upstream.
    id_to_chunk : lookup from chunk_id to full chunk dict.
    query : the original user query string.
    drug_keywords : drug name list from config (e.g., config.drug_keywords).
    condition_patterns : condition regex patterns from config.

    Returns
    -------
    Re-sorted list of (chunk_id, adjusted_score).
    """
    if not scored_ids:
        return scored_ids

    ql = query.lower()
    is_dosing = _query_has_dosing_intent(ql)
    query_drugs = _extract_drug_names(ql, drug_keywords)
    query_condition = _detect_condition(ql, condition_patterns)
    query_domains = _detect_domain_keywords(ql)

    boosted: List[Tuple[str, float]] = []
    for doc_id, score in scored_ids:
        chunk = id_to_chunk.get(doc_id)
        if chunk is None:
            boosted.append((doc_id, score))
            continue

        multiplier = 1.0
        meta = chunk.get("metadata") or {}
        chunk_type = chunk.get("chunk_type", meta.get("chunk_type", ""))
        pres = chunk.get("preservation_level", meta.get("preservation_level", ""))
        condition = meta.get("condition", "") or ""
        drug_name = meta.get("drug_name", "") or ""
        domain = chunk.get("clinical_domain", "") or ""
        content_lower = chunk.get("content", "").lower()
        is_nll = chunk.get("is_nll", False)

        # --- Boost 1: Drug-name match ---
        if query_drugs:
            # Check both metadata drug_name and content for matches.
            drug_match = any(
                d.lower() in drug_name.lower() or d.lower() in content_lower
                for d in query_drugs
            )
            if drug_match:
                multiplier *= _DRUG_MATCH_BOOST

        # --- Boost 2: Chunk-type for dosing queries ---
        if is_dosing:
            if chunk_type == "dosing_table" or pres == "verbatim":
                multiplier *= _DOSING_TYPE_BOOST
            elif is_nll:
                multiplier *= _NLL_BOOST
            elif chunk_type == "evidence_table":
                multiplier *= _EVIDENCE_TABLE_DEMOTE

        # --- Boost 3: Condition match ---
        if query_condition and condition:
            if query_condition.lower() in condition.lower():
                multiplier *= _CONDITION_MATCH_BOOST

        # --- Boost 4: Clinical domain match ---
        if query_domains and domain:
            domain_lower = domain.lower()
            matched = sum(1 for kw in query_domains if kw in domain_lower)
            if matched:
                # Scale boost by fraction of matched domain keywords (max = full boost).
                frac = min(matched / max(len(query_domains), 1), 1.0)
                multiplier *= 1.0 + (_DOMAIN_MATCH_BOOST - 1.0) * frac

        boosted.append((doc_id, score * multiplier))

    return sorted(boosted, key=lambda x: x[1], reverse=True)


def reciprocal_rank_fusion(
    *ranked_lists: List[Tuple[str, float]],
    k: int = _RRF_K_DEFAULT,
) -> List[Tuple[str, float]]:
    """
    Fuse multiple ranked lists with Reciprocal Rank Fusion.

        RRF(d) = Σ  1 / (k + rank_i(d))

    Returns a new ranked list sorted by fused score descending.
    """
    rrf_scores: Dict[str, float] = defaultdict(float)
    for ranked in ranked_lists:
        for rank, (doc_id, _) in enumerate(ranked):
            rrf_scores[doc_id] += 1.0 / (k + rank + 1)
    return sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)


class HybridRetriever:
    """
    Hybrid retrieval over a flat chunk list.

    Three-signal candidate generation:
      1. BM25 (sparse)  — keyword matching, strong for exact drug names
      2. FAISS primary   — general-purpose embeddings (MiniLM, fast)
      3. FAISS medical   — biomedical embeddings (PubMedBERT, optional)

    All three ranked lists are fused via Reciprocal Rank Fusion (RRF),
    then optionally reranked by a cross-encoder (MedCPT or ms-marco)
    with alpha-blended scoring, and finally boosted by metadata signals.

    When sentence-transformers or faiss are not installed the retriever
    operates in BM25-only mode — callers can check ``dense_available``.
    """

    def __init__(
        self,
        chunks: List[Dict[str, Any]],
        *,
        embed_model_name: str = DEFAULT_EMBED_MODEL,
        medical_embed_model_name: Optional[str] = None,
        rerank_model_name: Optional[str] = DEFAULT_RERANK_MODEL,
        enable_reranking: bool = True,
        top_k_initial: int = 20,
        top_k_fused: int = 10,
        rrf_k: int = _RRF_K_DEFAULT,
        drug_keywords: Optional[Sequence[str]] = None,
        condition_patterns: Optional[List[List[str]]] = None,
        enable_metadata_reranking: bool = True,
        colpali_index: Optional[Any] = None,
    ):
        self.chunks = chunks
        self.top_k_initial = top_k_initial
        self.top_k_fused = top_k_fused
        self.rrf_k = rrf_k
        self._drug_keywords = list(drug_keywords) if drug_keywords else []
        self._condition_patterns = condition_patterns or []
        self._enable_metadata_reranking = enable_metadata_reranking

        # Sparse index — always built (None when corpus is empty).
        self._corpus_tokens: List[List[str]]
        self._bm25: Optional[BM25Okapi]
        self._corpus_tokens, self._bm25 = self._build_bm25(chunks)

        # Primary dense index (general-purpose — fast, good at keyword-like
        # semantic similarity and table content).
        self._embed_model: Optional[Any] = None
        self._faiss_index: Optional[Any] = None
        if _SBERT_AVAILABLE and _FAISS_AVAILABLE:
            self._embed_model = SentenceTransformer(embed_model_name)
            self._faiss_index = self._build_faiss(chunks, self._embed_model)

        # Medical dense index (biomedical embeddings — understands medical
        # concept relationships like "treatment failure" ↔ "recrudescence").
        # Optional: set medical_embed_model_name=None to disable.
        self._medical_embed_model: Optional[Any] = None
        self._medical_faiss_index: Optional[Any] = None
        if (
            _SBERT_AVAILABLE
            and _FAISS_AVAILABLE
            and medical_embed_model_name
            and medical_embed_model_name != embed_model_name
        ):
            self._medical_embed_model = SentenceTransformer(
                medical_embed_model_name
            )
            self._medical_faiss_index = self._build_faiss(
                chunks, self._medical_embed_model
            )

        # ColPali visual retrieval — optional fourth tier.
        # When colpali_index is provided, ColPali MaxSim scores are included in
        # RRF fusion alongside BM25 and FAISS.  Pages containing tables receive
        # 2× weight; figure pages 1.5×; text-only pages 0.3× (noise suppression).
        # If colpali-engine / torch are not installed, this tier is silently skipped.
        self._colpali_index: Optional[Any] = colpali_index
        self._colpali_model: Optional[Any] = None
        self._colpali_processor: Optional[Any] = None
        self._colpali_device: Optional[Any] = None
        if colpali_index is not None and _COLPALI_MODULE_AVAILABLE:
            try:
                (
                    self._colpali_model,
                    self._colpali_processor,
                    self._colpali_device,
                ) = load_colpali_model(colpali_index.model_name)
            except Exception as _e:
                import logging as _logging
                _logging.getLogger(__name__).warning(
                    "ColPali model failed to load — visual retrieval disabled: %s", _e
                )

        # Cross-encoder reranker — enabled by default.  Scores are blended
        # with RRF (alpha-weighted) rather than replacing them, so medical-
        # keyword signals from BM25 are preserved.
        #
        # Supports two backends:
        #   1. MedCPT (ncbi/MedCPT-Cross-Encoder) — uses transformers
        #      AutoModelForSequenceClassification.  Preferred for medical.
        #   2. sentence-transformers CrossEncoder — for ms-marco or other
        #      general-purpose models.
        self._reranker: Optional[Any] = None
        self._reranker_tokenizer: Optional[Any] = None  # only for MedCPT
        self._reranker_is_medcpt: bool = False
        if enable_reranking and rerank_model_name:
            self._reranker = self._load_cross_encoder(rerank_model_name)

    # ------------------------------------------------------------------
    # Cross-encoder loading
    # ------------------------------------------------------------------

    def _load_cross_encoder(self, model_name: str) -> Optional[Any]:
        """Load a cross-encoder, trying MedCPT (transformers) first, then
        sentence-transformers CrossEncoder as fallback."""
        # Try MedCPT-style (AutoModelForSequenceClassification).
        if _TRANSFORMERS_CE_AVAILABLE and "MedCPT" in model_name:
            try:
                self._reranker_tokenizer = AutoTokenizer.from_pretrained(model_name)
                model = AutoModelForSequenceClassification.from_pretrained(
                    model_name, use_safetensors=True
                )
                model.eval()
                self._reranker_is_medcpt = True
                return model
            except Exception:
                pass  # fall through to sentence-transformers

        # Try sentence-transformers CrossEncoder (works for ms-marco etc.).
        if _CROSS_ENCODER_AVAILABLE:
            try:
                return CrossEncoder(model_name)
            except Exception:
                pass

        return None  # non-fatal — fall back to no reranking

    def _predict_cross_encoder(
        self, pairs: List[Tuple[str, str]]
    ) -> List[float]:
        """Score (query, passage) pairs with whichever cross-encoder is loaded."""
        if self._reranker_is_medcpt:
            # MedCPT uses transformers AutoModelForSequenceClassification.
            scores: List[float] = []
            with _torch.no_grad():
                for q, p in pairs:
                    inputs = self._reranker_tokenizer(
                        q, p, return_tensors="pt",
                        truncation=True, max_length=512, padding=True,
                    )
                    outputs = self._reranker(**inputs)
                    scores.append(outputs.logits.squeeze().item())
            return scores
        else:
            # sentence-transformers CrossEncoder.
            return [float(s) for s in self._reranker.predict(pairs)]

    # ------------------------------------------------------------------
    # Index-building helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _chunk_text(chunk: Dict[str, Any]) -> str:
        """
        Return the text to index/embed for a chunk, with heading weighting.

        Heading weighting (CT Health AI pattern):
          Level-1 headings (chapters) are repeated 5× in the BM25 corpus.
          Level-2 headings (topics) are repeated 3×.
          Level-3 headings (subsections) are repeated 2×.
        This ensures disease/chapter names dominate BM25 scoring for
        section-specific queries (e.g. "malaria treatment" → malaria chapter)
        without drowning out keyword signals in the content.

        Child chunks carry ``contextual_content`` (metadata header prepended) —
        that header already contains the heading once; we prepend extra
        repetitions so the total weighting still reflects the level hierarchy.

        Parent chunks fall back to: weighted_heading + text + table NLL.
        """
        heading = chunk.get("heading", "")
        level = chunk.get("level", 2)
        # Weight: level-1 → 5×, level-2 → 3×, level-3 → 2×
        heading_reps = {1: 5, 2: 3, 3: 2}.get(int(level) if level else 2, 2)

        cc = chunk.get("contextual_content", "")
        if cc:
            # contextual_content already contains the heading once in its
            # "[Context: heading | ...]" prefix.  Prepend (heading_reps - 1)
            # additional repetitions so the net weight equals heading_reps.
            extra_reps = max(0, heading_reps - 1)
            prefix = (heading + " ") * extra_reps if heading and extra_reps else ""
            return prefix + cc

        # Parent chunk: weighted heading + body text + table NLL
        heading_prefix = (heading + " ") * heading_reps if heading else ""
        parts = [heading_prefix, chunk.get("text", "")]
        for t in chunk.get("tables", []):
            nll = t.get("nll", "")
            if nll:
                parts.append(nll)
        return " ".join(p for p in parts if p)

    @staticmethod
    def _build_bm25(
        chunks: List[Dict[str, Any]],
    ) -> Tuple[List[List[str]], Optional[BM25Okapi]]:
        corpus_tokens: List[List[str]] = []
        for chunk in chunks:
            text = HybridRetriever._chunk_text(chunk).lower()
            tokens = [t for t in re.findall(r"[a-zA-Z0-9]+", text) if len(t) > 1]
            corpus_tokens.append(tokens)
        if not corpus_tokens:
            return corpus_tokens, None
        return corpus_tokens, BM25Okapi(corpus_tokens)

    @staticmethod
    def _build_faiss(
        chunks: List[Dict[str, Any]],
        embed_model: Any,
    ) -> Any:
        texts = [HybridRetriever._chunk_text(c) for c in chunks]
        embeddings = embed_model.encode(
            texts,
            batch_size=32,
            normalize_embeddings=True,
            show_progress_bar=False,
        ).astype(np.float32)
        if embeddings.ndim < 2 or embeddings.shape[0] == 0:
            # Empty chunk list: build a zero-vector index with the model's dimension
            d = embed_model.get_sentence_embedding_dimension() or 768
            index = faiss.IndexFlatIP(d)
            return index
        d = embeddings.shape[1]
        index = faiss.IndexFlatIP(d)
        index.add(embeddings)
        return index

    # ------------------------------------------------------------------
    # Single-modality search
    # ------------------------------------------------------------------

    def _search_faiss(
        self,
        query: str,
        k: int,
        model: Any,
        index: Any,
    ) -> List[Tuple[str, float]]:
        """Search a single FAISS index with the given embedding model."""
        if model is None or index is None:
            return []
        q_emb = model.encode(
            [query], normalize_embeddings=True, show_progress_bar=False
        ).astype(np.float32)
        n = min(k, index.ntotal)
        scores, indices = index.search(q_emb, n)
        return [
            (self.chunks[int(idx)]["chunk_id"], float(score))
            for score, idx in zip(scores[0], indices[0])
            if idx >= 0
        ]

    def _search_dense(self, query: str, k: int) -> List[Tuple[str, float]]:
        """Primary dense search (general-purpose embeddings)."""
        return self._search_faiss(
            query, k, self._embed_model, self._faiss_index
        )

    def _search_medical_dense(self, query: str, k: int) -> List[Tuple[str, float]]:
        """Medical dense search (biomedical embeddings)."""
        return self._search_faiss(
            query, k, self._medical_embed_model, self._medical_faiss_index
        )

    def _search_bm25(self, query: str, k: int) -> List[Tuple[str, float]]:
        if self._bm25 is None or not self.chunks:
            return []
        tokens = [
            t for t in re.findall(r"[a-zA-Z0-9]+", query.lower()) if len(t) > 1
        ]
        scores = self._bm25.get_scores(tokens)
        top_indices = np.argsort(scores)[::-1][:k]
        # Include all top-k results regardless of score — BM25 already ranks by
        # relevance; the caller's k limit handles the rest.  Filtering > 0 would
        # silently drop results when the IDF formula returns 0 for common terms
        # in small corpora (a known artefact of some rank_bm25 versions).
        return [
            (self.chunks[int(i)]["chunk_id"], float(scores[i]))
            for i in top_indices
        ]

    # ------------------------------------------------------------------
    # Public retrieval
    # ------------------------------------------------------------------

    def retrieve(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """
        Return up to k chunks ranked by hybrid score.

        Each returned chunk dict is a shallow copy of the original with two
        extra fields added:
          score          — fused (or reranked) relevance score
          retrieval_rank — 1-based rank in this result set
        """
        k_init = max(k, self.top_k_initial)
        id_to_chunk = {c["chunk_id"]: c for c in self.chunks}

        # Normalize American → British medical spelling before all searches.
        # This ensures queries like "diarrhea treatment" match passages that
        # use "diarrhoea" (Commonwealth guidelines).
        query = _normalize_medical_spelling(query)

        dense = self._search_dense(query, k_init)
        medical_dense = self._search_medical_dense(query, k_init)
        sparse = self._search_bm25(query, k_init)

        # ColPali visual retrieval tier — fourth signal in RRF fusion.
        # Catches dosing tables and clinical figures that are rendered as images
        # (invisible to BM25 and FAISS).  Content-aware weighting: table pages
        # 2×, figure pages 1.5×, text-only pages 0.3× (suppresses noise).
        colpali_ranked: List[Tuple[str, float]] = []
        if self._colpali_model is not None and self._colpali_index is not None:
            try:
                page_results = colpali_search(
                    query,
                    self._colpali_model,
                    self._colpali_processor,
                    self._colpali_device,
                    self._colpali_index,
                    top_k=k_init,
                )
                seen_cids: set = set()
                for pr in page_results:
                    if pr["has_tables"]:
                        w = _COLPALI_TABLE_WEIGHT
                    elif pr["has_figures"]:
                        w = _COLPALI_FIGURE_WEIGHT
                    else:
                        w = _COLPALI_TEXT_WEIGHT
                    for cid in pr["chunk_ids"]:
                        if cid not in seen_cids:
                            seen_cids.add(cid)
                            colpali_ranked.append((cid, pr["colpali_score"] * w))
                colpali_ranked.sort(key=lambda x: x[1], reverse=True)
            except Exception as _e:
                import logging as _logging
                _logging.getLogger(__name__).warning(
                    "ColPali search failed — text-only retrieval used: %s", _e
                )

        # Fuse all available ranked lists via RRF.  With dual embeddings and
        # ColPali we have up to 4 signals: BM25 + general FAISS + medical FAISS
        # + ColPali visual.  This widens the candidate pool so the cross-encoder
        # can see keyword-matched, concept-matched, and visually-matched chunks.
        ranked_lists = [r for r in (dense, medical_dense, sparse, colpali_ranked) if r]
        if len(ranked_lists) >= 2:
            fused: List[Tuple[str, float]] = reciprocal_rank_fusion(
                *ranked_lists, k=self.rrf_k
            )
        elif ranked_lists:
            fused = ranked_lists[0]
        else:
            fused = []

        fused = fused[: self.top_k_fused]

        # Optional cross-encoder reranking (blended with RRF scores).
        # Instead of fully replacing the RRF scores, we normalise both the
        # RRF and cross-encoder scores to [0, 1] and blend them:
        #   blended = alpha * norm(RRF) + (1 - alpha) * norm(CE)
        # This preserves medical-keyword signals from BM25/RRF while still
        # benefiting from the cross-encoder's semantic understanding.
        if self._reranker and fused:
            rrf_lookup: Dict[str, float] = {doc_id: s for doc_id, s in fused}
            valid_ids: List[str] = []
            pairs: List[Tuple[str, str]] = []
            for doc_id, _ in fused:
                chunk = id_to_chunk.get(doc_id)
                if chunk:
                    pairs.append((query, HybridRetriever._chunk_text(chunk)[:512]))
                    valid_ids.append(doc_id)
            if pairs:
                raw_ce = self._predict_cross_encoder(pairs)

                # Store the best absolute CE logit BEFORE normalization.
                # CE logits are unbounded: positive = relevant, negative = not
                # relevant.  This value is attached to the first result chunk as
                # "_ce_best_raw" so callers can detect "no match" queries where
                # ALL chunks score negatively (the normalised scores are useless
                # for this purpose because min-max normalisation always maps the
                # best chunk to 1.0 regardless of absolute relevance).
                _ce_best_raw = max(raw_ce)

                # Min-max normalise RRF scores for valid IDs.
                rrf_vals = [rrf_lookup[d] for d in valid_ids]
                rrf_min, rrf_max = min(rrf_vals), max(rrf_vals)
                rrf_range = rrf_max - rrf_min if rrf_max > rrf_min else 1.0

                # Min-max normalise cross-encoder scores.
                ce_min, ce_max = min(raw_ce), max(raw_ce)
                ce_range = ce_max - ce_min if ce_max > ce_min else 1.0

                alpha = _CE_BLEND_ALPHA
                blended: List[Tuple[str, float]] = []
                for doc_id, rrf_s, ce_s in zip(valid_ids, rrf_vals, raw_ce):
                    norm_rrf = (rrf_s - rrf_min) / rrf_range
                    norm_ce = (ce_s - ce_min) / ce_range
                    blended.append((doc_id, alpha * norm_rrf + (1 - alpha) * norm_ce))

                fused = sorted(blended, key=lambda x: x[1], reverse=True)
            else:
                _ce_best_raw = None

        # Metadata-aware re-ranking — applies four boost signals using
        # clinical metadata already present on each chunk.
        if self._enable_metadata_reranking and fused:
            fused = metadata_rerank(
                fused,
                id_to_chunk,
                query,
                drug_keywords=self._drug_keywords,
                condition_patterns=self._condition_patterns,
            )

        # Assemble final result list.
        results: List[Dict[str, Any]] = []
        seen: set = set()
        for doc_id, score in fused[:k]:
            if doc_id in seen:
                continue
            seen.add(doc_id)
            chunk = id_to_chunk.get(doc_id)
            if chunk:
                out = dict(chunk)
                out["score"] = float(score)
                out["retrieval_rank"] = len(results) + 1
                results.append(out)

        # Attach the absolute CE relevance to the top result so the caller
        # can run a "no match" check without rerunning the cross-encoder.
        if results and self._reranker:
            results[0]["_ce_best_raw"] = _ce_best_raw

        return results

    # ------------------------------------------------------------------
    # Capability flags
    # ------------------------------------------------------------------

    @property
    def colpali_available(self) -> bool:
        """True when a ColPali visual index is loaded and the model is ready."""
        return self._colpali_model is not None

    @property
    def dense_available(self) -> bool:
        """True when primary FAISS + sentence-transformers are installed and indexed."""
        return self._faiss_index is not None

    @property
    def medical_dense_available(self) -> bool:
        """True when the medical (PubMedBERT) FAISS index is built."""
        return self._medical_faiss_index is not None

    @property
    def reranking_available(self) -> bool:
        """True when a cross-encoder reranker is loaded."""
        return self._reranker is not None

    @property
    def metadata_reranking_enabled(self) -> bool:
        """True when metadata-aware re-ranking is active."""
        return self._enable_metadata_reranking
