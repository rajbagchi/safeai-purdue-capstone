"""
SafeAI Conversational Interface.

A plain-language chat interface for VHT workers and health staff to query
clinical guidelines.  No command-line flags needed — just run:

    python3 chat.py

The script auto-detects available knowledge bases, prompts for guideline
selection when more than one is found, then opens a conversational Q&A loop.

Every question goes through the full two-brain pipeline:
  Brain 1 (ResponseOrchestrator)  — retrieves and assembles the answer
  Brain 2 (MedicalGuardrailBrain) — validates safety before display
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Allow running from the project root without installing the package.
sys.path.insert(0, str(Path(__file__).parent))

from pipeline.config import (
    ExtractionConfig,
    extraction_config_uganda_clinical_2023,
    extraction_config_who_malaria_nih,
)
from pipeline.orchestrator import MedicalQASystem
from pipeline.response import TriageLevel

# ---------------------------------------------------------------------------
# Known presets — (display name, config factory function)
# ---------------------------------------------------------------------------

_PRESETS: List[Tuple[str, Any]] = [
    ("Uganda Clinical Guidelines 2023",   extraction_config_uganda_clinical_2023),
    ("WHO Malaria / iCCM Guidelines",     extraction_config_who_malaria_nih),
]

# Additional directories to scan for any knowledge_base.json.
# Left empty by default — preset configs cover standard locations.
# Add paths here if you store KBs in non-standard locations.
_SCAN_DIRS: List[Path] = []


# ---------------------------------------------------------------------------
# KB discovery
# ---------------------------------------------------------------------------

def _find_available_kbs() -> List[Tuple[str, ExtractionConfig]]:
    """Return (display_name, config) for every knowledge base that exists.

    Preset configs are always preferred over auto-discovered directories so
    the correct document title and keyword vocabulary are used.  Auto-discovery
    only adds directories that are not already covered by a preset.
    """
    found: List[Tuple[str, ExtractionConfig]] = []
    seen_abs: set = set()  # resolved absolute paths already added

    # 1. Known presets — these carry the full keyword vocabulary
    for name, config_fn in _PRESETS:
        cfg = config_fn()
        kb = Path(cfg.output_dir) / "knowledge_base.json"
        abs_dir = str(Path(cfg.output_dir).resolve())
        if kb.exists() and abs_dir not in seen_abs:
            found.append((name, cfg))
            seen_abs.add(abs_dir)

    # 2. Auto-discover any other knowledge_base.json files not covered above
    for scan_dir in _SCAN_DIRS:
        if not scan_dir.exists():
            continue
        for kb in sorted(scan_dir.glob("*/knowledge_base.json")):
            abs_dir = str(kb.parent.resolve())
            if abs_dir in seen_abs:
                continue
            cfg = ExtractionConfig(
                pdf_path="",
                output_dir=str(kb.parent),
                document_title=kb.parent.name.replace("_", " ").title(),
            )
            found.append((cfg.document_title, cfg))
            seen_abs.add(abs_dir)

    return found


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------

def _strip_markdown(text: str) -> str:
    """Remove **bold** and *italic* markdown markers for plain terminal display."""
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"\*(.+?)\*",     r"\1", text)
    return text


def _clean_list_items(items: List[str]) -> List[str]:
    """
    Filter and clean a list of text items for plain terminal display.

    - Normalises whitespace (collapses newlines/spaces to one space)
    - Strips stray pipe characters
    - Drops raw table rows (2+ pipe characters)
    - Drops items containing '~' (table cell separator in Uganda guidelines)
    - Drops items with table concatenation artifacts: 'mg(or', ')(', '~', ',~'
    - Drops items shorter than 20 characters (fragments / noise)
    - Drops items longer than 180 characters (concatenated table content)
    - Drops truncated sentences (end on a stop-word like 'the', 'if', 'for')
    - Deduplicates near-identical items (same first 40 characters)
    """
    _TRUNCATION_ENDINGS = re.compile(
        r"\b(the|if|for|and|or|a|an|of|in|to|with|that|this|is|are|be|by)\s*$",
        re.IGNORECASE,
    )
    cleaned: List[str] = []
    seen_prefixes: set = set()

    for item in items:
        item = re.sub(r"\s+", " ", item).strip().strip("|").strip()
        if item.count("|") >= 2:
            continue
        if len(item) < 20 or len(item) > 180:
            continue
        if _TRUNCATION_ENDINGS.search(item):
            continue
        # Near-duplicate check — skip if first 40 chars already seen
        prefix = item[:40].lower()
        if prefix in seen_prefixes:
            continue
        seen_prefixes.add(prefix)
        cleaned.append(item)

    return cleaned


def _triage_header(triage: TriageLevel) -> str:
    if triage == TriageLevel.RED:
        return (
            "╔══════════════════════════════════════════════════╗\n"
            "║  🔴  EMERGENCY — GO TO HEALTH FACILITY NOW        ║\n"
            "╚══════════════════════════════════════════════════╝"
        )
    if triage == TriageLevel.YELLOW:
        return "🟡  URGENT — Go to a health facility today."
    return "🟢  This can be managed at home with the guidance below."


def _format_response(result: Dict[str, Any]) -> str:
    """Format a pipeline result into clean, plain-language terminal output."""
    structured   = result["structured"]
    triage       = result["triage"]
    passed       = result["validation_passed"]
    conf         = structured.confidence_score

    lines: List[str] = []
    sep = "─" * 60

    lines.append("")
    lines.append(sep)
    lines.append(_triage_header(triage))
    lines.append(sep)

    # Step-by-step actions
    # For RED triage: remove any action that suggests home management and
    # relabel the section to make clear these are pre-transport steps.
    _HOME_MGMT_RE = re.compile(
        r"\bat home\b|\bhome treatment\b|\bhome management\b|\bmanage at home\b",
        re.IGNORECASE,
    )
    raw_actions = _clean_list_items(structured.actions)
    if triage == TriageLevel.RED:
        actions = [a for a in raw_actions if not _HOME_MGMT_RE.search(a)]
        action_label = "Steps while arranging referral:"
    else:
        actions = raw_actions
        action_label = "What to do:"
    if actions:
        lines.append("")
        lines.append(action_label)
        for i, action in enumerate(actions, 1):
            lines.append(f"  {i}. {_strip_markdown(action)}")

    # Monitoring / danger signs
    monitoring = _clean_list_items(structured.monitoring)
    danger_signs = _clean_list_items(structured.danger_signs)
    if monitoring:
        lines.append("")
        lines.append("Watch for:")
        for item in monitoring:
            lines.append(f"  • {_strip_markdown(item)}")
    elif danger_signs:
        lines.append("")
        lines.append("Danger signs — refer immediately if you see:")
        for sign in danger_signs:
            lines.append(f"  • {_strip_markdown(sign)}")

    # Referral criteria
    referral = _clean_list_items(structured.referral_criteria)
    if referral:
        lines.append("")
        lines.append("When to refer:")
        for item in referral:
            lines.append(f"  • {_strip_markdown(item)}")

    # Family message
    if structured.family_message:
        lines.append("")
        lines.append("What to tell the family:")
        lines.append(f"  {_strip_markdown(structured.family_message)}")

    # Dosing block (VERBATIM — never strip or alter)
    verbatim_citations = [
        c for c in structured.citations
        if c.get("preservation_level", "").lower() == "verbatim"
    ]
    if verbatim_citations:
        lines.append("")
        lines.append("Exact dosing (do not change these numbers):")
        for c in verbatim_citations[:2]:
            content = c.get("nll") or c.get("text", "")
            if content.strip():
                lines.append("")
                for ln in content.strip().splitlines():
                    lines.append(f"  {ln}")

    # Source citations
    if structured.citations:
        lines.append("")
        lines.append("From the guidelines:")
        for c in structured.citations[:3]:
            page    = c.get("page", "?")
            section = c.get("section", "")
            src     = c.get("source", "")
            if hasattr(src, "value"):
                src = src.value
            line = f"  • Page {page}"
            if section:
                line += f" — {section}"
            lines.append(line)

    # Confidence and safety signals
    lines.append("")
    if conf < 0.6:
        lines.append(
            f"⚠️  Low confidence ({conf:.0%}) — the guidelines may not cover "
            "this topic directly. Verify with a health worker."
        )
    if not passed:
        lines.append(
            "⚠️  Safety check flagged this response. Review carefully before acting."
        )

    lines.append(sep)

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Conversational loop
# ---------------------------------------------------------------------------

def _select_kb(available: List[Tuple[str, ExtractionConfig]]) -> Tuple[str, ExtractionConfig]:
    """Prompt user to choose a knowledge base when multiple are available."""
    print("Which guideline would you like to use?\n")
    for i, (name, _) in enumerate(available, 1):
        print(f"  {i}.  {name}")

    while True:
        try:
            raw = input("\nEnter a number: ").strip()
        except (EOFError, KeyboardInterrupt):
            sys.exit(0)
        if raw.isdigit() and 1 <= int(raw) <= len(available):
            return available[int(raw) - 1]
        print("Please enter one of the numbers above.")


def main() -> None:
    print()
    print("=" * 60)
    print("   SafeAI — Clinical Guidelines Assistant")
    print("=" * 60)
    print()

    # Discover knowledge bases
    available = _find_available_kbs()

    if not available:
        print(
            "No knowledge bases found.\n\n"
            "Run the pipeline first to process a guideline PDF:\n"
            "  python3 run_pipeline.py --preset uganda "
            "--pdf /path/to/Uganda_Clinical_Guidelines_2023.pdf\n"
            "  python3 run_pipeline.py --preset who-malaria "
            "--pdf /path/to/iccm_guidelines.pdf"
        )
        sys.exit(1)

    # Select KB
    if len(available) == 1:
        name, cfg = available[0]
        print(f"Using: {name}\n")
    else:
        name, cfg = _select_kb(available)
        print()

    # Load the knowledge base
    print("Loading knowledge base, please wait...\n")
    qa = MedicalQASystem(config=cfg)
    qa.initialize()

    print("=" * 60)
    print(f"  Ready  |  {name}")
    print("  Type 'quit' at any time to exit.")
    print("=" * 60)

    # Q&A loop
    first_question = True
    while True:
        try:
            if first_question:
                query = input("\nWhat can I help you with today?\n> ").strip()
                first_question = False
            else:
                query = input("\nAnything else I can help with?\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nTake care!")
            break

        if not query:
            continue

        if query.lower() in ("quit", "exit", "q", "bye", "no", "no thanks", "nothing"):
            print("\nTake care!")
            break

        print("\nLooking that up for you...")

        try:
            result = qa.answer_with_response(query)

            # No-match detection using the absolute cross-encoder score
            # stored by the retriever BEFORE min-max normalisation.
            # Normalised scores are useless here — the best chunk always
            # scores 1.0 relative to the others regardless of true relevance.
            # CE logit > 0  = the model thinks query and chunk are related
            # CE logit < 0  = the model thinks they are unrelated
            #
            # Threshold set conservatively at -4.0:
            # ms-marco-MiniLM-L-6-v2 was trained on general web search, not
            # medical text. A logit of -1.5 can simply mean vocabulary mismatch
            # ("appendicitis" query vs "acute abdomen" chunk) — not truly
            # out-of-domain. Genuinely irrelevant queries (weather, sports, etc.)
            # score around -5 to -8. Using -4.0 avoids false "no match" on
            # legitimate medical queries with terminology differences.
            _NO_MATCH_CE_THRESHOLD = -4.0
            chunks = result.get("_retrieved_chunks", [])
            ce_best = chunks[0].get("_ce_best_raw") if chunks else None

            if ce_best is not None and ce_best < _NO_MATCH_CE_THRESHOLD:
                print()
                print("─" * 60)
                print("  No matching guidelines found for this query.")
                print()
                print("  The loaded guidelines do not appear to cover this topic.")
                print("  Please consult a qualified health worker or refer the")
                print("  patient to a health facility.")
                print("─" * 60)
            else:
                print(_format_response(result))
        except Exception as e:
            print(f"\nSomething went wrong: {e}")
            print("Please try rephrasing your question.")


if __name__ == "__main__":
    main()
