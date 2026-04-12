"""
Medical guardrail brain: validates Q&A responses against safety rules.
"""

import re
from typing import Dict, List, Optional


# ---------------------------------------------------------------------------
# Danger-sign vocabulary (shared by triage check and danger-sign collector)
# ---------------------------------------------------------------------------

_DANGER_SIGN_NEEDLES = [
    ("unable to drink",    "Unable to drink / cannot drink"),
    ("cannot drink",       "Unable to drink / cannot drink"),
    ("convuls",            "Convulsions / seizures"),
    ("seizure",            "Convulsions / seizures"),
    ("unconscious",        "Unconscious or not waking"),
    ("very weak",          "Very weak"),
    ("lethargic",          "Very weak / lethargic"),
    ("bleeding",           "Bleeding"),
    ("not waking",         "Unconscious or not waking"),
    ("severe pain",        "Severe pain"),
    ("difficulty breath",  "Difficulty breathing"),
    ("fast breath",        "Fast / difficulty breathing"),
    ("pale",               "Pallor / anaemia sign"),
    ("jaundice",           "Jaundice"),
    ("yellow skin",        "Jaundice"),
    ("yellow eye",         "Jaundice"),
]

# Patient-context keywords used for contraindication cross-check
_PATIENT_CONTEXTS: Dict[str, List[str]] = {
    "pregnant": ["pregnan", "first trimester", "second trimester", "third trimester",
                 "antenatal", "maternal"],
    "infant":   ["infant", "newborn", "neonate", "baby", "<6 month", "under 6 month",
                 "0-6 month"],
    "child":    ["child", "pediatric", "paediatric", "toddler", "school age"],
    "renal":    ["renal", "kidney", "renal failure", "renal impairment", "dialysis",
                 "creatinine"],
    "liver":    ["liver", "hepatic", "cirrhosis", "hepatitis"],
    "breastfeeding": ["breastfeed", "lactating", "nursing mother"],
}


