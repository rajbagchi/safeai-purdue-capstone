# -*- coding: utf-8 -*-
"""
Stage 2: Cross-Validation with PyMuPDF
=======================================
Independent re-extraction using PyMuPDF to cross-validate Stage 1 (Docling)
output. Zero new dependencies — uses only PyMuPDF (fitz) which is already
installed.

Three cross-validation layers:
  1. Raw text verification — confirms ground-truth keywords exist in the PDF
     text stream, independent of any layout engine.
  2. Independent table extraction — uses PyMuPDF find_tables() to re-extract
     dosing tables and compare against Docling cell-by-cell.
  3. Page-boundary table stitching — detects tables that span page breaks,
     merges the fragments, and resolves known page-boundary failures.

Config-driven: reads document-specific settings from pipeline_config.json
    python stage2_cross_validation.py                         # uses default config
    python stage2_cross_validation.py --config configs/X.json # uses custom config

Run:
    python stage2_cross_validation.py
"""

# ─────────────────────────────────────────────────────────────────────────────
# 1.  IMPORTS
# ─────────────────────────────────────────────────────────────────────────────
import os
import re
import json
import time
from pathlib import Path

import fitz  # PyMuPDF

from pipeline_config import (
    load_config, get_pdf_path, get_ground_truth, get_dosing_pages,
)

# ─────────────────────────────────────────────────────────────────────────────
# 2.  CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────
CONFIG = load_config()
PDF_PATH = get_pdf_path(CONFIG)
OUTPUT_DIR = Path("extraction_output")

# Pages to cross-validate — from config, or auto-discover from Stage 1
_dosing_pages_cfg = get_dosing_pages(CONFIG)
_severe_pages_cfg = CONFIG.get("cross_validation", {}).get("severe_pages", [])

if _dosing_pages_cfg == "auto":
    # Auto-discover: read Stage 1 table_inventory.json for dosing pages
    _inv_path = OUTPUT_DIR / "table_inventory.json"
    if _inv_path.exists():
        _inv = json.loads(_inv_path.read_text(encoding="utf-8"))
        DOSING_PAGES = sorted(set(
            t["page"] for t in _inv
            if t.get("classification") in ("dosing", "dosing (no weight bands)")
        ))
    else:
        DOSING_PAGES = []
        print("⚠️  No table_inventory.json found — dosing pages auto-discovery skipped")
else:
    DOSING_PAGES = list(_dosing_pages_cfg) if _dosing_pages_cfg else []

CROSS_VALIDATE_PAGES = sorted(set(DOSING_PAGES + list(_severe_pages_cfg)))

# Page-boundary detection thresholds (fraction of page height)
BOTTOM_THRESHOLD = 0.90   # table bbox bottom > 90% of page height → likely truncated
TOP_THRESHOLD = 0.10      # table bbox top < 10% of page height → likely continuation

# ─────────────────────────────────────────────────────────────────────────────
# 3.  GROUND TRUTH  (loaded from pipeline_config.json — shared with Stage 1)
# ─────────────────────────────────────────────────────────────────────────────
GROUND_TRUTH = get_ground_truth(CONFIG)


# ─────────────────────────────────────────────────────────────────────────────
# 4.  RAW TEXT VERIFICATION
# ─────────────────────────────────────────────────────────────────────────────

def raw_text_verification(pdf_path: str) -> dict:
    """Verify all ground-truth keywords exist in the raw PDF text layer.

    Uses PyMuPDF page.get_text() — completely independent of Docling.
    This confirms the content physically exists in the PDF's text stream.
    """
    print(f"\n{'='*70}")
    print(f"  STAGE 2A: RAW TEXT VERIFICATION (PyMuPDF)")
    print(f"{'='*70}")

    doc = fitz.open(pdf_path)
    results = []

    for gt in GROUND_TRUTH:
        page_num = gt["page"]
        gt_type = gt["type"]
        keywords = gt["must_contain"]

        # Extract raw text from the specific page
        page = doc[page_num - 1]  # 0-indexed
        raw_text = page.get_text().lower()

        found = [kw for kw in keywords if kw.lower() in raw_text]
        missing = [kw for kw in keywords if kw.lower() not in raw_text]
        passed = len(missing) == 0

        results.append({
            "page": page_num,
            "type": gt_type,
            "passed": passed,
            "found": found,
            "missing": missing,
        })

        status = "\u2705 PASS" if passed else "\u274c FAIL"
        print(f"  {status}  Page {page_num:>3}  [{gt_type:5}]  "
              f"found={found}  missing={missing}")

    doc.close()

    n_pass = sum(1 for r in results if r["passed"])
    n_fail = len(results) - n_pass
    accuracy = round(n_pass / len(results) * 100, 1) if results else 0.0

    print(f"\n  Raw text verification: {n_pass}/{len(results)} pass ({accuracy}%)")

    return {
        "accuracy_pct": accuracy,
        "n_pass": n_pass,
        "n_fail": n_fail,
        "details": results,
    }


