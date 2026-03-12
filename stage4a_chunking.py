# -*- coding: utf-8 -*-
"""
Stage 4a: Chunking + Metadata Strategy
=======================================
Splits the full extraction markdown into discrete, metadata-rich chunks
that serve as atomic units for RAG retrieval and clinical verification.

Each chunk carries:
  - Section hierarchy and page provenance
  - Table classification (Stages 1/2) and validation status (Stage 3)
  - Safety metadata (preservation level: verbatim / high / standard)
  - Clinical verification placeholder (verified_by for Stage 4b physician review)
  - Structured clinical metadata (drug, condition, weight/age ranges, contraindications)
  - NLL (Natural Language Logic) for dosing tables
  - Related-chunk links for context retrieval

Run:
    python stage4a_chunking.py
"""

# ─────────────────────────────────────────────────────────────────────────────
# 1.  IMPORTS
# ─────────────────────────────────────────────────────────────────────────────
import os
import re
import json
import time
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple
from collections import defaultdict
from bisect import bisect_right

from pipeline_config import (
    load_config, get_document_title, get_condition_patterns,
    get_biomarker_patterns, build_high_preservation_regex,
    get_clinical_section_keywords, build_loc_regex,
    get_output_dir,
)

# ─────────────────────────────────────────────────────────────────────────────
# 2.  CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────
CONFIG = load_config()
OUTPUT_DIR = Path(get_output_dir(CONFIG))

# Chunk sizing
MAX_NARRATIVE_TOKENS = 1500
MIN_NARRATIVE_TOKENS = 200
TOKEN_MULTIPLIER = 1.3  # words × 1.3 ≈ tokens

# Page footer / header patterns to strip from content
PAGE_FOOTER_RE = re.compile(r"^\d+ of \d+$")
WHO_HEADER_RE = re.compile(
    r"^WHO guidelines for .* World Health Organization", re.IGNORECASE
)

# Section number extraction  e.g.  "5.2.1.1.2 Dosing of ACTs"
SECTION_NUMBER_RE = re.compile(r"^(\d+(?:\.\d+)*)\s+(.*)")

# Headings that are structural (skip when extracting clinical_domain)
STRUCTURAL_HEADING_RES = [
    re.compile(r"^(?:Strong|Conditional)\s+recommendation", re.I),
    re.compile(r"^Remark", re.I),
    re.compile(r"^Practice\s+Statement", re.I),
    re.compile(r"^Additional\s+comments", re.I),
    re.compile(r"^Rationale", re.I),
    re.compile(r"^Key\s+info", re.I),
    re.compile(r"^\*?Not\s+evaluated", re.I),
    re.compile(r"^Sections$", re.I),
    re.compile(r"^Contact$", re.I),
    re.compile(r"^Sponsors", re.I),
    re.compile(r"^Disclaimer", re.I),
    re.compile(r"^©", re.I),
]

# Keywords that elevate a narrative chunk to "high" preservation (from config)
HIGH_PRESERVATION_KW = build_high_preservation_regex(CONFIG)

# Level of Care regex for LOC extraction (HC2, HC3, etc.)
LOC_RE = build_loc_regex(CONFIG)

# Clinical section keywords for broader content classification
CLINICAL_SECTION_KW = get_clinical_section_keywords(CONFIG)

# Clinical metadata: age patterns
AGE_PATTERN_RE = re.compile(
    r"(?:children?\s+(?:under|<|below|aged?)\s*(\d+)\s*(years?|months?|yrs?))|"
    r"(?:infants?\s*(?:<|under)\s*(\d+)\s*(months?|weeks?))|"
    r"(?:(?:adults?|patients?)\s*(?:>|≥|aged?\s*≥?)\s*(\d+)\s*(years?|yrs?))|"
    r"(?:(\d+)\s*(?:to|–|-)\s*(\d+)\s*(years?|months?))",
    re.IGNORECASE,
)

# Clinical metadata: weight pattern in narrative
WEIGHT_NARRATIVE_RE = re.compile(
    r"(?:weighing|weight)\s*(?:<|>|≤|≥|less than|more than|under|over)?\s*"
    r"(\d+(?:\.\d+)?)\s*kg",
    re.IGNORECASE,
)

# Weight-band parser (reuses Stage 3 logic)
WEIGHT_RANGE_PATTERNS = [
    # Pattern 1:  "< N" or "<N"
    (re.compile(r"^[<]\s*([\d.]+)"), lambda m: (0.0, float(m.group(1)))),
    # Pattern 2:  "N to < M" or "N to <M" or "N–<M"
    (
        re.compile(r"([\d.]+)\s*(?:to|–|-)\s*[<]\s*([\d.]+)"),
        lambda m: (float(m.group(1)), float(m.group(2))),
    ),
    # Pattern 3:  "N to M" (no < or >)
    (
        re.compile(r"([\d.]+)\s*(?:to|–|-)\s*([\d.]+)"),
        lambda m: (float(m.group(1)), float(m.group(2))),
    ),
    # Pattern 4:  "> N to ≤ M"
    (
        re.compile(r"[>]\s*([\d.]+)\s*(?:to|–|-)\s*[≤]\s*([\d.]+)"),
        lambda m: (float(m.group(1)), float(m.group(2))),
    ),
    # Pattern 5:  "N < M" (unusual WHO format: "60 < 80")
    (
        re.compile(r"([\d.]+)\s*<\s*([\d.]+)"),
        lambda m: (float(m.group(1)), float(m.group(2))),
    ),
    # Pattern 6:  "≥ N" or ">=N" or "≥N"
    (re.compile(r"[≥>]=?\s*([\d.]+)"), lambda m: (float(m.group(1)), None)),
]

# Drug name extraction from table headers
DRUG_NAME_RE = re.compile(
    r"(?:dose\s*\(mg\)\s*of\s+)(.+?)(?:\s+given|\s+dose|\s*$)",
    re.IGNORECASE,
)

# Frequency / duration extraction
FREQUENCY_RE = re.compile(
    r"(once|twice|three times|four times)\s+(?:a\s+)?daily",
    re.IGNORECASE,
)
DURATION_RE = re.compile(
    r"(?:for|over)\s+(\d+)\s+(days?|weeks?)",
    re.IGNORECASE,
)


# ─────────────────────────────────────────────────────────────────────────────
# 3.  DATA LOADING
# ─────────────────────────────────────────────────────────────────────────────
def load_stage_data() -> Dict[str, Any]:
    """Load all upstream stage outputs."""
    data: Dict[str, Any] = {}

    # Full extraction markdown
    md_path = OUTPUT_DIR / "full_extraction.md"
    with open(md_path, encoding="utf-8") as f:
        data["markdown"] = f.read()

    # Table inventory (Stage 1)
    inv_path = OUTPUT_DIR / "table_inventory.json"
    with open(inv_path, encoding="utf-8") as f:
        data["inventory"] = json.load(f)

    # Cross-validation report (Stage 2)
    xval_path = OUTPUT_DIR / "cross_validation_report.json"
    with open(xval_path, encoding="utf-8") as f:
        data["xval"] = json.load(f)

    # Plausibility report (Stage 3)
    plaus_path = OUTPUT_DIR / "plausibility_report.json"
    with open(plaus_path, encoding="utf-8") as f:
        data["plausibility"] = json.load(f)

    # NLL text
    nll_path = OUTPUT_DIR / "tables_nll.txt"
    with open(nll_path, encoding="utf-8") as f:
        data["nll_text"] = f.read()

    # Image inventory (Stage 1) — optional, may not exist for older runs
    img_inv_path = OUTPUT_DIR / "image_inventory.json"
    if img_inv_path.exists():
        with open(img_inv_path, encoding="utf-8") as f:
            data["image_inventory"] = json.load(f)
    else:
        data["image_inventory"] = []

    return data


def parse_nll_file(nll_text: str) -> Dict:
    """Parse tables_nll.txt into {table_index: nll_string} and stitched NLL.

    Returns dict with integer keys for regular tables and "S1" for stitched.
    """
    nll_map: Dict = {}
    current_key = None
    current_lines: List[str] = []

    for line in nll_text.split("\n"):
        # Regular table header: ### Table 13 (p.173, dosing) ###
        m = re.match(r"^###\s+Table\s+(\d+)\s+\(p\.\d+", line)
        if m:
            if current_key is not None and current_lines:
                nll_map[current_key] = "\n".join(current_lines).strip()
            current_key = int(m.group(1))
            current_lines = []
            continue

        # Stitched table header: ### Stitched Table (pp.173–174, dosing) ###
        m2 = re.match(r"^###\s+Stitched\s+Table\s+\(pp\.", line)
        if m2:
            if current_key is not None and current_lines:
                nll_map[current_key] = "\n".join(current_lines).strip()
            current_key = "S1"
            current_lines = []
            continue

        # Section headers (skip)
        if line.startswith("# ──"):
            continue

        if current_key is not None and line.strip():
            current_lines.append(line)

    # Close last entry
    if current_key is not None and current_lines:
        nll_map[current_key] = "\n".join(current_lines).strip()

    return nll_map


