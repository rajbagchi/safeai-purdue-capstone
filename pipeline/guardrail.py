"""
Medical guardrail brain: validates Q&A responses against safety rules.
"""

import re
from typing import Dict, List


class MedicalGuardrailBrain:
    """
    Second brain for medical safety validation.
    """

    def __init__(self, chunks: List[Dict]):
        self.chunks = chunks

    def validate_response(self, query: str, response: str) -> Dict:
        """Validate response against medical safety rules."""
        validation: Dict = {
            "passed": True,
            "warnings": [],
            "errors": [],
            "suggestions": [],
        }

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

        triage_check = self._validate_triage(query, response)
        if not triage_check["passed"]:
            validation["warnings"].extend(triage_check["warnings"])
            if triage_check.get("critical"):
                validation["errors"].extend(triage_check["warnings"])
                validation["passed"] = False

        dangerous = self._check_dangerous_advice(response)
        if dangerous:
            validation["errors"].extend(dangerous)
            validation["passed"] = False

        citation_check = self._validate_citations(response)
        if not citation_check["passed"]:
            validation["warnings"].extend(citation_check["warnings"])

        return validation

    def _validate_triage(self, query: str, response: str) -> Dict:
        """Validate triage level appropriateness."""
        result: Dict = {"passed": True, "warnings": [], "critical": False}

        triage_match = re.search(
            r"Triage Level:\s*([🔴🟡🟢]?\s*RED|YELLOW|GREEN)",
            response,
        )
        if not triage_match:
            result["warnings"].append("Triage level not found")
            result["passed"] = False
            return result

        response_triage = triage_match.group(1)
        query_lower = query.lower()

        danger_signs = [
            "unable to drink",
            "cannot drink",
            "convuls",
            "seizure",
            "unconscious",
            "very weak",
            "lethargic",
            "bleeding",
        ]

        for sign in danger_signs:
            if sign in query_lower:
                if "RED" not in response_triage:
                    result["warnings"].append(
                        f"Danger sign '{sign}' present but triage is {response_triage}"
                    )
                    result["critical"] = True
                    result["passed"] = False
                break

        return result

    def _check_dangerous_advice(self, response: str) -> List[str]:
        """Check for potentially harmful advice."""
        dangerous: List[str] = []
        response_lower = response.lower()

        danger_patterns = [
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
                "Aspirin contraindicated in children",
            ),
        ]

        for pattern, warning in danger_patterns:
            if re.search(pattern, response_lower):
                dangerous.append(warning)

        return dangerous

    def _validate_citations(self, response: str) -> Dict:
        """Validate citations reference existing pages."""
        result: Dict = {"passed": True, "warnings": []}

        citations = re.findall(r"Page:?\s*(\d+)", response)
        citations.extend(re.findall(r"p\.?\s*(\d+)", response))

        available_pages = {
            c["page"] for c in self.chunks if "page" in c
        }

        for page in citations:
            page_num = int(page)
            if page_num not in available_pages:
                result["warnings"].append(
                    f"Citation to page {page_num} not found in knowledge base"
                )
                result["passed"] = False

        return result