# ─────────────────────────────────────────────────────────────────────────────
# 5.  INDEPENDENT TABLE EXTRACTION (PyMuPDF find_tables)
# ─────────────────────────────────────────────────────────────────────────────

def _extract_tables_from_page(page) -> list:
    """Extract all tables from a PyMuPDF page using find_tables().

    Returns a list of dicts with markdown, row/col counts, bbox, and cell data.
    """
    tables_result = page.find_tables()
    extracted = []

    for i, table in enumerate(tables_result.tables):
        try:
            # Extract as pandas DataFrame and then markdown
            df = table.to_pandas()
            md = table.to_markdown()
            cells = []
            for r_idx, row in df.iterrows():
                for c_idx, val in enumerate(row):
                    cells.append({
                        "row": int(r_idx) if isinstance(r_idx, (int, float)) else 0,
                        "col": c_idx,
                        "value": str(val).strip() if val is not None else "",
                    })

            extracted.append({
                "table_index_on_page": i,
                "markdown": md,
                "num_rows": len(df),
                "num_cols": len(df.columns),
                "bbox": list(table.bbox),   # (x0, y0, x1, y1)
                "cells": cells,
                "headers": [str(h) for h in df.columns.tolist()],
                "dataframe": df,  # keep for stitching (not serialised)
            })
        except Exception as e:
            extracted.append({
                "table_index_on_page": i,
                "error": str(e),
            })

    return extracted


def extract_pymupdf_tables(pdf_path: str) -> dict:
    """Extract tables from all cross-validation pages using PyMuPDF.

    Returns per-page table extractions for comparison against Docling.
    """
    print(f"\n{'='*70}")
    print(f"  STAGE 2B: INDEPENDENT TABLE EXTRACTION (PyMuPDF find_tables)")
    print(f"{'='*70}")

    doc = fitz.open(pdf_path)
    page_tables = {}

    for page_num in CROSS_VALIDATE_PAGES:
        page = doc[page_num - 1]
        tables = _extract_tables_from_page(page)
        page_tables[page_num] = tables

        n_tables = len(tables)
        if n_tables > 0:
            for t in tables:
                if "error" not in t:
                    print(f"  Page {page_num}: Table {t['table_index_on_page']+1} — "
                          f"{t['num_rows']}r x {t['num_cols']}c")
                else:
                    print(f"  Page {page_num}: Table {t['table_index_on_page']+1} — "
                          f"ERROR: {t['error'][:60]}")
        else:
            print(f"  Page {page_num}: no tables found")

    doc.close()

    total = sum(len(tbls) for tbls in page_tables.values())
    print(f"\n  Total: {total} tables across {len(CROSS_VALIDATE_PAGES)} pages")

    return page_tables


# ─────────────────────────────────────────────────────────────────────────────
# 6.  PAGE-BOUNDARY TABLE DETECTION & STITCHING
# ─────────────────────────────────────────────────────────────────────────────