def build_enrichment_lookups(
    inventory: List[Dict],
    xval: Dict,
    plausibility: Dict,
) -> Tuple[Dict, Dict, List, Dict]:
    """Build lookup dicts for reclassifications, validation, stitched tables.

    Returns (reclass_map, validation_map, stitched_tables, nll_map_placeholder).
    nll_map is built separately via parse_nll_file().
    """
    # A. Reclassification: table_index → new_classification
    reclass_map: Dict[int, str] = {}
    for r in xval.get("classification_refinements", []):
        reclass_map[r["table_index"]] = r["new_classification"]

    # B. Validation: table_index → result dict
    validation_map: Dict = {}
    for result in plausibility.get("per_table_results", []):
        idx = result["table_index"]
        if result.get("parsed"):
            checks = result.get("checks", {})
            validation_map[idx] = {
                "status": "pass" if result["overall_passed"] else "fail",
                "checks_passed": sum(
                    1 for c in checks.values() if c.get("passed")
                ),
                "checks_total": len(checks),
                "weight_bands": result.get("weight_bands"),
                "num_rows": result.get("num_rows"),
                "issues": [
                    issue
                    for c in checks.values()
                    for issue in c.get("issues", [])
                    if issue
                ],
            }
        else:
            validation_map[idx] = {
                "status": "skipped",
                "reason": result.get("error", "Unknown"),
            }

    # Stitched table validation
    st_result = plausibility.get("stitched_table_result")
    if st_result and st_result.get("parsed"):
        checks = st_result.get("checks", {})
        validation_map["S1"] = {
            "status": "pass" if st_result["overall_passed"] else "fail",
            "checks_passed": sum(
                1 for c in checks.values() if c.get("passed")
            ),
            "checks_total": len(checks),
            "weight_bands": st_result.get("weight_bands"),
            "num_rows": st_result.get("num_rows"),
            "issues": [
                issue
                for c in checks.values()
                for issue in c.get("issues", [])
                if issue
            ],
        }

    # C. Stitched tables
    stitched_tables = xval.get("page_boundary_stitches", [])

    return reclass_map, validation_map, stitched_tables


# ─────────────────────────────────────────────────────────────────────────────
# 4.  MARKDOWN PARSING
# ─────────────────────────────────────────────────────────────────────────────
def build_page_map(lines: List[str]) -> List[Tuple[int, int]]:
    """Scan for 'N of M' footers → [(line_no, page_no), ...]."""
    markers: List[Tuple[int, int]] = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        if PAGE_FOOTER_RE.match(stripped):
            page_num = int(stripped.split()[0])
            markers.append((i, page_num))
    return markers


def get_page_for_line(line_no: int, page_markers: List[Tuple[int, int]]) -> Optional[int]:
    """Binary search: return the page number for a given markdown line."""
    if not page_markers:
        return None
    line_positions = [m[0] for m in page_markers]
    idx = bisect_right(line_positions, line_no) - 1
    if idx < 0:
        return page_markers[0][1] if page_markers else None
    return page_markers[idx][1]


def parse_section_number(heading_text: str) -> Tuple[Optional[str], str]:
    """Extract (section_number, title) from heading text.

    "5.2.1.1.2 Dosing of ACTs" → ("5.2.1.1.2", "Dosing of ACTs")
    "Remark:" → (None, "Remark:")
    """
    m = SECTION_NUMBER_RE.match(heading_text.strip())
    if m:
        return m.group(1), m.group(2).strip()
    return None, heading_text.strip()


def parse_markdown_into_sections(markdown: str) -> List[Dict]:
    """Split full markdown on '## ' headings.

    Returns [{heading, content_lines, content_line_numbers, start_line}, ...].
    The first section (before any heading) has heading=None.
    content_line_numbers tracks the global line number for each content_line.
    """
    lines = markdown.split("\n")
    sections: List[Dict] = []
    current: Dict = {
        "heading": None,
        "content_lines": [],
        "content_line_numbers": [],
        "start_line": 0,
    }

    for i, line in enumerate(lines):
        if line.startswith("## "):
            # Close previous section
            if current["heading"] is not None or current["content_lines"]:
                sections.append(current)
            heading_text = line[3:].strip()
            current = {
                "heading": heading_text,
                "content_lines": [],
                "content_line_numbers": [],
                "start_line": i,
            }
        else:
            current["content_lines"].append(line)
            current["content_line_numbers"].append(i)

    # Final section
    if current["heading"] is not None or current["content_lines"]:
        sections.append(current)

    return sections


def build_section_hierarchy(sections: List[Dict]) -> None:
    """Assign section_hierarchy and section_number to each section in-place.

    Uses a depth stack based on section numbering: "5.2.1" = depth 3.
    Unnumbered headings inherit the current parent's hierarchy.
    """
    stack: List[Dict] = []  # [{sec_num, heading, depth}, ...]

    for section in sections:
        heading = section.get("heading") or ""
        sec_num, title = parse_section_number(heading)

        if sec_num is not None:
            depth = len(sec_num.split("."))
            # Pop until we find a parent with strictly less depth
            while stack and stack[-1]["depth"] >= depth:
                stack.pop()
            stack.append(
                {"sec_num": sec_num, "heading": heading, "depth": depth}
            )

        # Build hierarchy from current stack
        section["section_hierarchy"] = [s["heading"] for s in stack]
        section["section_number"] = sec_num or (
            stack[-1]["sec_num"] if stack else None
        )
        section["section_title"] = title if sec_num else heading


def extract_elements_from_section(section: Dict) -> List[Dict]:
    """Split a section's content into narrative / table / image elements.

    Filters out page footers and WHO header lines.
    Each element also carries 'first_line_no' — the global line number of its
    first content line, used for resolving the element's page.
    """
    elements: List[Dict] = []
    current_narrative: List[str] = []
    current_narrative_start: Optional[int] = None
    current_table: List[str] = []
    current_table_start: Optional[int] = None
    in_table = False

    content_lines = section.get("content_lines", [])
    line_numbers = section.get("content_line_numbers", list(range(len(content_lines))))

    for idx, line in enumerate(content_lines):
        stripped = line.strip()
        line_no = line_numbers[idx] if idx < len(line_numbers) else 0

        # Skip page footers and repeated WHO headers
        if PAGE_FOOTER_RE.match(stripped):
            continue
        if WHO_HEADER_RE.match(stripped):
            continue

        # Detect table lines (start with |)
        if stripped.startswith("|"):
            if not in_table and current_narrative:
                elements.append(
                    {"type": "narrative", "lines": current_narrative,
                     "first_line_no": current_narrative_start}
                )
                current_narrative = []
                current_narrative_start = None
            in_table = True
            if current_table_start is None:
                current_table_start = line_no
            current_table.append(line)
        else:
            if in_table:
                elements.append(
                    {"type": "table", "lines": current_table,
                     "first_line_no": current_table_start}
                )
                current_table = []
                current_table_start = None
                in_table = False

            if stripped == "<!-- image -->":
                if current_narrative:
                    elements.append(
                        {"type": "narrative", "lines": current_narrative,
                         "first_line_no": current_narrative_start}
                    )
                    current_narrative = []
                    current_narrative_start = None
                elements.append(
                    {"type": "image", "lines": [line],
                     "first_line_no": line_no}
                )
            else:
                if current_narrative_start is None:
                    current_narrative_start = line_no
                current_narrative.append(line)

    # Close remaining
    if in_table:
        elements.append(
            {"type": "table", "lines": current_table,
             "first_line_no": current_table_start}
        )
    if current_narrative:
        elements.append(
            {"type": "narrative", "lines": current_narrative,
             "first_line_no": current_narrative_start}
        )

    return elements


