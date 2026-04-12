"""
Pipeline configuration, enums, and shared data structures.

ExtractionConfig accepts any PDF path string (Windows absolute paths, paths with
spaces, etc.). Use the factory helpers for the two validated source documents
so output directories do not collide and medical-content checks match the doc.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional


class TriageLevel(Enum):
    RED = "🔴 RED (Immediate Referral Required)"
    YELLOW = "🟡 YELLOW (Urgent Referral - Assess Today)"
    GREEN = "🟢 GREEN (Manage at Community Level)"


class MedicalSource(Enum):
    """Canonical label for citation / VHT output (maps from active guideline preset)."""

    WHO_MALARIA_NIH = "WHO Malaria Guidelines (NCBI Bookshelf)"
    UGANDA_CLINICAL_2023 = "Uganda Clinical Guidelines 2023"
    GENERIC = "Clinical guidelines"


def medical_source_for_config(cfg: "ExtractionConfig") -> MedicalSource:
    """Infer MedicalSource from ExtractionConfig.document_title."""
    t = (cfg.document_title or "").lower()
    if "uganda" in t:
        return MedicalSource.UGANDA_CLINICAL_2023
    if "malaria" in t or "ncbi" in t or "bookshelf" in t:
        return MedicalSource.WHO_MALARIA_NIH
    return MedicalSource.GENERIC


class PreservationLevel(Enum):
    """
    How faithfully a chunk's text must be reproduced in a VHT response.

    VERBATIM  — dosing tables, drug names, and quantities: must be copied
                exactly; no paraphrasing allowed.
    HIGH      — procedural steps and diagnostic criteria: minor rephrasing
                acceptable but all clinical values must be preserved.
    STANDARD  — background / context paragraphs: may be summarised for the
                VHT audience while retaining clinical accuracy.
    """

    VERBATIM = "verbatim"
    HIGH = "high"
    STANDARD = "standard"


class DangerSign(Enum):
    # Pediatric danger signs (under 5)
    UNABLE_TO_DRINK = "Unable to drink or breastfeed"
    CONVULSIONS = "Convulsions"
    VOMITS_EVERYTHING = "Vomits everything"
    LETHARGIC = "Lethargic or unconscious"

    # Adult danger signs
    CHEST_PAIN = "Chest pain"
    DIFFICULT_BREATHING = "Difficulty breathing"
    SEVERE_HEADACHE = "Severe headache with neck stiffness"
    BLEEDING = "Unexplained bleeding"

    # General
    HIGH_FEVER = "High fever (>39°C) for >3 days"
    DEHYDRATION = "Signs of severe dehydration"


# ---------------------------------------------------------------------------
# Table classification keyword sets
# ---------------------------------------------------------------------------
# Used by MultiPassExtractor._classify_table() to assign every extracted table
# one of five types: dosing | evidence | clinical_management | structural | other
#
# DOSING_TABLE_KEYWORDS / CLINICAL_TABLE_KEYWORDS are the document-agnostic
# base sets.  Per-document additions go in ExtractionConfig.dosing_table_keywords
# and ExtractionConfig.clinical_table_keywords (see factory presets below).
# EVIDENCE_TABLE_KEYWORDS and STRUCTURAL_TABLE_KEYWORDS are universal and not
# overridable per-document.

DOSING_TABLE_KEYWORDS: List[str] = [
    "dose",
    "dosage",
    "dosing",
    "mg",
    "tablet",
    "regimen",
    "body weight",
    "twice daily",
    "once daily",
    "three times",
    "per day",
    "mg/kg",
    "course",
    "administration",
]

# GRADE / evidence quality table markers (universal across guideline documents)
EVIDENCE_TABLE_KEYWORDS: List[str] = [
    "certainty of evidence",
    "quality of evidence",
    "grade",
    "relative effect",
    "risk ratio",
    "odds ratio",
    "absolute effect",
    "anticipated effects",
    "moderate certainty",
    "low certainty",
    "high certainty",
    "very low certainty",
    "rr ",
    "or ",
    "ci ",
    "confidence interval",
]

# Structural / non-clinical table markers (ToC, abbreviation lists)
STRUCTURAL_TABLE_KEYWORDS: List[str] = [
    "abbreviation",
    "acronym",
    "definition",
    "table of contents",
    "glossary",
    "full name",
    "meaning",
]

# General clinical management keywords (non-dosing safety-critical content)
CLINICAL_TABLE_KEYWORDS: List[str] = [
    "management",
    "complication",
    "severe",
    "danger sign",
    "referral",
    "treatment failure",
    "emergency",
    "protocol",
    "guideline",
    "recommendation",
]

# Malaria-specific dosing table keywords (added to base set in who_malaria preset)
MALARIA_DOSING_TABLE_KEYWORDS: List[str] = [
    "artemether",
    "lumefantrine",
    "artesunate",
    "amodiaquine",
    "mefloquine",
    "sulfadoxine",
    "pyrimethamine",
    "piperaquine",
    "primaquine",
    "dihydroartemisinin",
    "dha",
    "chloroquine",
    "quinine",
]

# Uganda clinical guidelines dosing keywords (broader drug coverage)
UGANDA_DOSING_TABLE_KEYWORDS: List[str] = [
    "amoxicillin",
    "cotrimoxazole",
    "metronidazole",
    "ciprofloxacin",
    "doxycycline",
    "penicillin",
    "gentamicin",
    "ampicillin",
    "erythromycin",
    "fluconazole",
    "oral rehydration",
    "zinc",
    "vitamin a",
    "paracetamol",
    "ibuprofen",
    "prednisolone",
    "insulin",
    "glibenclamide",
    "metformin",
    "salbutamol",
]

# Uganda clinical management keywords (broader specialties)
UGANDA_CLINICAL_TABLE_KEYWORDS: List[str] = [
    "management",
    "complication",
    "severe",
    "danger sign",
    "referral",
    "treatment failure",
    "emergency",
    "protocol",
    "guideline",
    "recommendation",
    "diagnosis",
    "diagnostic criteria",
    "classification",
    "staging",
    "level of care",
    "hc2",
    "hc3",
    "hc4",
    "hospital",
    "outpatient",
    "inpatient",
    "antenatal",
    "postnatal",
    "immunisation",
    "nutrition",
    "hiv",
    "tb",
    "malaria",
    "diarrhoea",
    "pneumonia",
    "sepsis",
]


# ---------------------------------------------------------------------------
# Directory containing document-specific JSON config files.
_CONFIGS_DIR: Path = Path(__file__).parent.parent / "configs"


def _load_json_config(path: Path) -> Dict[str, Any]:
    """Load a document JSON config file.

    Returns the parsed dict, or an empty dict if the file is missing or
    cannot be parsed (so callers can safely use .get() without guarding).
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