def detect_and_stitch_page_boundary_tables(pdf_path: str,
                                           page_tables: dict) -> list:
    """Detect tables that span page breaks and merge the fragments.

    For each page, checks if any table's bounding box extends near the bottom.
    If so, checks the next page for a table near the top with matching columns.
    When a match is found, the two fragments are stitched into a single table.

    Returns a list of stitched table dicts.
    """
    print(f"\n{'='*70}")
    print(f"  STAGE 2C: PAGE-BOUNDARY TABLE STITCHING")
    print(f"{'='*70}")

    doc = fitz.open(pdf_path)
    stitched_tables = []

    # Check each page in the dosing range for bottom-truncated tables
    for page_num in DOSING_PAGES:
        page = doc[page_num - 1]
        page_height = page.rect.height

        tables_this_page = page_tables.get(page_num, [])
        tables_next_page = page_tables.get(page_num + 1, [])

        for tbl in tables_this_page:
            if "error" in tbl or "bbox" not in tbl:
                continue

            bbox = tbl["bbox"]
            table_bottom = bbox[3]

            # Check if table extends near the page bottom
            if table_bottom / page_height < BOTTOM_THRESHOLD:
                continue

            print(f"\n  \u26a0\ufe0f  Page {page_num}: table extends to {table_bottom:.0f}px "
                  f"(page height {page_height:.0f}px, "
                  f"{table_bottom/page_height*100:.0f}%)")

            # Look for a continuation table on the next page
            next_page = doc[page_num]  # 0-indexed: page_num+1 - 1 = page_num
            next_page_height = next_page.rect.height

            for next_tbl in tables_next_page:
                if "error" in next_tbl or "bbox" not in next_tbl:
                    continue

                next_bbox = next_tbl["bbox"]
                table_top = next_bbox[1]

                if table_top / next_page_height > TOP_THRESHOLD:
                    continue

                print(f"  \u2192  Page {page_num+1}: continuation table starts at "
                      f"{table_top:.0f}px ({table_top/next_page_height*100:.0f}%)")

                # Check column compatibility
                cols_this = tbl["num_cols"]
                cols_next = next_tbl["num_cols"]

                if cols_this != cols_next:
                    print(f"     Column mismatch: {cols_this} vs {cols_next} — skipping")
                    continue

                # Stitch: combine DataFrames
                try:
                    import pandas as pd
                    df_top = tbl["dataframe"]
                    df_bottom = next_tbl["dataframe"]

                    # Edge case: when a continuation fragment has 0 data rows,
                    # PyMuPDF puts the actual data into the DataFrame's column
                    # headers.  Convert those headers into a single data row.
                    if len(df_bottom) == 0 and len(df_bottom.columns) > 0:
                        header_vals = [str(h) for h in df_bottom.columns]
                        print(f"     0-row continuation — treating headers as data: "
                              f"{header_vals}")
                        df_bottom = pd.DataFrame(
                            [header_vals],
                            columns=df_top.columns[:len(header_vals)],
                        )

                    # Check if the bottom table's first row duplicates the header
                    # (some PDF tables repeat headers on continuation pages)
                    top_headers = [str(h).strip().lower() for h in df_top.columns]
                    if len(df_bottom) > 0:
                        first_row_bottom = [str(v).strip().lower()
                                            for v in df_bottom.iloc[0]]
                        if first_row_bottom == top_headers:
                            print(f"     Duplicate header detected — removing from continuation")
                            df_bottom = df_bottom.iloc[1:]

                    # Merge
                    # Align columns: use top table's headers for the stitched result
                    df_bottom.columns = df_top.columns[:len(df_bottom.columns)]
                    df_stitched = pd.concat([df_top, df_bottom], ignore_index=True)

                    # Generate stitched markdown — strip embedded newlines
                    # from cell values (PyMuPDF sometimes keeps line breaks
                    # from multi-line header text in the PDF).
                    def _clean(val):
                        s = str(val).replace("\n", " ").replace("<br>", " ")
                        return re.sub(r"\s+", " ", s).strip()

                    md_lines = ["| " + " | ".join(_clean(h) for h in df_stitched.columns) + " |"]
                    md_lines.append("| " + " | ".join("---" for _ in df_stitched.columns) + " |")
                    for _, row in df_stitched.iterrows():
                        md_lines.append("| " + " | ".join(_clean(v) for v in row) + " |")
                    stitched_md = "\n".join(md_lines)

                    stitched = {
                        "pages": [page_num, page_num + 1],
                        "num_rows": len(df_stitched),
                        "num_cols": len(df_stitched.columns),
                        "headers": [str(h) for h in df_stitched.columns],
                        "markdown": stitched_md,
                        "top_table_rows": len(df_top),
                        "bottom_table_rows": len(df_bottom),
                    }
                    stitched_tables.append(stitched)

                    print(f"     \u2705 STITCHED: {len(df_top)} + {len(df_bottom)} = "
                          f"{len(df_stitched)} rows, {cols_this} cols")
                    print(f"     Stitched markdown preview:")
                    for line in stitched_md.split("\n")[:8]:
                        print(f"       {line}")
                    if len(df_stitched) > 6:
                        print(f"       ... ({len(df_stitched)} rows total)")

                except Exception as e:
                    print(f"     \u274c Stitching failed: {e}")

    doc.close()

    if not stitched_tables:
        print("\n  No page-boundary tables detected.")
    else:
        print(f"\n  \u2705 {len(stitched_tables)} table(s) stitched across page boundaries")

    return stitched_tables


# ─────────────────────────────────────────────────────────────────────────────
# 7.  DOCLING vs PyMuPDF CELL-LEVEL COMPARISON
# ─────────────────────────────────────────────────────────────────────────────

def _normalise_cell(value: str) -> str:
    """Normalise a cell value for comparison (whitespace, special chars)."""
    v = str(value).strip()
    # Normalise unicode variants of comparison operators
    v = v.replace("\u2265", ">=").replace("\u2264", "<=")
    v = v.replace("\u2013", "-").replace("\u2014", "-")   # en/em dashes
    v = v.replace("\u00d7", "x")                            # multiplication sign
    v = v.replace("\u00b1", "+/-")                           # plus-minus
    # Collapse multiple spaces
    v = re.sub(r"\s+", " ", v)
    return v.lower()


def _parse_md_table(md: str) -> list:
    """Parse a Markdown table into a list of rows (each row = list of cell strings)."""
    rows = []
    for line in md.strip().split("\n"):
        line = line.strip()
        if not line or "---" in line:
            continue
        cells = [c.strip() for c in line.split("|")]
        # Remove empty first/last from leading/trailing |
        if cells and cells[0] == "":
            cells = cells[1:]
        if cells and cells[-1] == "":
            cells = cells[:-1]
        if cells:
            rows.append(cells)
    return rows


