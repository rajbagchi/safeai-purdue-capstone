"""
Docling-based table extraction for SafeAI pipeline.

Replaces PyMuPDF's heuristic find_tables() with IBM Docling 2.x +
TableFormer ACCURATE for complex clinical table structures.  Docling
handles multi-page table reconstruction natively, so pass2b stitching
is skipped when this extractor is used.

Graceful fallback: if docling is not installed, DOCLING_AVAILABLE is
False and the caller falls back to the existing PyMuPDF pass.

Usage (called from MultiPassExtractor.extract_all when use_docling_tables=True):

    from pipeline.docling_table_extractor import extract_tables_with_docling, DOCLING_AVAILABLE

    if DOCLING_AVAILABLE and config.use_docling_tables:
        tables = extract_tables_with_docling(config.pdf_path, config.output_dir)
    else:
        tables = pymupdf_tables  # existing pass2 result
"""

from __future__ import annotations

import os
import re
from typing import Any, Dict, List, Optional

import pandas as pd

# ---------------------------------------------------------------------------
# Graceful Docling import
# ---------------------------------------------------------------------------
try:
    from docling.document_converter import DocumentConverter, PdfFormatOption
    from docling.datamodel.pipeline_options import (
        PdfPipelineOptions,
        TableFormerMode,
    )
    from docling.datamodel.base_models import InputFormat
    DOCLING_AVAILABLE = True
except ImportError:
    DOCLING_AVAILABLE = False


def _build_docling_converter(table_mode: str = "accurate") -> Optional[Any]:
    """Build a DocumentConverter with TableFormer in the requested mode.

    Returns None if Docling is not installed.
    """
    if not DOCLING_AVAILABLE:
        return None

    mode = TableFormerMode.ACCURATE if table_mode == "accurate" else TableFormerMode.FAST

    pipeline_opts = PdfPipelineOptions()
    pipeline_opts.do_table_structure = True
    pipeline_opts.table_structure_options.mode = mode
    # Do not run VLM here — this extractor is for tables only.
    pipeline_opts.do_ocr = False

    return DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_opts)
        }
    )


def _docling_table_to_dataframe(table_obj: Any) -> pd.DataFrame:
    """Convert a Docling TableItem to a pandas DataFrame.

    Docling tables expose export_to_dataframe() in >=2.x.
    Falls back to reconstructing from table.data.grid (cell-level access).
    """
    # Preferred path: native DataFrame export
    if hasattr(table_obj, "export_to_dataframe"):
        try:
            return table_obj.export_to_dataframe()
        except Exception:
            pass

    # Fallback: reconstruct from grid cells
    if hasattr(table_obj, "data") and hasattr(table_obj.data, "grid"):
        grid = table_obj.data.grid
        if not grid:
            return pd.DataFrame()
        rows = []
        for row in grid:
            rows.append([cell.text if cell else "" for cell in row])
        if rows:
            return pd.DataFrame(rows[1:], columns=rows[0]) if len(rows) > 1 else pd.DataFrame(rows)

    return pd.DataFrame()


def _docling_table_to_markdown(table_obj: Any, df: pd.DataFrame) -> str:
    """Export a Docling table to markdown string.

    Tries Docling's native markdown export first, falls back to pandas.
    """
    if hasattr(table_obj, "export_to_markdown"):
        try:
            return table_obj.export_to_markdown()
        except Exception:
            pass

    if df.empty:
        return ""

    try:
        return df.to_markdown(index=False) or df.to_string(index=False)
    except Exception:
        return df.to_string(index=False)


def _get_table_page(table_obj: Any, doc_obj: Any) -> int:
    """Extract 1-based page number for a Docling TableItem."""
    try:
        prov = table_obj.prov
        if prov:
            p = prov[0]
            # Docling 2.x: page_no attribute
            if hasattr(p, "page_no"):
                return int(p.page_no)
            # Dict-style access
            if isinstance(p, dict):
                return int(p.get("page_no") or p.get("page", 1))
    except Exception:
        pass
    return 1


