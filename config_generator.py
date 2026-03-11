#!/usr/bin/env python3
"""
config_generator.py — AI-Powered Pipeline Config Generator
===========================================================
Scans a clinical guidelines PDF and generates a pipeline_config.json
so the extraction pipeline can process ANY clinical PDF without manual
configuration.

Usage:
    python config_generator.py --pdf Uganda-Clinical-Guidelines-20231.pdf
    python config_generator.py --pdf some_guideline.pdf --output configs/my_config.json
    python config_generator.py --pdf some_guideline.pdf --no-llm   # heuristic only

Steps:
  1. PDF Scan (no LLM) — extract text, tables, chapter outline
  2. Drug Discovery (no LLM) — regex-based drug name detection
  3. Dosing Page Discovery (no LLM) — table keyword scoring
  4. Ground Truth Generation (no LLM) — verified text snippets
  5. LLM Enrichment (optional) — fills dose_reference_ranges, catches
     drugs the regex missed, generates condition patterns
  6. Validation — verifies all ground truth against raw PDF text
  7. Output — writes pipeline_config.json

The generated config is a DRAFT meant for human review before use.
"""

import argparse
import json
import os
import re
import sys
import time
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

try:
    import fitz  # PyMuPDF
except ImportError:
    sys.exit("ERROR: PyMuPDF (fitz) is required.  pip install pymupdf")


# ─────────────────────────────────────────────────────────────────────────────
# 1.  PDF SCANNING
# ─────────────────────────────────────────────────────────────────────────────

def scan_pdf(pdf_path: str) -> Dict[str, Any]:
    """Extract basic metadata, page texts, and table locations from the PDF."""
    doc = fitz.open(pdf_path)
    page_count = doc.page_count

    print(f"\n  Scanning {pdf_path} ({page_count} pages)...")

    page_texts: List[str] = []
    table_pages: List[int] = []
    dosing_table_pages: List[int] = []

    dosing_keywords = [
        "mg", "dose", "kg", "tablet", "mg/kg", "daily",
        "twice", "body weight", "weight (kg)",
    ]

    for i in range(page_count):
        text = doc[i].get_text()
        page_texts.append(text)

        try:
            tables = doc[i].find_tables()
            if tables and len(tables.tables) > 0:
                table_pages.append(i + 1)  # 1-indexed
                # Score for dosing content
                for t in tables.tables:
                    try:
                        df = t.to_pandas()
                        all_text = " ".join(
                            str(v) for v in df.values.flatten() if v
                        ) + " " + " ".join(str(c) for c in df.columns)
                        score = sum(
                            1 for kw in dosing_keywords
                            if kw in all_text.lower()
                        )
                        if score >= 3:
                            dosing_table_pages.append(i + 1)
                            break
                    except Exception:
                        pass
        except Exception:
            pass

    doc.close()

    # Extract title from first few pages
    title = _extract_title(page_texts[:5])

    print(f"  Pages: {page_count}")
    print(f"  Pages with tables: {len(table_pages)}")
    print(f"  Potential dosing table pages: {len(dosing_table_pages)}")

    return {
        "pdf_path": pdf_path,
        "page_count": page_count,
        "title": title,
        "page_texts": page_texts,
        "table_pages": table_pages,
        "dosing_table_pages": dosing_table_pages,
    }


def _extract_title(first_pages: List[str]) -> str:
    """Try to extract the document title from first few pages."""
    combined = "\n".join(first_pages[:3])
    # Look for common title patterns
    lines = [l.strip() for l in combined.split("\n") if l.strip()]
    # Skip very short lines (page numbers, etc.)
    candidates = [l for l in lines[:20] if 10 < len(l) < 120]
    if candidates:
        return candidates[0]
    return "Unknown Clinical Guidelines"


# ─────────────────────────────────────────────────────────────────────────────
# 2.  DRUG DISCOVERY (heuristic, no LLM)
# ─────────────────────────────────────────────────────────────────────────────