def compare_tables_cell_level(stage1_tables: list,
                              pymupdf_page_tables: dict) -> list:
    """Compare Docling (Stage 1) tables against PyMuPDF tables cell-by-cell.

    For each dosing page, finds the best-matching table pair between the two
    engines and computes a cell-level agreement score.

    Args:
        stage1_tables: Table list from Stage 1 (from extraction_summary or
                       table_inventory + cached markdown).
        pymupdf_page_tables: Dict of {page_num: [table_dicts]} from PyMuPDF.

    Returns:
        List of comparison result dicts.
    """
    print(f"\n{'='*70}")
    print(f"  STAGE 2D: CELL-LEVEL COMPARISON (Docling vs PyMuPDF)")
    print(f"{'='*70}")

    comparisons = []

    # Group Stage 1 dosing tables by page
    docling_by_page = {}
    for tbl in stage1_tables:
        if tbl.get("classification") != "dosing":
            continue
        page = tbl.get("page_no")
        if page and page in CROSS_VALIDATE_PAGES:
            docling_by_page.setdefault(page, []).append(tbl)

    for page_num in CROSS_VALIDATE_PAGES:
        docling_tables = docling_by_page.get(page_num, [])
        pymupdf_tables = pymupdf_page_tables.get(page_num, [])

        if not docling_tables or not pymupdf_tables:
            continue

        # For each Docling table, find the best-matching PyMuPDF table
        for d_tbl in docling_tables:
            d_md = d_tbl.get("markdown", "")
            d_rows = _parse_md_table(d_md)
            if not d_rows:
                continue

            best_match = None
            best_score = -1

            for p_tbl in pymupdf_tables:
                if "error" in p_tbl:
                    continue
                p_md = p_tbl.get("markdown", "")
                p_rows = _parse_md_table(p_md)
                if not p_rows:
                    continue

                # Quick similarity: count matching normalised cells
                total = 0
                matches = 0
                for d_row, p_row in zip(d_rows, p_rows):
                    for d_cell, p_cell in zip(d_row, p_row):
                        total += 1
                        if _normalise_cell(d_cell) == _normalise_cell(p_cell):
                            matches += 1

                if total > 0:
                    score = matches / total
                    if score > best_score:
                        best_score = score
                        best_match = {
                            "pymupdf_table_idx": p_tbl["table_index_on_page"],
                            "pymupdf_md": p_md,
                            "pymupdf_rows": p_rows,
                        }

            if best_match is None:
                continue

            # Detailed cell comparison with the best match
            p_rows = best_match["pymupdf_rows"]
            cell_diffs = []
            total_cells = 0
            matching_cells = 0

            max_rows = max(len(d_rows), len(p_rows))
            for r_i in range(max_rows):
                d_row = d_rows[r_i] if r_i < len(d_rows) else []
                p_row = p_rows[r_i] if r_i < len(p_rows) else []
                max_cols = max(len(d_row), len(p_row))

                for c_i in range(max_cols):
                    d_val = d_row[c_i] if c_i < len(d_row) else ""
                    p_val = p_row[c_i] if c_i < len(p_row) else ""
                    total_cells += 1

                    if _normalise_cell(d_val) == _normalise_cell(p_val):
                        matching_cells += 1
                    else:
                        cell_diffs.append({
                            "row": r_i,
                            "col": c_i,
                            "docling": d_val,
                            "pymupdf": p_val,
                        })

            agreement = round(matching_cells / total_cells * 100, 1) if total_cells else 0.0

            comparison = {
                "page": page_num,
                "docling_table_idx": d_tbl["index"],
                "pymupdf_table_idx": best_match["pymupdf_table_idx"],
                "docling_rows": len(d_rows),
                "pymupdf_rows": len(p_rows),
                "total_cells": total_cells,
                "matching_cells": matching_cells,
                "agreement_pct": agreement,
                "cell_diffs": cell_diffs[:20],  # cap at 20 for readability
            }
            comparisons.append(comparison)

            status = "\u2705" if agreement >= 80.0 else "\u26a0\ufe0f" if agreement >= 50.0 else "\u274c"
            print(f"  {status} Page {page_num}, Docling Table {d_tbl['index']}: "
                  f"{agreement}% agreement ({matching_cells}/{total_cells} cells)")
            if cell_diffs:
                for diff in cell_diffs[:3]:
                    print(f"      Row {diff['row']}, Col {diff['col']}: "
                          f"Docling='{diff['docling']}' vs PyMuPDF='{diff['pymupdf']}'")
                if len(cell_diffs) > 3:
                    print(f"      ... and {len(cell_diffs) - 3} more differences")

    if not comparisons:
        print("  No matching table pairs found for comparison.")
    else:
        avg_agreement = sum(c["agreement_pct"] for c in comparisons) / len(comparisons)
        print(f"\n  Average agreement: {avg_agreement:.1f}% "
              f"across {len(comparisons)} table pairs")

    return comparisons


