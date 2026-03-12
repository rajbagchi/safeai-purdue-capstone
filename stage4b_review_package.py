#!/usr/bin/env python3
"""
Stage 4b — Clinical Verification Framework
===========================================
Safe AI Uganda · Purdue Capstone

Generates a physician review package from Stage 4a chunks so an IDI
physician can verify safety-critical content against the source PDF.

Two modes:
  Generate (default):  python stage4b_review_package.py
      → extraction_output/review_package.json
      → extraction_output/physician_review_report.md

  Ingest:  python stage4b_review_package.py --ingest completed_review.json
      → validates completed review, computes digital signatures,
        updates extraction_output/chunks.json with verified_by fields

Safety rule: No content proceeds to Phase B (Deployment) without
a verified_by signature and audit_hash.
"""

# ═══════════════════════════════════════════════════════════════════
# 1. IMPORTS
# ═══════════════════════════════════════════════════════════════════

import os
import re
import json
import time
import hashlib
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timezone

from pipeline_config import (
    load_config, get_document_title, get_source_pdf_label,
    get_contraindication_terms, build_contraindication_regex,
    get_output_dir,
)

# ═══════════════════════════════════════════════════════════════════
# 2. CONFIGURATION
# ═══════════════════════════════════════════════════════════════════

CONFIG = load_config()
BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / get_output_dir(CONFIG)
CHUNKS_PATH = OUTPUT_DIR / "chunks.json"
REVIEW_PKG_PATH = OUTPUT_DIR / "review_package.json"
PHYSICIAN_REPORT_PATH = OUTPUT_DIR / "physician_review_report.md"

# Context preview length for surrounding narratives
CONTEXT_PREVIEW_CHARS = 500

# Tiers
MANDATORY_TIERS = [1, 2, 3]
RECOMMENDED_TIERS = [4]
OPTIONAL_TIERS = [5]

# Review decisions
DECISIONS = ["approved", "flagged", "corrected"]

# Per-check statuses
CHECK_STATUSES = ["pass", "fail", "not_applicable", "corrected"]

# The 5 Clinical Verification Checks
CHECK_DEFINITIONS = {
    "dosage_accuracy": {
        "name": "Dosage Accuracy",
        "description": "Dose values match source PDF exactly (e.g., '80+480 mg', '1 tablet').",
        "check_number": 1,
    },
    "stratification": {
        "name": "Stratification",
        "description": "Age/weight ranges are preserved — no merged or missing rows.",
        "check_number": 2,
    },
    "contraindications": {
        "name": "Contraindications",
        "description": "Warnings are present (e.g., 'Do not use in first trimester').",
        "check_number": 3,
    },
    "conditional_logic": {
        "name": "Conditional Logic",
        "description": "IF/THEN referral logic is intact (e.g., NLL dosing rules, danger sign criteria).",
        "check_number": 4,
    },
    "provenance": {
        "name": "Provenance",
        "description": "Source page number and section citation are correctly cited.",
        "check_number": 5,
    },
}

# Check applicability by chunk_type
# True = always applicable, "conditional" = applicable if content matches
CHECK_APPLICABILITY = {
    "dosing_table": {
        "dosage_accuracy": True,
        "stratification": True,
        "contraindications": True,
        "conditional_logic": True,
        "provenance": True,
    },
    "clinical_table": {
        "dosage_accuracy": True,
        "stratification": True,
        "contraindications": True,
        "conditional_logic": True,
        "provenance": True,
    },
    "evidence_table": {
        "dosage_accuracy": False,
        "stratification": False,
        "contraindications": False,
        "conditional_logic": False,
        "provenance": True,
    },
    "narrative": {
        "dosage_accuracy": "conditional",
        "stratification": "conditional",
        "contraindications": "conditional",
        "conditional_logic": "conditional",
        "provenance": True,
    },
    "image": {
        "dosage_accuracy": "conditional",
        "stratification": "conditional",
        "contraindications": "conditional",
        "conditional_logic": "conditional",
        "provenance": True,
    },
}

# Tier definitions
TIER_DEFINITIONS = {
    1: {
        "label": "Validated dosing tables",
        "review_requirement": "mandatory",
        "description": "Passed all 6 Stage 3 automated plausibility checks. Physician confirms extraction accuracy.",
        "est_minutes_per_chunk": 2,
    },
    2: {
        "label": "Unvalidated dosing tables",
        "review_requirement": "mandatory",
        "description": "NOT validated by Stage 3 automated checks (no weight column or skipped). Extra care required.",
        "est_minutes_per_chunk": 2,
    },
    3: {
        "label": "Clinical management tables",
        "review_requirement": "mandatory",
        "description": "Safety-critical clinical management content. Full manual review required.",
        "est_minutes_per_chunk": 2,
    },
    4: {
        "label": "Evidence tables + high-priority narratives",
        "review_requirement": "recommended",
        "description": "Contains clinical thresholds, dosing keywords, or contraindication information.",
        "est_minutes_per_chunk": 0.5,
    },
    5: {
        "label": "Standard chunks",
        "review_requirement": "optional",
        "description": "General narrative, structural tables, images. No safety-critical content.",
        "est_minutes_per_chunk": 0,
    },
}

# Keywords for conditional check applicability on narratives
DOSAGE_KEYWORDS_RE = re.compile(
    r"mg/kg|mg\s*/\s*kg|tablet|dose|dosing|dosage|\d+\s*\+\s*\d+\s*mg",
    re.IGNORECASE,
)
STRATIFICATION_KEYWORDS_RE = re.compile(
    r"weight|kg|age|year|month|infant|child|adult|pediatric|neonate",
    re.IGNORECASE,
)
CONTRAINDICATION_KEYWORDS_RE = build_contraindication_regex(CONFIG)
CONDITIONAL_LOGIC_KEYWORDS_RE = re.compile(
    r"\bif\b.*\bthen\b|refer|danger sign|emergency|severe|failure|"
    r"switch to|escalate|hospitalize",
    re.IGNORECASE,
)

# Source document identifier (from config)
SOURCE_DOCUMENT = get_document_title(CONFIG)
SOURCE_PDF = get_source_pdf_label(CONFIG)


# ═══════════════════════════════════════════════════════════════════
# 3. DATA LOADING
# ═══════════════════════════════════════════════════════════════════