# ─────────────────────────────────────────────────────────────────────────────
# 5.  TABLE MATCHING
# ─────────────────────────────────────────────────────────────────────────────
def _table_fingerprint(table_lines: List[str]) -> str:
    """Build a normalised fingerprint from a markdown table's first data row."""
    for line in table_lines:
        stripped = line.strip()
        # Skip header separator rows
        if re.match(r"^\|[-:\s|]+\|$", stripped):
            continue
        # Return the first non-separator row, normalised
        return re.sub(r"\s+", " ", stripped.replace("|", " ")).strip().lower()
    return ""


def _inventory_fingerprint(inv_entry: Dict) -> str:
    """Build a normalised fingerprint from an inventory entry's markdown."""
    md = inv_entry.get("markdown_preview", "") or ""
    # If the inventory doesn't store a preview, use the full markdown
    # from the table_inventory.json (which may not include markdown).
    # In that case we return empty and rely on page-based matching.
    if not md:
        return ""
    lines = md.strip().split("\n")
    for line in lines:
        stripped = line.strip()
        if re.match(r"^\|[-:\s|]+\|$", stripped):
            continue
        if stripped.startswith("|"):
            return re.sub(r"\s+", " ", stripped.replace("|", " ")).strip().lower()
    return ""


def match_tables_to_inventory(
    all_table_elements: List[Dict],
    inventory: List[Dict],
    page_markers: List[Tuple[int, int]],
) -> Dict[int, Optional[Dict]]:
    """Match each inline markdown table element to an inventory entry.

    Strategy:
    1. Resolve each table element's page from its first_line_no.
    2. Group inventory tables by page_no.
    3. For each markdown table, match by page with a per-page positional counter.
    4. If no page match, try adjacent pages (± 1) as fallback.

    Returns {table_element_index: inventory_entry_or_None}.
    """
    # Build page → [inventory entries] lookup
    page_to_inv: Dict[int, List[Dict]] = defaultdict(list)
    for entry in inventory:
        page_to_inv[entry["page_no"]].append(entry)

    # Sort entries within each page by index
    for page in page_to_inv:
        page_to_inv[page].sort(key=lambda e: e["index"])

    # Track which inventory entries have been assigned
    assigned: set = set()
    # Per-page consumption counter
    page_counters: Dict[int, int] = defaultdict(int)

    result: Dict[int, Optional[Dict]] = {}

    for elem_idx, elem in enumerate(all_table_elements):
        # Resolve page from the table element's actual line position
        line_no = elem.get("first_line_no")
        if line_no is not None:
            page = get_page_for_line(line_no, page_markers)
        else:
            page = None

        if page is None:
            result[elem_idx] = None
            continue

        # Try exact page first, then adjacent pages
        for try_page in [page, page - 1, page + 1]:
            candidates = page_to_inv.get(try_page, [])
            available = [c for c in candidates if c["index"] not in assigned]
            if available:
                counter = page_counters[try_page]
                if counter < len(available):
                    match = available[counter]
                    page_counters[try_page] = counter + 1
                else:
                    match = available[-1]
                assigned.add(match["index"])
                result[elem_idx] = match
                break
        else:
            result[elem_idx] = None

    return result


# ─────────────────────────────────────────────────────────────────────────────
# 6.  CHUNK CREATION
# ─────────────────────────────────────────────────────────────────────────────
def estimate_tokens(text: str) -> int:
    """Estimate token count: word_count × TOKEN_MULTIPLIER."""
    if not text:
        return 0
    return int(len(text.split()) * TOKEN_MULTIPLIER)


def split_narrative_if_needed(
    text: str,
    max_tokens: int = MAX_NARRATIVE_TOKENS,
    min_tokens: int = MIN_NARRATIVE_TOKENS,
) -> List[str]:
    """Split oversized narrative text on paragraph boundaries."""
    tokens = estimate_tokens(text)
    if tokens <= max_tokens:
        return [text]

    paragraphs = text.split("\n\n")
    sub_chunks: List[str] = []
    current_parts: List[str] = []
    current_tokens = 0

    for para in paragraphs:
        para_tokens = estimate_tokens(para)
        if current_tokens + para_tokens > max_tokens and current_parts:
            sub_chunks.append("\n\n".join(current_parts))
            current_parts = []
            current_tokens = 0
        current_parts.append(para)
        current_tokens += para_tokens

    if current_parts:
        sub_chunks.append("\n\n".join(current_parts))

    # Merge tiny trailing chunks back
    if len(sub_chunks) > 1 and estimate_tokens(sub_chunks[-1]) < min_tokens:
        sub_chunks[-2] = sub_chunks[-2] + "\n\n" + sub_chunks[-1]
        sub_chunks.pop()

    return sub_chunks


def _get_final_classification(
    inv_entry: Optional[Dict], reclass_map: Dict[int, str]
) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """Return (stage1_class, stage2_class, final_class) for a table."""
    if inv_entry is None:
        return None, None, None
    idx = inv_entry["index"]
    stage1 = inv_entry["classification"]
    stage2 = reclass_map.get(idx, stage1)
    return stage1, stage2, stage2


def _chunk_type_from_classification(final_class: Optional[str]) -> str:
    """Map table classification → chunk_type."""
    mapping = {
        "dosing": "dosing_table",
        "evidence": "evidence_table",
        "structural": "structural_table",
        "clinical_management": "clinical_table",
        "other": "other_table",
    }
    return mapping.get(final_class or "", "other_table")


def extract_clinical_domain(section_hierarchy: List[str]) -> Optional[str]:
    """Extract clinical topic from section hierarchy (leaf → root).

    Skips structural headings (Remark, Recommendation, etc.).
    """
    for heading in reversed(section_hierarchy):
        _, title = parse_section_number(heading)
        if any(pat.match(title) for pat in STRUCTURAL_HEADING_RES):
            continue
        if title:
            return title
    return None


def create_narrative_chunk(
    text: str,
    section: Dict,
    chunk_counter: int,
    page_markers: List[Tuple[int, int]],
    first_line_no: Optional[int] = None,
) -> Dict:
    """Create a narrative chunk dict with all metadata fields."""
    line = first_line_no if first_line_no is not None else section["start_line"]
    page = get_page_for_line(line, page_markers)
    word_count = len(text.split())
    domain = extract_clinical_domain(section.get("section_hierarchy", []))

    chunk = {
        "chunk_id": f"narrative-{chunk_counter:04d}",
        "chunk_type": "narrative",
        "source_pages": [page] if page else [],
        "section_hierarchy": section.get("section_hierarchy", []),
        "section_number": section.get("section_number"),
        "section_title": section.get("section_title", ""),
        "content": text,
        "content_type": "markdown",
        "nll": None,
        "table_index": None,
        "table_classification": None,
        "validation": None,
        "clinical_domain": domain,
        "safety": {
            "preservation_level": "standard",
            "reasoning": "General narrative content",
        },
        "verified_by": {
            "status": "unverified",
            "reviewer_name": None,
            "reviewer_role": None,
            "institution": None,
            "digital_signature": None,
            "verified_at": None,
            "comments": None,
        },
        "clinical_metadata": {
            "condition": None,
            "drug_name": None,
            "dosage_summary": None,
            "patient_weight_min_kg": None,
            "patient_weight_max_kg": None,
            "patient_age_min": None,
            "patient_age_max": None,
            "route": None,
            "frequency": None,
            "duration": None,
            "contraindications": [],
            "special_populations": [],
            "level_of_care": [],
            "clinical_features": [],
            "danger_signs": [],
            "referral_criteria": [],
            "clinical_section_type": None,
        },
        "related_chunks": {
            "prev_sibling": None,
            "next_sibling": None,
            "preceding_narrative": None,
            "following_narrative": None,
            "context_for_tables": [],
            "section_siblings": [],
        },
        "word_count": word_count,
        "token_estimate": int(word_count * TOKEN_MULTIPLIER),
    }

    return chunk