# ─────────────────────────────────────────────────────────────────────────────
# 8.  CLASSIFICATION REFINEMENT
# ─────────────────────────────────────────────────────────────────────────────

def refine_classifications(stage1_tables: list) -> list:
    """Re-check tables classified as 'dosing' by Stage 1.

    Abbreviation/glossary tables on pp.27, 29 and GRADE evidence tables in the
    annexes (pp.415–473) are sometimes misclassified as 'dosing' because they
    contain drug names.  This check verifies that a dosing table actually has
    numeric weight-band patterns and dose values.

    Returns a list of reclassification dicts.
    """
    print(f"\n{'='*70}")
    print(f"  STAGE 2E: CLASSIFICATION REFINEMENT")
    print(f"{'='*70}")

    reclassifications = []

    # Patterns that real dosing tables should have.
    # Weight-band patterns in cell values (kg suffix is optional — often
    # only in the header, not repeated in every cell).
    weight_pattern = re.compile(
        r"(\d+\.?\d*)\s*(?:to|[-\u2013])\s*<?=?\s*(\d+\.?\d*)"   # "5 to < 15"
        r"|[>\u2265]=?\s*\d+\.?\d*"                                # "≥ 35"
        r"|<\s*\d+\.?\d*",                                         # "< 5"
        re.IGNORECASE,
    )
    # Dose patterns in cell values
    dose_pattern = re.compile(
        r"\d+\.?\d*\s*\+\s*\d+\.?\d*"     # e.g., "20 + 120"
        r"|\d+\.?\d*\s*mg"                  # e.g., "250 mg"
        r"|\d+\.?\d*\s*/\s*\d+\.?\d*",      # e.g., "250 / 12.5"
        re.IGNORECASE,
    )
    # Header-level keywords that strongly indicate a dosing table
    dosing_header_pattern = re.compile(
        r"body\s*weight|weight\s*\(kg\)|dose\s*\(mg|single\s*dose|mg\s*base"
        r"|mg/kg|tablet|daily\s*for\s*\d+\s*days",
        re.IGNORECASE,
    )

    for tbl in stage1_tables:
        if tbl.get("classification") != "dosing":
            continue
        if "error" in tbl:
            continue

        md = tbl.get("markdown", "")
        page = tbl.get("page_no", "?")
        idx = tbl["index"]

        # Extract the header row (first non-separator line)
        header_line = ""
        for line in md.strip().split("\n"):
            if line.strip() and "---" not in line:
                header_line = line
                break

        has_weight = bool(weight_pattern.search(md))
        has_dose = bool(dose_pattern.search(md))
        has_dosing_header = bool(dosing_header_pattern.search(header_line))

        # A table with dosing headers (e.g., "Body weight (kg) | Dose (mg)")
        # is confirmed dosing even if cell-level patterns are non-standard
        if has_dosing_header and (has_weight or has_dose):
            print(f"  \u2705 Table {idx} (p.{page}): confirmed dosing (header match)")
            continue

        if not has_weight and not has_dose:
            # Neither weight bands nor dose values → likely misclassified
            new_class = "structural"
            reclassifications.append({
                "table_index": idx,
                "page": page,
                "old_classification": "dosing",
                "new_classification": new_class,
                "reason": "No numeric weight bands or dose values found",
            })
            print(f"  \u26a0\ufe0f  Table {idx} (p.{page}): dosing \u2192 {new_class} "
                  f"(no weight/dose patterns)")
        elif not has_weight:
            # Has dose values but no weight bands — may still be dosing but flag it
            reclassifications.append({
                "table_index": idx,
                "page": page,
                "old_classification": "dosing",
                "new_classification": "dosing (no weight bands)",
                "reason": "Has dose values but no weight-band patterns",
            })
            print(f"  \u2753 Table {idx} (p.{page}): dosing (flagged \u2014 no weight bands)")
        else:
            print(f"  \u2705 Table {idx} (p.{page}): confirmed dosing")

    if not reclassifications:
        print("\n  No reclassifications needed.")
    else:
        n_reclass = sum(1 for r in reclassifications
                        if r["new_classification"] != "dosing (no weight bands)")
        n_flagged = len(reclassifications) - n_reclass
        print(f"\n  {n_reclass} table(s) reclassified, {n_flagged} flagged for review")

    return reclassifications


# ─────────────────────────────────────────────────────────────────────────────
# 9.  GROUND-TRUTH RE-CHECK WITH STITCHED TABLES
# ─────────────────────────────────────────────────────────────────────────────