# Default PDF paths for the two validated source documents.
# Resolved in order: MALARIA_PDF / UGANDA_PDF env var → legacy Windows path.
# On macOS/Linux set the env var to avoid passing --pdf every time:
#   export MALARIA_PDF=/path/to/Bookshelf_NBK588130.pdf
#   export UGANDA_PDF=/path/to/Uganda_Clinical_Guidelines_2023.pdf
DEFAULT_WHO_MALARIA_NIH_PDF = Path(
    os.environ.get("MALARIA_PDF")
    or os.environ.get("WHO_MALARIA_PDF")
    or r"C:\temp\capstone\Bookshelf_NBK588130.pdf"
)
DEFAULT_UGANDA_CLINICAL_2023_PDF = Path(
    os.environ.get("UGANDA_PDF")
    or os.environ.get("UGANDA_CLINICAL_PDF")
    or r"C:\temp\capstone\Uganda Clinical Guidelines 2023.pdf"
)

GENERAL_CLINICAL_CRITICAL_TERMS: List[str] = [
    "dose",
    "mg",
    "treatment",
    "patient",
    "child",
    "adult",
    "contraindication",
    "referral",
    "emergency",
    "management",
]

MALARIA_GUIDELINE_CRITICAL_TERMS: List[str] = [
    "dose",
    "mg",
    "contraindication",
    "warning",
    "severe malaria",
    "artemisinin",
    "pregnancy",
    "children",
    "infant",
    "emergency",
]

