# -*- coding: utf-8 -*-
"""
Stage 3: Automated Plausibility Checks
=======================================
Validates the clinical plausibility of extracted dosing tables using six
automated checks.  Operates on the refined set of dosing tables after
Stage 2 reclassification (29 true dosing tables, down from 41).

Checks:
  1. Weight-band contiguity  — no gaps between consecutive ranges
  2. Dose monotonicity       — both components of combination drugs increase
  3. Weight-band coverage    — tables span from pediatric through adult bands
  4. Clinical dose bounds    — per-kg dose within WHO reference ranges
  5. Combination consistency — component ratio is stable across weight bands
  6. Positive / no empty     — all doses > 0, no empty cells in dose columns

Run:
    python stage3_automated_checks.py
"""

# ─────────────────────────────────────────────────────────────────────────────
# 1.  IMPORTS
# ─────────────────────────────────────────────────────────────────────────────
import os
import re
import json
import time
from pathlib import Path
from typing import Optional

from pipeline_config import (
    load_config, get_drug_keywords, get_dose_reference_ranges,
)

# ─────────────────────────────────────────────────────────────────────────────
# 2.  CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────
CONFIG = load_config()
OUTPUT_DIR = Path("extraction_output")

# Weight-band coverage thresholds (kg)
COVERAGE_PEDIATRIC_LOW = 10.0    # table should start at or below this
COVERAGE_ADULT_HIGH = 35.0       # table should reach at least this (or open-ended)

# Clinical dose bounds tolerance
DOSE_BOUNDS_TOLERANCE = 2.5      # flag if per-kg dose is outside 0.4x–2.5x reference

# Combination drug ratio tolerance
RATIO_TOLERANCE = 0.35           # flag if ratio varies > 35% from median


# ─────────────────────────────────────────────────────────────────────────────
# 3.  ENHANCED WEIGHT-BAND PARSER
# ─────────────────────────────────────────────────────────────────────────────

def parse_weight_range(cell: str) -> Optional[tuple]:
    """Parse a weight-band cell into (low, high).

    Returns (low, high) as floats.  high=None means open-ended (≥, >).
    Returns None if the cell is not a weight range.

    Handles all formats found in WHO malaria guidelines:
      "< 15"         → (0, 15)
      "15 to < 25"   → (15, 25)
      "≥ 35"         → (35, None)
      "60 < 80"      → (60, 80)
      ">80"          → (80, None)
      "> 10 to ≤ 20" → (10, 20)
      "50 to 100"    → (50, 100)
      "5 to < 25 a"  → (5, 25)   [footnote marker stripped]
    """
    # Strip footnote markers (trailing letters/superscripts)
    cell = re.sub(r"\s*[a-d]\s*$", "", cell.strip(), flags=re.IGNORECASE)
    # Normalise unicode
    cell = cell.replace("\u2265", ">=").replace("\u2264", "<=")
    cell = cell.replace("\u2013", "-").replace("\u2014", "-")

    # Pattern 1: "> N to ≤ M" or "> N to < M"
    m = re.match(r"[>]\s*([\d.]+)\s*(?:to)\s*[<≤]=?\s*([\d.]+)", cell)
    if m:
        return (float(m.group(1)), float(m.group(2)))

    # Pattern 2: "N to < M" or "N to ≤ M" or "N to M"
    m = re.match(r"([\d.]+)\s*(?:to|[-])\s*[<≤]=?\s*([\d.]+)", cell)
    if m:
        return (float(m.group(1)), float(m.group(2)))

    # Pattern 3: "N < M" (e.g., "60 < 80" — means 60 to < 80)
    m = re.match(r"([\d.]+)\s*<\s*([\d.]+)", cell)
    if m:
        return (float(m.group(1)), float(m.group(2)))

    # Pattern 4: ">=N" or "≥ N" or "> N" (open-ended high)
    m = re.match(r"[>≥]=?\s*([\d.]+)", cell)
    if m:
        return (float(m.group(1)), None)

    # Pattern 5: "< N" or "≤ N" (upper bound only)
    m = re.match(r"[<≤]=?\s*([\d.]+)", cell)
    if m:
        return (0.0, float(m.group(1)))

    return None