def load_chunks(path: Path = CHUNKS_PATH) -> Tuple[Dict, List[Dict]]:
    """Load chunks.json and return (envelope_metadata, chunks_list)."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    chunks = data.pop("chunks")
    envelope = data  # everything except chunks
    return envelope, chunks


def build_chunk_lookup(chunks: List[Dict]) -> Dict[str, Dict]:
    """Build {chunk_id: chunk} lookup for context resolution."""
    return {c["chunk_id"]: c for c in chunks}


# ═══════════════════════════════════════════════════════════════════
# 4. AUDIT HASH COMPUTATION
# ═══════════════════════════════════════════════════════════════════

def compute_audit_hash(content: str) -> str:
    """SHA-256 of the chunk's content field.

    This hash locks the extraction text so any post-extraction tampering
    is detectable at review-ingestion time.
    """
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def compute_content_hash(chunk: Dict) -> str:
    """SHA-256 of the full chunk JSON (all metadata included).

    Used as a secondary integrity check — ensures the full metadata
    envelope wasn't altered between generation and review.
    """
    serialized = json.dumps(chunk, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def compute_digital_signature(
    reviewer_name: str,
    institution: str,
    chunk_id: str,
    audit_hash: str,
    reviewed_at: str,
) -> str:
    """Compute a tamper-evident digital signature.

    SHA-256 of (reviewer_name | institution | chunk_id | audit_hash | reviewed_at).
    Creates a verifiable link between reviewer identity and the specific
    review action on a specific chunk at a specific time.
    """
    payload = "|".join([reviewer_name, institution, chunk_id, audit_hash, reviewed_at])
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


# ═══════════════════════════════════════════════════════════════════
# 5. REVIEW TRIAGE
# ═══════════════════════════════════════════════════════════════════

def classify_chunk_tier(chunk: Dict) -> int:
    """Assign a review tier (1–5) to a chunk.

    Tier 1: Dosing table with passing Stage 3 validation
    Tier 2: Dosing table without passing validation (skipped / not applicable)
    Tier 3: Clinical management table
    Tier 4: Evidence table OR high-preservation narrative
    Tier 5: Everything else (standard preservation)
    """
    ct = chunk["chunk_type"]
    validation = chunk.get("validation") or {}
    preservation = chunk.get("safety", {}).get("preservation_level", "standard")

    # Tier 1: validated dosing tables (passed all Stage 3 checks)
    if ct == "dosing_table" and validation.get("status") == "pass":
        return 1

    # Tier 2: unvalidated dosing tables (skipped, not_applicable, or no validation)
    if ct == "dosing_table":
        return 2

    # Tier 3: clinical management tables
    if ct == "clinical_table":
        return 3

    # Tier 3 (catch-all): other_table with LOC or danger sign content
    if ct == "other_table":
        cm = chunk.get("clinical_metadata") or {}
        if cm.get("level_of_care") or cm.get("danger_signs"):
            return 3

    # Tier 4: evidence tables + high/verbatim-preservation narratives/images
    if ct == "evidence_table":
        return 4
    if ct == "narrative" and preservation in ("high", "verbatim"):
        return 4
    if ct == "image" and preservation in ("high", "verbatim"):
        return 4

    # Tier 5: everything else
    return 5


def determine_applicable_checks(chunk: Dict) -> Dict[str, Dict]:
    """Determine which of the 5 checks apply to this chunk.

    Returns {check_key: {"applicable": bool, "guidance": str}}.
    """
    ct = chunk["chunk_type"]
    content = chunk.get("content", "")
    pages = chunk.get("source_pages", [])
    section_num = chunk.get("section_number", "")
    section_title = chunk.get("section_title", "")
    drug_name = (chunk.get("clinical_metadata") or {}).get("drug_name", "")
    page_str = ", ".join(str(p) for p in pages) if pages else "unknown"
    section_str = f"{section_num} {section_title}".strip() if section_num else section_title

    # Get base applicability for this chunk type
    base = CHECK_APPLICABILITY.get(ct, CHECK_APPLICABILITY.get("narrative", {}))

    result = {}
    for check_key, check_def in CHECK_DEFINITIONS.items():
        base_val = base.get(check_key, False)

        # Resolve conditional applicability for narratives
        if base_val == "conditional":
            if check_key == "dosage_accuracy":
                applicable = bool(DOSAGE_KEYWORDS_RE.search(content))
            elif check_key == "stratification":
                applicable = bool(STRATIFICATION_KEYWORDS_RE.search(content))
            elif check_key == "contraindications":
                applicable = bool(CONTRAINDICATION_KEYWORDS_RE.search(content))
            elif check_key == "conditional_logic":
                applicable = bool(CONDITIONAL_LOGIC_KEYWORDS_RE.search(content))
            else:
                applicable = False
        else:
            applicable = bool(base_val)

        # Build guidance string
        if applicable:
            guidance = _build_guidance(check_key, ct, page_str, section_str, drug_name, chunk)
        else:
            guidance = "Not applicable for this chunk type/content."

        result[check_key] = {
            "applicable": applicable,
            "guidance": guidance,
        }

    return result


def _build_guidance(
    check_key: str, chunk_type: str, page_str: str, section_str: str,
    drug_name: str, chunk: Dict,
) -> str:
    """Build human-readable guidance for a specific check on a specific chunk."""
    drug_ref = f" for {drug_name}" if drug_name else ""

    if check_key == "dosage_accuracy":
        if chunk_type == "dosing_table":
            return f"Verify each weight band's dose{drug_ref} matches WHO guidelines source PDF page {page_str}."
        return f"Verify any dose values mentioned match source PDF page {page_str}."

    if check_key == "stratification":
        if chunk_type == "dosing_table":
            cm = chunk.get("clinical_metadata") or {}
            w_min = cm.get("patient_weight_min_kg")
            w_max = cm.get("patient_weight_max_kg")
            weight_ref = ""
            if w_min is not None or w_max is not None:
                weight_ref = f" (extracted range: {w_min}–{w_max} kg)"
            return f"Confirm weight/age bands cover the full intended population{weight_ref}; no merged or missing rows."
        return "Confirm any age/weight stratifications mentioned are correctly preserved."

    if check_key == "contraindications":
        cm = chunk.get("clinical_metadata") or {}
        existing = cm.get("contraindications", [])
        sp = cm.get("special_populations", [])
        dangers = cm.get("danger_signs", [])
        hints = []
        if existing:
            hints.append(f"Extracted contraindications: {', '.join(existing)}")
        if sp:
            hints.append(f"Special populations: {', '.join(sp)}")
        if dangers:
            hints.append(f"Danger signs: {', '.join(d[:60] for d in dangers[:3])}")
        base = "Check for warnings, danger signs, and referral criteria."
        if hints:
            base += " " + "; ".join(hints) + "."
        return base

    if check_key == "conditional_logic":
        has_nll = bool(chunk.get("nll"))
        cm = chunk.get("clinical_metadata") or {}
        loc = cm.get("level_of_care", [])
        if has_nll:
            return "Verify that the NLL (Natural Language Logic) correctly represents the weight→dose mapping from the table."
        if loc:
            return f"Verify Level of Care assignments ({', '.join(loc)}) match the source PDF. Confirm referral pathways between facility levels are intact."
        return "Verify any IF/THEN logic, referral criteria, or decision pathways are intact."

    if check_key == "provenance":
        return f"Confirm source page {page_str} and section {section_str} match the printed WHO guidelines."

    return "Review this check against the source PDF."


def triage_all_chunks(chunks: List[Dict]) -> Tuple[Dict[int, List[str]], Dict[str, int]]:
    """Classify all chunks into tiers.

    Returns:
        tier_groups: {tier_number: [chunk_ids]}
        chunk_tiers: {chunk_id: tier_number}
    """
    tier_groups: Dict[int, List[str]] = {1: [], 2: [], 3: [], 4: [], 5: []}
    chunk_tiers: Dict[str, int] = {}

    for chunk in chunks:
        tier = classify_chunk_tier(chunk)
        tier_groups[tier].append(chunk["chunk_id"])
        chunk_tiers[chunk["chunk_id"]] = tier

    return tier_groups, chunk_tiers


# ═══════════════════════════════════════════════════════════════════
# 6. REVIEW TEMPLATE GENERATION
# ═══════════════════════════════════════════════════════════════════

def get_context_preview(
    chunk: Dict, chunk_lookup: Dict[str, Dict], max_chars: int = CONTEXT_PREVIEW_CHARS,
) -> Dict[str, Optional[str]]:
    """Retrieve preceding/following narrative content previews."""
    related = chunk.get("related_chunks") or {}
    result = {
        "preceding_narrative_id": None,
        "preceding_narrative_preview": None,
        "following_narrative_id": None,
        "following_narrative_preview": None,
    }

    prec_id = related.get("preceding_narrative")
    if prec_id and prec_id in chunk_lookup:
        result["preceding_narrative_id"] = prec_id
        text = chunk_lookup[prec_id].get("content", "")
        result["preceding_narrative_preview"] = text[:max_chars].strip()

    foll_id = related.get("following_narrative")
    if foll_id and foll_id in chunk_lookup:
        result["following_narrative_id"] = foll_id
        text = chunk_lookup[foll_id].get("content", "")
        result["following_narrative_preview"] = text[:max_chars].strip()

    return result


def format_validation_summary(validation: Optional[Dict]) -> str:
    """Format Stage 3 validation into a human-readable string."""
    if not validation:
        return "No validation data"

    status = validation.get("status", "unknown")
    if status == "pass":
        passed = validation.get("checks_passed", "?")
        total = validation.get("checks_total", "?")
        bands = validation.get("weight_bands", "?")
        return f"Pass ({passed}/{total} automated checks, {bands} weight bands)"
    elif status == "skipped":
        reason = validation.get("reason", "unknown reason")
        return f"Skipped ({reason})"
    elif status == "fail":
        passed = validation.get("checks_passed", "?")
        total = validation.get("checks_total", "?")
        issues = validation.get("issues", [])
        issue_str = "; ".join(issues[:3]) if issues else "see details"
        return f"Fail ({passed}/{total} checks; {issue_str})"
    elif status == "not_applicable":
        return "Not applicable (non-weight-based table)"
    else:
        return f"Unknown ({status})"


def format_section_path(hierarchy: List[str]) -> str:
    """Format section_hierarchy into a readable path string."""
    if not hierarchy:
        return "Unknown section"
    return " > ".join(hierarchy)


def create_review_item(
    chunk: Dict,
    tier: int,
    applicable_checks: Dict,
    chunk_lookup: Dict[str, Dict],
) -> Dict:
    """Create a single review item with all context for physician review."""
    tier_def = TIER_DEFINITIONS[tier]
    cm = chunk.get("clinical_metadata") or {}

    # Compute audit hash
    audit_hash = compute_audit_hash(chunk["content"])
    content_hash = compute_content_hash(chunk)

    # Build context
    context = get_context_preview(chunk, chunk_lookup)

    # Build tier label
    if tier == 1:
        val = chunk.get("validation") or {}
        passed = val.get("checks_passed", "?")
        total = val.get("checks_total", "?")
        tier_label = f"Validated dosing table (Stage 3: {passed}/{total} checks pass)"
    elif tier == 2:
        tier_label = "Unvalidated dosing table (Stage 3 skipped — no automated validation)"
    elif tier == 3:
        tier_label = "Clinical management table — safety-critical content"
    elif tier == 4:
        ct = chunk["chunk_type"]
        if ct == "evidence_table":
            tier_label = "Evidence table — clinical facts must be preserved"
        else:
            tier_label = "High-priority narrative — contains dosing or contraindication information"
    else:
        tier_label = "Standard chunk — general content"

    # Determine review priority
    if tier in MANDATORY_TIERS:
        review_priority = "mandatory"
    elif tier in RECOMMENDED_TIERS:
        review_priority = "recommended"
    else:
        review_priority = "optional"

    return {
        "chunk_id": chunk["chunk_id"],
        "review_priority": review_priority,
        "review_tier": tier,
        "tier_label": tier_label,
        "preservation_level": chunk.get("safety", {}).get("preservation_level", "standard"),
        "chunk_type": chunk["chunk_type"],
        "source_pages": chunk.get("source_pages", []),
        "section_path": format_section_path(chunk.get("section_hierarchy", [])),
        "section_number": chunk.get("section_number"),
        "section_title": chunk.get("section_title", ""),
        "clinical_domain": chunk.get("clinical_domain"),
        "content": chunk["content"],
        "audit_hash": audit_hash,
        "content_hash": content_hash,
        "clinical_metadata": cm,
        "validation_summary": format_validation_summary(chunk.get("validation")),
        "nll": chunk.get("nll"),
        "context": context,
        "applicable_checks": applicable_checks,
        "review": {
            "checks": {
                key: {"status": None, "notes": None}
                for key in CHECK_DEFINITIONS
            },
            "overall_decision": None,
            "corrections": None,
            "reviewer_name": None,
            "reviewer_role": None,
            "institution": None,
            "reviewed_at": None,
            "digital_signature": None,
        },
    }


# ═══════════════════════════════════════════════════════════════════
# 7. REVIEW PACKAGE ASSEMBLY
# ═══════════════════════════════════════════════════════════════════

def assemble_review_package(
    chunks: List[Dict],
    chunk_lookup: Dict[str, Dict],
    tier_groups: Dict[int, List[str]],
    chunk_tiers: Dict[str, int],
) -> Dict:
    """Assemble the complete review package JSON."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # Build review items for tiers 1–4 (skip tier 5 — optional, not included in package)
    review_items = []
    for tier in [1, 2, 3, 4]:
        for cid in tier_groups[tier]:
            chunk = chunk_lookup[cid]
            checks = determine_applicable_checks(chunk)
            item = create_review_item(chunk, tier, checks, chunk_lookup)
            review_items.append(item)

    # Summary counts
    tier_counts = {t: len(ids) for t, ids in tier_groups.items()}
    mandatory_count = sum(tier_counts.get(t, 0) for t in MANDATORY_TIERS)
    recommended_count = sum(tier_counts.get(t, 0) for t in RECOMMENDED_TIERS)

    # Estimated review time
    est_minutes = sum(
        tier_counts.get(t, 0) * TIER_DEFINITIONS[t]["est_minutes_per_chunk"]
        for t in [1, 2, 3, 4]
    )

    # Review instructions
    review_instructions = (
        "This review package contains extracted clinical content from the WHO "
        "Consolidated Malaria Guidelines (B09514-eng.pdf, 478 pages). Each item "
        "must be verified against the source PDF using the 5 Clinical Verification "
        "Checks described below.\n\n"
        "THE 5 CLINICAL VERIFICATION CHECKS:\n"
        "1. Dosage Accuracy — Dose values match source PDF exactly.\n"
        "2. Stratification — Age/weight ranges are preserved; no merged or missing rows.\n"
        "3. Contraindications — Warnings are present where expected.\n"
        "4. Conditional Logic — IF/THEN referral logic is intact.\n"
        "5. Provenance — Source page and section are correctly cited.\n\n"
        "REVIEW WORKFLOW:\n"
        "For each item, evaluate each applicable check and then record an overall decision:\n"
        "  - 'approved' — All checks pass; content is accurate.\n"
        "  - 'flagged' — One or more checks fail; requires attention before deployment.\n"
        "  - 'corrected' — Content was incorrect; corrections noted in the corrections field.\n\n"
        "MANDATORY items (Tiers 1–3) MUST be reviewed before any content proceeds to deployment.\n"
        "RECOMMENDED items (Tier 4) SHOULD be reviewed for additional clinical safety assurance.\n\n"
        "SAFETY RULE: No content proceeds to Phase B (Deployment) without a verified_by "
        "signature and audit_hash."
    )

    package = {
        "pipeline_version": "4b",
        "source_document": SOURCE_DOCUMENT,
        "source_pdf": SOURCE_PDF,
        "generated_at": now,
        "review_instructions": review_instructions,
        "review_workflow": {
            "decisions": DECISIONS,
            "check_statuses": CHECK_STATUSES,
            "checks": {
                key: {
                    "check_number": defn["check_number"],
                    "name": defn["name"],
                    "description": defn["description"],
                }
                for key, defn in CHECK_DEFINITIONS.items()
            },
            "safety_rule": (
                "No content proceeds to Phase B (Deployment) without "
                "a verified_by signature and audit_hash."
            ),
        },
        "summary": {
            "total_chunks_in_pipeline": len(chunks),
            "total_review_items": len(review_items),
            "mandatory_review": mandatory_count,
            "recommended_review": recommended_count,
            "not_included_optional": tier_counts.get(5, 0),
            "estimated_review_time_minutes": round(est_minutes, 1),
            "by_tier": {
                str(t): {
                    "count": tier_counts.get(t, 0),
                    "label": TIER_DEFINITIONS[t]["label"],
                    "requirement": TIER_DEFINITIONS[t]["review_requirement"],
                }
                for t in [1, 2, 3, 4, 5]
            },
        },
        "review_items": review_items,
    }

    return package