# Slightly tuned for MoH / broad specialty content (avoid malaria-only terms).
UGANDA_CLINICAL_CRITICAL_TERMS: List[str] = [
    "dose",
    "mg",
    "treatment",
    "diagnosis",
    "patient",
    "child",
    "adult",
    "contraindication",
    "referral",
    "hospital",
    "symptom",
]


@dataclass
class ExtractionConfig:
    """Configuration for extraction pipeline."""

    pdf_path: str
    output_dir: str = "./medical_knowledge_base"
    cache_dir: str = "./cache"
    enable_ocr: bool = True
    enable_table_detection: bool = True
    enable_image_extraction: bool = True
    # Scan every page for PyMuPDF tables (not only the Pass-0 sample); slower but catches tables after page ~20.
    full_document_table_scan: bool = True
    # Bump to invalidate extraction pickle cache after engine changes.
    extraction_engine_version: int = 3
    min_chunk_size: int = 500
    max_chunk_size: int = 2000
    chunk_overlap: int = 200
    confidence_threshold: float = 0.8
    # Passes 0-4 always run (analyze, text, tables, OCR, cross-validate).
    # A supplementary image-extraction pass also runs when enable_image_extraction=True.
    num_extraction_passes: int = 5
    # Shown in Q&A responses and saved metadata
    document_title: str = "Clinical guidelines"
    # If None, validator uses GENERAL_CLINICAL_CRITICAL_TERMS
    critical_content_terms: Optional[List[str]] = None
    # Extra dosing keywords added to DOSING_TABLE_KEYWORDS for table classification.
    # Set per-document in factory presets (e.g., ACT drug names for malaria).
    dosing_table_keywords: Optional[List[str]] = None
    # Extra clinical management keywords added to CLINICAL_TABLE_KEYWORDS.
    clinical_table_keywords: Optional[List[str]] = None
    # Raw drug name keywords for retrieval-time metadata boosting.
    # Populated from JSON drug_keywords by factory presets.
    drug_keywords: Optional[List[str]] = None
    # Condition patterns for retrieval-time metadata boosting.
    # Each entry is [regex_pattern, canonical_label] from JSON domain_keywords.conditions.
    condition_patterns: Optional[List[List[str]]] = None
    # Use IBM Docling + TableFormer ACCURATE as primary table extractor.
    # When True (default), Docling replaces PyMuPDF's find_tables() for
    # tables; PyMuPDF is retained for text and cross-validation.
    # Set to False to revert to PyMuPDF-only extraction (legacy behaviour).
    # Requires: pip install 'docling>=2.64.0'
    use_docling_tables: bool = True

    def __post_init__(self) -> None:
        # Normalize path: expanduser, resolve for stable cache keys on absolute paths
        p = Path(self.pdf_path).expanduser()
        try:
            self.pdf_path = str(p.resolve(strict=False))
        except OSError:
            self.pdf_path = str(p)
        if not self.cache_dir or self.cache_dir == "./cache":
            self.cache_dir = str(Path(self.output_dir) / "cache")