# Common pharmaceutical suffixes
_DRUG_SUFFIXES = [
    "mycin", "cillin", "azole", "prazole", "statin", "pril", "sartan",
    "olol", "dipine", "sone", "olone", "quine", "mide", "zide", "pam",
    "lam", "pine", "oxin", "formin", "gliptin", "flozin", "lukast",
    "parin", "virin", "navir", "ciclovir", "bivir", "fenac", "profen",
    "oxicam", "triptan", "setron", "mab", "nib", "tinib", "zumab",
    "ximab", "tide", "retin", "mustine", "platin", "taxel", "rubicin",
    "ephrine", "butol", "thiazide", "pamide",
]

# Common known drug names (generic first-line drugs in clinical settings)
_KNOWN_DRUGS = {
    "paracetamol", "ibuprofen", "aspirin", "amoxicillin", "metronidazole",
    "ciprofloxacin", "doxycycline", "azithromycin", "erythromycin",
    "cotrimoxazole", "gentamicin", "ceftriaxone", "cloxacillin",
    "chloramphenicol", "penicillin", "ampicillin", "fluconazole",
    "ketoconazole", "quinine", "chloroquine", "artemether", "lumefantrine",
    "artesunate", "amodiaquine", "primaquine", "piperaquine",
    "dihydroartemisinin", "sulfadoxine", "pyrimethamine", "mefloquine",
    "isoniazid", "rifampicin", "pyrazinamide", "ethambutol", "streptomycin",
    "efavirenz", "nevirapine", "lopinavir", "ritonavir", "tenofovir",
    "lamivudine", "zidovudine", "abacavir", "dolutegravir", "atazanavir",
    "metformin", "glibenclamide", "insulin", "amlodipine", "enalapril",
    "losartan", "hydrochlorothiazide", "atenolol", "nifedipine",
    "furosemide", "spironolactone", "morphine", "tramadol", "codeine",
    "diazepam", "phenobarbital", "phenytoin", "carbamazepine",
    "valproic acid", "haloperidol", "chlorpromazine", "salbutamol",
    "beclomethasone", "prednisolone", "hydrocortisone", "dexamethasone",
    "oxytocin", "misoprostol", "magnesium sulfate", "ferrous sulfate",
    "folic acid", "vitamin a", "oral rehydration salts", "zinc",
}


def discover_drugs(page_texts: List[str]) -> List[str]:
    """Discover drug/medication names from PDF text using heuristics."""
    full_text = " ".join(page_texts).lower()
    words = set(re.findall(r"\b[a-z]{4,20}\b", full_text))

    found_drugs: Set[str] = set()

    # Check known drug names
    for drug in _KNOWN_DRUGS:
        if drug.lower() in full_text:
            found_drugs.add(drug.lower())

    # Check pharmaceutical suffix patterns
    for word in words:
        for suffix in _DRUG_SUFFIXES:
            if word.endswith(suffix) and len(word) > len(suffix) + 2:
                # Verify it appears near dosing context
                pattern = rf"\b{re.escape(word)}\b"
                matches = re.findall(pattern, full_text)
                if len(matches) >= 2:  # appears at least twice
                    found_drugs.add(word)
                break

    # Find words that appear near "mg" patterns
    mg_context = re.findall(
        r"(\b[a-z]{4,20}\b)\s+\d+\s*(?:mg|mcg|iu)\b", full_text
    )
    for word in mg_context:
        if word not in {"dose", "give", "take", "body", "weight", "oral",
                        "daily", "twice", "once", "every", "hours", "days",
                        "weeks", "months", "years", "than", "less", "more",
                        "above", "below", "over", "under", "from", "with"}:
            found_drugs.add(word)

    # Filter out common non-drug words
    stopwords = {
        "treatment", "management", "clinical", "patient", "diagnosis",
        "disease", "infection", "condition", "symptoms", "complications",
        "prevention", "monitoring", "assessment", "therapy", "protocol",
        "guidelines", "chapter", "section", "table", "figure",
        "children", "adults", "pregnant", "women", "refer",
    }
    found_drugs -= stopwords

    result = sorted(found_drugs)
    print(f"  Discovered {len(result)} drug/medication names")
    return result


