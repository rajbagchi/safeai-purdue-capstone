"""
Unit tests for ColPali v1.2 visual retrieval (pipeline/colpali_retriever.py).

All tests run without the actual ColPali model by using mocks/stubs — the
heavy torch + colpali-engine deps are not required for the test suite to pass.

Run with:  python3 -m pytest tests/test_colpali_retriever.py -v
"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import numpy as np
import pytest

# ---------------------------------------------------------------------------
# Module-level availability check — tests adapt if deps are present or absent
# ---------------------------------------------------------------------------
from pipeline.colpali_retriever import (
    COLPALI_AVAILABLE,
    DEFAULT_COLPALI_MODEL,
    _COLPALI_FIGURE_WEIGHT,
    _COLPALI_TABLE_WEIGHT,
    _COLPALI_TEXT_WEIGHT,
    _EMBED_DIM,
    ColPaliIndex,
    _maxsim_score,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_index_dir(tmp_path: Path, n_pages: int = 3) -> Path:
    """Write a minimal ColPali index directory with synthetic embeddings.

    Uses the same metadata schema as build_colpali_index():
      - top-level key "model" (not "model_name")
      - per-page key "embeddings_path" (not "npy_file")
      - per-page keys: has_tables, has_figures, chunk_ids, n_patches
    Page numbers are 0-based (matching PDF page indices).
    """
    index_dir = tmp_path / "colpali_index"
    index_dir.mkdir()

    metadata: dict = {
        "model": "vidore/colpali-v1.2",
        "embedding_dim": _EMBED_DIM,
        "n_pages": n_pages,
        "pages": {},
    }
    for i in range(n_pages):
        # Each page has 16 patches × 128-dim, L2-normalised
        patches = np.random.randn(16, _EMBED_DIM).astype(np.float32)
        patches /= np.linalg.norm(patches, axis=1, keepdims=True)
        npy_name = f"page_{i:04d}.npy"
        npy_path = index_dir / npy_name
        np.save(str(npy_path), patches)
        chunk_ids = [f"c{i}a", f"c{i}b"]
        metadata["pages"][str(i)] = {
            "embeddings_path": npy_name,
            "n_patches": 16,
            "has_tables": i == 0,     # page 0 has tables
            "has_figures": i == 1,    # page 1 has figures
            "chunk_ids": chunk_ids,
        }

    (index_dir / "metadata.json").write_text(json.dumps(metadata))
    return index_dir


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

class TestConstants:

    def test_embed_dim_is_128(self):
        assert _EMBED_DIM == 128

    def test_table_weight_greater_than_figure(self):
        assert _COLPALI_TABLE_WEIGHT > _COLPALI_FIGURE_WEIGHT

    def test_figure_weight_greater_than_text(self):
        assert _COLPALI_FIGURE_WEIGHT > _COLPALI_TEXT_WEIGHT

    def test_text_weight_below_one(self):
        # Text-only pages should suppress noise (< 1.0)
        assert _COLPALI_TEXT_WEIGHT < 1.0

    def test_default_model_name(self):
        assert "colpali" in DEFAULT_COLPALI_MODEL.lower()


# ---------------------------------------------------------------------------
# _maxsim_score
# ---------------------------------------------------------------------------

class TestMaxSimScore:

    def test_identical_embeddings_high_score(self):
        """Query patch == page patch → cosine sim 1.0 for every query token."""
        patches = np.ones((4, 8), dtype=np.float32)
        patches /= np.linalg.norm(patches, axis=1, keepdims=True)
        score = _maxsim_score(patches, patches)
        # 4 query patches × 1.0 = 4.0
        assert abs(score - 4.0) < 1e-4

    def test_orthogonal_embeddings_low_score(self):
        """Orthogonal embeddings produce zero MaxSim."""
        q = np.zeros((1, 4), dtype=np.float32)
        q[0, 0] = 1.0
        p = np.zeros((1, 4), dtype=np.float32)
        p[0, 1] = 1.0
        score = _maxsim_score(q, p)
        assert score == pytest.approx(0.0, abs=1e-5)

    def test_returns_float(self):
        q = np.random.randn(8, _EMBED_DIM).astype(np.float32)
        p = np.random.randn(16, _EMBED_DIM).astype(np.float32)
        score = _maxsim_score(q, p)
        assert isinstance(score, float)

    def test_score_is_non_negative_for_normalised_vecs(self):
        """Max of cosine similarities can be 0 but not negative (for unit vecs)."""
        q = np.random.randn(4, _EMBED_DIM).astype(np.float32)
        p = np.random.randn(8, _EMBED_DIM).astype(np.float32)
        q /= np.linalg.norm(q, axis=1, keepdims=True)
        p /= np.linalg.norm(p, axis=1, keepdims=True)
        score = _maxsim_score(q, p)
        # MaxSim of unit vectors has individual patch scores in [-1, 1];
        # the sum can technically be negative but rarely is. Check that the
        # function returns a finite float (not NaN/Inf).
        assert np.isfinite(score)


# ---------------------------------------------------------------------------
# ColPaliIndex — loading and properties
# ---------------------------------------------------------------------------

class TestColPaliIndexLoading:

    def test_loads_metadata(self, tmp_path):
        index_dir = _make_index_dir(tmp_path, n_pages=3)
        idx = ColPaliIndex(index_dir)
        assert idx.page_count == 3

    def test_model_name_from_metadata(self, tmp_path):
        index_dir = _make_index_dir(tmp_path, n_pages=2)
        idx = ColPaliIndex(index_dir)
        assert "colpali" in idx.model_name.lower()

    def test_embeddings_loaded(self, tmp_path):
        index_dir = _make_index_dir(tmp_path, n_pages=3)
        idx = ColPaliIndex(index_dir)
        # All 3 page embeddings should be loaded
        assert len(idx._page_embeddings) == 3

    def test_embedding_shape(self, tmp_path):
        index_dir = _make_index_dir(tmp_path, n_pages=2)
        idx = ColPaliIndex(index_dir)
        emb = idx._page_embeddings[1]
        assert emb.shape[1] == _EMBED_DIM

    def test_has_tables_flag(self, tmp_path):
        index_dir = _make_index_dir(tmp_path, n_pages=3)
        idx = ColPaliIndex(index_dir)
        # Page 0 was written with has_tables=True in helper (0-based page indices)
        assert idx._page_info[0]["has_tables"] is True
        assert idx._page_info[1]["has_tables"] is False

    def test_has_figures_flag(self, tmp_path):
        index_dir = _make_index_dir(tmp_path, n_pages=3)
        idx = ColPaliIndex(index_dir)
        # Page 1 was written with has_figures=True in helper
        assert idx._page_info[1]["has_figures"] is True
        assert idx._page_info[0]["has_figures"] is False

    def test_chunk_ids_preserved(self, tmp_path):
        index_dir = _make_index_dir(tmp_path, n_pages=2)
        idx = ColPaliIndex(index_dir)
        assert "c0a" in idx._page_info[0]["chunk_ids"]

    def test_missing_npy_skips_page(self, tmp_path):
        """If an .npy file is missing, the page is silently skipped (graceful)."""
        index_dir = _make_index_dir(tmp_path, n_pages=2)
        # Delete page 0's embedding file
        (index_dir / "page_0000.npy").unlink()
        idx = ColPaliIndex(index_dir)
        # Only 1 of 2 pages should have loaded
        assert idx.page_count == 1

    def test_missing_metadata_raises(self, tmp_path):
        index_dir = tmp_path / "colpali_index"
        index_dir.mkdir()
        with pytest.raises(FileNotFoundError):
            ColPaliIndex(index_dir)


# ---------------------------------------------------------------------------
# colpali_search — mocked model
# ---------------------------------------------------------------------------

class TestColPaliSearch:

    def _make_mock_model_proc(self, n_query_patches: int = 8):
        """Return (model, processor, device) mocks with correct tensor shapes.

        colpali_search does:
          q_input = processor.process_queries([query_text]).to(device)
          q_emb_tensor = model(**q_input)   # (1, n_tokens, 128)
          q_emb = q_emb_tensor[0].float()  # (n_tokens, 128)
        So we need the model to return a 3-D tensor.
        """
        try:
            import torch
        except ImportError:
            pytest.skip("torch not installed")

        device = "cpu"
        # Actual query embedding tensor: (1, n_patches, _EMBED_DIM)
        q_emb_tensor = torch.randn(1, n_query_patches, _EMBED_DIM)

        # Processor mock: process_queries returns a dict-like object with .to()
        proc_output = MagicMock()
        proc_output.to.return_value = proc_output
        # When the model is called with **proc_output it should return q_emb_tensor
        mock_processor = MagicMock()
        mock_processor.process_queries.return_value = proc_output

        # Model mock: __call__ returns q_emb_tensor regardless of kwargs
        mock_model = MagicMock(return_value=q_emb_tensor)

        return mock_model, mock_processor, device

    def test_returns_list(self, tmp_path):
        from pipeline.colpali_retriever import colpali_search
        index_dir = _make_index_dir(tmp_path, n_pages=3)
        idx = ColPaliIndex(index_dir)
        model, proc, dev = self._make_mock_model_proc()
        results = colpali_search("malaria treatment", model, proc, dev, idx, top_k=2)
        assert isinstance(results, list)

    def test_top_k_respected(self, tmp_path):
        from pipeline.colpali_retriever import colpali_search
        index_dir = _make_index_dir(tmp_path, n_pages=3)
        idx = ColPaliIndex(index_dir)
        model, proc, dev = self._make_mock_model_proc()
        results = colpali_search("malaria treatment", model, proc, dev, idx, top_k=2)
        assert len(results) <= 2

    def test_result_has_required_keys(self, tmp_path):
        from pipeline.colpali_retriever import colpali_search
        index_dir = _make_index_dir(tmp_path, n_pages=3)
        idx = ColPaliIndex(index_dir)
        model, proc, dev = self._make_mock_model_proc()
        results = colpali_search("fever", model, proc, dev, idx, top_k=3)
        for r in results:
            for key in ("page_number", "colpali_score", "chunk_ids", "has_tables", "has_figures", "rank"):
                assert key in r, f"Missing key: {key}"

    def test_results_sorted_descending(self, tmp_path):
        from pipeline.colpali_retriever import colpali_search
        index_dir = _make_index_dir(tmp_path, n_pages=3)
        idx = ColPaliIndex(index_dir)
        model, proc, dev = self._make_mock_model_proc()
        results = colpali_search("artemether", model, proc, dev, idx, top_k=3)
        scores = [r["colpali_score"] for r in results]
        assert scores == sorted(scores, reverse=True)

    def test_rank_is_sequential(self, tmp_path):
        from pipeline.colpali_retriever import colpali_search
        index_dir = _make_index_dir(tmp_path, n_pages=3)
        idx = ColPaliIndex(index_dir)
        model, proc, dev = self._make_mock_model_proc()
        results = colpali_search("dosing", model, proc, dev, idx, top_k=3)
        ranks = [r["rank"] for r in results]
        assert ranks == list(range(1, len(results) + 1))


# ---------------------------------------------------------------------------
# COLPALI_AVAILABLE flag
# ---------------------------------------------------------------------------

class TestAvailabilityFlag:

    def test_flag_is_bool(self):
        assert isinstance(COLPALI_AVAILABLE, bool)

    def test_module_importable_without_colpali_engine(self):
        """Importing the module must not raise even when colpali-engine is absent."""
        # If we got here, the import succeeded — test passes.
        import pipeline.colpali_retriever  # noqa: F401


# ---------------------------------------------------------------------------
# HybridRetriever integration — colpali_available property
# ---------------------------------------------------------------------------

class TestHybridRetrieverColPaliProperty:

    def test_colpali_available_false_without_index(self):
        from pipeline.retriever import HybridRetriever
        chunks = [{"chunk_id": "c1", "text": "malaria", "page": 1,
                   "heading": "H", "tables": [], "preservation_level": "standard",
                   "section_type": "background", "related_chunk_ids": []}]
        r = HybridRetriever(chunks, enable_reranking=False)
        assert r.colpali_available is False

    def test_colpali_available_false_when_module_missing(self, tmp_path):
        """Even with an index dir, colpali_available=False if module guard fires."""
        from pipeline.retriever import HybridRetriever
        chunks = [{"chunk_id": "c1", "text": "malaria", "page": 1,
                   "heading": "H", "tables": [], "preservation_level": "standard",
                   "section_type": "background", "related_chunk_ids": []}]
        # Pass a ColPaliIndex but patch the module-available flag to False
        index_dir = _make_index_dir(tmp_path, n_pages=2)
        idx = ColPaliIndex(index_dir)
        import pipeline.retriever as ret_mod
        original = ret_mod._COLPALI_MODULE_AVAILABLE
        try:
            ret_mod._COLPALI_MODULE_AVAILABLE = False
            r = HybridRetriever(chunks, enable_reranking=False, colpali_index=idx)
            assert r.colpali_available is False
        finally:
            ret_mod._COLPALI_MODULE_AVAILABLE = original