# ─────────────────────────────────────────────────────────────────────────────
# 4.  ENHANCED DOSE PARSER (handles combination drugs)
# ─────────────────────────────────────────────────────────────────────────────

def parse_dose_values(cell: str) -> list:
    """Parse a dose cell into a list of numeric values.

    Returns all numeric components found:
      "20 + 120"      → [20.0, 120.0]
      "250 / 12.5"    → [250.0, 12.5]
      "25 mg"          → [25.0]
      "3.75"           → [3.75]
      ""               → []

    For combination drugs, the order matches the header
    (e.g., artemether + lumefantrine → [artemether_mg, lumefantrine_mg]).
    """
    if not cell or not cell.strip():
        return []
    # Extract all numeric values
    values = re.findall(r"([\d]+\.?\d*)", cell)
    return [float(v) for v in values]


# ─────────────────────────────────────────────────────────────────────────────
# 5.  TABLE PARSING HELPER
# ─────────────────────────────────────────────────────────────────────────────

def parse_dosing_table(md: str) -> dict:
    """Parse a dosing table's markdown into structured data.

    Returns:
      {
        "headers": [str, ...],
        "weight_col": int or None,
        "dose_cols": [int, ...],
        "rows": [
          {"weight_cell": str, "weight_range": (lo, hi) or None,
           "dose_cells": [str, ...], "dose_values": [[float, ...], ...]},
          ...
        ]
      }
    """
    lines = [l.strip() for l in md.strip().split("\n") if l.strip() and "---" not in l]
    if len(lines) < 2:
        return {"headers": [], "weight_col": None, "dose_cols": [], "rows": []}

    # Parse header
    header_cells = [c.strip() for c in lines[0].split("|") if c.strip()]
    data_lines = lines[1:]

    # Identify weight and dose columns
    weight_col = None
    dose_cols = []
    for ci, h in enumerate(header_cells):
        h_lower = h.lower()
        if any(kw in h_lower for kw in [
            "body weight", "weight (kg)", "weight"
        ]) and weight_col is None:
            weight_col = ci
        elif any(kw in h_lower for kw in
                 ["dose", "mg", "tablet"] + get_drug_keywords(CONFIG)):
            dose_cols.append(ci)

    # If no dose column identified from header, assume column 1+
    if not dose_cols and weight_col is not None and len(header_cells) > 1:
        dose_cols = [i for i in range(len(header_cells)) if i != weight_col]

    # Parse data rows
    rows = []
    for line in data_lines:
        cells = [c.strip() for c in line.split("|") if c.strip()]
        if not cells:
            continue

        weight_cell = cells[weight_col] if weight_col is not None and weight_col < len(cells) else ""
        weight_range = parse_weight_range(weight_cell) if weight_cell else None

        dose_cells = []
        dose_values = []
        for dc in dose_cols:
            if dc < len(cells):
                dose_cells.append(cells[dc])
                dose_values.append(parse_dose_values(cells[dc]))
            else:
                dose_cells.append("")
                dose_values.append([])

        rows.append({
            "weight_cell": weight_cell,
            "weight_range": weight_range,
            "dose_cells": dose_cells,
            "dose_values": dose_values,
        })

    return {
        "headers": header_cells,
        "weight_col": weight_col,
        "dose_cols": dose_cols,
        "rows": rows,
    }


# ─────────────────────────────────────────────────────────────────────────────
# 6.  CHECK 1: WEIGHT-BAND CONTIGUITY
# ─────────────────────────────────────────────────────────────────────────────