def recheck_accuracy_with_stitched(pymupdf_page_tables: dict,
                                    stitched_tables: list,
                                    raw_verification: dict) -> dict:
    """Re-run the ground-truth table checks using PyMuPDF tables + stitched tables.

    This determines whether Stage 2 resolves the Stage 1 failures.
    """
    print(f"\n{'='*70}")
    print(f"  STAGE 2F: ACCURACY RE-CHECK (with stitched tables)")
    print(f"{'='*70}")

    # Build a combined search space from PyMuPDF tables + stitched tables
    all_table_text_parts = []

    for page_num, tables in pymupdf_page_tables.items():
        for tbl in tables:
            if "error" not in tbl:
                all_table_text_parts.append(tbl.get("markdown", ""))

    for stbl in stitched_tables:
        all_table_text_parts.append(stbl.get("markdown", ""))

    combined_table_text = " ".join(all_table_text_parts).lower()

    # Re-check only the TABLE ground-truth items
    results = []
    for gt in GROUND_TRUTH:
        if gt["type"] != "table":
            continue

        keywords = [kw.lower() for kw in gt["must_contain"]]
        found = [kw for kw in keywords if kw in combined_table_text]
        missing = [kw for kw in keywords if kw not in combined_table_text]
        passed = len(missing) == 0

        results.append({
            "page": gt["page"],
            "type": "table",
            "passed": passed,
            "found": found,
            "missing": missing,
        })

        status = "\u2705 PASS" if passed else "\u274c FAIL"
        print(f"  {status}  Page {gt['page']:>3}  [table]  "
              f"found={found}  missing={missing}")

    n_pass = sum(1 for r in results if r["passed"])
    n_fail = len(results) - n_pass
    accuracy = round(n_pass / len(results) * 100, 1) if results else 0.0

    print(f"\n  Table checks with PyMuPDF + stitching: {n_pass}/{len(results)} pass ({accuracy}%)")

    # Compare against Stage 1
    stage1_table_pass = sum(
        1 for r in raw_verification["details"]
        if r["type"] == "table" and r["passed"]
    )
    stage1_table_total = sum(1 for r in raw_verification["details"] if r["type"] == "table")

    # Overall combined accuracy (text from raw verification + tables from stitched)
    text_results = [r for r in raw_verification["details"] if r["type"] == "text"]
    image_results = [r for r in raw_verification["details"] if r["type"] == "image"]
    all_results = text_results + results + image_results

    combined_pass = sum(1 for r in all_results if r["passed"])
    combined_total = len(all_results)
    combined_accuracy = round(combined_pass / combined_total * 100, 1) if combined_total else 0.0

    print(f"\n  Combined Stage 2 accuracy (text + tables + images): "
          f"{combined_pass}/{combined_total} = {combined_accuracy}%")

    return {
        "table_accuracy_pct": accuracy,
        "table_pass": n_pass,
        "table_fail": n_fail,
        "table_details": results,
        "combined_accuracy_pct": combined_accuracy,
        "combined_pass": combined_pass,
        "combined_total": combined_total,
    }


# ─────────────────────────────────────────────────────────────────────────────
# 10. NLL REGENERATION FOR STITCHED TABLES
# ─────────────────────────────────────────────────────────────────────────────

def _table_to_nll(table_md: str) -> str:
    """Convert a Markdown table to Natural Language Logic (same logic as Stage 1)."""
    lines = [l.strip() for l in table_md.strip().split("\n") if l.strip()]
    if not lines:
        return ""

    headers = []
    data_lines = []
    for line in lines:
        if "---" in line:
            continue
        cells = [c.strip() for c in line.split("|") if c.strip()]
        if not headers:
            headers = cells
        else:
            data_lines.append(cells)

    if not headers or not data_lines:
        return table_md

    nll_sentences = []
    for row in data_lines:
        if not row or not any(row):
            continue
        parts = []
        for h, v in zip(headers, row):
            if v:
                parts.append(f"{h} is {v}")
        if parts:
            condition = parts[0]
            outcomes = ", ".join(parts[1:]) if len(parts) > 1 else ""
            sentence = f"IF {condition}"
            if outcomes:
                sentence += f", THEN {outcomes}."
            nll_sentences.append(sentence)

    return "\n".join(nll_sentences)


def regenerate_nll_for_stitched(stitched_tables: list) -> list:
    """Generate NLL linearisation for stitched page-boundary tables.

    Returns a list of {pages, nll} dicts.
    """
    print(f"\n{'='*70}")
    print(f"  STAGE 2G: NLL REGENERATION FOR STITCHED TABLES")
    print(f"{'='*70}")

    nll_results = []

    for stbl in stitched_tables:
        md = stbl.get("markdown", "")
        nll = _table_to_nll(md)
        pages = stbl.get("pages", [])

        nll_results.append({
            "pages": pages,
            "nll": nll,
            "num_rows": stbl["num_rows"],
        })

        print(f"\n  Stitched table (pp.{pages[0]}\u2013{pages[1]}): "
              f"{stbl['num_rows']} rows")
        for line in nll.split("\n"):
            print(f"    {line}")

    return nll_results