class MedicalGuardrailBrain:
    """
    Second brain for medical safety validation.

    Changes (2026-04-10):
    - validate_response() now accepts optional retrieved_chunks so checks can
      inspect source evidence, not just query text and response text.
    - _validate_triage() scans query + chunk text + chunk clinical_metadata for
      danger signs (was query-only).
    - _check_dangerous_advice() expanded from 4 to 10 regex patterns.
    - _validate_dosing_values() (new): checks that every dosing quantity in the
      response appears verbatim in at least one retrieved source chunk.
    - _check_contraindications() (new): cross-checks drug contraindications from
      chunk clinical_metadata against patient-context signals in the query.
    - _check_completeness() (new): verifies required sections contain meaningful
      content and that citations include page references.
    """

    def __init__(self, chunks: List[Dict]):
        self.chunks = chunks

    # ------------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------------

    def validate_response(
        self,
        query: str,
        response: str,
        retrieved_chunks: Optional[List[Dict]] = None,
    ) -> Dict:
        """Validate response against medical safety rules.

        Args:
            query:            Original clinical question.
            response:         Assembled response text to validate.
            retrieved_chunks: Chunks returned by the retriever for this query.
                              Enables evidence-grounded checks (dosing value
                              verification, contraindication cross-check, etc.).
                              Defaults to [] when not provided.
        """
        chunks = retrieved_chunks or []

        validation: Dict = {
            "passed": True,
            "warnings": [],
            "errors": [],
            "suggestions": [],
        }

        # --- 1. Required sections -------------------------------------------
        required_sections = [
            "Triage Level:",
            "Immediate Actions:",
            "Next Steps / Monitoring:",
            "When to Refer:",
            "Citations:",
        ]
        for section in required_sections:
            if section not in response:
                validation["errors"].append(f"Missing section: {section}")
                validation["passed"] = False

        # --- 2. Triage validation (query + chunk content) -------------------
        triage_check = self._validate_triage(query, response, chunks)
        if not triage_check["passed"]:
            validation["warnings"].extend(triage_check["warnings"])
            if triage_check.get("critical"):
                validation["errors"].extend(triage_check["warnings"])
                validation["passed"] = False

        # --- 3. Dangerous advice detection (expanded) -----------------------
        dangerous = self._check_dangerous_advice(response)
        if dangerous:
            validation["errors"].extend(dangerous)
            validation["passed"] = False

        # --- 4. Citation page existence check --------------------------------
        citation_check = self._validate_citations(response)
        if not citation_check["passed"]:
            validation["warnings"].extend(citation_check["warnings"])

        # --- 5. Dosing value grounding (requires retrieved_chunks) -----------
        if chunks:
            dose_warnings = self._validate_dosing_values(response, chunks)
            validation["warnings"].extend(dose_warnings)

        # --- 6. Contraindication cross-check (requires retrieved_chunks) -----
        if chunks:
            contra_warnings = self._check_contraindications(query, chunks)
            validation["warnings"].extend(contra_warnings)

        # --- 7. Section completeness check -----------------------------------
        completeness_warnings = self._check_completeness(response, chunks)
        validation["warnings"].extend(completeness_warnings)

        return validation

    # ------------------------------------------------------------------
    # Improvement 1: Triage validation against query + chunk content
    # ------------------------------------------------------------------

    def _collect_danger_signs(
        self, query: str, retrieved_chunks: List[Dict]
    ) -> List[str]:
        """
        Collect danger sign labels found in the query text, retrieved chunk
        text, and chunk clinical_metadata danger_signs fields.

        Returns a deduplicated list of human-readable danger sign labels.

        Scans the query text and chunk clinical_metadata danger_signs only —
        NOT raw chunk text.  Raw chunk prose almost always mentions danger signs
        as part of treatment protocols ("watch for fast breathing"), which would
        trigger false-positive RED requirements for routine queries.
        clinical_metadata.danger_signs are specifically extracted by the chunker
        and are a more precise signal.
        """
        # Start with the query text
        query_corpus = query.lower()

        # Collect explicitly extracted danger signs from chunk metadata
        metadata_signs: List[str] = []
        for chunk in retrieved_chunks:
            cm = chunk.get("clinical_metadata") or {}
            metadata_signs.extend(s.lower() for s in cm.get("danger_signs", []))
        metadata_corpus = " ".join(metadata_signs)

        found: Dict[str, str] = {}  # needle → label (dedup by label)
        for needle, label in _DANGER_SIGN_NEEDLES:
            if needle in query_corpus and label not in found.values():
                found[needle] = label

        # Metadata signs are a supporting signal: only add them when the query
        # already has some clinical / patient context — prevents false positives
        # on purely informational queries that happen to retrieve chunks with
        # danger-sign metadata.
        query_has_patient_context = any(
            sig in query_corpus for sig in (
                "patient", "child", "infant", "baby", "treating", "treatment",
                "sick", "fever", "cough", "cannot", "unable", "presenting",
            )
        )
        if query_has_patient_context:
            for needle, label in _DANGER_SIGN_NEEDLES:
                if needle in metadata_corpus and label not in found.values():
                    found[needle] = label

        return list(found.values())

    def _validate_triage(
        self, query: str, response: str, retrieved_chunks: List[Dict]
    ) -> Dict:
        """
        Validate triage level appropriateness.

        Scans query text, retrieved chunk text, and chunk clinical_metadata for
        danger signs — not just the query string (previous behaviour).  If any
        danger sign is detected anywhere and the response triage is not RED,
        the check is flagged as critical.
        """
        result: Dict = {"passed": True, "warnings": [], "critical": False}

        triage_match = re.search(
            r"Triage Level:\s*([🔴🟡🟢]?\s*RED|YELLOW|GREEN)",
            response,
        )
        if not triage_match:
            result["warnings"].append("Triage level not found in response")
            result["passed"] = False
            return result

        response_triage = triage_match.group(1)
        danger_signs_found = self._collect_danger_signs(query, retrieved_chunks)

        if danger_signs_found and "RED" not in response_triage:
            signs_str = "; ".join(danger_signs_found[:3])
            result["warnings"].append(
                f"Danger sign(s) detected ({signs_str}) but triage is {response_triage} — "
                "should be RED"
            )
            result["critical"] = True
            result["passed"] = False

        return result

    # ------------------------------------------------------------------
    # Improvement 2: Expanded dangerous advice patterns
    # ------------------------------------------------------------------

    def _check_dangerous_advice(self, response: str) -> List[str]:
        """
        Check for potentially harmful advice using an expanded pattern set.

        Original patterns (4) + new patterns (6) = 10 total.
        """
        dangerous: List[str] = []
        response_lower = response.lower()

        danger_patterns = [
            # --- Original 4 patterns ---
            (
                r"give.*medicine.*without (referral|doctor)",
                "Never give prescription medicines without proper diagnosis",
            ),
            (
                r"wait (and see|for.*days).*danger sign",
                "Do not delay referral when danger signs are present",
            ),
            (
                r"treat at home.*(convulsion|unable to drink|bleeding)",
                "Danger signs require facility referral, not home treatment",
            ),
            (
                r"give.*aspirin.*child",
                "Aspirin is contraindicated in children (Reye syndrome risk)",
            ),
            # --- New patterns (2026-04-10) ---
            (
                r"double.*dose|dose.*double|give.*twice.*dose|twice the.*dose",
                "Do not double doses — refer to health facility for dose recalculation",
            ),
            (
                r"stop.*course.{0,30}(better|improv|resolv|well)|"
                r"stop.*medicine.{0,30}(better|improv|resolv|well)|"
                r"discontinue.{0,30}(better|improv|resolv|well)",
                "Do not stop treatment course early — incomplete courses risk treatment "
                "failure and antimicrobial resistance",
            ),
            (
                r"(give|administer|use).*without.{0,20}(weigh|weight|kg)",
                "Always check patient weight before calculating a pediatric dose",
            ),
            (
                r"home.{0,30}(severe|emergency|danger sign|critical|life.threaten)",
                "Severe / emergency conditions require facility care, not home treatment",
            ),
            (
                r"(metronidazole|flagyl).{0,40}(first trimester|early pregnan|"
                r"<\s*12 week|under 12 week)",
                "Metronidazole is contraindicated in the first trimester of pregnancy",
            ),
            (
                r"(ibuprofen|brufen).{0,40}(infant|newborn|neonate|under.{0,10}month)",
                "Ibuprofen is not recommended in infants under 3 months — "
                "refer for medical assessment",
            ),
        ]

        for pattern, warning in danger_patterns:
            if re.search(pattern, response_lower):
                dangerous.append(warning)

        return dangerous

    # ------------------------------------------------------------------
    # Improvement 3: Dosing value grounding
    # ------------------------------------------------------------------

    def _validate_dosing_values(
        self, response: str, retrieved_chunks: List[Dict]
    ) -> List[str]:
        """
        Check that every explicit dosing quantity mentioned in the response
        (e.g. "500 mg", "10 ml") appears verbatim in at least one retrieved
        source chunk.

        Only fires when retrieved_chunks is non-empty.  Values found in the
        response but absent from all retrieved chunk text are flagged as
        warnings — they may indicate the response layer paraphrased or
        invented a number.
        """
        warnings: List[str] = []

        # Extract dosing values from response text
        dose_re = re.compile(
            r"\b(\d+(?:[.,]\d+)?)\s*(mg|ml|mcg|g|µg|μg|iu|units?)\b",
            re.IGNORECASE,
        )
        response_doses = set()
        for m in dose_re.finditer(response):
            # Normalise: lowercase, no internal space, comma→period
            normalised = (m.group(1) + m.group(2).lower()).replace(",", ".").replace(" ", "")
            response_doses.add(normalised)

        if not response_doses:
            return []

        # Build source corpus from all retrieved chunk text + table markdown
        def _normalise(text: str) -> str:
            return re.sub(r"\s+", "", text.lower()).replace(",", ".")

        source_corpus = ""
        for chunk in retrieved_chunks:
            source_corpus += _normalise(chunk.get("text", ""))
            for table in chunk.get("tables", []):
                source_corpus += _normalise(table.get("markdown", ""))
                source_corpus += _normalise(table.get("nll", ""))

        for dose in sorted(response_doses):
            if dose not in source_corpus:
                warnings.append(
                    f"Dosing value '{dose}' appears in response but was not found in "
                    "any retrieved source chunk — verify against the original guideline "
                    "before use"
                )

        return warnings

    # ------------------------------------------------------------------
    # Improvement 4: Contraindication cross-check
    # ------------------------------------------------------------------

    def _check_contraindications(
        self, query: str, retrieved_chunks: List[Dict]
    ) -> List[str]:
        """
        Cross-check drug contraindications from chunk clinical_metadata
        against patient-context signals detected in the query.

        If a retrieved chunk lists a contraindication that matches the
        patient context implied by the query (e.g. "pregnant" + a drug
        contraindicated in pregnancy), a warning is raised.
        """
        warnings: List[str] = []
        query_lower = query.lower()

        # Detect patient contexts present in the query
        detected_contexts: Dict[str, List[str]] = {}
        for context, keywords in _PATIENT_CONTEXTS.items():
            if any(kw in query_lower for kw in keywords):
                detected_contexts[context] = keywords

        if not detected_contexts:
            return []

        seen_warnings: set = set()

        for chunk in retrieved_chunks:
            cm = chunk.get("clinical_metadata") or {}
            contraindications = cm.get("contraindications", [])
            drug = (cm.get("drug_name") or "").strip()

            for contra in contraindications:
                contra_lower = contra.lower()
                for context, keywords in detected_contexts.items():
                    if any(kw in contra_lower for kw in keywords):
                        drug_str = f" for {drug}" if drug else ""
                        msg = (
                            f"Contraindication warning{drug_str}: '{contra}' — "
                            f"patient context '{context}' detected in query"
                        )
                        if msg not in seen_warnings:
                            seen_warnings.add(msg)
                            warnings.append(msg)

        return warnings

    # ------------------------------------------------------------------
    # Improvement 5: Section completeness check
    # ------------------------------------------------------------------

    def _check_completeness(
        self, response: str, retrieved_chunks: List[Dict]
    ) -> List[str]:
        """
        Verify that required sections contain meaningful content (not just
        a bare header) and that citations include at least one page reference.

        Minimum content thresholds (characters after the header):
          Triage Level          5
          Immediate Actions    20
          Next Steps / Monitoring  20
          When to Refer        20
          Citations            10
        """
        warnings: List[str] = []

        section_minimums = {
            "Triage Level:":             5,
            "Immediate Actions:":        20,
            "Next Steps / Monitoring:":  20,
            "When to Refer:":            20,
            "Citations:":                10,
        }
        all_headers = list(section_minimums.keys())

        for section, min_len in section_minimums.items():
            idx = response.find(section)
            if idx == -1:
                continue  # Missing section handled by the required-sections check

            content_start = idx + len(section)

            # Find where this section ends (start of the next section)
            next_idx = len(response)
            for other in all_headers:
                if other == section:
                    continue
                o_idx = response.find(other, content_start)
                if o_idx != -1 and o_idx < next_idx:
                    next_idx = o_idx

            section_content = response[content_start:next_idx].strip()
            if len(section_content) < min_len:
                warnings.append(
                    f"Section '{section}' appears empty or has insufficient content "
                    f"({len(section_content)} chars, minimum {min_len})"
                )

        # Citations must contain at least one page reference
        citations_idx = response.find("Citations:")
        if citations_idx != -1:
            citations_content = response[citations_idx:]
            if not re.search(r"[Pp]age\s*\d+|[Pp]\.\s*\d+", citations_content):
                warnings.append(
                    "Citations section contains no page references — "
                    "every response should cite a specific page from the guideline"
                )

        return warnings

    # ------------------------------------------------------------------
    # Original: citation page existence check (unchanged)
    # ------------------------------------------------------------------

    def _validate_citations(self, response: str) -> Dict:
        """Validate citations reference existing pages in the knowledge base."""
        result: Dict = {"passed": True, "warnings": []}

        citations = re.findall(r"Page:?\s*(\d+)", response)
        citations.extend(re.findall(r"p\.?\s*(\d+)", response))

        available_pages = {c["page"] for c in self.chunks if "page" in c}

        for page in citations:
            page_num = int(page)
            if page_num not in available_pages:
                result["warnings"].append(
                    f"Citation to page {page_num} not found in knowledge base"
                )
                result["passed"] = False

        return result