def check_weight_contiguity(parsed: dict) -> dict:
    """Verify no gaps exist between consecutive weight bands.

    Returns {"passed": bool, "issues": [str, ...]}.
    """
    issues = []
    weight_ranges = [r["weight_range"] for r in parsed["rows"] if r["weight_range"]]

    if len(weight_ranges) < 2:
        return {"passed": True, "issues": ["<2 weight bands — skipped"]}

    for i in range(len(weight_ranges) - 1):
        current_high = weight_ranges[i][1]
        next_low = weight_ranges[i + 1][0]

        if current_high is None:
            # Open-ended band (≥) should be last
            if i < len(weight_ranges) - 1:
                issues.append(
                    f"Open-ended band (>={weight_ranges[i][0]}) is not the last row"
                )
            continue

        if next_low is not None and abs(current_high - next_low) > 0.5:
            issues.append(
                f"Gap: band {i+1} ends at {current_high} kg, "
                f"band {i+2} starts at {next_low} kg "
                f"(gap = {abs(current_high - next_low):.1f} kg)"
            )

    return {"passed": len(issues) == 0, "issues": issues}


# ─────────────────────────────────────────────────────────────────────────────
# 7.  CHECK 2: DOSE MONOTONICITY (combination-aware)
# ─────────────────────────────────────────────────────────────────────────────

def check_dose_monotonicity(parsed: dict) -> dict:
    """Verify doses increase (or stay equal) with weight for every component.

    For combination drugs like "20 + 120", both values must individually
    be non-decreasing across rows.

    Returns {"passed": bool, "issues": [str, ...]}.
    """
    issues = []

    if not parsed["dose_cols"]:
        return {"passed": True, "issues": ["No dose columns found — skipped"]}

    # For each dose column, check every component
    for dc_idx, dc in enumerate(parsed["dose_cols"]):
        header = parsed["headers"][dc] if dc < len(parsed["headers"]) else f"Col {dc}"

        # Gather per-row component values
        all_row_values = []
        for row in parsed["rows"]:
            if dc_idx < len(row["dose_values"]):
                all_row_values.append(row["dose_values"][dc_idx])
            else:
                all_row_values.append([])

        if not all_row_values:
            continue

        # Determine max number of components (e.g., 2 for "20 + 120")
        max_components = max(len(v) for v in all_row_values) if all_row_values else 0

        for comp_idx in range(max_components):
            comp_label = f"component {comp_idx+1}" if max_components > 1 else "dose"
            prev_val = None
            for r_i, vals in enumerate(all_row_values):
                if comp_idx < len(vals):
                    curr_val = vals[comp_idx]
                    if prev_val is not None and curr_val < prev_val:
                        issues.append(
                            f"{header} {comp_label}: row {r_i} = {curr_val} < "
                            f"row {r_i-1} = {prev_val} (not monotonic)"
                        )
                    prev_val = curr_val

    return {"passed": len(issues) == 0, "issues": issues}


# ─────────────────────────────────────────────────────────────────────────────
# 8.  CHECK 3: WEIGHT-BAND COVERAGE COMPLETENESS
# ─────────────────────────────────────────────────────────────────────────────

def check_weight_coverage(parsed: dict, table_info: dict) -> dict:
    """Verify the table covers from pediatric through adult weight bands.

    Expected for first-line ACT dosing tables:
      - Starts at or below COVERAGE_PEDIATRIC_LOW (10 kg)
      - Ends at or above COVERAGE_ADULT_HIGH (35 kg) or is open-ended (≥)

    Returns {"passed": bool, "issues": [str, ...],
             "range_low": float, "range_high": float or None}.
    """
    issues = []
    weight_ranges = [r["weight_range"] for r in parsed["rows"] if r["weight_range"]]

    if not weight_ranges:
        return {"passed": True, "issues": ["No weight bands found — skipped"],
                "range_low": None, "range_high": None}

    # First band's lower bound
    range_low = weight_ranges[0][0]
    # Last band's upper bound (None = open-ended)
    range_high = weight_ranges[-1][1]
    last_low = weight_ranges[-1][0]

    # Check pediatric coverage
    if range_low > COVERAGE_PEDIATRIC_LOW:
        issues.append(
            f"Table starts at {range_low} kg — may be missing infant doses "
            f"(expected start <= {COVERAGE_PEDIATRIC_LOW} kg)"
        )

    # Check adult coverage
    if range_high is not None and range_high < COVERAGE_ADULT_HIGH:
        # Not open-ended and doesn't reach adult threshold
        issues.append(
            f"Table ends at {range_high} kg — may be missing adult doses "
            f"(expected >= {COVERAGE_ADULT_HIGH} kg or open-ended)"
        )
    elif range_high is None and last_low < COVERAGE_ADULT_HIGH:
        # Open-ended but starts below threshold — check it at least starts high enough
        # This is actually fine (e.g., "≥ 35" covers all adults)
        # Only flag if the open-ended band starts well below adult range
        if last_low < COVERAGE_ADULT_HIGH * 0.5:
            issues.append(
                f"Open-ended band starts at {last_low} kg — "
                f"unusually low for adult dosing"
            )

    return {
        "passed": len(issues) == 0,
        "issues": issues,
        "range_low": range_low,
        "range_high": range_high,
    }