# ─────────────────────────────────────────────────────────────────────────────
# 11. LOAD STAGE 1 RESULTS
# ─────────────────────────────────────────────────────────────────────────────

def load_stage1_tables() -> list:
    """Load Stage 1 table data from the extraction output.

    Loads table_inventory.json for metadata and extracts markdown from the
    Docling cache.  If the cache is not available, returns inventory-only data.
    """
    inv_path = OUTPUT_DIR / "table_inventory.json"
    if not inv_path.exists():
        print("  \u26a0\ufe0f  table_inventory.json not found — run Stage 1 first")
        return []

    with open(inv_path, "r", encoding="utf-8") as f:
        inventory = json.load(f)

    # Try to load full markdown from Docling cache for cell comparison
    cache_dir = OUTPUT_DIR / "cache"
    cache_files = list(cache_dir.glob("docling_*.json")) if cache_dir.exists() else []

    if cache_files:
        try:
            from docling.datamodel.document import DoclingDocument
            cache_path = cache_files[0]  # use most recent
            print(f"  Loading Docling cache: {cache_path.name}")
            doc = DoclingDocument.load_from_json(cache_path)

            # Match inventory entries with Docling table objects
            for i, tbl_obj in enumerate(doc.tables):
                if i < len(inventory):
                    try:
                        inventory[i]["markdown"] = tbl_obj.export_to_markdown(doc=doc)
                    except Exception:
                        pass
        except Exception as e:
            print(f"  \u26a0\ufe0f  Could not load Docling cache: {e}")
            print(f"     Cell-level comparison will be limited.")

    return inventory


# ─────────────────────────────────────────────────────────────────────────────
# 12. SAVE CROSS-VALIDATION REPORT
# ─────────────────────────────────────────────────────────────────────────────

def save_report(raw_verification: dict,
                pymupdf_page_tables: dict,
                stitched_tables: list,
                cell_comparisons: list,
                reclassifications: list,
                accuracy_recheck: dict,
                nll_results: list,
                timings: dict):
    """Save the cross-validation report as JSON."""

    # Serialise PyMuPDF tables (remove non-serialisable DataFrames)
    serialisable_tables = {}
    for page_num, tables in pymupdf_page_tables.items():
        serialisable_tables[str(page_num)] = []
        for tbl in tables:
            t_copy = {k: v for k, v in tbl.items() if k != "dataframe"}
            serialisable_tables[str(page_num)].append(t_copy)

    # Serialise stitched tables (remove DataFrames)
    serialisable_stitched = []
    for stbl in stitched_tables:
        s_copy = {k: v for k, v in stbl.items() if k != "dataframe"}
        serialisable_stitched.append(s_copy)

    # Collect all discrepancies
    discrepancies = []

    # From raw text: anything that fails in Stage 1 but passes in raw text
    for r in raw_verification["details"]:
        if r["passed"] and r["type"] == "table":
            # Check if this was a Stage 1 failure
            for gt in GROUND_TRUTH:
                if (gt["page"] == r["page"] and gt["type"] == "table"
                        and gt["must_contain"] == r["found"]):
                    # Check the extraction_summary for Stage 1 result
                    pass  # Will be populated if we load Stage 1 results

    # From cell-level comparison
    for comp in cell_comparisons:
        if comp["agreement_pct"] < 100.0:
            discrepancies.append({
                "page": comp["page"],
                "type": "cell_mismatch",
                "docling_table_idx": comp["docling_table_idx"],
                "agreement_pct": comp["agreement_pct"],
                "n_diffs": len(comp["cell_diffs"]),
            })

    # From stitched tables (page-boundary resolutions)
    for stbl in stitched_tables:
        discrepancies.append({
            "page": stbl["pages"][0],
            "type": "page_boundary_resolved",
            "pages": stbl["pages"],
            "rows_recovered": stbl["bottom_table_rows"],
        })

    # From reclassifications
    for reclass in reclassifications:
        if reclass["new_classification"] not in ("dosing", "dosing (no weight bands)"):
            discrepancies.append({
                "page": reclass["page"],
                "type": "reclassification",
                "table_index": reclass["table_index"],
                "old": reclass["old_classification"],
                "new": reclass["new_classification"],
            })

    report = {
        "raw_text_verification": raw_verification,
        "pymupdf_tables": serialisable_tables,
        "page_boundary_stitches": serialisable_stitched,
        "cell_level_comparison": cell_comparisons,
        "classification_refinements": reclassifications,
        "nll_regeneration": nll_results,
        "accuracy_recheck": accuracy_recheck,
        "discrepancies": discrepancies,
        "timings": timings,
    }

    report_path = OUTPUT_DIR / "cross_validation_report.json"
    report_path.write_text(json.dumps(report, indent=2, default=str),
                           encoding="utf-8")
    print(f"\n\U0001f4be Saved: {report_path}")

    # Append stitched NLL to tables_nll.txt
    if nll_results:
        nll_path = OUTPUT_DIR / "tables_nll.txt"
        with open(nll_path, "a", encoding="utf-8") as f:
            f.write("\n\n# ── Stage 2: Stitched page-boundary tables ──────────────\n")
            for nr in nll_results:
                pages = nr["pages"]
                f.write(f"\n### Stitched Table (pp.{pages[0]}\u2013{pages[1]}, dosing) ###\n")
                f.write(nr["nll"] + "\n")
        print(f"\U0001f4be Appended stitched NLL to: {nll_path}")

    return report


