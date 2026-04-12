"""
ColPali v1.2 visual retrieval for SafeAI.

Indexes each PDF page as a set of 128-dim patch embeddings (L2-normalized) using
the ColPali PaliGemma-3B model. At query time, MaxSim late-interaction scoring
ranks pages by visual relevance — catching dense dosing tables and clinical figures
that are rendered as images rather than parsed text, and therefore invisible to
BM25 and FAISS dense search.

When installed and indexed, this module adds a fourth retrieval tier to
HybridRetriever's RRF fusion alongside BM25, FAISS general, and FAISS medical.
Pages containing tables receive a 2× weight boost; figure pages 1.5×; text-only
pages 0.3× (suppressing noise from plain text pages).

Installation:
    pip install 'colpali-engine>=0.3.8' torch torchvision pypdfium2 pillow

Build the index (once per PDF, after running run_pipeline.py):
    python scripts/build_colpali_index.py \\
        --pdf /path/to/guideline.pdf \\
        --kb  ./my_output_dir

Enable in HybridRetriever:
    from pipeline.colpali_retriever import ColPaliIndex
    colpali_index = ColPaliIndex(Path("./my_output_dir/colpali_index"))
    retriever = HybridRetriever(chunks, colpali_index=colpali_index)

If colpali-engine is not installed, COLPALI_AVAILABLE is False and all functions
degrade gracefully — HybridRetriever continues with text-only retrieval.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Availability guard — colpali-engine + torch are heavy optional deps
# ---------------------------------------------------------------------------

try:
    import torch  # noqa: F401 — checked below
    from colpali_engine.models import ColPali, ColPaliProcessor  # noqa: F401
    COLPALI_AVAILABLE = True
except ImportError:
    COLPALI_AVAILABLE = False

_MODEL_CACHE: Dict[str, Tuple[Any, Any, Any]] = {}  # model_name → (model, processor, device)

DEFAULT_COLPALI_MODEL = "vidore/colpali-v1.2"
_EMBED_DIM = 128       # ColPali v1.2 output dimension per patch
_RENDER_DPI = 150      # sufficient for 448×448 ColPali input, same as CT Health AI
_BATCH_SIZE = 4        # pages per inference batch; reduce if OOM

# Content-aware RRF weight multipliers applied per page in HybridRetriever.
# Matching CT Health AI values (hybrid_search.py lines 451-462).
_COLPALI_TABLE_WEIGHT = 2.0   # pages with detected tables
_COLPALI_FIGURE_WEIGHT = 1.5  # pages with detected figures
_COLPALI_TEXT_WEIGHT = 0.3    # text-only pages (suppress noise)


# ---------------------------------------------------------------------------
# Model loading
# ---------------------------------------------------------------------------

def load_colpali_model(
    model_name: str = DEFAULT_COLPALI_MODEL,
) -> Tuple[Any, Any, Any]:
    """Load ColPali model and processor. Result is cached after first call.

    Device selection: MPS (Apple Silicon) > CUDA > CPU — same priority as
    CT Health AI's colpali_search.py.

    Returns:
        (model, processor, device)

    Raises:
        ImportError if colpali-engine or torch are not installed.
    """
    if not COLPALI_AVAILABLE:
        raise ImportError(
            "ColPali requires: pip install 'colpali-engine>=0.3.8' torch torchvision\n"
            "After installing, rebuild the index: python scripts/build_colpali_index.py"
        )

    if model_name in _MODEL_CACHE:
        return _MODEL_CACHE[model_name]

    import torch as _t
    from colpali_engine.models import ColPali, ColPaliProcessor

    if _t.backends.mps.is_available():
        device = _t.device("mps")
        dtype = _t.float32
    elif _t.cuda.is_available():
        device = _t.device("cuda")
        dtype = _t.bfloat16
    else:
        device = _t.device("cpu")
        dtype = _t.float32

    logger.info("Loading ColPali model %s on %s ...", model_name, device)
    model = ColPali.from_pretrained(
        model_name,
        torch_dtype=dtype,
        device_map=str(device),
        low_cpu_mem_usage=True,
    ).eval()
    processor = ColPaliProcessor.from_pretrained(model_name)

    entry = (model, processor, device)
    _MODEL_CACHE[model_name] = entry
    return entry


# ---------------------------------------------------------------------------
# Index
# ---------------------------------------------------------------------------

class ColPaliIndex:
    """Loaded ColPali page-embedding index. All page embeddings are held in memory.

    Attributes:
        model_name:  HuggingFace model ID used when building the index.
        page_count:  Number of pages embedded.
    """

    def __init__(self, index_dir: Path) -> None:
        self.index_dir = Path(index_dir)
        meta_path = self.index_dir / "metadata.json"
        if not meta_path.exists():
            raise FileNotFoundError(
                f"ColPali index metadata not found: {meta_path}\n"
                "Build the index first: python scripts/build_colpali_index.py "
                "--pdf /path/to.pdf --kb /path/to/kb_dir"
            )
        with open(meta_path, "r", encoding="utf-8") as f:
            self._meta = json.load(f)

        self.model_name: str = self._meta.get("model", DEFAULT_COLPALI_MODEL)
        self._page_embeddings: Dict[int, np.ndarray] = {}  # page → (n_patches, 128)
        self._page_info: Dict[int, Dict] = {}              # page → metadata entry

        n_loaded = 0
        for page_str, pinfo in self._meta.get("pages", {}).items():
            page = int(page_str)
            npy_path = self.index_dir / pinfo["embeddings_path"]
            if npy_path.exists():
                self._page_embeddings[page] = np.load(str(npy_path))
                self._page_info[page] = pinfo
                n_loaded += 1

        logger.info("ColPaliIndex loaded: %d pages from %s", n_loaded, self.index_dir)

    @property
    def page_count(self) -> int:
        return len(self._page_embeddings)

    def __len__(self) -> int:
        return self.page_count

    def __bool__(self) -> bool:
        return len(self._page_embeddings) > 0


# ---------------------------------------------------------------------------
# Index building
# ---------------------------------------------------------------------------

def build_colpali_index(
    pdf_path: Path,
    index_dir: Path,
    chunks: List[Dict[str, Any]],
    model_name: str = DEFAULT_COLPALI_MODEL,
    batch_size: int = _BATCH_SIZE,
    page_range: Optional[Tuple[int, int]] = None,
) -> ColPaliIndex:
    """Render PDF pages, embed with ColPali, save to index_dir/.

    Args:
        pdf_path:    Source PDF file.
        index_dir:   Directory where .npy files and metadata.json are written.
        chunks:      All chunks from knowledge_base.json — used to build the
                     page → chunk_id mapping and detect table/figure pages.
        model_name:  ColPali HuggingFace model ID.
        batch_size:  Pages per inference batch (lower = less GPU memory).
        page_range:  Optional (start, end) 0-based inclusive page range.
                     Default: all pages.

    Returns:
        Loaded ColPaliIndex ready for querying.
    """
    try:
        import pypdfium2 as pdfium
        from PIL import Image  # noqa: F401
    except ImportError as exc:
        raise ImportError(
            f"Index building requires: pip install pypdfium2 pillow\n{exc}"
        ) from exc

    model, processor, device = load_colpali_model(model_name)
    import torch as _t

    index_dir = Path(index_dir)
    index_dir.mkdir(parents=True, exist_ok=True)

    # Build page → chunk_ids mapping and detect content types per page.
    page_to_chunk_ids: Dict[int, List[str]] = {}
    page_has_tables: Dict[int, bool] = {}
    page_has_figures: Dict[int, bool] = {}

    for chunk in chunks:
        page = chunk.get("page")
        cid = chunk.get("chunk_id")
        if page is None or cid is None:
            continue
        page_to_chunk_ids.setdefault(int(page), []).append(str(cid))
        ct = chunk.get("content_type", "")
        # Detect table pages: chunk has tables list, is_table_only flag, or content_type=table.
        if chunk.get("is_table_only") or bool(chunk.get("tables")) or ct == "table":
            page_has_tables[int(page)] = True
        # Detect figure pages: image OCR or placeholder content.
        if ct in ("image_ocr", "image_placeholder"):
            page_has_figures[int(page)] = True

    # Render and embed pages.
    pdf_doc = pdfium.PdfDocument(str(pdf_path))
    n_pages = len(pdf_doc)
    scale = _RENDER_DPI / 72.0

    if page_range:
        start, end = page_range
        pages_to_process = [p for p in range(start, min(end + 1, n_pages))]
    else:
        pages_to_process = list(range(n_pages))

    logger.info(
        "Building ColPali index: %d pages at %d DPI, batch_size=%d",
        len(pages_to_process), _RENDER_DPI, batch_size,
    )

    meta_pages: Dict[str, Any] = {}

    for batch_start in range(0, len(pages_to_process), batch_size):
        batch_indices = pages_to_process[batch_start: batch_start + batch_size]
        images = []

        for page_idx in batch_indices:
            page_obj = pdf_doc[page_idx]
            bitmap = page_obj.render(scale=scale)
            images.append(bitmap.to_pil().convert("RGB"))

        with _t.no_grad():
            inputs = processor.process_images(images).to(device)
            batch_emb = model(**inputs)  # (batch, n_patches, 128)

        for j, page_idx in enumerate(batch_indices):
            emb = batch_emb[j].float()
            norms = emb.norm(dim=-1, keepdim=True).clamp(min=1e-8)
            emb_norm = (emb / norms).cpu().numpy()  # L2-normalized, (n_patches, 128)

            npy_path = index_dir / f"page_{page_idx:04d}.npy"
            np.save(str(npy_path), emb_norm)

            meta_pages[str(page_idx)] = {
                "embeddings_path": npy_path.name,
                "n_patches": int(emb_norm.shape[0]),
                "has_tables": page_has_tables.get(page_idx, False),
                "has_figures": page_has_figures.get(page_idx, False),
                "chunk_ids": page_to_chunk_ids.get(page_idx, []),
            }

        done = min(batch_start + batch_size, len(pages_to_process))
        if done % 20 == 0 or done == len(pages_to_process):
            logger.info("  %d / %d pages embedded", done, len(pages_to_process))

    metadata = {
        "model": model_name,
        "embedding_dim": _EMBED_DIM,
        "pdf_path": str(pdf_path),
        "n_pages": len(meta_pages),
        "pages": meta_pages,
    }
    with open(index_dir / "metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    logger.info("ColPali index saved to %s (%d pages)", index_dir, len(meta_pages))
    return ColPaliIndex(index_dir)


# ---------------------------------------------------------------------------
# MaxSim scoring
# ---------------------------------------------------------------------------

def _maxsim_score(query_emb: np.ndarray, page_emb: np.ndarray) -> float:
    """MaxSim late-interaction score (ColPali scoring function).

    query_emb : (n_query_tokens, dim) — L2-normalised
    page_emb  : (n_patches, dim)      — L2-normalised

    Score = Σ_t  max_p  (query_emb[t] · page_emb[p])

    For each query token, find the most similar page patch, then sum all
    token-wise maxima. This provides fine-grained spatial matching —
    e.g., a query token "5mg/kg" can match the specific cell in a dosing
    table that contains that value, even if the surrounding text is irrelevant.
    """
    sims = query_emb @ page_emb.T          # (n_query_tokens, n_patches)
    return float(sims.max(axis=1).sum())   # sum of per-token max similarities


# ---------------------------------------------------------------------------
# Query
# ---------------------------------------------------------------------------

def colpali_search(
    query_text: str,
    model: Any,
    processor: Any,
    device: Any,
    index: ColPaliIndex,
    top_k: int = 20,
) -> List[Dict[str, Any]]:
    """Run ColPali visual retrieval for a text query.

    Embeds the query with ColPali's query encoder, then computes MaxSim scores
    against every page embedding in the index.

    Args:
        query_text:  Text query.
        model:       Loaded ColPali model (from load_colpali_model).
        processor:   Loaded ColPaliProcessor.
        device:      Torch device.
        index:       Loaded ColPaliIndex.
        top_k:       Number of top pages to return.

    Returns:
        List of page result dicts, sorted by colpali_score descending:
            page_number   (int)    — matches render order used during indexing
            colpali_score (float)  — raw MaxSim score
            chunk_ids     (List[str]) — chunk_ids on this page
            has_tables    (bool)
            has_figures   (bool)
            rank          (int)    — 1-based rank
            source        (str)    — "colpali"
    """
    if not COLPALI_AVAILABLE or not index:
        return []

    import torch as _t

    with _t.no_grad():
        q_input = processor.process_queries([query_text]).to(device)
        q_emb_tensor = model(**q_input)  # (1, n_tokens, 128)

    q_emb = q_emb_tensor[0].float()
    norms = q_emb.norm(dim=-1, keepdim=True).clamp(min=1e-8)
    q_emb_norm = (q_emb / norms).cpu().numpy()  # (n_tokens, 128)

    scores: List[Tuple[int, float]] = [
        (page_idx, _maxsim_score(q_emb_norm, page_emb))
        for page_idx, page_emb in index._page_embeddings.items()
    ]
    scores.sort(key=lambda x: x[1], reverse=True)

    results = []
    for rank, (page_idx, score) in enumerate(scores[:top_k], 1):
        info = index._page_info.get(page_idx, {})
        results.append({
            "page_number": page_idx,
            "colpali_score": score,
            "chunk_ids": info.get("chunk_ids", []),
            "has_tables": info.get("has_tables", False),
            "has_figures": info.get("has_figures", False),
            "rank": rank,
            "source": "colpali",
        })
    return results
