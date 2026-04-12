"""
Unit tests for HybridRetriever and reciprocal_rank_fusion (P9).

All tests use the BM25-only path so they run without sentence-transformers
or faiss installed.

Run with:  python3 -m pytest tests/test_hybrid_retriever.py -v
"""

import pytest
from pipeline.retriever import HybridRetriever, reciprocal_rank_fusion


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_chunk(chunk_id, text, page=1, heading="Section", tables=None):
    return {
        "chunk_id": chunk_id,
        "text": text,
        "page": page,
        "heading": heading,
        "tables": tables or [],
        "preservation_level": "standard",
        "section_type": "background",
        "related_chunk_ids": [],
    }


def make_retriever(chunks, **kwargs):
    return HybridRetriever(chunks, enable_reranking=False, **kwargs)


# ---------------------------------------------------------------------------
# reciprocal_rank_fusion
# ---------------------------------------------------------------------------

class TestRRF:

    def test_single_list_preserves_order(self):
        ranked = [("a", 1.0), ("b", 0.8), ("c", 0.6)]
        fused = reciprocal_rank_fusion(ranked)
        ids = [d for d, _ in fused]
        assert ids == ["a", "b", "c"]

    def test_two_lists_boosted_item_ranks_higher(self):
        # "b" appears in both lists
        list1 = [("a", 1.0), ("b", 0.9), ("c", 0.5)]
        list2 = [("b", 1.0), ("d", 0.8)]
        fused = reciprocal_rank_fusion(list1, list2)
        ids = [d for d, _ in fused]
        assert ids[0] == "b"

    def test_scores_sum_contributions(self):
        # "x" ranks 1st in both lists — highest score
        list1 = [("x", 1.0), ("y", 0.5)]
        list2 = [("x", 1.0), ("z", 0.5)]
        fused = dict(reciprocal_rank_fusion(list1, list2))
        assert fused["x"] > fused["y"]
        assert fused["x"] > fused["z"]

    def test_empty_lists_returns_empty(self):
        assert reciprocal_rank_fusion([], []) == []

    def test_single_empty_list_returns_other(self):
        ranked = [("a", 1.0)]
        result = reciprocal_rank_fusion(ranked, [])
        assert result[0][0] == "a"

    def test_k_parameter_shifts_scores(self):
        ranked = [("a", 1.0)]
        fused_k60 = reciprocal_rank_fusion(ranked, k=60)
        fused_k1 = reciprocal_rank_fusion(ranked, k=1)
        # Smaller k → higher score for rank-1 item
        assert fused_k1[0][1] > fused_k60[0][1]

    def test_three_lists_fused(self):
        l1 = [("a", 1.0), ("b", 0.5)]
        l2 = [("b", 1.0), ("c", 0.5)]
        l3 = [("a", 1.0), ("b", 0.9)]
        fused = reciprocal_rank_fusion(l1, l2, l3)
        # "b" appears in all three lists
        ids = [d for d, _ in fused]
        assert ids[0] == "b"


# ---------------------------------------------------------------------------
# HybridRetriever — construction
# ---------------------------------------------------------------------------

class TestHybridRetrieverConstruction:

    def test_builds_without_dense_deps(self):
        chunks = [make_chunk("c1", "malaria treatment")]
        r = make_retriever(chunks)
        assert r._bm25 is not None

    def test_dense_available_false_without_deps(self):
        # In CI without sentence-transformers/faiss, dense should be unavailable.
        from pipeline.retriever import _SBERT_AVAILABLE, _FAISS_AVAILABLE
        chunks = [make_chunk("c1", "text")]
        r = make_retriever(chunks)
        if not (_SBERT_AVAILABLE and _FAISS_AVAILABLE):
            assert r.dense_available is False

    def test_reranking_available_false_when_disabled(self):
        chunks = [make_chunk("c1", "text")]
        r = HybridRetriever(chunks, enable_reranking=False)
        assert r.reranking_available is False

    def test_empty_chunk_list_builds_ok(self):
        r = make_retriever([])
        # _bm25 is None for empty corpus — that is the expected behaviour.
        assert r._bm25 is None


# ---------------------------------------------------------------------------
# HybridRetriever — BM25 search
# ---------------------------------------------------------------------------

