#!/usr/bin/env python3
"""
Rerun the retrieval benchmark using the current HybridRetriever
(with metadata-aware re-ranking) against the existing child chunks.

Supports two modes:
  1. Original 12-query benchmark (labels from git commit e32337e)
  2. Expanded 30-query benchmark (12 original + 18 new with independent labels)

Reads:
  rag_output/child_chunks.json         — 1,695 child chunks
  configs/malaria_who_2025.json        — drug_keywords and condition_patterns

Writes:
  rag_output/retrieval_test_results.json — updated with new rankings/scores
  rag_output/build_report.json           — updated aggregate metrics

Usage:
  python scripts/rerun_retrieval_benchmark.py           # expanded 30-query benchmark
  python scripts/rerun_retrieval_benchmark.py --original # original 12-query only
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Set

# Ensure repo root is on the path.
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from pipeline.retriever import HybridRetriever  # noqa: E402
from pipeline.config import extraction_config_who_malaria_nih  # noqa: E402


# =========================================================================
# Expanded benchmark: 18 new queries with independently labelled relevance
# =========================================================================

def _search_chunks(
    children: List[dict],
    patterns: List[str],
    domain_filter: Optional[List[str]] = None,
    limit: int = 5,
) -> List[str]:
    """Find child_ids matching ALL regex patterns (AND logic).

    This is used to build relevance labels *independently* of the retriever,
    by searching chunk text content directly.
    """
    results: List[str] = []
    for c in children:
        text = (c.get("content", "") or "") + " " + (c.get("contextual_content", "") or "")
        text_lower = text.lower()
        if all(re.search(p, text_lower) for p in patterns):
            if domain_filter:
                dom = c.get("clinical_domain", "").lower()
                if not any(d in dom for d in domain_filter):
                    continue
            results.append(c["child_id"])
    return results[:limit]


def build_expanded_queries(children: List[dict]) -> Dict[str, dict]:
    """Build the 18 new benchmark queries (Q13–Q30) with independent labels.

    Categories covered:
      - diagnostic (2)           - prevention (2)
      - treatment_protocol (4)   - population_specific (2)
      - procedural (2)           - safety (2)
      - evidence (2)             - operational (2)
    """
    S = lambda *a, **kw: _search_chunks(children, *a, **kw)  # noqa: E731

    return {
        "Q13": {
            "query": "When should G6PD testing be done before prescribing primaquine?",
            "category": "diagnostic",
            "relevant_ids": S(["g6pd", "primaquine|8.aminoquinoline"]),
        },
        "Q14": {
            "query": "What are the WHO criteria for confirming severe malaria diagnosis?",
            "category": "diagnostic",
            "relevant_ids": S(
                ["severe\\s+malaria", "feature|clinical|present|sign|mortalit|convuls|coma"],
                domain_filter=["treating severe", "severe malaria", "management"],
            ),
        },
        "Q15": {
            "query": "Who is eligible for seasonal malaria chemoprevention and what drugs are used?",
            "category": "prevention",
            "relevant_ids": S(
                ["seasonal\\s+malaria\\s+chemoprevention|\\bsmc\\b",
                 "eligib|children|age|drug|amodiaquine"],
                domain_filter=["seasonal", "chemoprevention", "national adaptation"],
            ),
        },
        "Q16": {
            "query": "What type of insecticide-treated bed nets does WHO recommend?",
            "category": "prevention",
            "relevant_ids": S(
                ["insecticide.treated|\\bitn|\\bllin", "recommend"],
                domain_filter=["large-scale", "vector", "intervention"],
            ),
        },
        "Q17": {
            "query": "What is the role of rectal artesunate in pre-referral treatment?",
            "category": "treatment_protocol",
            "relevant_ids": S(["rectal\\s+artesunate", "pre.referral|refer"]),
        },
        "Q18": {
            "query": "When should quinine be used instead of artesunate for severe malaria?",
            "category": "treatment_protocol",
            "relevant_ids": S(
                ["quinine", "artesunate|severe"],
                domain_filter=["severe", "parenteral", "treatment"],
            ),
        },
        "Q19": {
            "query": "How is chloroquine-resistant P. vivax malaria treated?",
            "category": "treatment_protocol",
            "relevant_ids": S(["chloroquine.resist", "vivax"]),
        },
        "Q20": {
            "query": "What antimalarials are safe in the first trimester of pregnancy?",
            "category": "population_specific",
            "relevant_ids": S(
                ["first\\s+trimester|early\\s+pregnancy",
                 "antimalarial|treatment|safe|quinine|act"],
            ),
        },
        "Q21": {
            "query": "How should malaria be managed in malnourished children?",
            "category": "population_specific",
            "relevant_ids": S(["malnourish|malnutrition|underweight", "malaria|treatment|child"]),
        },
        "Q22": {
            "query": "What is the recommended procedure for mass drug administration in emergencies?",
            "category": "procedural",
            "relevant_ids": S(["mass\\s+drug\\s+admin", "emergenc"]),
        },
        "Q23": {
            "query": "Steps for managing a patient with artemisinin-resistant malaria",
            "category": "procedural",
            "relevant_ids": S(["artemisinin.resist", "treat|manag|recommend"]),
        },
        "Q24": {
            "query": "What are the contraindications for sulfadoxine-pyrimethamine in IPTp?",
            "category": "safety",
            "relevant_ids": S(
                ["sulfadoxine.pyrimethamine|\\bsp\\b",
                 "iptp|intermittent\\s+prevent.*pregnan"],
            ),
        },
        "Q25": {
            "query": "Drug interactions between antimalarials and antiretroviral therapy",
            "category": "safety",
            "relevant_ids": S(["antiretroviral|\\barv|\\bhiv", "antimalarial|interact|co.admin"]),
        },
        "Q26": {
            "query": "What is the evidence for post-discharge malaria chemoprevention?",
            "category": "evidence",
            "relevant_ids": S(["post.discharge", "chemoprevention|pdmc"]),
        },
        "Q27": {
            "query": "How effective are malaria vaccines and which populations should be prioritized?",
            "category": "evidence",
            "relevant_ids": S(
                ["vaccin", "efficac|effective|priorit"],
                domain_filter=["vaccin"],
            ),
        },
        "Q28": {
            "query": "What are the criteria for indoor residual spraying deployment?",
            "category": "operational",
            "relevant_ids": S(
                ["indoor\\s+residual\\s+spray|\\birs\\b", "criteria|recommend|deploy|when"],
                domain_filter=["residual spray", "vector", "intervention"],
            ),
        },
        "Q29": {
            "query": "How should anti-relapse therapy with primaquine be dosed for P. vivax?",
            "category": "treatment_protocol",
            "relevant_ids": S(
                ["anti.relapse|radical\\s+cure|relapse", "primaquine", "vivax|dose|dos"],
            ),
        },
        "Q30": {
            "query": "What is the recommended approach for malaria treatment in areas approaching elimination?",
            "category": "operational",
            "relevant_ids": S(
                ["eliminat", "treatment|recommend|strateg"],
                domain_filter=["eliminat", "final phase"],
            ),
        },
    }


# =========================================================================
# Core helpers
# =========================================================================

def load_child_chunks(path: Path) -> List[dict]:
    """Load child chunks and add a 'chunk_id' field the retriever expects."""
    with open(path) as f:
        data = json.load(f)
    children = data["children"]
    for c in children:
        if "chunk_id" not in c:
            c["chunk_id"] = c["child_id"]
    return children


def load_original_queries() -> Dict[str, dict]:
    """Load the original 12 queries with relevance labels.

    Tries git commit e32337e first (canonical source), then falls back to
    the current rag_output/retrieval_test_results.json (for repos without
    that commit in their history).
    """
    print("  Loading original 12-query labels from git (e32337e)...")
    result = subprocess.run(
        ["git", "show", "e32337e:rag_output/retrieval_test_results.json"],
        capture_output=True, text=True, cwd=str(ROOT),
    )
    if result.returncode != 0:
        # Fallback: read from current file on disk.
        fallback = ROOT / "rag_output" / "retrieval_test_results.json"
        if not fallback.exists():
            raise RuntimeError("Cannot recover original benchmark from git and no fallback file found")
        print("  (git commit not found -- loading labels from rag_output/retrieval_test_results.json)")
        with open(fallback) as f:
            data = json.load(f)
    else:
        data = json.loads(result.stdout)

    queries: Dict[str, dict] = {}
    for qid, qdata in data["queries"].items():
        queries[qid] = {
            "query": qdata["query"],
            "category": "original",
            "relevant_ids": [
                r["child_id"] for r in qdata.get("results", []) if r.get("relevant")
            ],
        }
    return queries


def compute_metrics(results: List[dict], relevant_ids: Set[str], k: int) -> float:
    """Precision@k: fraction of top-k results that are relevant."""
    top_k = results[:k]
    if not top_k:
        return 0.0
    hits = sum(1 for r in top_k if r["child_id"] in relevant_ids)
    return hits / len(top_k)


def compute_mrr(results: List[dict], relevant_ids: Set[str]) -> float:
    """Mean Reciprocal Rank: 1/rank of the first relevant result."""
    for i, r in enumerate(results):
        if r["child_id"] in relevant_ids:
            return 1.0 / (i + 1)
    return 0.0


# =========================================================================
# Main benchmark runner
# =========================================================================

def run_benchmark(original_only: bool = False) -> None:
    rag_dir = ROOT / "rag_output"
    chunks_path = rag_dir / "child_chunks.json"
    bench_path = rag_dir / "retrieval_test_results.json"
    report_path = rag_dir / "build_report.json"

    print("Loading child chunks...")
    children = load_child_chunks(chunks_path)
    print(f"  {len(children)} chunks loaded")

    # Build query set.
    print("Loading benchmark queries and relevance labels...")
    queries = load_original_queries()
    if not original_only:
        expanded = build_expanded_queries(children)
        queries.update(expanded)
        print(f"  {len(queries)} queries total (12 original + {len(expanded)} expanded)")
    else:
        print(f"  {len(queries)} queries (original only)")

    # Build config to get drug_keywords and condition_patterns.
    print("Loading config for drug_keywords and condition_patterns...")
    cfg = extraction_config_who_malaria_nih(pdf_path="dummy.pdf")
    drug_kw = cfg.drug_keywords or []
    cond_pat = cfg.condition_patterns or []
    print(f"  {len(drug_kw)} drug keywords, {len(cond_pat)} condition patterns")

    print("Building HybridRetriever (BM25 + FAISS + RRF + blended CE + metadata reranking)...")
    t0 = time.time()
    retriever = HybridRetriever(
        children,
        drug_keywords=drug_kw,
        condition_patterns=cond_pat,
        enable_metadata_reranking=True,
    )
    build_time = time.time() - t0
    print(f"  Built in {build_time:.1f}s")
    print(f"  Dense available: {retriever.dense_available}")
    print(f"  Medical dense available: {retriever.medical_dense_available}")
    print(f"  Reranking available: {retriever.reranking_available}")
    print(f"  Metadata reranking: {retriever.metadata_reranking_enabled}")

    # Run each query.
    new_queries: Dict[str, dict] = {}
    all_p3: List[float] = []
    all_p5: List[float] = []
    all_mrr: List[float] = []

    # Track per-category metrics.
    cat_metrics: Dict[str, List[float]] = {}

    for qid in sorted(queries.keys()):
        qdef = queries[qid]
        query = qdef["query"]
        relevant_ids = set(qdef["relevant_ids"])
        category = qdef.get("category", "original")

        print(f"\n  {qid}: {query[:70]}...")
        t1 = time.time()
        results = retriever.retrieve(query, k=5)
        latency = time.time() - t1

        # Build result entries.
        result_entries: List[dict] = []
        for r in results:
            cid = r.get("child_id", r.get("chunk_id", ""))
            query_tokens = set(query.lower().split())
            content_lower = r.get("content", "").lower()
            found = [t for t in query_tokens if t in content_lower and len(t) > 2]
            missing = [t for t in query_tokens if t not in content_lower and len(t) > 2]

            entry = {
                "rank": r.get("retrieval_rank", 0),
                "child_id": cid,
                "parent_chunk_id": r.get("parent_chunk_id", ""),
                "chunk_type": r.get("chunk_type", ""),
                "preservation_level": r.get("preservation_level", ""),
                "type_match": r.get("chunk_type", "") in ("dosing_table", "narrative"),
                "keyword_coverage": len(found) / max(len(found) + len(missing), 1),
                "keywords_found": found,
                "keywords_missing": missing,
                "relevant": cid in relevant_ids,
                "preservation_tag": (
                    "[VERBATIM]" if r.get("preservation_level") == "verbatim"
                    else "[HIGH FIDELITY]" if r.get("preservation_level") == "high"
                    else "[STANDARD]"
                ),
                "content_preview": r.get("content", "")[:200],
                "source_pages": r.get("source_pages", []),
                "score": r.get("score", 0.0),
            }
            result_entries.append(entry)

        p3 = compute_metrics(result_entries, relevant_ids, 3)
        p5 = compute_metrics(result_entries, relevant_ids, 5)
        mrr = compute_mrr(result_entries, relevant_ids)
        all_p3.append(p3)
        all_p5.append(p5)
        all_mrr.append(mrr)

        cat_metrics.setdefault(category, []).append(p3)

        new_queries[qid] = {
            "query_id": qid,
            "query": query,
            "category": category,
            "num_results": len(result_entries),
            "precision_at_3": round(p3, 3),
            "precision_at_5": round(p5, 3),
            "mrr": round(mrr, 3),
            "latency_ms": round(latency * 1000, 1),
            "results": result_entries,
        }

        status = "PERFECT" if p3 == 1.0 else f"P@3={p3:.3f}"
        print(
            f"    {status} | MRR={mrr:.3f} | [{category}] | {latency*1000:.0f}ms"
        )
        for re_ in result_entries[:3]:
            rel_mark = "REL" if re_["relevant"] else "   "
            print(
                f"      #{re_['rank']} [{rel_mark}] {re_['child_id']} "
                f"{re_['chunk_type']:15s} p{re_['source_pages']} "
                f"score={re_.get('score',0):.4f}"
            )

    # Aggregate metrics.
    n = len(all_p3)
    mean_p3 = sum(all_p3) / n if n else 0
    mean_p5 = sum(all_p5) / n if n else 0
    mean_mrr = sum(all_mrr) / n if n else 0
    perfect_p3 = sum(1 for p in all_p3 if p >= 1.0)

    aggregate = {
        "mean_precision_at_3": round(mean_p3, 3),
        "mean_precision_at_5": round(mean_p5, 3),
        "mean_mrr": round(mean_mrr, 3),
        "num_queries": n,
        "perfect_p3_count": perfect_p3,
        "metadata_reranking": True,
    }

    # Per-category breakdown.
    cat_summary: Dict[str, dict] = {}
    for cat, scores in sorted(cat_metrics.items()):
        cat_summary[cat] = {
            "num_queries": len(scores),
            "mean_p3": round(sum(scores) / len(scores), 3),
            "perfect": sum(1 for s in scores if s >= 1.0),
        }

    print("\n" + "=" * 60)
    print("AGGREGATE RESULTS")
    print("=" * 60)
    print(f"  Mean P@3:  {mean_p3:.3f}")
    print(f"  Mean P@5:  {mean_p5:.3f}")
    print(f"  Mean MRR:  {mean_mrr:.3f}")
    print(f"  Perfect P@3: {perfect_p3}/{n}")
    print()
    print("  Per-category P@3:")
    for cat, info in sorted(cat_summary.items()):
        print(f"    {cat:25s}  {info['mean_p3']:.3f}  ({info['perfect']}/{info['num_queries']} perfect)")

    # Write updated benchmark.
    new_bench = {
        "queries": new_queries,
        "aggregate": aggregate,
        "per_category": cat_summary,
    }
    with open(bench_path, "w") as f:
        json.dump(new_bench, f, indent=2)
    print(f"\nWrote {bench_path}")

    # Update build_report.json aggregate section.
    if report_path.exists():
        with open(report_path) as f:
            report = json.load(f)
        report["test_aggregate"] = aggregate
        report["per_category"] = cat_summary
        report["metadata_reranking"] = {
            "enabled": True,
            "drug_keywords_count": len(drug_kw),
            "condition_patterns_count": len(cond_pat),
            "boosts": {
                "drug_match": 1.35,
                "dosing_type": 1.25,
                "nll": 1.15,
                "evidence_table_demote": 0.85,
                "condition_match": 1.20,
                "domain_match": 1.10,
            },
        }
        with open(report_path, "w") as f:
            json.dump(report, f, indent=2)
        print(f"Wrote {report_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rerun retrieval benchmark")
    parser.add_argument(
        "--original", action="store_true",
        help="Run only the original 12 queries (skip expanded benchmark)",
    )
    args = parser.parse_args()
    run_benchmark(original_only=args.original)