# ─────────────────────────────────────────────────────────────────────────────
# 9.  CHECK 4: CLINICAL DOSE BOUNDS
# ─────────────────────────────────────────────────────────────────────────────

# Reference per-kg dose ranges (loaded from pipeline_config.json).
# These are wide ranges to catch only gross extraction errors, not subtle
# clinical deviations.
_DRUG_DOSE_RANGES = get_dose_reference_ranges(CONFIG)


def _identify_drug(header: str) -> Optional[str]:
    """Try to identify which drug a dose column refers to from its header."""
    h = header.lower()
    for drug in _DRUG_DOSE_RANGES:
        if drug in h:
            return drug
    # For combination headers like "artemether + lumefantrine dose"
    # return the first match
    for drug in _DRUG_DOSE_RANGES:
        if drug in h:
            return drug
    return None


def _identify_drugs_from_header(header: str) -> list:
    """Identify all drugs mentioned in a combination header."""
    h = header.lower()
    found = []
    for drug in _DRUG_DOSE_RANGES:
        if drug in h:
            found.append(drug)
    return found


def check_clinical_bounds(parsed: dict) -> dict:
    """Verify per-kg dose values fall within plausible clinical ranges.

    For each row: dose / midpoint_weight should be within the expected
    range for the drug (with tolerance).

    Returns {"passed": bool, "issues": [str, ...]}.
    """
    issues = []

    for dc_idx, dc in enumerate(parsed["dose_cols"]):
        header = parsed["headers"][dc] if dc < len(parsed["headers"]) else ""
        drugs = _identify_drugs_from_header(header)

        if not drugs:
            continue  # Can't identify drug — skip bounds check

        for r_i, row in enumerate(parsed["rows"]):
            wr = row["weight_range"]
            if wr is None:
                continue

            # Compute midpoint weight for per-kg calculation
            lo, hi = wr
            if hi is None:
                # Open-ended: use lo + 20 as estimate (e.g., ≥ 35 → midpoint ~55)
                mid_weight = lo + 20.0
            elif lo == 0:
                mid_weight = hi / 2.0
            else:
                mid_weight = (lo + hi) / 2.0

            if mid_weight <= 0:
                continue

            # Get dose values for this row
            if dc_idx < len(row["dose_values"]):
                dose_vals = row["dose_values"][dc_idx]
            else:
                continue

            # Check each component against its drug reference
            for comp_idx, (dose_val, drug) in enumerate(zip(dose_vals, drugs)):
                if dose_val <= 0:
                    continue

                per_kg = dose_val / mid_weight
                ref_lo, ref_hi = _DRUG_DOSE_RANGES[drug]

                # Apply tolerance
                bound_lo = ref_lo / DOSE_BOUNDS_TOLERANCE
                bound_hi = ref_hi * DOSE_BOUNDS_TOLERANCE

                if per_kg < bound_lo or per_kg > bound_hi:
                    issues.append(
                        f"Row {r_i+1} ({row['weight_cell']}): "
                        f"{drug} {dose_val} mg / {mid_weight:.0f} kg = "
                        f"{per_kg:.2f} mg/kg — "
                        f"outside range [{ref_lo}–{ref_hi}] mg/kg "
                        f"(with {DOSE_BOUNDS_TOLERANCE}x tolerance: "
                        f"[{bound_lo:.2f}–{bound_hi:.1f}])"
                    )

    return {"passed": len(issues) == 0, "issues": issues}