def create_table_chunk(
    table_lines: List[str],
    section: Dict,
    inv_entry: Optional[Dict],
    reclass_map: Dict[int, str],
    validation_map: Dict,
    nll_map: Dict,
    page_markers: List[Tuple[int, int]],
    first_line_no: Optional[int] = None,
) -> Dict:
    """Create a table chunk with classification, validation, NLL metadata."""
    table_md = "\n".join(table_lines)
    line = first_line_no if first_line_no is not None else section["start_line"]
    page = get_page_for_line(line, page_markers)
    word_count = len(table_md.split())

    # Classification
    stage1, stage2, final = _get_final_classification(inv_entry, reclass_map)
    chunk_type = _chunk_type_from_classification(final)
    table_idx = inv_entry["index"] if inv_entry else None

    # Validation
    validation = None
    if table_idx is not None and table_idx in validation_map:
        validation = validation_map[table_idx]

    # NLL
    nll = None
    if table_idx is not None and table_idx in nll_map:
        nll = nll_map[table_idx]

    domain = extract_clinical_domain(section.get("section_hierarchy", []))

    chunk = {
        "chunk_id": f"{chunk_type}-{table_idx:04d}" if table_idx is not None else f"unmatched_table-{id(table_lines):010d}",
        "chunk_type": chunk_type,
        "source_pages": [page] if page else [],
        "section_hierarchy": section.get("section_hierarchy", []),
        "section_number": section.get("section_number"),
        "section_title": section.get("section_title", ""),
        "content": table_md,
        "content_type": "markdown_table",
        "nll": nll,
        "table_index": table_idx,
        "table_classification": {
            "stage1": stage1,
            "stage2_refined": stage2,
            "final": final,
        }
        if inv_entry
        else None,
        "validation": validation,
        "clinical_domain": domain,
        "safety": {
            "preservation_level": "standard",
            "reasoning": "Table content",
        },
        "verified_by": {
            "status": "unverified",
            "reviewer_name": None,
            "reviewer_role": None,
            "institution": None,
            "digital_signature": None,
            "verified_at": None,
            "comments": None,
        },
        "clinical_metadata": {
            "condition": None,
            "drug_name": None,
            "dosage_summary": None,
            "patient_weight_min_kg": None,
            "patient_weight_max_kg": None,
            "patient_age_min": None,
            "patient_age_max": None,
            "route": None,
            "frequency": None,
            "duration": None,
            "contraindications": [],
            "special_populations": [],
            "level_of_care": [],
            "clinical_features": [],
            "danger_signs": [],
            "referral_criteria": [],
            "clinical_section_type": None,
        },
        "related_chunks": {
            "prev_sibling": None,
            "next_sibling": None,
            "preceding_narrative": None,
            "following_narrative": None,
            "context_for_tables": [],
            "section_siblings": [],
        },
        "word_count": word_count,
        "token_estimate": int(word_count * TOKEN_MULTIPLIER),
    }

    return chunk


def create_image_chunk(
    section: Dict,
    image_counter: int,
    page_markers: List[Tuple[int, int]],
    first_line_no: Optional[int] = None,
    image_data: Optional[Dict] = None,
) -> Dict:
    """Create an image chunk, enriched with OCR text when available.

    If image_data is provided (from image_inventory.json), the chunk
    gets the OCR text as content and content_type 'image_ocr'.
    Otherwise it remains a placeholder with content '<!-- image -->'.
    """
    line = first_line_no if first_line_no is not None else section["start_line"]
    page = get_page_for_line(line, page_markers)
    domain = extract_clinical_domain(section.get("section_hierarchy", []))

    # Build content from OCR text + caption when available
    if image_data:
        ocr_text = (image_data.get("ocr_text") or "").strip()
        caption = (image_data.get("caption") or "").strip()
        parts = []
        if caption:
            parts.append(f"[Image caption: {caption}]")
        if ocr_text:
            parts.append(ocr_text)
        content = "\n".join(parts) if parts else "<!-- image -->"
        content_type = "image_ocr" if parts else "image_placeholder"
        image_path = image_data.get("saved_path", "")
    else:
        content = "<!-- image -->"
        content_type = "image_placeholder"
        image_path = ""

    word_count = len(content.split()) if content_type == "image_ocr" else 0

    return {
        "chunk_id": f"image-{image_counter:04d}",
        "chunk_type": "image",
        "source_pages": [page] if page else [],
        "section_hierarchy": section.get("section_hierarchy", []),
        "section_number": section.get("section_number"),
        "section_title": section.get("section_title", ""),
        "content": content,
        "content_type": content_type,
        "image_path": image_path,
        "nll": None,
        "table_index": None,
        "table_classification": None,
        "validation": None,
        "clinical_domain": domain,
        "safety": {
            "preservation_level": "standard",
            "reasoning": "Image placeholder",
        },
        "verified_by": {
            "status": "unverified",
            "reviewer_name": None,
            "reviewer_role": None,
            "institution": None,
            "digital_signature": None,
            "verified_at": None,
            "comments": None,
        },
        "clinical_metadata": {
            "condition": None,
            "drug_name": None,
            "dosage_summary": None,
            "patient_weight_min_kg": None,
            "patient_weight_max_kg": None,
            "patient_age_min": None,
            "patient_age_max": None,
            "route": None,
            "frequency": None,
            "duration": None,
            "contraindications": [],
            "special_populations": [],
            "level_of_care": [],
            "clinical_features": [],
            "danger_signs": [],
            "referral_criteria": [],
            "clinical_section_type": None,
        },
        "related_chunks": {
            "prev_sibling": None,
            "next_sibling": None,
            "preceding_narrative": None,
            "following_narrative": None,
            "context_for_tables": [],
            "section_siblings": [],
        },
        "word_count": word_count,
        "token_estimate": int(word_count * TOKEN_MULTIPLIER),
    }


# ─────────────────────────────────────────────────────────────────────────────
# 6b. SAFETY METADATA
# ─────────────────────────────────────────────────────────────────────────────
def assign_safety_metadata(chunk: Dict) -> None:
    """Assign preservation_level based on chunk_type and content.

    Levels:
      verbatim  — dosing tables, clinical tables (no paraphrasing of dosages)
      high      — evidence tables, narratives with dosing/contraindication keywords
      standard  — everything else
    """
    ct = chunk["chunk_type"]
    final_class = None
    if chunk.get("table_classification"):
        final_class = chunk["table_classification"].get("final")

    # Rule 1: Dosing tables → verbatim
    if ct == "dosing_table" or (ct.endswith("_table") and final_class == "dosing"):
        chunk["safety"] = {
            "preservation_level": "verbatim",
            "reasoning": "Dosing table — no paraphrasing allowed for drug dosages",
        }
        return

    # Rule 2: Clinical management tables → verbatim
    if ct == "clinical_table":
        chunk["safety"] = {
            "preservation_level": "verbatim",
            "reasoning": "Clinical management table — safety-critical content",
        }
        return

    # Rule 3: Evidence tables → high
    if ct == "evidence_table":
        chunk["safety"] = {
            "preservation_level": "high",
            "reasoning": "Evidence table — clinical facts must be preserved",
        }
        return

    # Rule 4: Narrative/image with danger signs or referral criteria → verbatim
    if ct in ("narrative", "image"):
        content = chunk.get("content", "")
        content_lower = content.lower() if content else ""
        has_danger = "danger sign" in content_lower
        has_referral = (
            "refer immediately" in content_lower
            or "refer urgently" in content_lower
            or "referral criteria" in content_lower
        )
        if has_danger or has_referral:
            chunk["safety"] = {
                "preservation_level": "verbatim",
                "reasoning": f"{'Image OCR' if ct == 'image' else 'Narrative'} contains danger signs or referral criteria — safety-critical",
            }
            return

    # Rule 5: Narrative/image with dosing/contraindication/high-preservation keywords → high
    if ct in ("narrative", "image"):
        content = chunk.get("content", "")
        if content and HIGH_PRESERVATION_KW.search(content):
            chunk["safety"] = {
                "preservation_level": "high",
                "reasoning": f"{'Image OCR' if ct == 'image' else 'Narrative'} contains dosing, contraindication, or clinical safety information",
            }
            return

    # Default: standard
    chunk["safety"] = {
        "preservation_level": "standard",
        "reasoning": "General content — paraphrasing acceptable",
    }


# ─────────────────────────────────────────────────────────────────────────────
# 6c. CLINICAL METADATA EXTRACTION
# ─────────────────────────────────────────────────────────────────────────────
def _parse_weight_range(cell: str) -> Optional[Tuple[float, Optional[float]]]:
    """Parse a weight-band cell into (low, high). Reuses Stage 3 logic."""
    cleaned = re.sub(r"[a-zA-Z]$", "", cell.strip())  # strip footnote markers
    cleaned = cleaned.replace("kg", "").strip()
    for pattern, extractor in WEIGHT_RANGE_PATTERNS:
        m = pattern.search(cleaned)
        if m:
            return extractor(m)
    return None


def _extract_drug_from_header(table_md: str) -> Optional[str]:
    """Extract drug name from the table header row."""
    lines = table_md.strip().split("\n")
    if not lines:
        return None
    header = lines[0]

    # Try: "Dose (mg) of <drug> given..."
    m = DRUG_NAME_RE.search(header)
    if m:
        return m.group(1).strip()

    # Try: "<drug> dose (mg)..." pattern
    m2 = re.search(r"^[|]\s*[^|]*[|]\s*(.+?)(?:\s+dose|\s*\()", header, re.I)
    if m2:
        drug = m2.group(1).strip().rstrip("|").strip()
        if drug and len(drug) > 3:
            return drug

    return None