# ═══════════════════════════════════════════════════════════════════
# 8. PHYSICIAN-READABLE REPORT (MARKDOWN)
# ═══════════════════════════════════════════════════════════════════

def format_review_item_markdown(item: Dict, item_number: int) -> str:
    """Render one review item as a markdown section."""
    lines = []
    cid = item["chunk_id"]
    ct = item["chunk_type"]
    pages = item["source_pages"]
    page_str = ", ".join(str(p) for p in pages) if pages else "?"
    section_title = item.get("section_title", "")
    section_num = item.get("section_number", "")
    section_ref = f"{section_num} {section_title}".strip() if section_num else section_title
    cm = item.get("clinical_metadata") or {}
    drug = cm.get("drug_name", "")
    condition = cm.get("condition", "")
    nll = item.get("nll")
    val_summary = item.get("validation_summary", "")
    context = item.get("context", {})

    # Header
    if drug:
        lines.append(f"### {item_number}. {cid} — {drug}")
    else:
        lines.append(f"### {item_number}. {cid}")

    # Metadata line
    meta_parts = [f"**Pages:** {page_str}"]
    if section_ref:
        meta_parts.append(f"**Section:** {section_ref}")
    lines.append(" | ".join(meta_parts))

    # Validation + clinical metadata
    detail_parts = []
    if val_summary:
        if "Pass" in val_summary:
            detail_parts.append(f"**Validation:** ✅ {val_summary}")
        elif "Fail" in val_summary:
            detail_parts.append(f"**Validation:** ❌ {val_summary}")
        elif "Skipped" in val_summary:
            detail_parts.append(f"**Validation:** ⚠️ {val_summary}")
        else:
            detail_parts.append(f"**Validation:** {val_summary}")
    if condition:
        detail_parts.append(f"**Condition:** {condition}")

    weight_min = cm.get("patient_weight_min_kg")
    weight_max = cm.get("patient_weight_max_kg")
    if weight_min is not None or weight_max is not None:
        w_str = f"{weight_min}–{weight_max} kg" if weight_max else f"{weight_min}+ kg"
        detail_parts.append(f"**Weight range:** {w_str}")

    freq = cm.get("frequency", "")
    dur = cm.get("duration", "")
    route = cm.get("route", "")
    dosage_parts = [x for x in [freq, dur, route] if x]
    if dosage_parts:
        detail_parts.append(f"**Dosage:** {', '.join(dosage_parts)}")

    if detail_parts:
        lines.append(" | ".join(detail_parts))

    lines.append("")

    # Audit hash
    lines.append(f"**Audit hash:** `{item['audit_hash'][:16]}...`")
    lines.append("")

    # Content
    lines.append("#### Extracted Content")
    lines.append("```")
    lines.append(item["content"])
    lines.append("```")
    lines.append("")

    # NLL (for dosing tables)
    if nll:
        lines.append("#### Natural Language Logic (NLL)")
        lines.append("```")
        lines.append(nll)
        lines.append("```")
        lines.append("")

    # Context
    prec_preview = context.get("preceding_narrative_preview")
    foll_preview = context.get("following_narrative_preview")
    if prec_preview or foll_preview:
        lines.append("#### Clinical Context")
        if prec_preview:
            prec_id = context.get("preceding_narrative_id", "")
            lines.append(f"> **Before this item** ({prec_id}): {prec_preview}")
            lines.append(">")
        if foll_preview:
            foll_id = context.get("following_narrative_id", "")
            lines.append(f"> **After this item** ({foll_id}): {foll_preview}")
        lines.append("")

    # Contraindications / special populations from metadata
    contras = cm.get("contraindications", [])
    specials = cm.get("special_populations", [])
    if contras or specials:
        lines.append("#### Extracted Clinical Flags")
        if contras:
            lines.append(f"- **Contraindications:** {', '.join(contras)}")
        if specials:
            lines.append(f"- **Special populations:** {', '.join(specials)}")
        lines.append("")

    # Verification checklist
    lines.append("#### Verification Checklist")
    applicable = item.get("applicable_checks", {})
    for check_key, check_def in CHECK_DEFINITIONS.items():
        check_info = applicable.get(check_key, {})
        if check_info.get("applicable", False):
            guidance = check_info.get("guidance", "")
            lines.append(f"- [ ] **{check_def['name']}** — {guidance}")
        else:
            lines.append(f"- ~~**{check_def['name']}**~~ — Not applicable")
    lines.append("")

    # Decision
    lines.append("**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected")
    lines.append("")
    lines.append("**Reviewer notes:** _____")
    lines.append("")
    lines.append("**Corrections (if any):** _____")
    lines.append("")
    lines.append("---")
    lines.append("")

    return "\n".join(lines)