def _get_table_bbox(table_obj: Any) -> Optional[tuple]:
    """Extract (x0, y0, x1, y1) bounding box from Docling prov if available."""
    try:
        prov = table_obj.prov
        if prov:
            p = prov[0]
            bbox = getattr(p, "bbox", None) or (p.get("bbox") if isinstance(p, dict) else None)
            if bbox:
                return (
                    float(getattr(bbox, "l", 0)),
                    float(getattr(bbox, "t", 0)),
                    float(getattr(bbox, "r", 0)),
                    float(getattr(bbox, "b", 0)),
                )
    except Exception:
        pass
    return None


def extract_tables_with_docling(
    pdf_path: str,
    output_dir: str,
    table_mode: str = "accurate",
) -> List[Dict[str, Any]]:
    """Extract tables from a PDF using Docling + TableFormer.

    Returns a list of table dicts in SafeAI's format (compatible with the
    rest of the pipeline — classification and NLL are set to empty strings
    here and populated downstream by MultiPassExtractor._classify_table()
    and _generate_nll() as usual).

    Args:
        pdf_path:   Absolute path to the PDF file.
        output_dir: Pipeline output directory (for CSV exports).
        table_mode: "accurate" (TableFormerMode.ACCURATE, default) or "fast".

    Returns:
        List of table dicts with keys matching SafeAI's existing table schema:
        page, method, data, headers, markdown, num_rows, num_cols,
        bbox, confidence, stitched, classification (empty), nll (empty).
        The "source" key is set to "docling" so callers can gate stitching.
    """
    if not DOCLING_AVAILABLE:
        raise RuntimeError(
            "Docling is not installed. Run: pip install 'docling>=2.64.0'"
        )

    tables_dir = os.path.join(output_dir, "tables")
    os.makedirs(tables_dir, exist_ok=True)

    converter = _build_docling_converter(table_mode)
    if converter is None:
        return []

    print(f"\n[Docling] Extracting tables with TableFormer {table_mode.upper()}...")

    try:
        result = converter.convert(pdf_path)
    except Exception as e:
        print(f"  [Docling] Conversion failed: {e}. Falling back to PyMuPDF tables.")
        return []

    doc = result.document
    tables: List[Dict[str, Any]] = []

    table_items = list(doc.tables) if hasattr(doc, "tables") else []
    print(f"  [Docling] Found {len(table_items)} table(s)")

    for idx, table_obj in enumerate(table_items):
        try:
            df = _docling_table_to_dataframe(table_obj)
            if df.empty:
                continue

            df = df.fillna("")
            markdown = _docling_table_to_markdown(table_obj, df)
            page_no = _get_table_page(table_obj, doc)
            bbox = _get_table_bbox(table_obj)

            headers = [str(c) for c in df.columns.tolist()]
            data = df.to_dict(orient="records")

            # Export CSV for traceability
            csv_path = os.path.join(tables_dir, f"docling_table_p{page_no}_{idx + 1}.csv")
            try:
                df.to_csv(csv_path, index=False)
            except Exception:
                csv_path = ""

            table_dict: Dict[str, Any] = {
                "page": page_no,
                "method": "docling_tableformer",
                "source": "docling",          # gating key for stitch bypass
                "data": data,
                "headers": headers,
                "markdown": markdown,
                "num_rows": len(df),
                "num_cols": len(df.columns),
                "file": csv_path,
                "confidence": 0.97,           # TableFormer ACCURATE confidence
                "bbox": bbox,
                "stitched": False,            # Docling reconstructs multi-page natively
                "stitched_from_rows": [],
                # Classification and NLL populated downstream by SafeAI's classifier
                "classification": "",
                "nll": "",
            }
            tables.append(table_dict)

        except Exception as e:
            print(f"  [Docling] Table {idx} failed: {e}")
            continue

    print(f"  [Docling] Successfully extracted {len(tables)} table(s)")
    return tables
