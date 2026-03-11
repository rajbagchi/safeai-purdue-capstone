"""
pipeline_config.py — Shared configuration loader for the extraction pipeline.

All disease-specific constants (drug keywords, ground truth, dose ranges,
condition patterns, etc.) live in a JSON config file.  Each stage script
imports `load_config()` and reads from the returned dict instead of
hard-coding malaria-specific values.

Usage in any stage script:
    from pipeline_config import load_config
    CONFIG = load_config()            # uses default or --config flag
    pdf_path = CONFIG["document"]["pdf_path"]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# ─────────────────────────────────────────────────────────────────────────────
# 1.  LOAD / RESOLVE CONFIG PATH
# ─────────────────────────────────────────────────────────────────────────────

_DEFAULT_CONFIG = Path(__file__).resolve().parent / "configs" / "malaria_who_2025.json"


def resolve_config_path() -> Path:
    """Return the config path from --config CLI flag, or the default."""
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--config", type=str, default=None,
                        help="Path to pipeline_config JSON file")
    args, _ = parser.parse_known_args()
    if args.config:
        p = Path(args.config)
        if not p.exists():
            sys.exit(f"ERROR: config file not found: {p}")
        return p
    return _DEFAULT_CONFIG


def load_config(path: Optional[str] = None) -> Dict[str, Any]:
    """Load and return the pipeline configuration dictionary.

    Parameters
    ----------
    path : str or None
        Explicit path to a config JSON file.  If *None*, the path is
        resolved from the ``--config`` CLI flag or falls back to
        ``configs/malaria_who_2025.json``.
    """
    config_path = Path(path) if path else resolve_config_path()
    if not config_path.exists():
        sys.exit(f"ERROR: config file not found: {config_path}")
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    _validate(config)
    return config


# ─────────────────────────────────────────────────────────────────────────────
# 2.  CONVENIENCE ACCESSORS
# ─────────────────────────────────────────────────────────────────────────────

def get_pdf_path(config: Dict) -> str:
    return config["document"]["pdf_path"]


def get_document_title(config: Dict) -> str:
    return config["document"].get("title", "Unknown Document")


def get_ground_truth(config: Dict) -> List[Dict]:
    return config.get("ground_truth", [])


def get_drug_keywords(config: Dict) -> List[str]:
    return config.get("drug_keywords", [])


def get_dosing_keywords(config: Dict) -> List[str]:
    return config.get("dosing_keywords", [])


def get_all_table_keywords(config: Dict) -> List[str]:
    """Merge drug_keywords + dosing_keywords for table classification."""
    return get_dosing_keywords(config) + get_drug_keywords(config)


def get_dose_reference_ranges(config: Dict) -> Dict[str, Tuple[float, float]]:
    """Return {drug_name: (min_mg_per_kg, max_mg_per_kg)}."""
    raw = config.get("dose_reference_ranges", {})
    return {
        drug: (v["min_mg_per_kg"], v["max_mg_per_kg"])
        for drug, v in raw.items()
    }


def get_condition_patterns(config: Dict) -> List[Tuple[str, str]]:
    """Return [(regex_pattern, label), ...] for condition inference."""
    raw = config.get("domain_keywords", {}).get("conditions", [])
    # Each entry is [pattern_str, label]
    return [(pat, label) for pat, label in raw]


def get_biomarker_patterns(config: Dict) -> List[str]:
    return config.get("domain_keywords", {}).get("biomarkers", [])


def get_contraindication_terms(config: Dict) -> List[str]:
    return config.get("domain_keywords", {}).get("contraindication_terms", [])


def get_high_preservation_keywords(config: Dict) -> List[str]:
    return config.get("domain_keywords", {}).get("high_preservation_keywords", [])


def build_contraindication_regex(config: Dict) -> re.Pattern:
    """Build a compiled regex from the config's contraindication terms."""
    terms = get_contraindication_terms(config)
    if not terms:
        return re.compile(r"(?!)")  # matches nothing
    pattern = "|".join(re.escape(t) for t in terms)
    return re.compile(pattern, re.IGNORECASE)


def build_high_preservation_regex(config: Dict) -> re.Pattern:
    """Build a compiled regex from the config's high-preservation keywords."""
    kws = get_high_preservation_keywords(config)
    if not kws:
        return re.compile(r"(?!)")
    # Some entries use regex-like patterns (e.g. "mg/kg"), escape them
    pattern = "|".join(re.escape(k) for k in kws)
    return re.compile(pattern, re.IGNORECASE)


def get_benchmark_pages(config: Dict) -> Tuple[int, ...]:
    """Return benchmark page tuple for Stage 1."""
    pages = config.get("processing", {}).get("benchmark_pages", [])
    if pages == "auto" or not pages:
        return ()
    return tuple(pages)


def get_dosing_pages(config: Dict) -> Any:
    """Return dosing pages list or 'auto'."""
    return config.get("cross_validation", {}).get("dosing_pages", "auto")


def get_source_pdf_label(config: Dict) -> str:
    """Human-readable label like 'B09514-eng.pdf (478 pages)'."""
    doc = config["document"]
    pdf = doc["pdf_path"]
    pc = doc.get("page_count", "")
    return f"{pdf} ({pc} pages)" if pc else pdf


# ─────────────────────────────────────────────────────────────────────────────
# 3.  VALIDATION
# ─────────────────────────────────────────────────────────────────────────────

_REQUIRED_KEYS = ["document"]


def _validate(config: Dict) -> None:
    """Minimal schema validation — fail fast on missing required keys."""
    for key in _REQUIRED_KEYS:
        if key not in config:
            sys.exit(f"ERROR: config missing required key: '{key}'")
    doc = config["document"]
    if "pdf_path" not in doc:
        sys.exit("ERROR: config['document'] must contain 'pdf_path'")