def generate_physician_report(
    package: Dict, chunk_lookup: Dict[str, Dict],
) -> str:
    """Generate the complete physician-readable markdown review report."""
    lines = []
    now = package["generated_at"]
    summary = package["summary"]

    # ── Header ──
    lines.append("# Clinical Verification Report — WHO Consolidated Malaria Guidelines")
    lines.append("## Stage 4b: Physician Review Package")
    lines.append("")
    lines.append(f"**Generated:** {now} | **Pipeline version:** 4b")
    lines.append(f"**Source:** {SOURCE_PDF}")
    lines.append(
        "**Safety rule:** No content proceeds to deployment without "
        "`verified_by` signature + `audit_hash`."
    )
    lines.append("")
    lines.append("---")
    lines.append("")

    # ── Instructions ──
    lines.append("## How to Use This Document")
    lines.append("")
    lines.append("1. Review each item against the **5 Clinical Verification Checks**:")
    for check_key, check_def in CHECK_DEFINITIONS.items():
        lines.append(f"   - **{check_def['name']}**: {check_def['description']}")
    lines.append("2. For each check, mark: ✅ Pass | ❌ Fail | ⚠️ Corrected | — Not applicable")
    lines.append("3. Record your **overall decision**: Approved / Flagged / Corrected")
    lines.append("4. Enter corrections in the notes field if flagging or correcting")
    lines.append("5. Fill in your reviewer details (name, role, institution, date)")
    lines.append("")
    lines.append("---")
    lines.append("")

    # ── Summary table ──
    lines.append("## Review Summary")
    lines.append("")
    lines.append("| Tier | Description | Chunks | Priority | Est. Time |")
    lines.append("|---|---|---|---|---|")
    for t in [1, 2, 3, 4]:
        td = TIER_DEFINITIONS[t]
        count = summary["by_tier"][str(t)]["count"]
        est = count * td["est_minutes_per_chunk"]
        if est >= 60:
            time_str = f"~{est/60:.1f} hrs"
        else:
            time_str = f"~{est:.0f} min"
        lines.append(
            f"| {t}. {td['label']} | {td['description'][:60]}{'...' if len(td['description']) > 60 else ''} "
            f"| {count} | {td['review_requirement'].capitalize()} | {time_str} |"
        )
    mandatory_total = summary["mandatory_review"]
    mandatory_est = sum(
        summary["by_tier"][str(t)]["count"] * TIER_DEFINITIONS[t]["est_minutes_per_chunk"]
        for t in MANDATORY_TIERS
    )
    lines.append(f"| **Total mandatory** | | **{mandatory_total}** | | **~{mandatory_est:.0f} min** |")
    lines.append("")
    lines.append(
        f"**Total review items:** {summary['total_review_items']} "
        f"(mandatory: {summary['mandatory_review']}, "
        f"recommended: {summary['recommended_review']}). "
        f"Optional chunks not included: {summary['not_included_optional']}."
    )
    lines.append("")
    lines.append("---")
    lines.append("")

    # ── Group items by tier ──
    items_by_tier: Dict[int, List[Dict]] = {1: [], 2: [], 3: [], 4: []}
    for item in package["review_items"]:
        t = item["review_tier"]
        if t in items_by_tier:
            items_by_tier[t].append(item)

    # ── Tier 1 ──
    tier1 = items_by_tier[1]
    if tier1:
        lines.append(f"## TIER 1 — Validated Dosing Tables ({len(tier1)} chunks) — MANDATORY REVIEW")
        lines.append("")
        lines.append(
            "> These tables passed all 6 automated plausibility checks (Stage 3). "
            "The physician confirms extraction accuracy against the source PDF."
        )
        lines.append("")
        for i, item in enumerate(tier1, 1):
            lines.append(format_review_item_markdown(item, i))

    # ── Tier 2 ──
    tier2 = items_by_tier[2]
    if tier2:
        lines.append(f"## TIER 2 — Unvalidated Dosing Tables ({len(tier2)} chunks) — MANDATORY REVIEW")
        lines.append("")
        lines.append(
            "> ⚠️ These tables were NOT validated by Stage 3 automated checks "
            "(no weight column identified or checks not applicable). "
            "Extra care required — verify all values against the source PDF."
        )
        lines.append("")
        for i, item in enumerate(tier2, len(tier1) + 1):
            lines.append(format_review_item_markdown(item, i))

    # ── Tier 3 ──
    tier3 = items_by_tier[3]
    if tier3:
        lines.append(f"## TIER 3 — Clinical Management Tables ({len(tier3)} chunk) — MANDATORY REVIEW")
        lines.append("")
        lines.append(
            "> Safety-critical clinical management content. "
            "Full manual review required — no automated validation was performed."
        )
        lines.append("")
        offset = len(tier1) + len(tier2)
        for i, item in enumerate(tier3, offset + 1):
            lines.append(format_review_item_markdown(item, i))

    # ── Tier 4 ──
    tier4 = items_by_tier[4]
    if tier4:
        lines.append(
            f"## TIER 4 — Evidence Tables + High-Priority Narratives "
            f"({len(tier4)} chunks) — RECOMMENDED REVIEW"
        )
        lines.append("")
        lines.append(
            "> Contains clinical thresholds, dosing keywords, or contraindication "
            "information. Recommended review for additional clinical safety assurance."
        )
        lines.append("")

        # Group tier 4 by section for efficient review
        section_groups: Dict[str, List[Tuple[int, Dict]]] = {}
        offset = len(tier1) + len(tier2) + len(tier3)
        for i, item in enumerate(tier4, offset + 1):
            section = item.get("section_path", "Unknown")
            if section not in section_groups:
                section_groups[section] = []
            section_groups[section].append((i, item))

        for section_path, items in section_groups.items():
            lines.append(f"### Section: {section_path}")
            lines.append("")
            for item_num, item in items:
                lines.append(format_review_item_markdown(item, item_num))

    # ── Appendix ──
    lines.append("---")
    lines.append("")
    lines.append("## Appendix: Reviewer Sign-Off")
    lines.append("")
    lines.append("Upon completing the review, please fill in the following:")
    lines.append("")
    lines.append("| Field | Value |")
    lines.append("|---|---|")
    lines.append("| **Reviewer name** | _____ |")
    lines.append("| **Reviewer role** | _____ |")
    lines.append("| **Institution** | _____ |")
    lines.append("| **Date** | _____ |")
    lines.append("| **Signature** | _____ |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Appendix: Glossary")
    lines.append("")
    lines.append("| Term | Meaning |")
    lines.append("|---|---|")
    lines.append("| **ACT** | Artemisinin-based combination therapy |")
    lines.append("| **NLL** | Natural Language Logic — human-readable representation of table logic |")
    lines.append("| **Audit hash** | SHA-256 hash of extracted content; ensures tamper detection |")
    lines.append("| **Preservation level** | Controls whether RAG/LLM may paraphrase: verbatim (no), high (minimal), standard (yes) |")
    lines.append("| **Tier 1** | Dosing tables that passed all 6 automated plausibility checks |")
    lines.append("| **Tier 2** | Dosing tables that were not validated by automated checks |")
    lines.append("| **Tier 3** | Clinical management tables (safety-critical) |")
    lines.append("| **Tier 4** | Evidence tables and narratives containing dosing/contraindication keywords |")
    lines.append("| **G6PD** | Glucose-6-phosphate dehydrogenase (enzyme deficiency relevant to antimalarial safety) |")
    lines.append("")

    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════