def _extract_frequency_duration(text: str) -> Tuple[Optional[str], Optional[str]]:
    """Extract frequency and duration from header or context text."""
    freq = None
    duration = None
    m_freq = FREQUENCY_RE.search(text)
    if m_freq:
        freq = m_freq.group(0).strip()
    m_dur = DURATION_RE.search(text)
    if m_dur:
        duration = f"{m_dur.group(1)} {m_dur.group(2)}"
    return freq, duration


def _infer_condition_from_hierarchy(hierarchy: List[str]) -> Optional[str]:
    """Infer clinical condition from section hierarchy.

    Walks the hierarchy looking for treatment/condition indicators.
    """
    condition_keywords = get_condition_patterns(CONFIG)
    for heading in reversed(hierarchy):
        for pattern, label in condition_keywords:
            if re.search(pattern, heading, re.I):
                return label
    return None


def extract_clinical_metadata_for_dosing_table(
    chunk: Dict, table_md: str
) -> None:
    """Populate clinical_metadata for a dosing table chunk."""
    cm = chunk["clinical_metadata"]

    # Drug name from table header
    drug = _extract_drug_from_header(table_md)
    if drug:
        cm["drug_name"] = drug

    # Frequency / duration from table header
    freq, dur = _extract_frequency_duration(table_md)
    if freq:
        cm["frequency"] = freq
    if dur:
        cm["duration"] = dur

    # Route — default oral for ACTs
    cm["route"] = "oral"

    # Dosage summary from header
    lines = table_md.strip().split("\n")
    if lines:
        header_clean = re.sub(r"[|]", " ", lines[0]).strip()
        header_clean = re.sub(r"\s+", " ", header_clean)
        if freq or dur:
            summary_parts = []
            if freq:
                summary_parts.append(freq)
            if dur:
                summary_parts.append(f"for {dur}")
            cm["dosage_summary"] = f"Weight-based, {' '.join(summary_parts)}"

    # Weight ranges from table body
    weight_lows: List[float] = []
    weight_highs: List[float] = []
    for line in lines:
        if line.strip().startswith("|") and not re.match(r"^\|[-:\s|]+\|$", line.strip()):
            cells = [c.strip() for c in line.split("|") if c.strip()]
            if cells:
                parsed = _parse_weight_range(cells[0])
                if parsed:
                    low, high = parsed
                    weight_lows.append(low)
                    if high is not None:
                        weight_highs.append(high)

    if weight_lows:
        cm["patient_weight_min_kg"] = min(weight_lows)
    if weight_highs:
        cm["patient_weight_max_kg"] = max(weight_highs)
    elif weight_lows:
        # Open-ended (≥ N with no upper bound)
        cm["patient_weight_max_kg"] = None  # unbounded

    # Condition from section hierarchy
    condition = _infer_condition_from_hierarchy(
        chunk.get("section_hierarchy", [])
    )
    if condition:
        cm["condition"] = condition


def _normalize_loc(raw: str) -> str:
    """Normalize LOC mentions: 'HC III' -> 'HC3', 'HC IV' -> 'HC4', etc."""
    norm = raw.upper().strip()
    norm = norm.replace("HC II", "HC2").replace("HC III", "HC3").replace("HC IV", "HC4")
    norm = norm.replace(" ", "")
    return norm


def extract_clinical_metadata_for_clinical_table(chunk: Dict, table_md: str) -> None:
    """Populate clinical_metadata for a clinical_management table.

    Extracts:
      - Level of Care (HC2/HC3/HC4) indicators
      - Danger signs mentioned in the table
      - Referral criteria
      - Condition from section hierarchy
    """
    cm = chunk["clinical_metadata"]
    content_lower = table_md.lower()

    # Level of Care extraction
    if LOC_RE.pattern != r"(?!)":
        loc_matches = LOC_RE.findall(table_md)
        if loc_matches:
            normalized = set(_normalize_loc(m) for m in loc_matches)
            cm["level_of_care"] = sorted(normalized)

    # Danger signs from table content
    danger_patterns = [
        r"danger\s+signs?\s*[:;]\s*([^|]+)",
        r"danger\s+signs?\s+include\s*([^|]+)",
        r"(?:refer|send)\s+(?:immediately|urgently)\s+(?:if|when)\s+([^|]+)",
    ]
    dangers = []
    for pat in danger_patterns:
        for m in re.finditer(pat, content_lower):
            dangers.append(m.group(1).strip()[:120])
    if dangers:
        cm["danger_signs"] = dangers

    # Referral criteria
    referral_patterns = [
        r"refer\s+(?:to|for)\s+([^|]+)",
        r"refer\s+(?:immediately|urgently)[^|]*",
    ]
    referrals = []
    for pat in referral_patterns:
        for m in re.finditer(pat, content_lower):
            referrals.append(m.group(0).strip()[:120])
    if referrals:
        cm["referral_criteria"] = list(set(referrals))

    # Condition from section hierarchy (same logic as dosing tables)
    condition = _infer_condition_from_hierarchy(
        chunk.get("section_hierarchy", [])
    )
    if condition:
        cm["condition"] = condition


def extract_clinical_metadata_for_narrative(chunk: Dict) -> None:
    """Populate clinical_metadata for a narrative chunk by scanning content."""
    cm = chunk["clinical_metadata"]
    content = chunk.get("content", "")

    # Condition from section hierarchy
    condition = _infer_condition_from_hierarchy(
        chunk.get("section_hierarchy", [])
    )
    if condition:
        cm["condition"] = condition

    # Age patterns
    for m in AGE_PATTERN_RE.finditer(content):
        groups = m.groups()
        # "children under N years"
        if groups[0]:
            cm["patient_age_max"] = f"{groups[0]} {groups[1]}"
        # "infants <N months"
        if groups[2]:
            cm["patient_age_max"] = f"{groups[2]} {groups[3]}"
        # "adults ≥N years"
        if groups[4]:
            cm["patient_age_min"] = f"{groups[4]} {groups[5]}"
        # "N to M years"
        if groups[6] and groups[7]:
            cm["patient_age_min"] = f"{groups[6]} {groups[8]}"
            cm["patient_age_max"] = f"{groups[7]} {groups[8]}"

    # Weight mentions
    for m in WEIGHT_NARRATIVE_RE.finditer(content):
        weight = float(m.group(1))
        if "less" in m.group(0).lower() or "<" in m.group(0):
            cm["patient_weight_max_kg"] = weight
        else:
            cm["patient_weight_min_kg"] = weight

    # Contraindications
    contraindication_patterns = [
        r"contraindicated\s+(?:in|for)\s+([^.;]+)",
        r"(?:do not give|should not be (?:given|used)|avoid)\s+(?:in|for|to)\s+([^.;]+)",
        r"not recommended\s+(?:in|for)\s+([^.;]+)",
    ]
    contras = []
    for pat in contraindication_patterns:
        for m in re.finditer(pat, content, re.I):
            contras.append(m.group(1).strip())
    if contras:
        cm["contraindications"] = contras

    # Special populations (generic + config biomarkers)
    special_pop_patterns = [
        r"(pregnant\s+women[^.;]*)",
        r"(children\s+(?:under|<|weighing\s*<)\s*[\d]+\s*(?:kg|years?|months?)[^.;]*)",
        r"(infants?\s*(?:<|under)\s*[\d]+\s*(?:months?|weeks?)[^.;]*)",
        r"(HIV[^.;]*patients?[^.;]*)",
    ]
    # Add biomarker-specific patterns from config
    for bm in get_biomarker_patterns(CONFIG):
        special_pop_patterns.append(rf"({re.escape(bm)}\s+deficien[ct][^.;]*)")
    pops = []
    for pat in special_pop_patterns:
        for m in re.finditer(pat, content, re.I):
            pops.append(m.group(1).strip()[:100])  # cap length
    if pops:
        cm["special_populations"] = list(set(pops))

    # ── NEW: Clinical section type inference from hierarchy ──
    hierarchy = chunk.get("section_hierarchy", [])
    for heading in hierarchy:
        heading_lower = heading.lower()
        for section_type, keywords in CLINICAL_SECTION_KW.items():
            if any(kw in heading_lower for kw in keywords):
                cm["clinical_section_type"] = section_type
                break
        if cm.get("clinical_section_type"):
            break

    # ── NEW: Level of Care extraction from narrative ──
    if LOC_RE.pattern != r"(?!)":
        loc_matches = LOC_RE.findall(content)
        if loc_matches:
            normalized = set(_normalize_loc(m) for m in loc_matches)
            cm["level_of_care"] = sorted(normalized)

    # ── NEW: Danger signs from narrative ──
    danger_patterns = [
        r"danger\s+signs?\s*[:;–-]\s*([^.;]+)",
        r"danger\s+signs?\s+include\s*([^.;]+)",
    ]
    dangers = []
    for pat in danger_patterns:
        for m in re.finditer(pat, content, re.I):
            dangers.append(m.group(1).strip()[:120])
    if dangers:
        cm["danger_signs"] = dangers

    # ── NEW: Referral criteria from narrative ──
    referral_patterns = [
        r"refer\s+(?:immediately|urgently)\s+(?:if|when|to)\s+([^.;]+)",
        r"refer(?:ral)?\s+(?:to|criteria)\s*[:;–-]\s*([^.;]+)",
    ]
    referrals = []
    for pat in referral_patterns:
        for m in re.finditer(pat, content, re.I):
            referrals.append(m.group(1).strip()[:120])
    if referrals:
        cm["referral_criteria"] = list(set(referrals))

    # ── NEW: Clinical features from narrative ──
    feature_patterns = [
        r"clinical\s+features?\s*[:;–-]\s*([^.;]{10,})",
        r"(?:signs?\s+and\s+symptoms?|presenting\s+features?)\s*[:;–-]\s*([^.;]{10,})",
    ]
    features = []
    for pat in feature_patterns:
        for m in re.finditer(pat, content, re.I):
            features.append(m.group(1).strip()[:150])
    if features:
        cm["clinical_features"] = features