# ─────────────────────────────────────────────────────────────────────────────
# 10. CHECK 5: COMBINATION DRUG CONSISTENCY
# ─────────────────────────────────────────────────────────────────────────────

def check_combination_consistency(parsed: dict) -> dict:
    """Verify combination drug component ratios are stable across weight bands.

    For drugs like "20 + 120" (ratio 1:6), the ratio should be approximately
    constant across all rows.  Large deviations suggest parsing or extraction
    errors.

    Returns {"passed": bool, "issues": [str, ...]}.
    """
    issues = []

    for dc_idx, dc in enumerate(parsed["dose_cols"]):
        header = parsed["headers"][dc] if dc < len(parsed["headers"]) else ""

        # Collect all rows' component values for this dose column
        row_values = []
        for row in parsed["rows"]:
            if dc_idx < len(row["dose_values"]):
                vals = row["dose_values"][dc_idx]
                if len(vals) >= 2:
                    row_values.append(vals)

        if len(row_values) < 2:
            continue  # Not a combination drug or too few rows

        # Compute ratio (component2 / component1) for each row
        ratios = []
        for vals in row_values:
            if vals[0] > 0:
                ratios.append(vals[1] / vals[0])

        if not ratios:
            continue

        # Check ratio stability: compare each to the median
        ratios_sorted = sorted(ratios)
        median_ratio = ratios_sorted[len(ratios_sorted) // 2]

        if median_ratio <= 0:
            continue

        for r_i, ratio in enumerate(ratios):
            deviation = abs(ratio - median_ratio) / median_ratio
            if deviation > RATIO_TOLERANCE:
                row = parsed["rows"][r_i] if r_i < len(parsed["rows"]) else {}
                issues.append(
                    f"Row {r_i+1} ({row.get('weight_cell', '?')}): "
                    f"ratio = {ratio:.2f} vs median {median_ratio:.2f} "
                    f"(deviation {deviation*100:.0f}% > {RATIO_TOLERANCE*100:.0f}% threshold)"
                )

    return {"passed": len(issues) == 0, "issues": issues}


# ─────────────────────────────────────────────────────────────────────────────
# 11. CHECK 6: POSITIVE VALUES AND EMPTY CELLS
# ─────────────────────────────────────────────────────────────────────────────

def check_positive_no_empty(parsed: dict) -> dict:
    """Verify all dose values are positive and no dose cells are empty.

    Returns {"passed": bool, "issues": [str, ...]}.
    """
    issues = []

    for r_i, row in enumerate(parsed["rows"]):
        # Check weight cell
        if not row["weight_cell"].strip():
            issues.append(f"Row {r_i+1}: empty weight cell")

        # Check dose cells
        for dc_idx, dose_cell in enumerate(row["dose_cells"]):
            if not dose_cell.strip():
                issues.append(f"Row {r_i+1}, dose col {dc_idx+1}: empty dose cell")
                continue

            for comp_idx, val in enumerate(row["dose_values"][dc_idx] if dc_idx < len(row["dose_values"]) else []):
                if val <= 0:
                    issues.append(
                        f"Row {r_i+1}, dose col {dc_idx+1}, "
                        f"component {comp_idx+1}: non-positive value {val}"
                    )

    return {"passed": len(issues) == 0, "issues": issues}


# ─────────────────────────────────────────────────────────────────────────────
# 12. LOAD DATA (Stage 1 tables + Stage 2 reclassifications + stitched table)
# ─────────────────────────────────────────────────────────────────────────────

def load_dosing_tables() -> list:
    """Load all dosing tables with markdown, applying Stage 2 reclassifications.

    Returns a list of table dicts with 'index', 'page_no', 'classification',
    'markdown', etc.  Only tables still classified as 'dosing' are returned.
    """
    print(f"\n{'='*70}")
    print(f"  LOADING DATA")
    print(f"{'='*70}")

    # Load table inventory
    inv_path = OUTPUT_DIR / "table_inventory.json"
    if not inv_path.exists():
        raise FileNotFoundError("table_inventory.json not found — run Stage 1 first")
    with open(inv_path, "r", encoding="utf-8") as f:
        inventory = json.load(f)
    print(f"  Loaded table_inventory.json: {len(inventory)} tables")

    # Load Stage 2 reclassifications
    xval_path = OUTPUT_DIR / "cross_validation_report.json"
    reclassified_indices = set()
    if xval_path.exists():
        with open(xval_path, "r", encoding="utf-8") as f:
            xval = json.load(f)
        for reclass in xval.get("classification_refinements", []):
            if reclass.get("new_classification") not in ("dosing", "dosing (no weight bands)"):
                reclassified_indices.add(reclass["table_index"])
        print(f"  Loaded cross_validation_report.json: "
              f"{len(reclassified_indices)} reclassifications to exclude")
    else:
        print(f"  cross_validation_report.json not found — using Stage 1 classifications")

    # Load Docling cache for full markdown
    cache_dir = OUTPUT_DIR / "cache"
    cache_files = list(cache_dir.glob("docling_*.json")) if cache_dir.exists() else []

    doc = None
    if cache_files:
        try:
            from docling.datamodel.document import DoclingDocument
            cache_path = cache_files[0]
            print(f"  Loading Docling cache: {cache_path.name}")
            doc = DoclingDocument.load_from_json(cache_path)
        except Exception as e:
            print(f"  Warning: could not load Docling cache: {e}")

    # Build dosing table list
    dosing_tables = []
    for i, entry in enumerate(inventory):
        idx = entry["index"]

        # Skip reclassified tables
        if idx in reclassified_indices:
            continue

        # Only include dosing tables
        if entry.get("classification") != "dosing":
            continue

        tbl = dict(entry)

        # Add markdown from Docling cache
        if doc is not None and i < len(doc.tables):
            try:
                tbl["markdown"] = doc.tables[i].export_to_markdown(doc=doc)
            except Exception:
                pass

        dosing_tables.append(tbl)

    print(f"  Dosing tables to validate: {len(dosing_tables)}")

    # Load stitched table from Stage 2 (if any page-boundary tables were detected)
    stitched_table = None
    if xval_path.exists():
        with open(xval_path, "r", encoding="utf-8") as f:
            xval = json.load(f)
        stitches = xval.get("page_boundary_stitches", [])
        if stitches:
            stitched_table = stitches[0]
            print(f"  Loaded stitched table: pp.{stitched_table['pages'][0]}-"
                  f"{stitched_table['pages'][1]} ({stitched_table['num_rows']} rows)")

    return dosing_tables, stitched_table


# ─────────────────────────────────────────────────────────────────────────────
# 13. RUN ALL CHECKS ON A TABLE
# ─────────────────────────────────────────────────────────────────────────────

def validate_table(tbl: dict) -> dict:
    """Run all 6 plausibility checks on a single dosing table.

    Returns a dict with per-check results and an overall pass/fail.
    """
    md = tbl.get("markdown", "")
    if not md:
        return {
            "table_index": tbl.get("index", "?"),
            "page": tbl.get("page_no", "?"),
            "parsed": False,
            "overall_passed": False,
            "checks": {},
            "error": "No markdown content",
        }

    parsed = parse_dosing_table(md)

    if parsed["weight_col"] is None:
        return {
            "table_index": tbl.get("index", "?"),
            "page": tbl.get("page_no", "?"),
            "parsed": False,
            "overall_passed": False,
            "checks": {},
            "error": "No weight column identified",
        }

    checks = {
        "weight_contiguity": check_weight_contiguity(parsed),
        "dose_monotonicity": check_dose_monotonicity(parsed),
        "weight_coverage": check_weight_coverage(parsed, tbl),
        "clinical_bounds": check_clinical_bounds(parsed),
        "combination_consistency": check_combination_consistency(parsed),
        "positive_no_empty": check_positive_no_empty(parsed),
    }

    overall = all(c["passed"] for c in checks.values())

    return {
        "table_index": tbl.get("index", "?"),
        "page": tbl.get("page_no", "?"),
        "parsed": True,
        "num_rows": len(parsed["rows"]),
        "weight_bands": len([r for r in parsed["rows"] if r["weight_range"]]),
        "overall_passed": overall,
        "checks": checks,
    }


# ─────────────────────────────────────────────────────────────────────────────
# 14. SAVE REPORT
# ─────────────────────────────────────────────────────────────────────────────

def save_report(results: list, stitched_result: dict, timings: dict):
    """Save the plausibility report as JSON."""

    # Aggregate check-level stats
    check_names = [
        "weight_contiguity", "dose_monotonicity", "weight_coverage",
        "clinical_bounds", "combination_consistency", "positive_no_empty",
    ]
    check_stats = {}
    for name in check_names:
        passes = sum(1 for r in results
                     if r.get("parsed") and r["checks"].get(name, {}).get("passed", False))
        fails = sum(1 for r in results
                    if r.get("parsed") and not r["checks"].get(name, {}).get("passed", True))
        details = []
        for r in results:
            if r.get("parsed") and r["checks"].get(name, {}).get("issues"):
                issues = r["checks"][name]["issues"]
                if issues and issues != ["<2 weight bands — skipped"] and \
                   issues != ["No dose columns found — skipped"] and \
                   issues != ["No weight bands found — skipped"]:
                    details.append({
                        "table_index": r["table_index"],
                        "page": r["page"],
                        "issues": issues,
                    })
        check_stats[name] = {"pass": passes, "fail": fails, "details": details}

    tables_checked = sum(1 for r in results if r.get("parsed"))
    tables_passed_all = sum(1 for r in results if r.get("overall_passed"))
    tables_with_issues = tables_checked - tables_passed_all

    tables_skipped = sum(1 for r in results if not r.get("parsed"))
    skipped_tables = [
        {"table_index": r["table_index"], "page": r["page"], "reason": r.get("error", "")}
        for r in results if not r.get("parsed")
    ]

    report = {
        "tables_from_stage2": len(results),
        "tables_checked": tables_checked,
        "tables_skipped": tables_skipped,
        "skipped_tables": skipped_tables,
        "tables_passed_all": tables_passed_all,
        "tables_with_issues": tables_with_issues,
        "checks": check_stats,
        "stitched_table_result": stitched_result,
        "per_table_results": results,
        "timings": timings,
    }

    report_path = OUTPUT_DIR / "plausibility_report.json"
    report_path.write_text(json.dumps(report, indent=2, default=str),
                           encoding="utf-8")
    print(f"\n\U0001f4be Saved: {report_path}")

    return report


# ─────────────────────────────────────────────────────────────────────────────
# 15. MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    print(f"\n{'='*70}")
    print(f"  STAGE 3: AUTOMATED PLAUSIBILITY CHECKS")
    print(f"{'='*70}")

    timings = {}
    t_start = time.perf_counter()

    # ── Load data ─────────────────────────────────────────────────────────
    t0 = time.perf_counter()
    dosing_tables, stitched_table = load_dosing_tables()
    timings["load_data_s"] = round(time.perf_counter() - t0, 3)

    # ── Validate each dosing table ────────────────────────────────────────
    print(f"\n{'='*70}")
    print(f"  RUNNING PLAUSIBILITY CHECKS ({len(dosing_tables)} dosing tables)")
    print(f"{'='*70}")

    t0 = time.perf_counter()
    results = []
    skipped = []
    for tbl in dosing_tables:
        result = validate_table(tbl)
        results.append(result)

        idx = result["table_index"]
        page = result["page"]

        if not result.get("parsed"):
            skipped.append(result)
            continue

        if result["overall_passed"]:
            print(f"  \u2705 Table {idx} (p.{page}): ALL CHECKS PASS "
                  f"({result['weight_bands']} weight bands, {result['num_rows']} rows)")
        else:
            failed_checks = [
                name for name, chk in result["checks"].items()
                if not chk["passed"]
            ]
            print(f"  \u274c Table {idx} (p.{page}): ISSUES FOUND "
                  f"({result['weight_bands']} weight bands, {result['num_rows']} rows)")
            for name in failed_checks:
                chk = result["checks"][name]
                print(f"      [{name}]:")
                for issue in chk["issues"]:
                    print(f"        - {issue}")

    timings["validate_tables_s"] = round(time.perf_counter() - t0, 3)

    # Report skipped tables (no weight column = not weight-based dosing)
    if skipped:
        print(f"\n  {'─'*60}")
        print(f"  Skipped {len(skipped)} table(s) — classified as 'dosing' by keyword")
        print(f"  matching but have no weight column (GRADE evidence tables,")
        print(f"  abbreviation lists, values & preferences summaries):")
        for s in skipped:
            print(f"    Table {s['table_index']} (p.{s['page']}): {s.get('error', 'not parseable')}")
        print(f"  \u2192 Recommend reclassifying these as 'evidence' or 'other'")

    # ── Validate stitched table separately ────────────────────────────────
    stitched_result = None
    if stitched_table:
        print(f"\n{'='*70}")
        print(f"  STITCHED TABLE VALIDATION (pp.{stitched_table['pages'][0]}-"
              f"{stitched_table['pages'][1]})")
        print(f"{'='*70}")

        t0 = time.perf_counter()
        stitched_tbl = {
            "index": "S1",
            "page_no": f"{stitched_table['pages'][0]}-{stitched_table['pages'][1]}",
            "classification": "dosing",
            "markdown": stitched_table["markdown"],
        }
        stitched_result = validate_table(stitched_tbl)
        timings["validate_stitched_s"] = round(time.perf_counter() - t0, 3)

        if stitched_result["overall_passed"]:
            print(f"\n  \u2705 Stitched table: ALL CHECKS PASS "
                  f"({stitched_result['weight_bands']} weight bands, "
                  f"{stitched_result['num_rows']} rows)")
        else:
            failed_checks = [
                name for name, chk in stitched_result["checks"].items()
                if not chk["passed"]
            ]
            print(f"\n  \u274c Stitched table: ISSUES FOUND")
            for name in failed_checks:
                chk = stitched_result["checks"][name]
                print(f"      [{name}]:")
                for issue in chk["issues"]:
                    print(f"        - {issue}")

    # ── Total ─────────────────────────────────────────────────────────────
    timings["total_s"] = round(time.perf_counter() - t_start, 3)

    # ── Save report ───────────────────────────────────────────────────────
    report = save_report(results, stitched_result, timings)

    # ── Final scorecard ───────────────────────────────────────────────────
    print(f"\n{'='*70}")
    print(f"  STAGE 3 — FINAL SCORECARD")
    print(f"{'='*70}")

    tables_checked = report["tables_checked"]
    tables_passed = report["tables_passed_all"]
    tables_issues = report["tables_with_issues"]

    tables_skipped = sum(1 for r in results if not r.get("parsed"))
    print(f"  Dosing tables (Stage 2)       : {len(dosing_tables)}")
    print(f"  Weight-based (checked)        : {tables_checked}")
    print(f"  Non-weight-based (skipped)    : {tables_skipped}")
    print(f"  Passed all checks             : {tables_passed}")
    print(f"  With issues                   : {tables_issues}")
    print()

    for name in ["weight_contiguity", "dose_monotonicity", "weight_coverage",
                  "clinical_bounds", "combination_consistency", "positive_no_empty"]:
        stats = report["checks"][name]
        label = name.replace("_", " ").title()
        print(f"  {label:<30}: {stats['pass']} pass / {stats['fail']} fail")

    if stitched_result:
        st_status = "\u2705 PASS" if stitched_result["overall_passed"] else "\u274c FAIL"
        st_pages = stitched_result.get("pages", "?")
        print(f"\n  Stitched table (pp.{st_pages}): {st_status}")

    print(f"\n  Total time           : {timings['total_s']}s")
    print(f"{'='*70}\n")

    return report


if __name__ == "__main__":
    main()