# ─────────────────────────────────────────────────────────────────────────────
# 3.  CONDITION / CHAPTER DISCOVERY
# ─────────────────────────────────────────────────────────────────────────────

def discover_conditions(page_texts: List[str]) -> List[List[str]]:
    """Discover clinical conditions from heading patterns and chapter text."""
    full_text = " ".join(page_texts[:30])  # Focus on TOC / early pages

    # Common clinical conditions
    condition_patterns = [
        (r"malaria", "Malaria"),
        (r"HIV|AIDS", "HIV/AIDS"),
        (r"tubercul", "Tuberculosis"),
        (r"pneumonia", "Pneumonia"),
        (r"diarrh", "Diarrhoeal disease"),
        (r"diabetes", "Diabetes"),
        (r"hypertension", "Hypertension"),
        (r"asthma", "Asthma"),
        (r"anemia|anaemia", "Anaemia"),
        (r"epilepsy", "Epilepsy"),
        (r"meningitis", "Meningitis"),
        (r"hepatitis", "Hepatitis"),
        (r"measles", "Measles"),
        (r"cholera", "Cholera"),
        (r"typhoid", "Typhoid"),
        (r"malnutrition", "Malnutrition"),
        (r"pregnancy|obstetric|maternal", "Maternal health"),
        (r"neonatal|newborn", "Neonatal care"),
        (r"dental|oral health", "Oral health"),
        (r"mental health|depression|anxiety", "Mental health"),
        (r"cancer|oncology", "Cancer"),
        (r"renal|kidney", "Renal disease"),
        (r"cardiac|heart", "Cardiac disease"),
        (r"respiratory", "Respiratory disease"),
        (r"skin|dermatol", "Skin conditions"),
    ]

    found = []
    for pattern, label in condition_patterns:
        if re.search(pattern, full_text, re.I):
            found.append([pattern, label])

    print(f"  Discovered {len(found)} clinical conditions")
    return found


# ─────────────────────────────────────────────────────────────────────────────
# 4.  GROUND TRUTH GENERATION (verified against raw text)
# ─────────────────────────────────────────────────────────────────────────────

def generate_ground_truth(
    scan: Dict[str, Any], drugs: List[str]
) -> List[Dict]:
    """Generate verified ground truth entries from PDF content."""
    page_texts = scan["page_texts"]
    dosing_pages = scan["dosing_table_pages"]
    gt_entries: List[Dict] = []

    # Strategy 1: Pick verified text snippets from dosing pages
    for pg in dosing_pages[:10]:  # cap at 10
        text = page_texts[pg - 1]
        # Find drug mentions on this page
        for drug in drugs[:20]:  # cap at 20
            if drug.lower() in text.lower():
                # Find a short distinctive phrase containing the drug
                sentences = re.split(r"[.;\n]", text)
                for sent in sentences:
                    if drug.lower() in sent.lower() and 10 < len(sent.strip()) < 120:
                        # Extract 2-3 keywords from this sentence
                        words = [w for w in sent.strip().split() if len(w) > 3]
                        if len(words) >= 2:
                            keywords = [drug.lower()]
                            # Add one more distinctive word
                            for w in words:
                                wl = w.lower().strip(".,;:()")
                                if wl != drug.lower() and wl not in {
                                    "with", "from", "that", "this", "have",
                                    "been", "also", "should", "which", "will",
                                }:
                                    keywords.append(wl)
                                    break
                            if len(keywords) >= 2:
                                gt_entries.append({
                                    "page": pg,
                                    "type": "text",
                                    "must_contain": keywords,
                                })
                                break
                break  # one entry per page

    # Strategy 2: Pick table value checks from dosing pages
    try:
        doc = fitz.open(scan["pdf_path"])
        for pg in dosing_pages[:8]:
            tables = doc[pg - 1].find_tables()
            if tables and tables.tables:
                for t in tables.tables:
                    try:
                        df = t.to_pandas()
                        if len(df) > 1:
                            # Pick a cell value that contains a number
                            for _, row in df.iterrows():
                                for val in row.values:
                                    val_str = str(val).strip()
                                    if re.search(r"\d", val_str) and 3 < len(val_str) < 40:
                                        gt_entries.append({
                                            "page": pg,
                                            "type": "table",
                                            "must_contain": [val_str],
                                        })
                                        break
                                else:
                                    continue
                                break
                    except Exception:
                        pass
                break  # one table check per page
        doc.close()
    except Exception:
        pass

    # Deduplicate by page+type
    seen = set()
    unique = []
    for gt in gt_entries:
        key = (gt["page"], gt["type"])
        if key not in seen:
            seen.add(key)
            unique.append(gt)

    # Cap at 15 entries
    unique = unique[:15]

    print(f"  Generated {len(unique)} ground truth entries")
    return unique