def extract_clinical_metadata_for_image(chunk: Dict) -> None:
    """Populate clinical_metadata for an image chunk using its OCR text.

    Reuses the same extraction patterns as narrative chunks (condition,
    drug name, LOC, danger signs, referral, clinical features, age/weight,
    contraindications, special populations) applied to the OCR text content.
    """
    cm = chunk["clinical_metadata"]
    content = chunk.get("content", "")
    if not content or content == "<!-- image -->":
        return

    # Condition from section hierarchy
    condition = _infer_condition_from_hierarchy(
        chunk.get("section_hierarchy", [])
    )
    if condition:
        cm["condition"] = condition

    # Age patterns
    for m in AGE_PATTERN_RE.finditer(content):
        groups = m.groups()
        if groups[0]:
            cm["patient_age_max"] = f"{groups[0]} {groups[1]}"
        if groups[2]:
            cm["patient_age_max"] = f"{groups[2]} {groups[3]}"
        if groups[4]:
            cm["patient_age_min"] = f"{groups[4]} {groups[5]}"
        if groups[6] and groups[7]:
            cm["patient_age_min"] = f"{groups[6]} {groups[8]}"
            cm["patient_age_max"] = f"{groups[7]} {groups[8]}"

    # Weight mentions
    for m in WEIGHT_NARRATIVE_RE.finditer(content):
        weight = float(m.group(1))
        if "less" in m.group(0).lower() or "<" in m.group(0):
            cm["patient_weight_max_kg"] = weight
        else:
            cm["patient_weight_min_kg"] = weight

    # Contraindications
    contraindication_patterns = [
        r"contraindicated\s+(?:in|for)\s+([^.;]+)",
        r"(?:do not give|should not be (?:given|used)|avoid)\s+(?:in|for|to)\s+([^.;]+)",
        r"not recommended\s+(?:in|for)\s+([^.;]+)",
    ]
    contras = []
    for pat in contraindication_patterns:
        for m in re.finditer(pat, content, re.I):
            contras.append(m.group(1).strip())
    if contras:
        cm["contraindications"] = contras

    # Special populations
    special_pop_patterns = [
        r"(pregnant\s+women[^.;]*)",
        r"(children\s+(?:under|<|weighing\s*<)\s*[\d]+\s*(?:kg|years?|months?)[^.;]*)",
        r"(infants?\s*(?:<|under)\s*[\d]+\s*(?:months?|weeks?)[^.;]*)",
        r"(HIV[^.;]*patients?[^.;]*)",
    ]
    for bm in get_biomarker_patterns(CONFIG):
        special_pop_patterns.append(rf"({re.escape(bm)}\s+deficien[ct][^.;]*)")
    pops = []
    for pat in special_pop_patterns:
        for m in re.finditer(pat, content, re.I):
            pops.append(m.group(1).strip()[:100])
    if pops:
        cm["special_populations"] = list(set(pops))

    # Clinical section type from hierarchy
    hierarchy = chunk.get("section_hierarchy", [])
    for heading in hierarchy:
        heading_lower = heading.lower()
        for section_type, keywords in CLINICAL_SECTION_KW.items():
            if any(kw in heading_lower for kw in keywords):
                cm["clinical_section_type"] = section_type
                break
        if cm.get("clinical_section_type"):
            break

    # Level of Care extraction
    if LOC_RE.pattern != r"(?!)":
        loc_matches = LOC_RE.findall(content)
        if loc_matches:
            normalized = set(_normalize_loc(m) for m in loc_matches)
            cm["level_of_care"] = sorted(normalized)

    # Danger signs
    danger_patterns = [
        r"danger\s+signs?\s*[:;–-]\s*([^.;]+)",
        r"danger\s+signs?\s+include\s*([^.;]+)",
    ]
    dangers = []
    for pat in danger_patterns:
        for m in re.finditer(pat, content, re.I):
            dangers.append(m.group(1).strip()[:120])
    if dangers:
        cm["danger_signs"] = dangers

    # Referral criteria
    referral_patterns = [
        r"refer\s+(?:immediately|urgently)\s+(?:if|when|to)\s+([^.;]+)",
        r"refer(?:ral)?\s+(?:to|criteria)\s*[:;–-]\s*([^.;]+)",
    ]
    referrals = []
    for pat in referral_patterns:
        for m in re.finditer(pat, content, re.I):
            referrals.append(m.group(1).strip()[:120])
    if referrals:
        cm["referral_criteria"] = list(set(referrals))

    # Clinical features
    feature_patterns = [
        r"clinical\s+features?\s*[:;–-]\s*([^.;]{10,})",
        r"(?:signs?\s+and\s+symptoms?|presenting\s+features?)\s*[:;–-]\s*([^.;]{10,})",
    ]
    features = []
    for pat in feature_patterns:
        for m in re.finditer(pat, content, re.I):
            features.append(m.group(1).strip()[:150])
    if features:
        cm["clinical_features"] = features


# ─────────────────────────────────────────────────────────────────────────────
# 7.  STITCHED TABLE HANDLING
# ─────────────────────────────────────────────────────────────────────────────
def create_stitched_table_chunks(
    stitched_tables: List[Dict],
    xval: Dict,
    validation_map: Dict,
    nll_map: Dict,
) -> List[Dict]:
    """Create chunk(s) for page-boundary stitched tables from Stage 2."""
    chunks: List[Dict] = []

    for i, st in enumerate(stitched_tables):
        pages = st.get("pages", [])
        md = st.get("markdown", "")
        word_count = len(md.split())

        # NLL from Stage 2's nll_regeneration (or from nll_map)
        nll = nll_map.get("S1")
        # Also check xval's nll_regeneration
        if not nll:
            for regen in xval.get("nll_regeneration", []):
                if regen.get("pages") == pages:
                    nll = regen.get("nll")
                    break

        validation = validation_map.get("S1")

        chunk = {
            "chunk_id": "stitched_table-S1",
            "chunk_type": "dosing_table",
            "source_pages": pages,
            "section_hierarchy": [
                "5. Case management",
                "5.2 Treating malaria",
                "5.2.1 Treating uncomplicated malaria",
                "5.2.1.1 Artemisinin-based combination therapy",
                "5.2.1.1.2 Dosing of ACTs",
            ],
            "section_number": "5.2.1.1.2",
            "section_title": "Dosing of ACTs",
            "content": md,
            "content_type": "markdown_table",
            "nll": nll,
            "table_index": "S1",
            "table_classification": {
                "stage1": "dosing",
                "stage2_refined": "dosing",
                "final": "dosing",
            },
            "validation": validation,
            "clinical_domain": "Dosing of ACTs",
            "safety": {
                "preservation_level": "verbatim",
                "reasoning": "Stitched dosing table — no paraphrasing allowed",
            },
            "verified_by": {
                "status": "unverified",
                "reviewer_name": None,
                "reviewer_role": None,
                "institution": None,
                "digital_signature": None,
                "verified_at": None,
                "comments": None,
            },
            "clinical_metadata": {
                "condition": "Uncomplicated malaria",
                "drug_name": None,
                "dosage_summary": None,
                "patient_weight_min_kg": None,
                "patient_weight_max_kg": None,
                "patient_age_min": None,
                "patient_age_max": None,
                "route": "oral",
                "frequency": None,
                "duration": None,
                "contraindications": [],
                "special_populations": [],
            },
            "related_chunks": {
                "prev_sibling": None,
                "next_sibling": None,
                "preceding_narrative": None,
                "following_narrative": None,
                "context_for_tables": [],
                "section_siblings": [],
            },
            "word_count": word_count,
            "token_estimate": int(word_count * TOKEN_MULTIPLIER),
        }

        # Fill clinical metadata from the stitched table content
        extract_clinical_metadata_for_dosing_table(chunk, md)
        chunks.append(chunk)

    return chunks