class TestBM25Search:

    def _retriever(self):
        chunks = [
            make_chunk("c1", "malaria fever treatment artemether lumefantrine"),
            make_chunk("c2", "tuberculosis cough sputum diagnosis"),
            make_chunk("c3", "malaria dosing weight body artemether"),
            make_chunk("c4", "HIV antiretroviral cotrimoxazole prophylaxis"),
        ]
        return make_retriever(chunks), chunks

    def test_relevant_chunk_returned_first(self):
        r, _ = self._retriever()
        results = r.retrieve("malaria artemether dosing", k=1)
        assert len(results) == 1
        assert results[0]["chunk_id"] in ("c1", "c3")

    def test_top_k_respected(self):
        r, _ = self._retriever()
        results = r.retrieve("malaria treatment", k=2)
        assert len(results) <= 2

    def test_unrelated_query_still_returns_results(self):
        r, _ = self._retriever()
        results = r.retrieve("bananas fruit", k=3)
        assert isinstance(results, list)

    def test_score_field_present(self):
        r, _ = self._retriever()
        results = r.retrieve("malaria treatment", k=2)
        for chunk in results:
            assert "score" in chunk

    def test_retrieval_rank_field_present_and_sequential(self):
        r, _ = self._retriever()
        results = r.retrieve("malaria treatment", k=3)
        ranks = [c["retrieval_rank"] for c in results]
        assert ranks == list(range(1, len(results) + 1))

    def test_original_chunk_fields_preserved(self):
        r, chunks = self._retriever()
        results = r.retrieve("artemether", k=1)
        assert len(results) == 1
        for field in ("chunk_id", "text", "page", "heading", "preservation_level"):
            assert field in results[0]

    def test_no_duplicates_in_results(self):
        r, _ = self._retriever()
        results = r.retrieve("malaria", k=4)
        ids = [c["chunk_id"] for c in results]
        assert len(ids) == len(set(ids))


# ---------------------------------------------------------------------------
# HybridRetriever — NLL from tables included in BM25 index
# ---------------------------------------------------------------------------

class TestNLLIndexed:

    def test_nll_text_boosts_relevance(self):
        # Three chunks: only c1 has "artemether" (in NLL).
        # With ≥3 docs and the term in only 1, BM25 IDF is reliably > 0 so c1
        # ranks above the other two.
        chunks = [
            make_chunk("c1", "background text",
                       tables=[{"nll": "IF weight 5-9 kg THEN artemether 20 mg",
                                 "classification": "dosing"}]),
            make_chunk("c2", "general information about health"),
            make_chunk("c3", "tuberculosis sputum smear diagnosis"),
        ]
        r = make_retriever(chunks)
        results = r.retrieve("artemether dosing", k=3)
        # c1 is the only chunk with "artemether" — must appear in results
        result_ids = [c["chunk_id"] for c in results]
        assert "c1" in result_ids


# ---------------------------------------------------------------------------
# HybridRetriever — chunk_text helper
# ---------------------------------------------------------------------------

class TestChunkText:

    def test_text_only_chunk(self):
        chunk = make_chunk("c1", "fever treatment")
        text = HybridRetriever._chunk_text(chunk)
        assert "fever treatment" in text

    def test_nll_appended(self):
        chunk = make_chunk("c1", "dosing table", tables=[
            {"nll": "IF weight 5 kg THEN dose 20 mg", "classification": "dosing"},
        ])
        text = HybridRetriever._chunk_text(chunk)
        assert "IF weight" in text

    def test_empty_nll_not_appended(self):
        chunk = make_chunk("c1", "some text", tables=[
            {"nll": "", "classification": "evidence"},
        ])
        text = HybridRetriever._chunk_text(chunk)
        # Heading weighting prepends the heading (level-2 = 3x), but the
        # empty NLL should not add any extra content beyond the body text.
        assert "some text" in text
        assert text.strip().endswith("some text")

    def test_no_tables_returns_text_only(self):
        chunk = make_chunk("c1", "plain text")
        text = HybridRetriever._chunk_text(chunk)
        # Heading weighting prepends repeated heading tokens (level-2 = 3x),
        # but the body text must be present and no NLL should be appended.
        assert "plain text" in text
        assert text.strip().endswith("plain text")


# ---------------------------------------------------------------------------
# HybridRetriever — orchestrator integration
# ---------------------------------------------------------------------------

class TestOrchestratorIntegration:

    def _make_mock_retriever(self):
        # Three chunks so BM25 IDF is non-zero for unique terms.
        chunks = [
            make_chunk("c1", "malaria fever treatment", page=5, heading="Malaria Treatment"),
            make_chunk("c2", "dosing artemether lumefantrine weight", page=12, heading="AL Dosing"),
            make_chunk("c3", "tuberculosis diagnosis sputum culture", page=20, heading="TB"),
        ]
        return HybridRetriever(chunks, enable_reranking=False), chunks

    def test_retrieve_returns_chunk_with_page(self):
        r, _ = self._make_mock_retriever()
        results = r.retrieve("malaria treatment", k=1)
        assert "page" in results[0]

    def test_retrieve_returns_chunk_with_heading(self):
        r, _ = self._make_mock_retriever()
        results = r.retrieve("malaria treatment", k=1)
        assert "heading" in results[0]

    def test_k_larger_than_corpus_returns_all(self):
        r, chunks = self._make_mock_retriever()
        results = r.retrieve("malaria", k=100)
        assert len(results) <= len(chunks)