def extraction_config_who_malaria_nih(
    pdf_path: str | Path = DEFAULT_WHO_MALARIA_NIH_PDF,
    *,
    output_dir: Optional[str | Path] = None,
) -> ExtractionConfig:
    """Preset for the WHO Malaria Guidelines PDF (NCBI Bookshelf NBK588130).

    Vocabulary is loaded from configs/malaria_who_2025.json when present,
    augmented by the hard-coded MALARIA_DOSING_TABLE_KEYWORDS constants.
    Falls back gracefully to the constants-only vocabulary if the JSON is
    absent (so the module works out-of-the-box from any working directory).
    """
    doc = _load_json_config(_CONFIGS_DIR / "malaria_who_2025.json")

    pdf = Path(pdf_path).expanduser()
    base = pdf.parent
    out_name: str = doc.get("output_dir") or "medical_kb_who_malaria"
    out = Path(output_dir) if output_dir else base / out_name

    # Dosing keywords: JSON drug_keywords + dosing_keywords + hard-coded constants
    drug_kws: List[str] = doc.get("drug_keywords") or []
    dosing_kws: List[str] = doc.get("dosing_keywords") or []
    all_dosing: List[str] = list(dict.fromkeys(
        drug_kws + dosing_kws + list(MALARIA_DOSING_TABLE_KEYWORDS)
    )) or list(MALARIA_DOSING_TABLE_KEYWORDS)

    # Clinical table keywords: malaria PDF has none in JSON (empty list is fine)
    clinical_kws: List[str] = doc.get("clinical_table_keywords") or []

    title: str = (
        (doc.get("document") or {}).get("title")
        or "WHO Malaria Guidelines (NCBI Bookshelf)"
    )

    # Condition patterns for retrieval metadata boosting
    raw_conditions = (doc.get("domain_keywords") or {}).get("conditions") or []

    return ExtractionConfig(
        pdf_path=str(pdf),
        output_dir=str(out),
        document_title=title,
        critical_content_terms=list(MALARIA_GUIDELINE_CRITICAL_TERMS),
        dosing_table_keywords=all_dosing,
        clinical_table_keywords=clinical_kws or None,
        drug_keywords=drug_kws or None,
        condition_patterns=raw_conditions or None,
    )


def extraction_config_uganda_clinical_2023(
    pdf_path: str | Path = DEFAULT_UGANDA_CLINICAL_2023_PDF,
    *,
    output_dir: Optional[str | Path] = None,
) -> ExtractionConfig:
    """Preset for the Uganda Clinical Guidelines 2023 PDF (broad MoH content).

    Vocabulary is loaded from configs/uganda_clinical_2023.json when present,
    augmented by the hard-coded UGANDA_* constants.  The JSON carries 200+
    drug names and 30+ clinical table keywords tuned for Uganda MoH content.
    Falls back to constants-only vocabulary if the JSON file is absent.
    """
    doc = _load_json_config(_CONFIGS_DIR / "uganda_clinical_2023.json")

    pdf = Path(pdf_path).expanduser()
    base = pdf.parent
    out_name: str = doc.get("output_dir") or "medical_kb_uganda_clinical_2023"
    out = Path(output_dir) if output_dir else base / out_name

    # Dosing keywords: JSON drug_keywords + dosing_keywords + hard-coded constants
    drug_kws = doc.get("drug_keywords") or []
    dosing_kws = doc.get("dosing_keywords") or []
    all_dosing = list(dict.fromkeys(
        drug_kws + dosing_kws + list(UGANDA_DOSING_TABLE_KEYWORDS)
    )) or list(UGANDA_DOSING_TABLE_KEYWORDS)

    # Clinical table keywords: JSON list is more comprehensive than the constant
    clinical_kws = doc.get("clinical_table_keywords") or []
    all_clinical = list(dict.fromkeys(
        clinical_kws + list(UGANDA_CLINICAL_TABLE_KEYWORDS)
    )) or list(UGANDA_CLINICAL_TABLE_KEYWORDS)

    title = (
        (doc.get("document") or {}).get("title")
        or "Uganda Clinical Guidelines 2023"
    )

    # Condition patterns for retrieval metadata boosting
    raw_conditions = (doc.get("domain_keywords") or {}).get("conditions") or []

    return ExtractionConfig(
        pdf_path=str(pdf),
        output_dir=str(out),
        document_title=title,
        critical_content_terms=list(UGANDA_CLINICAL_CRITICAL_TERMS),
        dosing_table_keywords=all_dosing,
        clinical_table_keywords=all_clinical,
        drug_keywords=drug_kws or None,
        condition_patterns=raw_conditions or None,
    )


@dataclass
class ValidationReport:
    """Report from validation stages."""

    stage: str
    passed: bool
    issues: List[str]
    confidence: float
    suggestions: List[str]
    metadata: Dict[str, Any]