# ─────────────────────────────────────────────────────────────────────────────
# 5.  VALIDATION
# ─────────────────────────────────────────────────────────────────────────────

def validate_ground_truth(
    gt_entries: List[Dict], page_texts: List[str]
) -> List[Dict]:
    """Verify each ground truth entry actually exists in the PDF text."""
    valid = []
    rejected = 0
    for gt in gt_entries:
        pg = gt["page"]
        if pg < 1 or pg > len(page_texts):
            rejected += 1
            continue

        text_lower = page_texts[pg - 1].lower()
        keywords = [kw.lower() for kw in gt["must_contain"]]
        all_found = all(kw in text_lower for kw in keywords)

        if all_found:
            valid.append(gt)
        else:
            rejected += 1

    if rejected:
        print(f"  Validation: {len(valid)} passed, {rejected} rejected")
    else:
        print(f"  Validation: {len(valid)} passed, all verified")
    return valid


# ─────────────────────────────────────────────────────────────────────────────
# 6.  LLM ENRICHMENT (optional)
# ─────────────────────────────────────────────────────────────────────────────

def llm_enrich(
    scan: Dict, drugs: List[str], conditions: List[List[str]]
) -> Dict[str, Any]:
    """Use an LLM to generate dose_reference_ranges and enrich the config.

    Returns a dict with optional enrichments. Returns empty dict if
    no API key is available.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        print("  LLM enrichment: skipped (no ANTHROPIC_API_KEY)")
        return {}

    try:
        import anthropic
    except ImportError:
        print("  LLM enrichment: skipped (anthropic package not installed)")
        return {}

    # Build a concise prompt with sample pages
    sample_pages = []
    page_texts = scan["page_texts"]
    dosing_pages = scan["dosing_table_pages"]

    # Pick 5 representative dosing pages
    for pg in dosing_pages[:5]:
        sample_pages.append(f"--- Page {pg} ---\n{page_texts[pg-1][:800]}")

    # Pick 2 early pages (TOC/intro)
    for pg in [1, 2]:
        if pg <= len(page_texts):
            sample_pages.append(f"--- Page {pg} ---\n{page_texts[pg-1][:500]}")

    samples_text = "\n\n".join(sample_pages)

    prompt = f"""You are analyzing a clinical guidelines document. Below are sample pages.

The document title appears to be: {scan['title']}
Total pages: {scan['page_count']}
Drugs discovered by heuristic scan: {', '.join(drugs[:30])}

SAMPLE PAGES:
{samples_text}

Generate a JSON object with ONLY these fields:
1. "dose_reference_ranges": For each drug found in the document, provide safe per-kg dose ranges.
   Format: {{"drug_name": {{"min_mg_per_kg": float, "max_mg_per_kg": float}}}}
   Only include drugs you're confident about. Use wide ranges to catch gross errors only.

