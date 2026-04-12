"""
Output layer: VHT-oriented formatting after retrieval + guardrail.

Pipeline order: extraction → validation → chunking → indexing → guardrail → response.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

from .config import MedicalSource, TriageLevel
from .retrieval import infer_query_intent


class ResponseFormat(Enum):
    """Output format types."""

    VHT_QUICK = "vht_quick"
    VHT_STANDARD = "vht_standard"
    CLINICIAN = "clinician"
    REFERRAL = "referral"


@dataclass
class ResponseContent:
    """Structured response (output of the response layer)."""

    query: str
    triage: TriageLevel
    triage_reasons: List[str]
    actions: List[str]
    monitoring: List[str]
    referral_criteria: List[str]
    citations: List[Dict[str, Any]]
    medication_dosage: Optional[Dict[str, Any]] = None
    family_message: Optional[str] = None
    validation_warnings: List[str] = field(default_factory=list)
    confidence_score: float = 1.0

    def to_vht_format(self) -> str:
        return VHTResponseFormatter().format(self, ResponseFormat.VHT_STANDARD)


class VHTResponseFormatter:
    """Formats responses for Village Health Teams."""

    TRANSLATIONS = {
        "lethargic": "very weak",
        "unable to drink": "cannot drink",
        "convulsions": "shaking/fitting",
        "dehydration": "dry mouth, no tears",
        "dyspnea": "difficulty breathing",
        "malaria": "fever with chills",
    }

    def format(self, content: ResponseContent, fmt: ResponseFormat) -> str:
        if fmt == ResponseFormat.VHT_QUICK:
            return self._format_quick(content)
        if fmt == ResponseFormat.REFERRAL:
            return self._format_referral_note(content)
        return self._format_standard(content)

    def _format_standard(self, content: ResponseContent) -> str:
        lines: List[str] = []
        if content.triage == TriageLevel.RED:
            lines.append(self._emergency_header())
        lines.append(self._quick_summary(content))
        act = self._actions_section(content)
        if act:
            lines.append(act)
        if content.monitoring:
            lines.append(self._monitoring_section(content))
        lines.append(self._danger_signs_section())
        if content.family_message:
            lines.append(self._family_message_section(content.family_message))
        lines.append(self._vht_reminder(content.triage))
        lines.append(self._citations_section(content.citations))
        if content.validation_warnings:
            lines.append(self._warnings_section(content.validation_warnings))
        return "\n\n".join(lines)

    def _emergency_header(self) -> str:
        return (
            "╔══════════════════════════════════════════════════════════╗\n"
            "║  EMERGENCY! ACT NOW - DO NOT DELAY                       ║\n"
            "║  This patient needs to go to health facility IMMEDIATELY ║\n"
            "╚══════════════════════════════════════════════════════════╝"
        )

    def _quick_summary(self, content: ResponseContent) -> str:
        triage_symbol = {
            TriageLevel.RED: "RED (Immediate Referral Required)",
            TriageLevel.YELLOW: "YELLOW (Urgent Referral - Assess Today)",
            TriageLevel.GREEN: "GREEN (Manage at Community Level)",
        }.get(content.triage, "Unknown")
        reasons = ", ".join(content.triage_reasons[:2]) if content.triage_reasons else "See guidelines"
        return (
            f"**QUICK SUMMARY: {triage_symbol}**\n\n"
            f"• What I see: {reasons}\n"
            f"• What to do: {self._get_instruction_for_triage(content.triage)}\n"
            "• What NOT to do: Do NOT give medicine at home for danger signs"
        )

    def _actions_section(self, content: ResponseContent) -> str:
        if not content.actions:
            return ""
        lines = ["**WHAT TO DO (step by step):**", ""]
        for i, action in enumerate(content.actions[:5], 1):
            lines.append(f"**Step {i}:** {action}")
        return "\n".join(lines)

    def _monitoring_section(self, content: ResponseContent) -> str:
        lines = ["**MONITORING:**", ""]
        for item in content.monitoring[:6]:
            lines.append(f"• {item}")
        return "\n".join(lines)

    def _danger_signs_section(self) -> str:
        return (
            "**DANGER SIGNS - STOP AND REFER IF YOU SEE:**\n\n"
            "• Cannot drink or breastfeed\n"
            "• Very weak, cannot sit up or wake up\n"
            "• Shaking/fitting (convulsions)\n"
            "• Vomiting everything\n"
            "• Difficulty breathing\n"
            "• Pale or yellow skin/eyes\n"
            "• Bleeding from any place"
        )

    def _family_message_section(self, message: str) -> str:
        return f"**WHAT TO TELL THE FAMILY:**\n\n{message}"

    def _vht_reminder(self, triage: TriageLevel) -> str:
        if triage == TriageLevel.RED:
            return (
                "**REMEMBER AS A VHT:**\n\n"
                "• You are not expected to treat this at home\n"
                "• Your job is to identify danger and refer quickly\n"
                "• Do not give any medicine without health worker instruction\n"
                "• Saving time saves lives – do not delay"
            )
        return (
            "**REMEMBER AS A VHT:**\n\n"
            "• Always check for danger signs first\n"
            "• If you are unsure, it is better to refer\n"
            "• Record all patients you see\n"
            "• Keep your VHT kit and referral forms ready"
        )

    def _citations_section(self, citations: List[Dict[str, Any]]) -> str:
        if not citations:
            return "**FROM THE GUIDELINES:**\n\n• Refer to national / MoH handbook"
        lines = ["**FROM THE GUIDELINES:**", ""]
        for c in citations[:3]:
            src = c.get("source", "Guidelines")
            if isinstance(src, MedicalSource):
                src = src.value
            page = c.get("page", "?")
            section = c.get("section", "")
            if section:
                lines.append(f"• {src}, Page {page}: {section}")
            else:
                lines.append(f"• {src}, Page {page}")
        return "\n".join(lines)

    def _warnings_section(self, warnings: List[str]) -> str:
        lines = ["---", "**GUARDRAIL WARNINGS:**", ""]
        for w in warnings[:3]:
            lines.append(f"• {w}")
        return "\n".join(lines)

    def _format_referral_note(self, content: ResponseContent) -> str:
        lines = [
            "**VHT REFERRAL NOTE**",
            "",
            f"**Triage:** {content.triage.value}",
            f"**Reason:** {', '.join(content.triage_reasons)}",
            "",
        ]
        if content.actions:
            lines.append("**Actions taken:**")
            for a in content.actions[:3]:
                lines.append(f"• {a}")
            lines.append("")
        lines.extend(
            [
                "**Referral completed:** [ ]",
                "**Health worker received:** [ ]",
                "",
                "---",
                "_This is a VHT referral. Please assess patient promptly._",
            ]
        )
        return "\n".join(lines)

    def _format_quick(self, content: ResponseContent) -> str:
        triage_symbol = {
            TriageLevel.RED: "REFER NOW",
            TriageLevel.YELLOW: "REFER TODAY",
            TriageLevel.GREEN: "MANAGE AT HOME",
        }.get(content.triage, "?")
        reasons = ", ".join(content.triage_reasons[:2]) if content.triage_reasons else ""
        return (
            f"{triage_symbol}\n"
            f"Reason: {reasons}\n"
            f"Action: {self._get_instruction_for_triage(content.triage)}"
        )

    def _get_instruction_for_triage(self, triage: TriageLevel) -> str:
        if triage == TriageLevel.RED:
            return "Go to health facility NOW"
        if triage == TriageLevel.YELLOW:
            return "Go to health facility today"
        return "Follow advice below, monitor for changes"


class ResponseOrchestrator:
    """
    Builds ResponseContent from retrieval chunks + guardrail output + triage inference.
    """

    def __init__(self, default_format: ResponseFormat = ResponseFormat.VHT_STANDARD):
        self.default_format = default_format
        self.formatter = VHTResponseFormatter()
        self.action_templates: Dict[str, List[str]] = {
            "cannot_drink": [
                "Check if child can swallow: gently try small sips of water",
                "If cannot swallow, do NOT force – spitting out means cannot drink",
                "Keep child lying on side (recovery position)",
                "Keep warm, not hot",
                "Do NOT give food or medicine",
                "Arrange transport NOW – carry child, do not let them walk",
            ],
            "convulsions": [
                "Place child on soft surface (mat, blanket)",
                "Remove dangerous objects nearby",
                "Loosen tight clothing",
                "DO NOT: put anything in mouth, hold child down, or give water",
                "After shaking stops: place on side, check breathing",
                "Go to health facility IMMEDIATELY",
            ],
            "fever": [
                "Check temperature – feel child's body, hot to touch?",
                "Remove extra clothing",
                "Wipe with cool (not cold) cloth",
                "Offer frequent small drinks if able to swallow",
                "Continue breastfeeding if baby",
                "Monitor for danger signs every 2-4 hours",
            ],
            "rash": [
                "Keep skin clean and dry",
                "Do NOT scratch or apply any ointment",
                "Do NOT give any medicine at home",
                "Monitor for fever or spread of rash",
                "Refer to health facility for assessment",
            ],
        }
        self.monitoring_templates: Dict[str, List[str]] = {
            "generic": [
                "Check if patient can drink normally",
                "Watch for convulsions or shaking",
                "Monitor breathing – is it fast or difficult?",
                "Check if patient is awake and alert",
                "Look for pale or yellow skin/eyes",
            ],
            "fever": [
                "Check temperature every 4 hours",
                "Watch for danger signs (cannot drink, convulsions, lethargy)",
                "If fever >3 days → refer immediately",
            ],
        }
        self.referral_templates: Dict[str, List[str]] = {
            "immediate": [
                "Cannot drink or breastfeed",
                "Convulsions/shaking",
                "Unconscious or cannot wake",
                "Vomiting everything",
                "Difficulty breathing",
            ],
            "urgent": [
                "Fever >3 days",
                "Cough >3 weeks",
                "Painful rash",
                "Fatigue with night sweats (elderly)",
            ],
        }

    def create(
        self,
        *,
        query: str,
        triage: TriageLevel,
        triage_reasons: List[str],
        guardrail_output: Dict[str, Any],
        retrieved_chunks: List[Dict[str, Any]],
        source: MedicalSource,
        dosage_info: Optional[Dict[str, Any]] = None,
        query_intent: Optional[str] = None,
    ) -> ResponseContent:
        intent = query_intent if query_intent is not None else infer_query_intent(query)
        actions = self._select_actions(query, triage, intent)
        monitoring = self._select_monitoring(query)
        referral_criteria = self._select_referral_criteria(triage, intent)
        citations = self._build_citations(retrieved_chunks, source)
        family_message = self._generate_family_message(query, triage, intent)
        warnings = list(guardrail_output.get("warnings", []))
        return ResponseContent(
            query=query,
            triage=triage,
            triage_reasons=triage_reasons,
            actions=actions,
            monitoring=monitoring,
            referral_criteria=referral_criteria,
            citations=citations,
            medication_dosage=dosage_info,
            family_message=family_message,
            validation_warnings=warnings,
            confidence_score=self._calculate_confidence(triage, guardrail_output, intent),
        )

    def _select_actions(self, query: str, triage: TriageLevel, intent: str) -> List[str]:
        q = query.lower()
        if triage == TriageLevel.RED:
            if "cannot drink" in q or "unable to drink" in q:
                return list(self.action_templates["cannot_drink"])
            if "convulsion" in q or "seizure" in q:
                return list(self.action_templates["convulsions"])
            return list(self.action_templates["cannot_drink"])
        if intent == "referral_hospital":
            return [
                "Use your national/WHO severe-malaria or referral chart: who must go to hospital now",
                "Check every danger sign (cannot drink, convulsions, very weak, difficult breathing, confusion)",
                "If severe malaria is possible or any danger sign → arrange urgent transport to hospital",
                "If the guideline excerpts are unclear, ask a clinician or supervisor - when unsure, refer",
            ]
        if "fever" in q:
            return list(self.action_templates["fever"])
        if "rash" in q:
            return list(self.action_templates["rash"])
        if "dose" in q or "dosage" in q:
            return [
                "Confirm patient weight before calculating dose",
                "Explain dosing schedule to caregiver",
                "Observe first dose if possible",
                "Complete full course even if symptoms improve",
            ]
        return [
            "Assess patient carefully",
            "Check for danger signs (see below)",
            "If unsure, refer to health facility",
            "Record all findings",
        ]

    def _select_monitoring(self, query: str) -> List[str]:
        if "fever" in query.lower():
            return list(self.monitoring_templates["fever"])
        return list(self.monitoring_templates["generic"])

    def _select_referral_criteria(self, triage: TriageLevel, intent: str) -> List[str]:
        if triage == TriageLevel.RED:
            return list(self.referral_templates["immediate"])
        if triage == TriageLevel.YELLOW:
            base = list(self.referral_templates["urgent"])
            if intent == "referral_hospital":
                base = [
                    "Hospital referral when national chart says severe disease or danger signs",
                    "Any danger sign → refer urgently (do not wait)",
                    "Severe or complicated malaria per local definition → hospital care",
                ] + base
            return base
        if intent == "referral_hospital":
            return [
                "Refer urgently if any danger sign appears while you read this",
                "Refer if national guidelines say this patient needs injectable care or monitoring",
                "If you are unsure, err on the side of referral",
            ]
        return [
            "If symptoms worsen",
            "If new danger signs appear",
            "If you are unsure about the condition",
        ]

    def _build_citations(
        self,
        chunks: List[Dict[str, Any]],
        source: MedicalSource,
    ) -> List[Dict[str, Any]]:
        out: List[Dict[str, Any]] = []
        for chunk in chunks[:5]:
            page = chunk.get("page")
            if page is None:
                continue
            out.append({
                "source": source,
                "page": page,
                "section": chunk.get("heading", "Clinical guideline"),
            })
        return out

    def _generate_family_message(self, query: str, triage: TriageLevel, intent: str) -> str:
        q = query.lower()
        if triage == TriageLevel.RED:
            if "cannot drink" in q or "unable to drink" in q:
                return (
                    "Your child is very sick because they cannot drink. This is a danger sign. "
                    "The child needs to be seen by a health worker TODAY. Do not give any medicine at home. "
                    "We need to go to the health facility now."
                )
            if "convulsion" in q or "seizure" in q:
                return (
                    "Your child had a fit/shaking. This is a serious sign. The child needs help from a health worker. "
                    "We must go to the health facility now."
                )
            return (
                "This is a serious condition. The patient needs to go to the health facility immediately. "
                "Do not delay."
            )
        if triage == TriageLevel.YELLOW:
            if intent == "referral_hospital":
                return (
                    "You asked when to go to the hospital. Use danger signs and the national chart: "
                    "if there is any severe sign or you are not sure, go to the health facility today."
                )
            return (
                "The symptoms need to be checked by a health worker. Please go to the health facility today."
            )
        if intent == "dosing":
            return (
                "Medicine amounts depend on weight and age. Use the national dosing chart or a health worker; "
                "the short excerpts here may not show every dose."
            )
        if intent == "referral_hospital":
            return (
                "This question is about hospital care. Follow danger signs and national referral rules; "
                "if anything worries you, go to the health facility."
            )
        return (
            "The symptoms can be managed at home with guidance. Follow the advice you were given. "
            "Come back if symptoms get worse."
        )

    def _calculate_confidence(
        self,
        triage: TriageLevel,
        guardrail_output: Dict[str, Any],
        intent: str,
    ) -> float:
        base = 0.95 if triage == TriageLevel.RED else 0.9
        if intent in ("referral_hospital", "dosing"):
            base -= 0.03
        if guardrail_output.get("warnings"):
            base -= 0.05 * min(len(guardrail_output["warnings"]), 3)
        if not guardrail_output.get("passed", True):
            base -= 0.1
        return max(0.6, min(1.0, base))


def infer_triage_from_query(query: str) -> tuple[TriageLevel, List[str]]:
    """
    Rule-based triage aligned with danger-sign list used in guardrail footer.
    YELLOW: non-immediate but time-sensitive phrasing in the query, or explicit
    hospital-referral questions (so VHT text is not framed as routine home care).
    """
    q = query.lower()
    reasons: List[str] = []
    danger_kw = (
        ("unable to drink", "Unable to drink / cannot drink"),
        ("cannot drink", "Unable to drink / cannot drink"),
        ("convuls", "Convulsions / seizures"),
        ("seizure", "Convulsions / seizures"),
        ("unconscious", "Unconscious or not waking"),
        ("very weak", "Very weak"),
        ("lethargic", "Very weak / lethargic"),
        ("bleeding", "Bleeding"),
    )
    for needle, label in danger_kw:
        if needle in q:
            reasons.append(label)
    if reasons:
        return TriageLevel.RED, list(dict.fromkeys(reasons))

    if infer_query_intent(query) == "referral_hospital":
        return TriageLevel.YELLOW, [
            "Question asks about hospital referral - use national criteria and danger signs"
        ]

    yellow_triggers = (
        ("fever" in q and ("3 day" in q or ">3" in q or "more than 3" in q)),
        ("cough" in q and ("3 week" in q or ">3" in q)),
        ("urgent" in q and "refer" in q),
        ("assess today" in q),
        ("same day" in q and "refer" in q),
    )
    if any(yellow_triggers):
        return TriageLevel.YELLOW, ["Time-sensitive symptoms — assess at facility today"]

    return TriageLevel.GREEN, ["Routine evidence retrieval from national guidelines"]