# ─────────────────────────────────────────────────────────────────────────────
# 8.  RELATED-CHUNK LINKING
# ─────────────────────────────────────────────────────────────────────────────
def link_related_chunks(chunks: List[Dict]) -> None:
    """Establish bidirectional relationships between chunks.

    Pass 1: Sequential prev/next siblings
    Pass 2: Table ↔ Narrative proximity
    Pass 3: Section-based grouping
    """
    # Pass 1: Sequential linking
    for i in range(len(chunks)):
        if i > 0:
            chunks[i]["related_chunks"]["prev_sibling"] = chunks[i - 1]["chunk_id"]
        if i < len(chunks) - 1:
            chunks[i]["related_chunks"]["next_sibling"] = chunks[i + 1]["chunk_id"]

    # Pass 2: Table ↔ Narrative proximity
    for i, chunk in enumerate(chunks):
        if chunk["chunk_type"] != "narrative":
            # Walk backward for preceding narrative
            for j in range(i - 1, -1, -1):
                if chunks[j]["chunk_type"] == "narrative":
                    chunk["related_chunks"]["preceding_narrative"] = chunks[j]["chunk_id"]
                    chunks[j]["related_chunks"]["context_for_tables"].append(
                        chunk["chunk_id"]
                    )
                    break
            # Walk forward for following narrative
            for j in range(i + 1, len(chunks)):
                if chunks[j]["chunk_type"] == "narrative":
                    chunk["related_chunks"]["following_narrative"] = chunks[j]["chunk_id"]
                    break

    # Pass 3: Section grouping
    section_groups: Dict[str, List[str]] = defaultdict(list)
    for chunk in chunks:
        key = "|".join(chunk.get("section_hierarchy", []))
        section_groups[key].append(chunk["chunk_id"])

    for chunk in chunks:
        key = "|".join(chunk.get("section_hierarchy", []))
        siblings = [
            cid for cid in section_groups[key] if cid != chunk["chunk_id"]
        ]
        chunk["related_chunks"]["section_siblings"] = siblings


# ─────────────────────────────────────────────────────────────────────────────
# 9.  VALIDATION & STATISTICS
# ─────────────────────────────────────────────────────────────────────────────
def validate_chunks(
    chunks: List[Dict], inventory: List[Dict]
) -> Dict[str, Any]:
    """Run sanity checks on chunking output."""
    issues: List[str] = []

    # 1. Check for duplicate chunk_ids
    ids = [c["chunk_id"] for c in chunks]
    dupes = [cid for cid in ids if ids.count(cid) > 1]
    if dupes:
        issues.append(f"Duplicate chunk_ids: {set(dupes)}")

    # 2. Check that inventory tables have matching chunks
    inv_indices = {e["index"] for e in inventory}
    chunk_table_indices = {
        c["table_index"] for c in chunks if c["table_index"] is not None
    }
    missing = inv_indices - chunk_table_indices
    if missing:
        issues.append(
            f"{len(missing)} inventory tables not matched to chunks: "
            f"{sorted(list(missing))[:10]}..."
        )

    # 3. Check related_chunks references are valid
    valid_ids = set(ids)
    bad_refs = 0
    for c in chunks:
        rc = c.get("related_chunks", {})
        for key in ["prev_sibling", "next_sibling", "preceding_narrative", "following_narrative"]:
            ref = rc.get(key)
            if ref is not None and ref not in valid_ids:
                bad_refs += 1
        for ref in rc.get("context_for_tables", []):
            if ref not in valid_ids:
                bad_refs += 1
    if bad_refs:
        issues.append(f"{bad_refs} invalid related_chunk references")

    # 4. Check token estimates
    narrative_tokens = [
        c["token_estimate"]
        for c in chunks
        if c["chunk_type"] == "narrative" and c["token_estimate"] > 0
    ]
    if narrative_tokens:
        max_t = max(narrative_tokens)
        if max_t > MAX_NARRATIVE_TOKENS * 2:
            issues.append(
                f"Narrative chunk with {max_t} tokens exceeds 2× limit"
            )

    # 5. Safety level distribution
    levels = defaultdict(int)
    for c in chunks:
        level = c.get("safety", {}).get("preservation_level", "unknown")
        levels[level] += 1

    # 6. Verified-by status check
    unverified = sum(
        1 for c in chunks
        if c.get("verified_by", {}).get("status") == "unverified"
    )

    # 7. Clinical metadata coverage for dosing tables
    dosing_chunks = [
        c for c in chunks if c["chunk_type"] == "dosing_table"
    ]
    dosing_with_drug = sum(
        1 for c in dosing_chunks
        if c.get("clinical_metadata", {}).get("drug_name")
    )
    dosing_with_weight = sum(
        1 for c in dosing_chunks
        if c.get("clinical_metadata", {}).get("patient_weight_min_kg") is not None
    )

    return {
        "total_chunks": len(chunks),
        "issues": issues,
        "is_valid": len(issues) == 0,
        "inventory_tables": len(inv_indices),
        "matched_tables": len(chunk_table_indices & inv_indices),
        "unmatched_tables": len(missing) if missing else 0,
        "duplicate_ids": len(set(dupes)) if dupes else 0,
        "invalid_references": bad_refs,
        "preservation_levels": dict(levels),
        "all_unverified": unverified == len(chunks),
        "dosing_tables_with_drug_name": dosing_with_drug,
        "dosing_tables_with_weight_range": dosing_with_weight,
        "total_dosing_table_chunks": len(dosing_chunks),
    }


# ─────────────────────────────────────────────────────────────────────────────
# 10. SAVE OUTPUT
# ─────────────────────────────────────────────────────────────────────────────
def save_chunks(
    chunks: List[Dict],
    validation: Dict,
    timings: Dict,
) -> Dict:
    """Save chunks.json with envelope metadata."""
    # Count chunk types
    type_counts: Dict[str, int] = defaultdict(int)
    for c in chunks:
        type_counts[c["chunk_type"]] += 1

    envelope = {
        "pipeline_version": "4a",
        "source_document": get_document_title(CONFIG),
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "total_chunks": len(chunks),
        "chunk_type_counts": dict(type_counts),
        "stages_loaded": {
            "stage1_inventory": True,
            "stage2_cross_validation": True,
            "stage3_plausibility": True,
        },
        "validation_summary": validation,
        "timings": timings,
        "chunks": chunks,
    }

    out_path = OUTPUT_DIR / "chunks.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(envelope, f, indent=2, ensure_ascii=False)

    print(f"\n  Saved {out_path} ({os.path.getsize(out_path) / 1024:.0f} KB)")
    return envelope