# 9. REVIEW INGESTION (--ingest mode)
# ═══════════════════════════════════════════════════════════════════

def load_completed_review(path: str) -> Dict:
    """Load a physician-completed review_package.json."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_completed_review(
    completed: Dict, chunks: List[Dict],
) -> Tuple[bool, List[str], Dict]:
    """Validate a completed review package.

    Returns (is_valid, issues, stats).
    Runs 6 validation checks:
      1. All mandatory chunks have overall_decision set
      2. All applicable checks have status set
      3. Audit hashes match (content wasn't tampered with)
      4. Reviewer identity filled for all reviewed items
      5. reviewed_at is a valid ISO datetime
      6. Flagged/corrected items have notes or corrections
    """
    issues = []
    stats = {
        "total_reviewed": 0,
        "approved": 0,
        "flagged": 0,
        "corrected": 0,
        "unreviewed_mandatory": 0,
        "hash_mismatches": 0,
        "missing_identity": 0,
        "missing_datetime": 0,
        "missing_notes_on_flags": 0,
        "missing_check_statuses": 0,
    }

    chunk_lookup = build_chunk_lookup(chunks)
    review_items = completed.get("review_items", [])

    for item in review_items:
        cid = item["chunk_id"]
        review = item.get("review", {})
        decision = review.get("overall_decision")
        tier = item.get("review_tier", 5)

        # Check 1: mandatory chunks must have decision
        if tier in MANDATORY_TIERS:
            if not decision:
                stats["unreviewed_mandatory"] += 1
                issues.append(f"Mandatory chunk {cid} (tier {tier}) has no decision")
                continue

        if not decision:
            continue  # unreviewed recommended/optional — OK

        stats["total_reviewed"] += 1
        if decision == "approved":
            stats["approved"] += 1
        elif decision == "flagged":
            stats["flagged"] += 1
        elif decision == "corrected":
            stats["corrected"] += 1

        # Check 2: applicable checks have status
        applicable = item.get("applicable_checks", {})
        checks = review.get("checks", {})
        for check_key, check_info in applicable.items():
            if check_info.get("applicable", False):
                check_review = checks.get(check_key, {})
                if not check_review.get("status"):
                    stats["missing_check_statuses"] += 1
                    issues.append(f"{cid}: check '{check_key}' is applicable but has no status")

        # Check 3: audit hash integrity
        if cid in chunk_lookup:
            expected_hash = compute_audit_hash(chunk_lookup[cid]["content"])
            if item.get("audit_hash") != expected_hash:
                stats["hash_mismatches"] += 1
                issues.append(f"{cid}: audit_hash MISMATCH — content may have been altered")

        # Check 4: reviewer identity
        if not review.get("reviewer_name") or not review.get("institution"):
            stats["missing_identity"] += 1
            issues.append(f"{cid}: missing reviewer_name or institution")

        # Check 5: reviewed_at is valid
        reviewed_at = review.get("reviewed_at")
        if not reviewed_at:
            stats["missing_datetime"] += 1
            issues.append(f"{cid}: missing reviewed_at timestamp")
        else:
            try:
                datetime.fromisoformat(reviewed_at.replace("Z", "+00:00"))
            except (ValueError, AttributeError):
                stats["missing_datetime"] += 1
                issues.append(f"{cid}: reviewed_at '{reviewed_at}' is not valid ISO datetime")

        # Check 6: flagged/corrected items need notes
        if decision in ("flagged", "corrected"):
            notes = review.get("corrections") or review.get("checks", {})
            has_notes = bool(review.get("corrections"))
            has_check_notes = any(
                checks.get(k, {}).get("notes")
                for k in checks
            )
            if not has_notes and not has_check_notes:
                stats["missing_notes_on_flags"] += 1
                issues.append(f"{cid}: decision is '{decision}' but no corrections or notes provided")

    is_valid = (
        stats["unreviewed_mandatory"] == 0
        and stats["hash_mismatches"] == 0
        and stats["missing_identity"] == 0
        and stats["missing_datetime"] == 0
    )

    return is_valid, issues, stats


def apply_reviews_to_chunks(
    completed: Dict, chunks: List[Dict],
) -> Tuple[List[Dict], Dict]:
    """Apply completed reviews to chunks, updating verified_by fields.

    Returns (updated_chunks, application_stats).
    """
    chunk_lookup = build_chunk_lookup(chunks)
    review_items = completed.get("review_items", [])
    applied_count = 0
    skipped_count = 0

    # Build review lookup
    review_lookup = {}
    for item in review_items:
        review = item.get("review", {})
        if review.get("overall_decision"):
            review_lookup[item["chunk_id"]] = item

    # Apply to chunks
    for chunk in chunks:
        cid = chunk["chunk_id"]
        if cid in review_lookup:
            item = review_lookup[cid]
            review = item["review"]

            # Map decision to verified_by status
            decision = review["overall_decision"]
            if decision == "approved":
                status = "verified"
            elif decision in ("flagged", "corrected"):
                status = "flagged"
            else:
                status = "unverified"

            # Compute digital signature
            audit_hash = compute_audit_hash(chunk["content"])
            sig = compute_digital_signature(
                reviewer_name=review.get("reviewer_name", ""),
                institution=review.get("institution", ""),
                chunk_id=cid,
                audit_hash=audit_hash,
                reviewed_at=review.get("reviewed_at", ""),
            )

            # Collect comments
            comments_parts = []
            if review.get("corrections"):
                comments_parts.append(f"Corrections: {review['corrections']}")
            # Collect per-check notes
            for check_key, check_review in review.get("checks", {}).items():
                if check_review.get("notes"):
                    check_name = CHECK_DEFINITIONS.get(check_key, {}).get("name", check_key)
                    comments_parts.append(f"{check_name}: {check_review['notes']}")
            comments = "; ".join(comments_parts) if comments_parts else None

            # Update chunk
            chunk["verified_by"] = {
                "status": status,
                "reviewer_name": review.get("reviewer_name"),
                "reviewer_role": review.get("reviewer_role"),
                "institution": review.get("institution"),
                "digital_signature": sig,
                "verified_at": review.get("reviewed_at"),
                "comments": comments,
            }
            chunk["audit_hash"] = audit_hash

            # Also store the 5 check results
            chunk["clinical_verification_checks"] = {
                check_key: {
                    "status": review.get("checks", {}).get(check_key, {}).get("status"),
                    "notes": review.get("checks", {}).get(check_key, {}).get("notes"),
                }
                for check_key in CHECK_DEFINITIONS
            }

            applied_count += 1
        else:
            skipped_count += 1

    stats = {
        "applied": applied_count,
        "skipped": skipped_count,
        "total": len(chunks),
    }
    return chunks, stats


def generate_audit_summary(
    validation_stats: Dict, application_stats: Dict,
) -> Dict:
    """Generate a summary of the review ingestion process."""
    return {
        "validation": validation_stats,
        "application": application_stats,
        "review_coverage_pct": round(
            100 * application_stats["applied"] / application_stats["total"], 1
        ) if application_stats["total"] > 0 else 0,
    }


# ═══════════════════════════════════════════════════════════════════
# 10. SAVE OUTPUTS
# ═══════════════════════════════════════════════════════════════════

def save_review_package(package: Dict, path: Path) -> None:
    """Write review_package.json."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(package, f, indent=2, ensure_ascii=False)
    size_mb = path.stat().st_size / (1024 * 1024)
    print(f"  Saved {path.name} ({size_mb:.1f} MB)")


def save_physician_report(report_md: str, path: Path) -> None:
    """Write physician_review_report.md."""
    with open(path, "w", encoding="utf-8") as f:
        f.write(report_md)
    size_kb = path.stat().st_size / 1024
    print(f"  Saved {path.name} ({size_kb:.1f} KB)")


def save_updated_chunks(
    chunks: List[Dict], envelope: Dict, path: Path,
) -> None:
    """Write updated chunks.json with verified_by fields populated."""
    # Update envelope metadata
    envelope["pipeline_version"] = "4b"
    envelope["last_updated"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    output = {**envelope, "chunks": chunks}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    size_mb = path.stat().st_size / (1024 * 1024)
    print(f"  Saved updated {path.name} ({size_mb:.1f} MB)")


# ═══════════════════════════════════════════════════════════════════
# 11. SCORECARD & REPORTING
# ═══════════════════════════════════════════════════════════════════

def print_generate_scorecard(package: Dict, timings: Dict) -> None:
    """Print generation scorecard to stdout."""
    s = package["summary"]
    print()
    print("=" * 65)
    print("  STAGE 4b — REVIEW PACKAGE GENERATION SCORECARD")
    print("=" * 65)
    print()
    print(f"  Source document:       {SOURCE_PDF}")
    print(f"  Pipeline version:      4b")
    print(f"  Generated at:          {package['generated_at']}")
    print()
    print("  ── Chunk Triage ──")
    print(f"  Total chunks in pipeline:    {s['total_chunks_in_pipeline']}")
    print(f"  Total review items:          {s['total_review_items']}")
    for t in [1, 2, 3, 4, 5]:
        tier_info = s["by_tier"][str(t)]
        emoji = "🔴" if t <= 3 else ("🟡" if t == 4 else "🟢")
        req = tier_info["requirement"].capitalize()
        print(f"    {emoji} Tier {t} ({tier_info['label']}): {tier_info['count']:>5}  [{req}]")
    print()
    print(f"  Mandatory review:    {s['mandatory_review']:>5} chunks")
    print(f"  Recommended review:  {s['recommended_review']:>5} chunks")
    print(f"  Optional (excluded): {s['not_included_optional']:>5} chunks")
    print(f"  Est. review time:    ~{s['estimated_review_time_minutes']} min")
    print()

    # Audit hash stats
    items = package["review_items"]
    hashes = sum(1 for it in items if it.get("audit_hash"))
    nlls = sum(1 for it in items if it.get("nll"))
    with_context = sum(
        1 for it in items
        if it.get("context", {}).get("preceding_narrative_preview")
        or it.get("context", {}).get("following_narrative_preview")
    )
    print("  ── Integrity ──")
    print(f"  Audit hashes computed:  {hashes}/{len(items)} ✅")
    print(f"  Items with NLL:         {nlls}")
    print(f"  Items with context:     {with_context}")
    print()

    # Check applicability summary
    applicable_counts = {}
    for item in items:
        for ck, ci in item.get("applicable_checks", {}).items():
            if ci.get("applicable"):
                applicable_counts[ck] = applicable_counts.get(ck, 0) + 1
    print("  ── Check Applicability ──")
    for ck, cdef in CHECK_DEFINITIONS.items():
        count = applicable_counts.get(ck, 0)
        print(f"    {cdef['name']}: {count}/{len(items)} items")
    print()

    # Timing
    print("  ── Timing ──")
    for phase, secs in timings.items():
        print(f"    {phase}: {secs:.3f}s")
    total = sum(timings.values())
    print(f"    Total: {total:.3f}s")
    print()
    print("=" * 65)
    print()

    # Validation
    print("  ✅ Review package generated successfully.")
    print(f"  📄 JSON:     {REVIEW_PKG_PATH}")
    print(f"  📋 Markdown: {PHYSICIAN_REPORT_PATH}")
    print()


def print_ingest_scorecard(
    is_valid: bool, issues: List[str], val_stats: Dict,
    app_stats: Dict, audit: Dict, timings: Dict,
) -> None:
    """Print ingestion scorecard to stdout."""
    print()
    print("=" * 65)
    print("  STAGE 4b — REVIEW INGESTION SCORECARD")
    print("=" * 65)
    print()

    status = "✅ PASSED" if is_valid else "❌ FAILED"
    print(f"  Validation: {status}")
    print()

    print("  ── Review Statistics ──")
    print(f"  Total reviewed:          {val_stats.get('total_reviewed', 0)}")
    print(f"    Approved:              {val_stats.get('approved', 0)}")
    print(f"    Flagged:               {val_stats.get('flagged', 0)}")
    print(f"    Corrected:             {val_stats.get('corrected', 0)}")
    print(f"  Unreviewed mandatory:    {val_stats.get('unreviewed_mandatory', 0)}")
    print()

    print("  ── Integrity Checks ──")
    print(f"  Hash mismatches:         {val_stats.get('hash_mismatches', 0)}")
    print(f"  Missing identity:        {val_stats.get('missing_identity', 0)}")
    print(f"  Missing datetime:        {val_stats.get('missing_datetime', 0)}")
    print(f"  Missing notes on flags:  {val_stats.get('missing_notes_on_flags', 0)}")
    print(f"  Missing check statuses:  {val_stats.get('missing_check_statuses', 0)}")
    print()

    print("  ── Application ──")
    print(f"  Chunks updated:          {app_stats.get('applied', 0)}")
    print(f"  Chunks unchanged:        {app_stats.get('skipped', 0)}")
    print(f"  Review coverage:         {audit.get('review_coverage_pct', 0)}%")
    print()

    if issues:
        print(f"  ── Issues ({len(issues)}) ──")
        for issue in issues[:20]:
            print(f"    ⚠️  {issue}")
        if len(issues) > 20:
            print(f"    ... and {len(issues) - 20} more")
        print()

    # Timing
    print("  ── Timing ──")
    for phase, secs in timings.items():
        print(f"    {phase}: {secs:.3f}s")
    total = sum(timings.values())
    print(f"    Total: {total:.3f}s")
    print()
    print("=" * 65)


# ═══════════════════════════════════════════════════════════════════
# 12. MAIN
# ═══════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="Stage 4b — Clinical Verification Framework"
    )
    parser.add_argument(
        "--ingest",
        type=str,
        default=None,
        help="Path to completed review_package.json for ingestion",
    )
    parser.add_argument(
        "--config",
        type=str,
        default=None,
        help="Path to pipeline_config JSON file (handled by pipeline_config.py)",
    )
    args = parser.parse_args()

    if args.ingest:
        # ── INGEST MODE ──
        print()
        print("=" * 65)
        print("  STAGE 4b — REVIEW INGESTION MODE")
        print("=" * 65)
        print()

        timings = {}

        # Step 1: Load data
        t0 = time.time()
        print("  [1/4] Loading chunks and completed review...")
        envelope, chunks = load_chunks()
        completed = load_completed_review(args.ingest)
        timings["load_data"] = time.time() - t0
        print(f"         Loaded {len(chunks)} chunks + {len(completed.get('review_items', []))} review items")

        # Step 2: Validate
        t0 = time.time()
        print("  [2/4] Validating completed review...")
        is_valid, issues, val_stats = validate_completed_review(completed, chunks)
        timings["validate"] = time.time() - t0
        status = "PASSED" if is_valid else "FAILED"
        print(f"         Validation: {status} ({len(issues)} issues)")

        if not is_valid:
            print()
            print("  ❌ Validation failed. Fix the issues below before re-ingesting.")
            print_ingest_scorecard(is_valid, issues, val_stats, {"applied": 0, "skipped": len(chunks), "total": len(chunks)}, {"review_coverage_pct": 0}, timings)
            return

        # Step 3: Apply reviews
        t0 = time.time()
        print("  [3/4] Applying reviews to chunks...")
        chunks, app_stats = apply_reviews_to_chunks(completed, chunks)
        timings["apply"] = time.time() - t0
        print(f"         Applied {app_stats['applied']} reviews")

        # Step 4: Save
        t0 = time.time()
        print("  [4/4] Saving updated chunks.json...")
        save_updated_chunks(chunks, envelope, CHUNKS_PATH)
        timings["save"] = time.time() - t0

        audit = generate_audit_summary(val_stats, app_stats)
        print_ingest_scorecard(is_valid, issues, val_stats, app_stats, audit, timings)

    else:
        # ── GENERATE MODE ──
        print()
        print("=" * 65)
        print("  STAGE 4b — REVIEW PACKAGE GENERATION")
        print("=" * 65)
        print()

        timings = {}

        # Step 1: Load chunks
        t0 = time.time()
        print("  [1/5] Loading chunks.json...")
        envelope, chunks = load_chunks()
        chunk_lookup = build_chunk_lookup(chunks)
        timings["load_data"] = time.time() - t0
        print(f"         Loaded {len(chunks)} chunks")

        # Step 2: Triage
        t0 = time.time()
        print("  [2/5] Classifying chunks into review tiers...")
        tier_groups, chunk_tiers = triage_all_chunks(chunks)
        timings["triage"] = time.time() - t0
        for t in [1, 2, 3, 4, 5]:
            td = TIER_DEFINITIONS[t]
            print(f"         Tier {t} ({td['label']}): {len(tier_groups[t])}")

        # Step 3: Assemble review package
        t0 = time.time()
        print("  [3/5] Assembling review package...")
        package = assemble_review_package(chunks, chunk_lookup, tier_groups, chunk_tiers)
        timings["assemble"] = time.time() - t0
        print(f"         {len(package['review_items'])} review items created")

        # Step 4: Generate physician report
        t0 = time.time()
        print("  [4/5] Generating physician review report (markdown)...")
        report_md = generate_physician_report(package, chunk_lookup)
        timings["report"] = time.time() - t0
        print(f"         {len(report_md)} characters generated")

        # Step 5: Save outputs
        t0 = time.time()
        print("  [5/5] Saving outputs...")
        save_review_package(package, REVIEW_PKG_PATH)
        save_physician_report(report_md, PHYSICIAN_REPORT_PATH)
        timings["save"] = time.time() - t0

        # Scorecard
        print_generate_scorecard(package, timings)


if __name__ == "__main__":
    main()
