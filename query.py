"""
Verbatim RAG Query Interface for SafeAI pipeline.

Returns retrieved passages exactly as they appear in the source PDF —
no LLM synthesis, no paraphrasing.  Every result includes the section
heading, page number, preservation level, and the verbatim source text.

This interface is optimised for 100% accuracy: the answer IS the
retrieved passage.  For dosing tables the full VERBATIM chunk text is
returned unchanged.

Usage:
    python query.py "What is the treatment for malaria in children?"
    python query.py "ACT dosing by weight" --top-k 3
    python query.py "Danger signs requiring referral" --kb ./medical_kb_who_malaria
    python query.py "Amoxicillin dosing" --child-only

Pipeline (no LLM involved):
    1. Normalize American → British spelling in query
    2. Hybrid search: BM25 + FAISS dense + cross-encoder reranking + metadata boosts
    3. Return verbatim parent chunk (or child chunk with --child-only)
    4. Print section, page, preservation level, and passage text
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# Allow running from project root without installing.
sys.path.insert(0, str(Path(__file__).parent))

from pipeline.retriever import HybridRetriever, _normalize_medical_spelling


# ---------------------------------------------------------------------------
# Knowledge-base loader
# ---------------------------------------------------------------------------

def _load_knowledge_base(kb_dir: Path) -> tuple[List[Dict], Dict]:
    """Load chunks and metadata from a SafeAI knowledge base directory.

    Looks for knowledge_base.json (preferred, contains metadata) or
    chunks.json (flat chunk list).

    Returns:
        (chunks, metadata) — chunks is a list of chunk dicts;
        metadata is the KB metadata dict (empty dict if not available).
    """
    kb_file = kb_dir / "knowledge_base.json"
    chunks_file = kb_dir / "chunks.json"

    if kb_file.exists():
        with open(kb_file, "r", encoding="utf-8") as f:
            kb = json.load(f)
        chunks = kb.get("chunks", [])
        metadata = kb.get("metadata", {})
        return chunks, metadata

    if chunks_file.exists():
        with open(chunks_file, "r", encoding="utf-8") as f:
            chunks = json.load(f)
        return chunks, {}

    raise FileNotFoundError(
        f"No knowledge base found at {kb_dir}.\n"
        f"Expected: {kb_file} or {chunks_file}\n"
        "Run the pipeline first: python run_pipeline.py --pdf /path/to/guideline.pdf"
    )


def _find_parent_chunk(child: Dict[str, Any], all_chunks: List[Dict]) -> Optional[Dict]:
    """Return the parent chunk for a child chunk, or None if not found."""
    parent_id = child.get("parent_chunk_id")
    if not parent_id:
        return None
    for chunk in all_chunks:
        if chunk.get("chunk_id") == parent_id:
            return chunk
    return None


# ---------------------------------------------------------------------------
# Display
# ---------------------------------------------------------------------------

def _preservation_label(level: str) -> str:
    labels = {
        "verbatim": "VERBATIM (exact source text)",
        "high": "HIGH FIDELITY",
        "standard": "STANDARD",
    }
    return labels.get((level or "").lower(), level or "unknown")


def _print_results(
    query: str,
    results: List[Dict[str, Any]],
    all_chunks: List[Dict],
    *,
    show_parent: bool = True,
) -> None:
    print()
    print("=" * 80)
    print(f"QUERY: {query}")
    print("=" * 80)

    if not results:
        print("No results found.")
        return

    for i, result in enumerate(results, 1):
        score = result.get("score", 0.0)
        page = result.get("page", "?")
        heading = result.get("heading", "")
        pres = result.get("preservation_level", "")
        section_type = result.get("section_type", "")

        print(f"\n{'─' * 80}")
        print(
            f"Result {i}  |  score: {score:.3f}  |  page: {page}  |  "
            f"{_preservation_label(pres)}"
        )
        if heading:
            print(f"Section: {heading}")
        if section_type:
            print(f"Type: {section_type}")
        print(f"{'─' * 80}")

        if show_parent:
            # Try to return the full parent chunk for maximum context.
            parent = _find_parent_chunk(result, all_chunks)
            text_to_show = (
                parent.get("text", "") if parent
                else result.get("text", result.get("contextual_content", ""))
            )
            # Strip contextual header ([Context: ...]) from display — the
            # section/page info is shown above; the header is indexing metadata.
            text_to_show = _strip_context_header(text_to_show)
        else:
            raw = result.get("text", result.get("contextual_content", ""))
            text_to_show = _strip_context_header(raw)

        print(text_to_show)

    print(f"\n{'=' * 80}")
    print(f"{len(results)} result(s) returned.")
    print("=" * 80)


def _strip_context_header(text: str) -> str:
    """Remove the [Context: ...] prefix that SafeAI prepends to child chunks."""
    if text.startswith("[Context:"):
        end = text.find("]\n\n")
        if end != -1:
            return text[end + 3:]
        end = text.find("]")
        if end != -1:
            return text[end + 1:].lstrip()
    return text


# ---------------------------------------------------------------------------
# Core query function
# ---------------------------------------------------------------------------

def query(
    question: str,
    kb_dir: Path,
    top_k: int = 5,
    show_parent: bool = True,
    drug_keywords: Optional[List[str]] = None,
    condition_patterns: Optional[List[List[str]]] = None,
) -> List[Dict[str, Any]]:
    """Retrieve the most relevant passages for a clinical question.

    Args:
        question:           Natural language clinical question.
        kb_dir:             Path to the SafeAI knowledge base directory
                            (must contain knowledge_base.json or chunks.json).
        top_k:              Number of results to return.
        show_parent:        If True, display full parent chunk; else child only.
        drug_keywords:      Optional drug name list for metadata boosting
                            (auto-loaded from KB metadata if available).
        condition_patterns: Optional condition regex patterns for boosting.

    Returns:
        List of result dicts with score, page, heading, preservation_level,
        section_type, and text fields.
    """
    print(f"Loading knowledge base from {kb_dir}...", end=" ", flush=True)
    chunks, kb_meta = _load_knowledge_base(kb_dir)
    print(f"done. ({len(chunks)} chunks)")

    # Auto-load drug keywords and condition patterns from KB metadata.
    cfg = kb_meta.get("config", {})
    if drug_keywords is None:
        drug_keywords = cfg.get("drug_keywords") or []
    if condition_patterns is None:
        condition_patterns = cfg.get("condition_patterns") or []

    # Auto-detect ColPali visual index if present in the KB directory.
    colpali_index = None
    colpali_index_dir = kb_dir / "colpali_index"
    if (colpali_index_dir / "metadata.json").exists():
        try:
            from pipeline.colpali_retriever import ColPaliIndex
            colpali_index = ColPaliIndex(colpali_index_dir)
            print(f"ColPali visual index detected ({colpali_index.page_count} pages). "
                  "Visual retrieval enabled.")
        except Exception as _e:
            print(f"ColPali index found but failed to load ({_e}) — text-only retrieval.")

    print(f"Building retrieval index...", end=" ", flush=True)
    retriever = HybridRetriever(
        chunks,
        drug_keywords=drug_keywords,
        condition_patterns=condition_patterns,
        colpali_index=colpali_index,
    )
    print("done.")

    normalized_q = _normalize_medical_spelling(question)
    if normalized_q != question:
        print(f"Query normalized: '{question}' → '{normalized_q}'")

    print(f"Searching top-{top_k} results...", end=" ", flush=True)
    results = retriever.retrieve(normalized_q, k=top_k)
    print("done.")

    _print_results(question, results, chunks, show_parent=show_parent)
    return results


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Query a SafeAI clinical guideline knowledge base (verbatim retrieval, no LLM)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python query.py "What is the treatment for malaria in children?"
  python query.py "ACT dosing by weight" --top-k 3
  python query.py "Danger signs requiring referral" --kb ./medical_kb_who_malaria
  python query.py "Amoxicillin dose for pneumonia" --child-only
        """,
    )
    parser.add_argument("question", help="Clinical question to search for")
    parser.add_argument(
        "--top-k", type=int, default=5,
        help="Number of results to return (default: 5)",
    )
    parser.add_argument(
        "--kb", type=Path, default=None,
        help="Path to knowledge base directory (default: auto-detect in current dir)",
    )
    parser.add_argument(
        "--child-only", action="store_true",
        help="Show only the matching child chunk, not the full parent context",
    )

    args = parser.parse_args()

    # Auto-detect KB directory if not specified.
    if args.kb is None:
        candidates = [
            Path("./medical_kb_who_malaria"),
            Path("./medical_kb_uganda_clinical_2023"),
            Path("./medical_knowledge_base"),
        ]
        for c in candidates:
            if c.exists() and (
                (c / "knowledge_base.json").exists() or (c / "chunks.json").exists()
            ):
                args.kb = c
                break
        if args.kb is None:
            print(
                "ERROR: No knowledge base found. Run the pipeline first:\n"
                "  python run_pipeline.py --pdf /path/to/guideline.pdf\n"
                "Or specify the KB directory with --kb /path/to/kb",
                file=sys.stderr,
            )
            sys.exit(1)

    try:
        query(
            question=args.question,
            kb_dir=args.kb,
            top_k=args.top_k,
            show_parent=not args.child_only,
        )
    except FileNotFoundError as e:
        print(f"\nERROR: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nAborted.")
        sys.exit(0)
    except Exception as e:
        print(f"\nERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