# ─────────────────────────────────────────────────────────────────────────────
# 13. MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    print(f"\n{'='*70}")
    print(f"  STAGE 2: CROSS-VALIDATION WITH PyMuPDF")
    print(f"{'='*70}")
    print(f"  Source : {PDF_PATH}")
    print(f"  Pages  : {CROSS_VALIDATE_PAGES}")
    print()

    if not os.path.exists(PDF_PATH):
        raise FileNotFoundError(f"PDF not found: {PDF_PATH}")

    timings = {}
    t_start = time.perf_counter()

    # ── Step 1: Raw text verification ─────────────────────────────────────
    t0 = time.perf_counter()
    raw_verification = raw_text_verification(PDF_PATH)
    timings["raw_text_verification_s"] = round(time.perf_counter() - t0, 3)

    # ── Step 2: Independent table extraction ──────────────────────────────
    t0 = time.perf_counter()
    pymupdf_page_tables = extract_pymupdf_tables(PDF_PATH)
    timings["pymupdf_table_extraction_s"] = round(time.perf_counter() - t0, 3)

    # ── Step 3: Page-boundary stitching ───────────────────────────────────
    t0 = time.perf_counter()
    stitched_tables = detect_and_stitch_page_boundary_tables(
        PDF_PATH, pymupdf_page_tables)
    timings["page_boundary_stitching_s"] = round(time.perf_counter() - t0, 3)

    # ── Step 4: Load Stage 1 tables and compare cell-level ────────────────
    t0 = time.perf_counter()
    stage1_tables = load_stage1_tables()
    cell_comparisons = compare_tables_cell_level(stage1_tables, pymupdf_page_tables)
    timings["cell_comparison_s"] = round(time.perf_counter() - t0, 3)

    # ── Step 5: Classification refinement ─────────────────────────────────
    t0 = time.perf_counter()
    reclassifications = refine_classifications(stage1_tables)
    timings["classification_refinement_s"] = round(time.perf_counter() - t0, 3)

    # ── Step 6: Accuracy re-check with stitched tables ────────────────────
    t0 = time.perf_counter()
    accuracy_recheck = recheck_accuracy_with_stitched(
        pymupdf_page_tables, stitched_tables, raw_verification)
    timings["accuracy_recheck_s"] = round(time.perf_counter() - t0, 3)

    # ── Step 7: NLL regeneration for stitched tables ──────────────────────
    t0 = time.perf_counter()
    nll_results = regenerate_nll_for_stitched(stitched_tables)
    timings["nll_regeneration_s"] = round(time.perf_counter() - t0, 3)

    # ── Total ─────────────────────────────────────────────────────────────
    timings["total_s"] = round(time.perf_counter() - t_start, 3)

    # ── Save report ───────────────────────────────────────────────────────
    report = save_report(
        raw_verification, pymupdf_page_tables, stitched_tables,
        cell_comparisons, reclassifications, accuracy_recheck,
        nll_results, timings,
    )

    # ── Final scorecard ───────────────────────────────────────────────────
    print(f"\n{'='*70}")
    print(f"  STAGE 2 — FINAL SCORECARD")
    print(f"{'='*70}")
    print(f"  Raw text verification  : {raw_verification['n_pass']}/{len(raw_verification['details'])} "
          f"({raw_verification['accuracy_pct']}%)")
    print(f"  Table recheck (stitched): {accuracy_recheck['table_pass']}/{accuracy_recheck['table_pass'] + accuracy_recheck['table_fail']} "
          f"({accuracy_recheck['table_accuracy_pct']}%)")
    print(f"  Combined accuracy      : {accuracy_recheck['combined_pass']}/{accuracy_recheck['combined_total']} "
          f"({accuracy_recheck['combined_accuracy_pct']}%)")
    print(f"  Page-boundary stitches : {len(stitched_tables)}")
    print(f"  Classification changes : {len(reclassifications)}")
    print(f"  Cell-level comparisons : {len(cell_comparisons)}")
    if cell_comparisons:
        avg_agree = sum(c['agreement_pct'] for c in cell_comparisons) / len(cell_comparisons)
        print(f"  Average cell agreement : {avg_agree:.1f}%")
    print(f"  Total time             : {timings['total_s']}s")
    n_disc = len(report.get("discrepancies", []))
    print(f"  Discrepancies found    : {n_disc}")
    print(f"{'='*70}\n")

    return report


if __name__ == "__main__":
    main()