# ─────────────────────────────────────────────────────────────────────────────
# 11. MAIN
# ─────────────────────────────────────────────────────────────────────────────
def main():
    """Full Stage 4a pipeline: chunk, enrich, link, validate, save."""
    t_start = time.perf_counter()
    timings: Dict[str, float] = {}

    print("=" * 70)
    print("  STAGE 4a — CHUNKING + METADATA")
    print("=" * 70)

    # ── Step 1: Load data ────────────────────────────────────────────────
    print("\n  [1/7] Loading stage data...")
    t0 = time.perf_counter()
    data = load_stage_data()
    timings["load_data_s"] = round(time.perf_counter() - t0, 3)
    print(f"        Loaded in {timings['load_data_s']}s")
    print(f"        Markdown: {len(data['markdown']):,} chars")
    print(f"        Inventory: {len(data['inventory'])} tables")

    # ── Step 2: Build enrichment lookups ─────────────────────────────────
    print("\n  [2/7] Building enrichment lookups...")
    t0 = time.perf_counter()
    nll_map = parse_nll_file(data["nll_text"])
    reclass_map, validation_map, stitched_tables = build_enrichment_lookups(
        data["inventory"], data["xval"], data["plausibility"]
    )
    timings["build_lookups_s"] = round(time.perf_counter() - t0, 3)
    print(f"        NLL entries: {len(nll_map)}")
    print(f"        Reclassifications: {len(reclass_map)}")
    print(f"        Validation entries: {len(validation_map)}")
    print(f"        Stitched tables: {len(stitched_tables)}")

    # Build page→image mapping for image chunk enrichment
    image_inventory = data.get("image_inventory", [])
    image_by_page: Dict[int, List[Dict]] = defaultdict(list)
    for img in image_inventory:
        pg = img.get("page_no")
        if pg:
            image_by_page[pg].append(img)
    if image_inventory:
        print(f"        Image inventory: {len(image_inventory)} images")

    # ── Step 3: Parse markdown ───────────────────────────────────────────
    print("\n  [3/7] Parsing markdown...")
    t0 = time.perf_counter()
    md_lines = data["markdown"].split("\n")
    page_markers = build_page_map(md_lines)
    sections = parse_markdown_into_sections(data["markdown"])
    build_section_hierarchy(sections)
    timings["parse_markdown_s"] = round(time.perf_counter() - t0, 3)
    print(f"        Sections: {len(sections)}")
    print(f"        Page markers: {len(page_markers)}")

    # ── Step 4: Create chunks ────────────────────────────────────────────
    print("\n  [4/7] Creating chunks...")
    t0 = time.perf_counter()
    all_chunks: List[Dict] = []
    narrative_counter = 0
    table_counter = 0
    image_counter = 0
    unmatched_table_counter = 0

    # Pass 1: Collect all table elements with resolved page from first_line_no
    all_table_elements: List[Dict] = []
    section_elements_cache: List[Tuple[Dict, List[Dict]]] = []

    for section in sections:
        elements = extract_elements_from_section(section)
        section_elements_cache.append((section, elements))
        for elem in elements:
            if elem["type"] == "table":
                all_table_elements.append(elem)

    # Match all table elements to inventory using first_line_no for page
    table_matches = match_tables_to_inventory(
        all_table_elements, data["inventory"], page_markers
    )

    # Pass 2: Create chunks in document order
    table_elem_idx = 0
    for section, elements in section_elements_cache:
        for elem in elements:
            if elem["type"] == "narrative":
                text = "\n".join(elem["lines"]).strip()
                if not text:
                    continue
                sub_chunks = split_narrative_if_needed(text)
                for sub in sub_chunks:
                    if not sub.strip():
                        continue
                    narrative_counter += 1
                    chunk = create_narrative_chunk(
                        sub, section, narrative_counter, page_markers,
                        first_line_no=elem.get("first_line_no"),
                    )
                    all_chunks.append(chunk)

            elif elem["type"] == "table":
                inv_entry = table_matches.get(table_elem_idx)
                table_elem_idx += 1
                table_counter += 1
                chunk = create_table_chunk(
                    elem["lines"],
                    section,
                    inv_entry,
                    reclass_map,
                    validation_map,
                    nll_map,
                    page_markers,
                    first_line_no=elem.get("first_line_no"),
                )
                # Fix chunk_id for unmatched tables (avoid duplicates)
                if inv_entry is None:
                    unmatched_table_counter += 1
                    chunk["chunk_id"] = f"unmatched_table-{unmatched_table_counter:04d}"
                all_chunks.append(chunk)

            elif elem["type"] == "image":
                image_counter += 1
                # Match this image to its Stage 1 OCR data via page number
                page = get_page_for_line(
                    elem.get("first_line_no") or section["start_line"],
                    page_markers,
                )
                img_data = None
                if page and page in image_by_page:
                    candidates = image_by_page[page]
                    if candidates:
                        img_data = candidates.pop(0)  # consume in order
                chunk = create_image_chunk(
                    section, image_counter, page_markers,
                    first_line_no=elem.get("first_line_no"),
                    image_data=img_data,
                )
                all_chunks.append(chunk)

    timings["create_chunks_s"] = round(time.perf_counter() - t0, 3)
    enriched_images = sum(
        1 for c in all_chunks
        if c.get("chunk_type") == "image" and c.get("content_type") == "image_ocr"
    )
    print(f"        Narrative chunks: {narrative_counter}")
    print(f"        Table chunks: {table_counter}")
    print(f"        Image chunks: {image_counter} ({enriched_images} with OCR text)")

    # ── Step 5: Safety + Clinical metadata ───────────────────────────────
    print("\n  [5/7] Enriching with safety + clinical metadata...")
    t0 = time.perf_counter()
    for chunk in all_chunks:
        assign_safety_metadata(chunk)
        if chunk["chunk_type"] == "dosing_table":
            extract_clinical_metadata_for_dosing_table(
                chunk, chunk.get("content", "")
            )
        elif chunk["chunk_type"] == "clinical_table":
            extract_clinical_metadata_for_clinical_table(
                chunk, chunk.get("content", "")
            )
        elif chunk["chunk_type"] == "narrative":
            extract_clinical_metadata_for_narrative(chunk)
        elif chunk["chunk_type"] == "image" and chunk.get("content_type") == "image_ocr":
            extract_clinical_metadata_for_image(chunk)

    # Add stitched table chunks
    stitched_chunks = create_stitched_table_chunks(
        stitched_tables, data["xval"], validation_map, nll_map
    )
    all_chunks.extend(stitched_chunks)
    timings["enrich_metadata_s"] = round(time.perf_counter() - t0, 3)

    verbatim_count = sum(
        1 for c in all_chunks
        if c.get("safety", {}).get("preservation_level") == "verbatim"
    )
    high_count = sum(
        1 for c in all_chunks
        if c.get("safety", {}).get("preservation_level") == "high"
    )
    print(f"        Verbatim preservation: {verbatim_count} chunks")
    print(f"        High preservation: {high_count} chunks")
    print(f"        Stitched table chunks: {len(stitched_chunks)}")

    # ── Step 6: Link related chunks ──────────────────────────────────────
    print("\n  [6/7] Linking related chunks...")
    t0 = time.perf_counter()
    link_related_chunks(all_chunks)
    timings["link_chunks_s"] = round(time.perf_counter() - t0, 3)

    # ── Step 7: Validate and save ────────────────────────────────────────
    print("\n  [7/7] Validating and saving...")
    t0 = time.perf_counter()
    validation = validate_chunks(all_chunks, data["inventory"])
    timings["validate_s"] = round(time.perf_counter() - t0, 3)

    timings["total_s"] = round(time.perf_counter() - t_start, 3)

    envelope = save_chunks(all_chunks, validation, timings)

    # ── Final scorecard ──────────────────────────────────────────────────
    print(f"\n{'='*70}")
    print(f"  STAGE 4a — FINAL SCORECARD")
    print(f"{'='*70}")

    tc = envelope["chunk_type_counts"]
    print(f"  Total chunks              : {envelope['total_chunks']}")
    for ctype, count in sorted(tc.items()):
        print(f"    {ctype:<22}: {count}")

    print()
    print(f"  Safety preservation levels:")
    for level, count in sorted(
        validation["preservation_levels"].items()
    ):
        print(f"    {level:<22}: {count}")

    print()
    print(f"  Clinical metadata coverage (dosing tables):")
    print(
        f"    With drug_name          : {validation['dosing_tables_with_drug_name']}"
        f" / {validation['total_dosing_table_chunks']}"
    )
    print(
        f"    With weight range       : {validation['dosing_tables_with_weight_range']}"
        f" / {validation['total_dosing_table_chunks']}"
    )

    print()
    print(f"  Verification status       : All unverified (ready for Stage 4b)")

    print()
    v = validation
    if v["is_valid"]:
        print(f"  ✅ Validation: PASSED ({v['matched_tables']}/{v['inventory_tables']} tables matched)")
    else:
        print(f"  ⚠️  Validation issues:")
        for issue in v["issues"]:
            print(f"      - {issue}")

    print(f"\n  Timings:")
    for key, val in timings.items():
        label = key.replace("_", " ").replace(" s", "")
        print(f"    {label:<25}: {val}s")

    print(f"\n{'='*70}\n")

    return envelope


if __name__ == "__main__":
    main()
