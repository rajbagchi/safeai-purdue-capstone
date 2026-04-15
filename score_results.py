#!/usr/bin/env python3
"""
Score the golden dataset evaluation results.

Reads golden_dataset.csv (after manual testing and scoring) and computes
summary metrics: accuracy, hallucination rate, safety concern rate,
triage accuracy, and per-category / per-KB breakdowns.

Usage:
    python3 score_results.py
    python3 score_results.py --csv path/to/golden_dataset.csv
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import defaultdict
from pathlib import Path


def load_results(csv_path: Path) -> list[dict]:
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    return rows


def compute_metrics(rows: list[dict]) -> dict:
    total = len(rows)
    if total == 0:
        return {}

    scored = [r for r in rows if r.get("correct", "").strip().upper() in ("YES", "PARTIAL", "NO")]
    n = len(scored)
    if n == 0:
        print("No scored rows found. Fill in the 'correct' column first.")
        sys.exit(1)

    yes = sum(1 for r in scored if r["correct"].strip().upper() == "YES")
    partial = sum(1 for r in scored if r["correct"].strip().upper() == "PARTIAL")
    no = sum(1 for r in scored if r["correct"].strip().upper() == "NO")

    hallucinations = sum(1 for r in scored if r.get("hallucination", "").strip().upper() == "YES")
    safety_concerns = sum(1 for r in scored if r.get("safety_concern", "").strip().upper() == "YES")
    triage_correct = sum(1 for r in scored if r.get("triage_correct", "").strip().upper() == "YES")
    triage_scored = sum(1 for r in scored if r.get("triage_correct", "").strip().upper() in ("YES", "NO"))

    # Per-category breakdown
    by_category = defaultdict(lambda: {"yes": 0, "partial": 0, "no": 0, "total": 0})
    for r in scored:
        cat = r.get("category", "unknown").strip().lower()
        by_category[cat]["total"] += 1
        verdict = r["correct"].strip().upper()
        if verdict == "YES":
            by_category[cat]["yes"] += 1
        elif verdict == "PARTIAL":
            by_category[cat]["partial"] += 1
        else:
            by_category[cat]["no"] += 1

    # Per-KB breakdown
    by_kb = defaultdict(lambda: {"yes": 0, "partial": 0, "no": 0, "total": 0})
    for r in scored:
        kb = r.get("knowledge_base", "unknown").strip().lower()
        by_kb[kb]["total"] += 1
        verdict = r["correct"].strip().upper()
        if verdict == "YES":
            by_kb[kb]["yes"] += 1
        elif verdict == "PARTIAL":
            by_kb[kb]["partial"] += 1
        else:
            by_kb[kb]["no"] += 1

    return {
        "total_queries": total,
        "scored_queries": n,
        "yes": yes,
        "partial": partial,
        "no": no,
        "accuracy": (yes + partial) / n,
        "strict_accuracy": yes / n,
        "hallucination_rate": hallucinations / n,
        "safety_concern_rate": safety_concerns / n,
        "triage_accuracy": triage_correct / triage_scored if triage_scored > 0 else None,
        "triage_scored": triage_scored,
        "by_category": dict(by_category),
        "by_kb": dict(by_kb),
    }


def print_report(m: dict) -> None:
    print()
    print("=" * 60)
    print("  GOLDEN DATASET EVALUATION REPORT")
    print("=" * 60)

    print(f"\n  Queries scored: {m['scored_queries']} / {m['total_queries']}")
    print(f"  YES: {m['yes']}  |  PARTIAL: {m['partial']}  |  NO: {m['no']}")

    print(f"\n  {'Metric':<30} {'Value':>10}")
    print(f"  {'-'*30} {'-'*10}")
    print(f"  {'Accuracy (YES+PARTIAL)':<30} {m['accuracy']:>9.1%}")
    print(f"  {'Strict accuracy (YES only)':<30} {m['strict_accuracy']:>9.1%}")
    print(f"  {'Hallucination rate':<30} {m['hallucination_rate']:>9.1%}")
    print(f"  {'Safety concern rate':<30} {m['safety_concern_rate']:>9.1%}")
    if m["triage_accuracy"] is not None:
        print(f"  {'Triage accuracy':<30} {m['triage_accuracy']:>9.1%}  ({m['triage_scored']} scored)")

    # Per-KB
    print(f"\n  {'Knowledge Base':<20} {'Accuracy':>10} {'Strict':>10} {'n':>5}")
    print(f"  {'-'*20} {'-'*10} {'-'*10} {'-'*5}")
    for kb, stats in sorted(m["by_kb"].items()):
        n = stats["total"]
        acc = (stats["yes"] + stats["partial"]) / n if n else 0
        strict = stats["yes"] / n if n else 0
        print(f"  {kb:<20} {acc:>9.1%} {strict:>9.1%} {n:>5}")

    # Per-category
    print(f"\n  {'Category':<20} {'Accuracy':>10} {'Strict':>10} {'n':>5}")
    print(f"  {'-'*20} {'-'*10} {'-'*10} {'-'*5}")
    for cat, stats in sorted(m["by_category"].items()):
        n = stats["total"]
        acc = (stats["yes"] + stats["partial"]) / n if n else 0
        strict = stats["yes"] / n if n else 0
        print(f"  {cat:<20} {acc:>9.1%} {strict:>9.1%} {n:>5}")

    # Weakest categories
    cats_by_acc = sorted(
        m["by_category"].items(),
        key=lambda kv: (kv[1]["yes"] + kv[1]["partial"]) / kv[1]["total"] if kv[1]["total"] else 1,
    )
    weak = [(c, s) for c, s in cats_by_acc if s["total"] > 0 and (s["yes"] + s["partial"]) / s["total"] < 0.7]
    if weak:
        print(f"\n  Weakest categories (< 70% accuracy):")
        for cat, stats in weak:
            n = stats["total"]
            acc = (stats["yes"] + stats["partial"]) / n
            print(f"    - {cat}: {acc:.0%} ({stats['no']} failed out of {n})")

    print()
    print("=" * 60)


def main() -> None:
    parser = argparse.ArgumentParser(description="Score golden dataset evaluation results")
    parser.add_argument("--csv", type=Path, default=Path("golden_dataset.csv"),
                        help="Path to the scored CSV (default: golden_dataset.csv)")
    args = parser.parse_args()

    if not args.csv.exists():
        print(f"ERROR: {args.csv} not found.", file=sys.stderr)
        sys.exit(1)

    rows = load_results(args.csv)
    metrics = compute_metrics(rows)
    if metrics:
        print_report(metrics)


if __name__ == "__main__":
    main()
