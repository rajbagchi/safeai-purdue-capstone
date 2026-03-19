"""
Run WHO-malaria preset end-to-end and write a Markdown report:
per-stage metrics + 25 BM25/guardrail searches.

Usage (from repo root):
  python scripts/who_malaria_pipeline_report.py
  python scripts/who_malaria_pipeline_report.py --reuse-kb
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from typing import Any, Dict, List

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from pipeline.config import extraction_config_who_malaria_nih
from pipeline.orchestrator import MedicalQASystem
from pipeline.extractor import MultiPassExtractor
from pipeline.validator import ExtractionValidator
from pipeline.chunker import SmartChunker
from pipeline.guardrail import MedicalGuardrailBrain


def _dataclass_or_dict(obj: Any) -> Any:
    if hasattr(obj, "__dataclass_fields__"):
        return asdict(obj)
    return obj


def build_kb_fresh(cfg) -> tuple:
    extractor = MultiPassExtractor(cfg)
    extraction = extractor.extract_all()

    validator = ExtractionValidator(extraction, cfg)
    validation = validator.validate_all()

    chunker = SmartChunker(extraction, cfg)
    chunks = chunker.chunk_by_headings()
    search_index = chunker.create_search_index()

    qa = MedicalQASystem(config=cfg)
    qa.extraction_result = extraction
    qa.validation_result = validation
    qa.chunks = chunks
    qa.search_index = search_index
    qa.guardrail = MedicalGuardrailBrain(chunks)
    qa._save_knowledge_base()

    return qa, extraction


def load_or_build(cfg, reuse_kb: bool) -> tuple:
    kb_file = os.path.join(cfg.output_dir, "knowledge_base.json")
    if reuse_kb and os.path.isfile(kb_file):
        qa = MedicalQASystem(config=cfg)
        qa.initialize()
        return qa, None
    return build_kb_fresh(cfg)


def extraction_section(extraction: Dict[str, Any] | None, qa: MedicalQASystem) -> str:
    if extraction is None:
        summ = qa.get_extraction_summary_from_disk()
        lines = [
            "## Stage 1: Multi-pass extraction",
            "",
            "_Loaded from existing `knowledge_base.json` (pass-level log not in memory)._",
            "",
            "| Metric | Value |",
            "|--------|-------|",
            f"| Pages (summary) | {summ.get('pages', '—')} |",
            f"| Tables (summary) | {summ.get('tables', '—')} |",
            f"| Extraction passes (summary) | {summ.get('passes', '—')} |",
            "",
        ]
        return "\n".join(lines)

    meta = extraction.get("metadata", {})
    pages = extraction.get("pages", [])
    tables = extraction.get("tables", [])
    ocr = extraction.get("ocr_data", [])
    cross = extraction.get("cross_validation", {})
    log = extraction.get("extraction_log", [])

    pass_rows = []
    for entry in log:
        sid = entry.get("pass", "?")
        strat = entry.get("strategy", "")
        rest = {k: v for k, v in entry.items() if k != "profile"}
        if "profile" in entry and isinstance(entry["profile"], dict):
            rest["profile_pages_sample"] = str(entry["profile"].get("page_types", ""))[:80]
        pass_rows.append(f"| {sid} | `{strat}` | `{json.dumps(rest, default=str)[:240]}` |")

    lines = [
        "## Stage 1: Multi-pass extraction",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| PDF path | `{meta.get('pdf_path', '')}` |",
        f"| Extraction timestamp | {meta.get('extraction_date', '—')} |",
        f"| Total pages extracted | {len(pages)} |",
        f"| Tables extracted | {len(tables)} |",
        f"| OCR / manual-review flags | {len(ocr)} |",
        f"| Cross-validation method | {cross.get('method', '—')} |",
        f"| Cross-validation consistency score | {cross.get('consistency_score', '—')} |",
        f"| Passes logged | {len(log)} |",
        "",
        "### Extraction passes",
        "",
        "| Pass | Strategy | Details |",
        "|------|----------|---------|",
    ]
    lines.extend(pass_rows)
    lines.append("")
    return "\n".join(lines)


def validation_section(qa: MedicalQASystem) -> str:
    v = qa.validation_result or {}
    lines = [
        "## Stage 2: Validation",
        "",
    ]
    overall = v.get("overall", {})
    conf = overall.get("confidence")
    conf_s = f"{conf:.2%}" if isinstance(conf, (int, float)) else str(conf)
    lines.extend(
        [
            "### Overall",
            "",
            f"- **Passed (threshold)**: {overall.get('passed', '—')}",
            f"- **Confidence**: {conf_s}",
            f"- **Needs human review**: {overall.get('needs_human_review', '—')}",
            "",
        ]
    )
    for key in ("structure", "tables", "cross", "medical", "human_review"):
        block = v.get(key)
        if block is None:
            continue
        d = _dataclass_or_dict(block)
        blob = json.dumps(d, indent=2, default=str)
        lines.append(f"### {key.replace('_', ' ').title()}")
        lines.append("")
        lines.append("```json")
        lines.append(blob[:8000])
        if len(blob) > 8000:
            lines.append("... (truncated)")
        lines.append("```")
        lines.append("")
    return "\n".join(lines)


def chunking_section(qa: MedicalQASystem) -> str:
    chunks = qa.chunks or []
    with_tables = sum(1 for c in chunks if c.get("has_tables"))
    lines = [
        "## Stage 3: Chunking + BM25 index",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| Total chunks | {len(chunks)} |",
        f"| Chunks with tables | {with_tables} |",
        "",
        "### Sample chunk headings (first 15)",
        "",
    ]
    for c in chunks[:15]:
        h = str(c.get("heading", ""))[:80]
        lines.append(f"- p.{c.get('page')} — **{h}**")
    lines.append("")
    return "\n".join(lines)


def guardrail_section() -> str:
    return "\n".join(
        [
            "## Stage 4: Guardrail brain",
            "",
            "`MedicalGuardrailBrain` validates each composed answer: triage headings, dangerous patterns, citations vs. chunk pages.",
            "",
        ]
    )


SEARCH_QUERIES = [
    "What is the treatment for uncomplicated Plasmodium falciparum malaria?",
    "Dosing artemisinin-based combination therapy in children under 5",
    "Severe malaria definition and management",
    "When to refer a patient with malaria to hospital?",
    "Pregnancy and malaria treatment recommendations",
    "Drug interactions with artemether lumefantrine",
    "Prophylaxis for travelers to endemic areas",
    "Rapid diagnostic test interpretation false positives",
    "G6PD deficiency and primaquine",
    "Malaria vaccine recommendations RTS,S R21",
    "Resistance to artemisinin in Southeast Asia",
    "Hypoglycemia in severe malaria",
    "Fluid management in severe malaria adults",
    "Exchange transfusion malaria criteria",
    "Cerebral malaria supportive care",
    "Artesunate dose for severe malaria IV",
    "Rectal artesunate pre-referral children",
    "Malaria in HIV coinfection",
    "Species Plasmodium vivax relapse treatment",
    "Monitoring after antimalarial treatment failure",
    "Quality assurance microscopy",
    "Integrated community case management fever",
    "Ethics of placebo-controlled malaria trials",
    "Vector control bed nets IRS",
    "Elimination strategies and surveillance",
]


def searches_section(qa: MedicalQASystem) -> str:
    lines = [
        "## Stage 5: Search & Q&A (25 queries)",
        "",
        "BM25 top-5 excerpts per query; guardrail summary below each.",
        "",
    ]
    for i, q in enumerate(SEARCH_QUERIES, 1):
        result = qa.answer(q)
        resp = result["response"]
        val = result["validation"]
        lines.append(f"### {i}. Query")
        lines.append("")
        lines.append(f"> {q}")
        lines.append("")
        lines.append("**Sources (top hits)**")
        for s in result.get("sources", []):
            h = str(s.get("heading", ""))[:120]
            lines.append(f"- Page {s.get('page')}: {h}")
        lines.append("")
        lines.append("**Response**")
        lines.append("")
        lines.append("```")
        lines.append(resp[:4000])
        if len(resp) > 4000:
            lines.append("\n... [truncated for report length]")
        lines.append("```")
        lines.append("")
        lines.append(
            f"**Guardrail**: passed=`{val.get('passed')}` | "
            f"errors={len(val.get('errors', []))} | warnings={len(val.get('warnings', []))}"
        )
        if val.get("errors"):
            lines.append(f"- Errors: `{val['errors']}`")
        if val.get("warnings"):
            lines.append(f"- Warnings: `{val['warnings'][:5]}`")
        lines.append("")
        lines.append("---")
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--reuse-kb",
        action="store_true",
        help="Load existing KB if present instead of rebuilding.",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help="Markdown output path",
    )
    args = parser.parse_args()

    cfg = extraction_config_who_malaria_nih()
    reports_dir = os.path.join(ROOT, "reports")
    os.makedirs(reports_dir, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    out_path = args.output or os.path.join(
        reports_dir, f"who_malaria_pipeline_report_{ts}.md"
    )

    qa, extraction = load_or_build(cfg, reuse_kb=args.reuse_kb)

    header = "\n".join(
        [
            "# WHO Malaria pipeline run report",
            "",
            f"- **Generated (UTC)**: {datetime.now(timezone.utc).isoformat()}",
            f"- **Preset**: who-malaria (NIH Bookshelf)",
            f"- **PDF**: `{cfg.pdf_path}`",
            f"- **KB output directory**: `{cfg.output_dir}`",
            f"- **Reuse KB flag**: `{args.reuse_kb}`",
            "",
            "---",
            "",
        ]
    )

    body = "\n".join(
        [
            extraction_section(extraction, qa),
            validation_section(qa),
            chunking_section(qa),
            guardrail_section(),
            searches_section(qa),
        ]
    )

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(header + body)

    latest = os.path.join(reports_dir, "who_malaria_pipeline_report.md")
    with open(latest, "w", encoding="utf-8") as f:
        f.write(header + body)

    print(f"Wrote report: {out_path}")
    print(f"Also wrote: {latest}")


if __name__ == "__main__":
    main()
