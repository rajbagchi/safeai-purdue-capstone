#!/usr/bin/env python3
"""
Build a ColPali v1.2 visual retrieval index for a SafeAI knowledge base.

This script renders each PDF page to an image (150 DPI), embeds it with
ColPali's PaliGemma-3B model (128-dim patch embeddings, L2-normalized), and
saves the index to <kb_dir>/colpali_index/. Once built, HybridRetriever
auto-detects and uses the index as a fourth retrieval tier alongside BM25,
FAISS general, and FAISS medical.

Prerequisites:
    pip install 'colpali-engine>=0.3.8' torch torchvision pypdfium2 pillow

The knowledge base must already be built before running this script:
    python run_pipeline.py --pdf /path/to/guideline.pdf --output-dir ./my_kb

Usage:
    # Index all pages
    python scripts/build_colpali_index.py \\
        --pdf /path/to/guideline.pdf \\
        --kb  ./my_kb

    # Index only pages 0–49 (useful for testing on a large document)
    python scripts/build_colpali_index.py \\
        --pdf /path/to/guideline.pdf \\
        --kb  ./my_kb \\
        --pages 0-49

    # Use ColQwen2 instead of ColPali (stronger, same interface)
    python scripts/build_colpali_index.py \\
        --pdf /path/to/guideline.pdf \\
        --kb  ./my_kb \\
        --model vidore/colqwen2-v1.0

    # Reduce batch size if GPU runs out of memory
    python scripts/build_colpali_index.py \\
        --pdf /path/to/guideline.pdf \\
        --kb  ./my_kb \\
        --batch-size 2

Index output:
    <kb_dir>/colpali_index/
      metadata.json          — page count, model name, per-page content flags, chunk_ids
      page_0000.npy          — patch embeddings for page 0  (n_patches, 128) float32
      page_0001.npy          — patch embeddings for page 1
      ...

Loading the index in HybridRetriever:
    from pathlib import Path
    from pipeline.colpali_retriever import ColPaliIndex
    from pipeline.retriever import HybridRetriever

    colpali_index = ColPaliIndex(Path("./my_kb/colpali_index"))
    retriever = HybridRetriever(chunks, colpali_index=colpali_index)
    results = retriever.retrieve("ACT dosing by weight in children")
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger(__name__)

# Allow running from project root or scripts/ directory.
sys.path.insert(0, str(Path(__file__).parent.parent))


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _load_chunks(kb_dir: Path) -> list:
    """Load chunks from knowledge_base.json (preferred) or chunks.json."""
    kb_file = kb_dir / "knowledge_base.json"
    chunks_file = kb_dir / "chunks.json"

    if kb_file.exists():
        with open(kb_file, "r", encoding="utf-8") as f:
            kb = json.load(f)
        chunks = kb.get("chunks", [])
        # Use child chunks (have parent_chunk_id) for page → chunk_id mapping;
        # they are what HybridRetriever indexes, so ColPali chunk_ids match.
        child_chunks = [c for c in chunks if c.get("parent_chunk_id") is not None]
        return child_chunks if child_chunks else chunks

    if chunks_file.exists():
        with open(chunks_file, "r", encoding="utf-8") as f:
            return json.load(f)

    raise FileNotFoundError(
        f"No knowledge base found at {kb_dir}.\n"
        "Run the pipeline first: python run_pipeline.py --pdf /path/to/pdf"
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build ColPali visual retrieval index for a SafeAI knowledge base",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/build_colpali_index.py --pdf guideline.pdf --kb ./output
  python scripts/build_colpali_index.py --pdf guideline.pdf --kb ./output --pages 0-49
  python scripts/build_colpali_index.py --pdf guideline.pdf --kb ./output --batch-size 2
  python scripts/build_colpali_index.py --pdf guideline.pdf --kb ./output --model vidore/colqwen2-v1.0
        """,
    )
    parser.add_argument(
        "--pdf", required=True, type=Path,
        help="Path to the source PDF (must be the same PDF used to build the KB)",
    )
    parser.add_argument(
        "--kb", required=True, type=Path,
        help="Knowledge base directory (must contain knowledge_base.json or chunks.json)",
    )
    parser.add_argument(
        "--model", default="vidore/colpali-v1.2",
        help="ColPali model on HuggingFace (default: vidore/colpali-v1.2)",
    )
    parser.add_argument(
        "--batch-size", type=int, default=4,
        help="Pages per inference batch. Reduce to 1-2 if GPU out-of-memory (default: 4)",
    )
    parser.add_argument(
        "--pages", default=None,
        help="0-based page range to index, e.g. '0-49'. Default: all pages",
    )

    args = parser.parse_args()

    # Validate inputs.
    if not args.pdf.exists():
        logger.error("PDF not found: %s", args.pdf)
        sys.exit(1)
    if not args.kb.is_dir():
        logger.error("Knowledge base directory not found: %s", args.kb)
        sys.exit(1)

    # Parse optional page range.
    page_range = None
    if args.pages:
        try:
            parts = args.pages.split("-")
            page_range = (int(parts[0]), int(parts[1]))
        except (ValueError, IndexError):
            logger.error("Invalid --pages format. Use 'start-end', e.g. '0-49'")
            sys.exit(1)

    # Load chunks.
    logger.info("Loading chunks from %s ...", args.kb)
    try:
        chunks = _load_chunks(args.kb)
    except FileNotFoundError as e:
        logger.error(str(e))
        sys.exit(1)
    logger.info("Loaded %d chunks", len(chunks))

    # Check ColPali availability before spending time on anything else.
    try:
        from pipeline.colpali_retriever import COLPALI_AVAILABLE, build_colpali_index
    except ImportError as e:
        logger.error("Failed to import pipeline: %s", e)
        sys.exit(1)

    if not COLPALI_AVAILABLE:
        logger.error(
            "colpali-engine or torch is not installed.\n"
            "Install with: pip install 'colpali-engine>=0.3.8' torch torchvision"
        )
        sys.exit(1)

    # Build the index.
    index_dir = args.kb / "colpali_index"
    logger.info("Building ColPali index -> %s", index_dir)

    try:
        build_colpali_index(
            pdf_path=args.pdf,
            index_dir=index_dir,
            chunks=chunks,
            model_name=args.model,
            batch_size=args.batch_size,
            page_range=page_range,
        )
    except Exception as e:
        logger.error("Index build failed: %s", e)
        sys.exit(1)

    print()
    print("ColPali index built successfully.")
    print()
    print("To use in HybridRetriever:")
    print("    from pathlib import Path")
    print("    from pipeline.colpali_retriever import ColPaliIndex")
    print("    from pipeline.retriever import HybridRetriever")
    print()
    print(f"    colpali_index = ColPaliIndex(Path('{index_dir}'))")
    print("    retriever = HybridRetriever(chunks, colpali_index=colpali_index)")
    print()
    print("To use in query.py (auto-detected when colpali_index/ exists in --kb dir):")
    print(f"    python query.py 'ACT dosing by weight' --kb {args.kb}")


if __name__ == "__main__":
    main()