2. "additional_drugs": List any drug names you found in the samples that the heuristic missed.

3. "additional_conditions": List any clinical conditions found in the samples, as
   [["regex_pattern", "Label"], ...] format.

4. "biomarkers": List any lab values / biomarkers mentioned (e.g., "G6PD", "CD4", "HbA1c").

5. "contraindication_terms": List phrases that indicate contraindications in this document.

Return ONLY valid JSON, no markdown formatting."""

    print("  LLM enrichment: calling Anthropic API...")
    try:
        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = response.content[0].text.strip()
        # Strip markdown code fences if present
        if raw.startswith("```"):
            raw = re.sub(r"^```\w*\n?", "", raw)
            raw = re.sub(r"\n?```$", "", raw)

        enrichment = json.loads(raw)
        print(f"  LLM enrichment: received {len(enrichment)} fields")
        return enrichment

    except Exception as e:
        print(f"  LLM enrichment: failed ({e})")
        return {}


# ─────────────────────────────────────────────────────────────────────────────
# 7.  CONFIG ASSEMBLY
# ─────────────────────────────────────────────────────────────────────────────

def assemble_config(
    scan: Dict[str, Any],
    drugs: List[str],
    conditions: List[List[str]],
    ground_truth: List[Dict],
    enrichment: Dict[str, Any],
) -> Dict[str, Any]:
    """Assemble the final pipeline_config.json structure."""

    # Merge LLM-discovered drugs
    all_drugs = list(dict.fromkeys(
        drugs + enrichment.get("additional_drugs", [])
    ))

    # Merge conditions
    all_conditions = conditions[:]
    for cond in enrichment.get("additional_conditions", []):
        if isinstance(cond, list) and len(cond) == 2:
            all_conditions.append(cond)

    # Generic dosing keywords (not disease-specific)
    dosing_keywords = [
        "body weight", "kg", "dose", "mg", "tablet",
        "twice daily", "daily for", "single dose", "every 8 hours",
        "mg/kg", "dose (mg)", "dose given",
    ]

    # Generic high preservation keywords
    high_pres = [
        "mg/kg", "contraindicated", "do not give", "danger sign",
        "refer urgently", "emergency", "not recommended",
        "should not be used", "avoid", "first-line treatment",
    ]

    # Generic contraindication terms
    contra_terms = enrichment.get("contraindication_terms", [
        "contraindicated", "do not give", "not recommended",
        "avoid", "should not", "first trimester",
        "allergy", "hypersensitivity",
    ])

    # Biomarkers
    biomarkers = enrichment.get("biomarkers", [])

    # Dose ranges from LLM (empty if no LLM)
    dose_ranges = {}
    for drug, vals in enrichment.get("dose_reference_ranges", {}).items():
        if isinstance(vals, dict) and "min_mg_per_kg" in vals and "max_mg_per_kg" in vals:
            dose_ranges[drug] = {
                "min_mg_per_kg": float(vals["min_mg_per_kg"]),
                "max_mg_per_kg": float(vals["max_mg_per_kg"]),
            }

    config = {
        "document": {
            "pdf_path": os.path.basename(scan["pdf_path"]),
            "title": scan["title"],
            "short_name": _make_short_name(scan["title"]),
            "page_count": scan["page_count"],
        },
        "processing": {
            "benchmark_pages": "auto",
            "page_range": None,
            "max_pages_per_batch": 200 if scan["page_count"] > 500 else None,
        },
        "ground_truth": ground_truth,
        "drug_keywords": all_drugs,
        "dosing_keywords": dosing_keywords,
        "dose_reference_ranges": dose_ranges,
        "domain_keywords": {
            "conditions": all_conditions,
            "biomarkers": biomarkers,
            "contraindication_terms": contra_terms,
            "high_preservation_keywords": high_pres,
        },
        "cross_validation": {
            "dosing_pages": scan["dosing_table_pages"][:50],  # cap
            "severe_pages": [],
        },
    }

    return config


def _make_short_name(title: str) -> str:
    """Create a short identifier from the document title."""
    words = re.findall(r"[A-Za-z]+", title)
    if len(words) >= 3:
        return "-".join(w[:6] for w in words[:3])
    return title[:30].replace(" ", "-")


# ─────────────────────────────────────────────────────────────────────────────
# 8.  MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Generate pipeline_config.json for a clinical PDF"
    )
    parser.add_argument(
        "--pdf", required=True,
        help="Path to the clinical guidelines PDF",
    )
    parser.add_argument(
        "--output", type=str, default=None,
        help="Output path for the config JSON (default: configs/<short_name>.json)",
    )
    parser.add_argument(
        "--no-llm", action="store_true",
        help="Skip LLM enrichment (heuristic-only mode)",
    )
    args = parser.parse_args()

    if not os.path.exists(args.pdf):
        sys.exit(f"ERROR: PDF not found: {args.pdf}")

    t_start = time.perf_counter()

    print(f"\n{'='*70}")
    print(f"  CONFIG GENERATOR — Pipeline Configuration Builder")
    print(f"{'='*70}")

    # Step 1: Scan PDF
    print(f"\n  Step 1: Scanning PDF...")
    scan = scan_pdf(args.pdf)

    # Step 2: Discover drugs
    print(f"\n  Step 2: Discovering drug names...")
    drugs = discover_drugs(scan["page_texts"])

    # Step 3: Discover conditions
    print(f"\n  Step 3: Discovering clinical conditions...")
    conditions = discover_conditions(scan["page_texts"])

    # Step 4: Generate ground truth
    print(f"\n  Step 4: Generating ground truth...")
    raw_gt = generate_ground_truth(scan, drugs)

    # Step 5: Validate ground truth
    print(f"\n  Step 5: Validating ground truth...")
    valid_gt = validate_ground_truth(raw_gt, scan["page_texts"])

    # Step 6: LLM enrichment
    enrichment = {}
    if not args.no_llm:
        print(f"\n  Step 6: LLM enrichment...")
        enrichment = llm_enrich(scan, drugs, conditions)
    else:
        print(f"\n  Step 6: LLM enrichment... SKIPPED (--no-llm)")

    # Step 7: Assemble config
    print(f"\n  Step 7: Assembling config...")
    config = assemble_config(scan, drugs, conditions, valid_gt, enrichment)

    # Determine output path
    if args.output:
        out_path = Path(args.output)
    else:
        os.makedirs("configs", exist_ok=True)
        short = config["document"]["short_name"].lower()
        out_path = Path("configs") / f"{short}.json"

    # Write config
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    elapsed = time.perf_counter() - t_start

    # Clean up page_texts from memory (can be large)
    del scan["page_texts"]

    # Summary
    print(f"\n{'='*70}")
    print(f"  CONFIG GENERATION COMPLETE")
    print(f"{'='*70}")
    print(f"  Document      : {config['document']['title']}")
    print(f"  Pages         : {config['document']['page_count']}")
    print(f"  Drugs found   : {len(config['drug_keywords'])}")
    print(f"  Conditions    : {len(config['domain_keywords']['conditions'])}")
    print(f"  Ground truth  : {len(config['ground_truth'])} verified entries")
    print(f"  Dose ranges   : {len(config['dose_reference_ranges'])} drugs")
    print(f"  Dosing pages  : {len(config['cross_validation']['dosing_pages'])}")
    llm_status = "enriched" if enrichment else "heuristic only"
    print(f"  LLM status    : {llm_status}")
    print(f"  Output        : {out_path}")
    print(f"  Time          : {elapsed:.1f}s")
    print(f"{'='*70}")
    print(f"\n  ⚠️  This config is a DRAFT. Please review before running the pipeline.")
    print(f"      In particular, verify dose_reference_ranges with a clinician.\n")


if __name__ == "__main__":
    main()
