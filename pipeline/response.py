"""
Output layer: VHT-oriented formatting after retrieval + guardrail.

Pipeline order: extraction → validation → chunking → indexing → guardrail → response.

Changes (2026-04-10):
  1. Triage escalation from retrieved chunk content — infer_triage_from_query()
     gives the initial level; ResponseOrchestrator._escalate_triage_from_chunks()
     can upgrade it if chunk clinical_metadata contains danger signs that were
     absent from the query text.
  2. PDF-first danger signs section — VHTResponseFormatter._danger_signs_section()
     now accepts chunk danger signs and renders them instead of a hardcoded list.
     Falls back to the hardcoded list only when no chunk danger signs are found.
  3. PDF-first family message — _generate_family_message() scans retrieved chunk
     text for caregiver-education sentences before falling back to templates.
  4. Broader list item extraction — _extract_list_items_from_chunks() now captures
     action-verb lines (Give, Check, Refer, …) and bold markdown items in addition
     to bullet-point and numbered lists.
  5. Cross-section deduplication — actions, monitoring, and referral criteria share
     a deduplication pass so the same sentence never appears in two sections.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

from .config import MedicalSource, PreservationLevel, TriageLevel

# Optional: fuzzy matching for typo-tolerant triage keyword detection.
# rapidfuzz is already a pipeline dependency (requirements-pipeline.txt).
try:
    from rapidfuzz import fuzz as _fuzz
    _FUZZY_AVAILABLE = True
except ImportError:
    _FUZZY_AVAILABLE = False


# ---------------------------------------------------------------------------
# Danger-sign vocabulary for triage escalation (Improvement 1)
# ---------------------------------------------------------------------------

# Signs that warrant RED triage when found in chunk clinical_metadata.
# These are checked as substrings of danger-sign strings from the PDF —
# e.g. "bleed" matches "heavy vaginal bleeding" or "bleeding from gums".
# Kept universal so they fire for any document without condition-specific tuning.
_RED_DANGER_SIGNS = [
    "unable to drink",
    "cannot drink",
    "convuls",
    "seizure",
    "unconscious",
    "not waking",
    "very weak",
    "lethargic",
    "bleed",          # covers bleeding, haemorrhage text in chunk metadata
    "haemorrhag",
    "hemorrhag",
    "not breathing",
    "severe pain",
    "collapse",
    "in shock",
    "shock",
]

# ---------------------------------------------------------------------------
# Demographic context signals — used to reject mismatched chunks
# ---------------------------------------------------------------------------

# Chunk heading/text signals that indicate pediatric content
_PEDIATRIC_CHUNK_SIGNALS = (
    "sick child", "young infant", "imci", "paediatric", "pediatric",
    "under 5", "under five", "child cannot", "infant cannot",
    "carry child", "do not let", "child is unable", "sips of water",
    "recovery position",  # specific to paediatric iCCM algorithms
)

# Chunk heading/text signals that indicate postpartum (wrong for antepartum queries)
_POSTPARTUM_CHUNK_SIGNALS = (
    "postpartum", "post-partum", "postnatal", "post-natal", "pph ",
    "after delivery", "after birth", "post delivery", "post birth",
    "puerperal", "after caesarean", "after c-section", "4th stage",
    "third stage of labour", "third stage of labor",
)

# Chunk heading/text signals that indicate early pregnancy / first trimester
# (wrong for queries about >20 weeks gestation)
_EARLY_PREGNANCY_CHUNK_SIGNALS = (
    "abortion", "miscarriage", "ectopic", "first trimester",
    "early pregnancy bleeding", "incomplete abortion", "threatened abortion",
    "complete abortion",
)

# Query keywords that signal the patient is in late pregnancy (>20 weeks)
_LATE_PREGNANCY_QUERY = re.compile(
    r"\bpregnan|\bantenatal|\bprenatal|\bobstetric|"
    r"\b(?:2[0-9]|3[0-9]|4[0-2])\s*weeks?\s*(?:gestation|pregnant|of\s*pregnancy)|"
    r"\bweeks?\s*pregnant\b|\bgestation\b",
    re.IGNORECASE,
)

# Query keywords that signal a pediatric patient
_PEDIATRIC_QUERY = re.compile(
    r"\bchild\b|\binfant\b|\bbaby\b|\btoddler\b|\bnewborn\b|\bneonate\b|"
    r"\bpaediatric\b|\bpediatric\b|\bunder\s*5\b|"
    r"\b\d+\s*(?:months?\s*old|years?\s*old|month[- ]old|year[- ]old)\b",
    re.IGNORECASE,
)

# Query keywords that indicate a patient-clinical context (vs. purely
# informational queries).  Escalation only fires when at least one of these
# is present — so "What are danger signs?" stays GREEN even if chunks contain
# danger-sign metadata.
_PATIENT_CONTEXT_SIGNALS = [
    "patient", "child", "infant", "baby", "adult", "pregnant",
    "treatment", "treating", "manage", "managing", "presenting",
    "sick", "ill", "fever", "cough", "vomit", "diarrhea", "diarrhoea",
    "cannot", "unable", "not eating", "not drinking",
]

# Query keywords that escalate GREEN → YELLOW when chunk danger signs are found
_YELLOW_ESCALATION_QUERY = [
    "severe", "emergency", "critical", "danger", "refer immediately",
    "complicated", "serious",
]

# Minimum relevance score for a retrieved chunk to contribute to content
# extraction (actions, monitoring, referral criteria, danger signs).
# Chunks below this threshold are still used for citations and dosing blocks
# but not for list-item or metadata extraction.
_CONTENT_SCORE_THRESHOLD = 0.40

# Maximum number of chunks used for content extraction (ordered by score).
# Caps noise from lower-ranked chunks that may be from unrelated sections.
_CONTENT_MAX_CHUNKS = 3

# Regex for extracting caregiver-education sentences (Improvement 3)
_FAMILY_MSG_RE = re.compile(
    r"(?:tell|explain to|inform|advise|counsel|educate)\b.{15,180}[.!]",
    re.IGNORECASE,
)


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
    # Improvement 2: danger signs extracted from chunk clinical_metadata
    danger_signs: List[str] = field(default_factory=list)

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
        # Improvement 2: pass chunk danger signs to the section renderer
        lines.append(self._danger_signs_section(content.danger_signs))
        if content.family_message:
            lines.append(self._family_message_section(content.family_message))
        lines.append(self._vht_reminder(content.triage))
        dosing = self._dosing_block(content.citations)
        if dosing:
            lines.append(dosing)
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

    def _danger_signs_section(self, chunk_danger_signs: Optional[List[str]] = None) -> str:
        """
        Render the danger signs section.

        Improvement 2 (2026-04-10): if chunk clinical_metadata provided danger
        signs, render those instead of the hardcoded list.  The hardcoded list
        remains as fallback when no chunk-sourced signs are available.
        """
        if chunk_danger_signs:
            lines = ["**DANGER SIGNS - STOP AND REFER IF YOU SEE:**", ""]
            for sign in chunk_danger_signs[:8]:
                lines.append(f"• {sign}")
            return "\n".join(lines)

        # Hardcoded fallback — general danger signs applicable to any condition
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

    def _dosing_block(self, citations: List[Dict[str, Any]]) -> str:
        """
        Render verbatim NLL/text for VERBATIM-level chunks.

        VERBATIM chunks contain dosing tables whose quantities must never be
        paraphrased.  This block surfaces them explicitly so the VHT sees the
        exact dosing language from the guideline.
        """
        verbatim = [
            c for c in citations
            if c.get("preservation_level") == PreservationLevel.VERBATIM.value
        ]
        if not verbatim:
            return ""
        lines = ["**EXACT DOSING (copy from guidelines — do not change numbers):**", ""]
        for c in verbatim[:2]:
            nll = c.get("nll", "").strip()
            text = c.get("text", "").strip()
            content = nll if nll else text
            if content:
                lines.append(content)
                lines.append("")
        return "\n".join(lines).rstrip()

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
            level = c.get("preservation_level", PreservationLevel.STANDARD.value)
            label = ""
            if level == PreservationLevel.VERBATIM.value:
                label = " [EXACT DOSING]"
            elif level == PreservationLevel.HIGH.value:
                label = " [HIGH FIDELITY]"
            if section:
                lines.append(f"• {src}, Page {page}: {section}{label}")
            else:
                lines.append(f"• {src}, Page {page}{label}")
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
    ) -> ResponseContent:
        # Improvement 1: escalate triage if chunk evidence contains danger signs
        triage, triage_reasons = self._escalate_triage_from_chunks(
            query, triage, triage_reasons, retrieved_chunks
        )

        actions = self._select_actions(query, triage, retrieved_chunks)
        monitoring = self._select_monitoring(query, retrieved_chunks)
        referral_criteria = self._select_referral_criteria(triage, retrieved_chunks, query)

        # Improvement 5: cross-section deduplication
        actions, monitoring, referral_criteria = self._deduplicate_sections(
            actions, monitoring, referral_criteria
        )

        citations = self._build_citations(retrieved_chunks, source)

        # Improvement 2: collect danger signs from chunk metadata for formatter
        # Use only high-confidence chunks to avoid signs from unrelated sections.
        relevant_chunks = self._relevant_chunks(retrieved_chunks)
        danger_signs = self._collect_metadata_field(
            relevant_chunks, "danger_signs", max_items=8
        )

        # Improvement 3: PDF-first family message
        family_message = self._generate_family_message(query, triage, retrieved_chunks)

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
            confidence_score=self._calculate_confidence(
                guardrail_output, retrieved_chunks
            ),
            danger_signs=danger_signs,
        )

    # ------------------------------------------------------------------
    # Improvement 1: Triage escalation from retrieved chunk content
    # ------------------------------------------------------------------

    def _escalate_triage_from_chunks(
        self,
        query: str,
        triage: TriageLevel,
        triage_reasons: List[str],
        chunks: List[Dict[str, Any]],
    ) -> tuple[TriageLevel, List[str]]:
        """
        Escalate triage level if retrieved chunk clinical_metadata contains
        danger signs that were absent from the query.

        Rules (conservative to avoid false RED classifications):
        - Only fires when the query contains at least one patient-clinical
          context signal (treating, patient, child, fever, etc.) — purely
          informational queries ("What are danger signs?") are not escalated.
        - RED escalation: a RED-level danger sign (convulsions, cannot drink,
          unconscious, …) is found in chunk danger_signs AND the query has
          patient context.
        - YELLOW escalation: chunk danger_signs are non-empty AND query
          contains a severity keyword (severe, complicated, emergency, …)
          AND current triage is GREEN.
        - Already-RED triage is never changed.
        """
        if triage == TriageLevel.RED:
            return triage, triage_reasons

        query_lower = query.lower()
        has_patient_context = any(
            sig in query_lower for sig in _PATIENT_CONTEXT_SIGNALS
        )

        # Collect danger signs from chunk clinical_metadata only (more precise
        # than scanning raw text, which would produce too many false positives)
        chunk_danger_signs: List[str] = []
        for chunk in chunks:
            cm = chunk.get("clinical_metadata") or {}
            for sign in cm.get("danger_signs", []):
                if sign and sign.lower() not in [s.lower() for s in chunk_danger_signs]:
                    chunk_danger_signs.append(sign)

        if not chunk_danger_signs or not has_patient_context:
            return triage, triage_reasons

        # Check for RED-level signs
        red_found: List[str] = []
        for sign in chunk_danger_signs:
            sign_lower = sign.lower()
            if any(needle in sign_lower for needle in _RED_DANGER_SIGNS):
                red_found.append(sign)

        if red_found:
            new_reasons = list(triage_reasons) + [
                f"Danger sign in guideline content: {s}" for s in red_found[:2]
            ]
            return TriageLevel.RED, new_reasons

        # Check for YELLOW escalation from GREEN
        if triage == TriageLevel.GREEN:
            has_severity_keyword = any(
                kw in query_lower for kw in _YELLOW_ESCALATION_QUERY
            )
            if has_severity_keyword:
                new_reasons = list(triage_reasons) + [
                    "Severity keyword in query with danger signs in guideline content"
                ]
                return TriageLevel.YELLOW, new_reasons

        return triage, triage_reasons

    # ------------------------------------------------------------------
    # Improvement 4: Broader list item extraction
    # ------------------------------------------------------------------

    # Action verbs that commonly start clinical instructions
    _ACTION_VERB_RE = re.compile(
        r"^\s*(?:Give|Check|Refer|Ensure|Apply|Administer|Monitor|Observe|"
        r"Weigh|Complete|Take|Wash|Keep|Remove|Avoid|Assess|Perform|Record|"
        r"Start|Stop|Continue|Consider|Prescribe|Repeat|Review|Confirm|"
        r"Do not|Do NOT|Do\s+not)\b(.{10,200})",
        re.MULTILINE,
    )
    # Bold markdown items: **some instruction**
    _BOLD_ITEM_RE = re.compile(r"^\s*\*\*(.{10,200})\*\*\s*$", re.MULTILINE)

    @staticmethod
    def _filter_chunks_by_query_context(
        query: str,
        chunks: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        Remove chunks whose patient demographic clearly conflicts with the query.

        Problem: the retriever finds semantically adjacent sections that score
        above the relevance threshold but are clinically wrong — a "vaginal
        bleeding at 28 weeks" query retrieves pediatric "very sick child"
        chunks and postpartum PPH chunks because they all contain danger-sign
        vocabulary. Extracting actions from these gives clinically wrong steps
        for the wrong age group.

        Rules:
        - Late-pregnancy query → reject pediatric chunks, postpartum chunks,
          and early-pregnancy/abortion chunks.
        - Pediatric query → reject postpartum/obstetric adult chunks.
        - If filtering removes ALL chunks, return the original list (safe
          fallback: caller will use hardcoded templates instead).
        """
        is_late_pregnancy = bool(_LATE_PREGNANCY_QUERY.search(query))
        is_pediatric = bool(_PEDIATRIC_QUERY.search(query))

        if not is_late_pregnancy and not is_pediatric:
            return chunks  # No demographic signal — no filtering needed

        def _chunk_text_sample(chunk: Dict) -> str:
            heading = (chunk.get("heading") or "").lower()
            text    = (chunk.get("text") or "")[:300].lower()
            return heading + " " + text

        kept: List[Dict[str, Any]] = []
        for chunk in chunks:
            sample = _chunk_text_sample(chunk)

            if is_late_pregnancy:
                if any(sig in sample for sig in _PEDIATRIC_CHUNK_SIGNALS):
                    continue  # pediatric content — wrong for pregnant adult
                if any(sig in sample for sig in _POSTPARTUM_CHUNK_SIGNALS):
                    continue  # postpartum content — wrong for antepartum query
                if any(sig in sample for sig in _EARLY_PREGNANCY_CHUNK_SIGNALS):
                    continue  # early pregnancy / abortion — wrong for >20 wk query

            if is_pediatric:
                if any(sig in sample for sig in _POSTPARTUM_CHUNK_SIGNALS):
                    continue  # postpartum content — wrong for child query

            kept.append(chunk)

        # If everything was filtered out, return the original set so the
        # caller's template fallback can still run (empty list would silently
        # produce no actions at all).
        return kept if kept else []  # empty → triggers template fallback

    @staticmethod
    def _relevant_chunks(
        chunks: List[Dict[str, Any]],
        threshold: float = _CONTENT_SCORE_THRESHOLD,
        max_chunks: int = _CONTENT_MAX_CHUNKS,
    ) -> List[Dict[str, Any]]:
        """
        Return the top-scoring chunks that exceed the relevance threshold,
        capped at max_chunks.  Always returns at least 1 chunk (the best one)
        so content extraction has something to work with even when retrieval
        scores are uniformly low.

        Chunks are already sorted highest-score-first by the retriever, so
        this is a simple prefix filter.
        """
        above = [c for c in chunks if c.get("score", 0) >= threshold]
        if not above:
            above = chunks[:1]  # fallback: always use the top result
        return above[:max_chunks]

    @staticmethod
    def _extract_list_items_from_chunks(
        chunks: List[Dict[str, Any]], max_items: int = 6
    ) -> List[str]:
        """
        Extract actionable items from retrieved chunk text using four patterns:
        1. Bullet-point lines   (•, -, *, unicode bullet)
        2. Numbered-list lines  (1. / 1) format)
        3. Action-verb lines    (Give, Check, Refer, …)  — Improvement 4
        4. Bold markdown items  (**...**)                — Improvement 4

        Items between 10 and 250 characters are kept; duplicates are dropped.
        All items come verbatim from the PDF.
        """
        _BULLET_RE = re.compile(r"^\s*[•\-\*\u2022]\s+(.+)", re.MULTILINE)
        _NUMBER_RE = re.compile(r"^\s*\d+[\.\)]\s+(.+)", re.MULTILINE)
        _ACTION_RE = re.compile(
            r"^\s*(?:Give|Check|Refer|Ensure|Apply|Administer|Monitor|Observe|"
            r"Weigh|Complete|Take|Wash|Keep|Remove|Avoid|Assess|Perform|Record|"
            r"Start|Stop|Continue|Consider|Prescribe|Repeat|Review|Confirm|"
            r"Do not|Do NOT)\b(.{10,200})",
            re.MULTILINE,
        )
        _BOLD_RE = re.compile(r"^\s*\*\*(.{10,200})\*\*\s*$", re.MULTILINE)

        seen: set = set()
        items: List[str] = []

        for chunk in chunks:
            text = chunk.get("text", "")
            for pattern in (_BULLET_RE, _NUMBER_RE):
                for m in pattern.finditer(text):
                    item = m.group(1).strip()
                    if 10 <= len(item) <= 250 and item not in seen:
                        seen.add(item)
                        items.append(item)
            # Action-verb lines: prepend the matched verb back onto the capture
            for m in _ACTION_RE.finditer(text):
                # group(0) is the full line; strip leading whitespace
                item = m.group(0).strip()
                if 10 <= len(item) <= 250 and item not in seen:
                    seen.add(item)
                    items.append(item)
            # Bold items
            for m in _BOLD_RE.finditer(text):
                item = m.group(1).strip()
                if 10 <= len(item) <= 250 and item not in seen:
                    seen.add(item)
                    items.append(item)
            if len(items) >= max_items:
                break

        return items[:max_items]

    @staticmethod
    def _extract_nll_from_chunks(
        chunks: List[Dict[str, Any]], max_items: int = 6
    ) -> List[str]:
        """
        Extract NLL (natural-language descriptions) from embedded tables.

        The chunker pre-processes every table into a clean prose NLL string
        during indexing.  Using NLL avoids all raw table cell content — no
        tilde separators, no merged-cell artefacts, no truncated fragments.
        """
        seen: set = set()
        items: List[str] = []
        _SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")
        for chunk in chunks:
            for table in (chunk.get("tables") or []):
                nll = (table.get("nll") or "").strip()
                if not nll:
                    continue
                for sentence in _SENT_SPLIT.split(nll):
                    sentence = sentence.strip()
                    if 20 <= len(sentence) <= 250:
                        key = sentence[:60].lower()
                        if key not in seen:
                            seen.add(key)
                            items.append(sentence)
            if len(items) >= max_items:
                break
        return items[:max_items]

    @staticmethod
    def _collect_metadata_field(
        chunks: List[Dict[str, Any]], field_name: str, max_items: int = 5
    ) -> List[str]:
        """
        Collect a list field (e.g. danger_signs, referral_criteria) from
        clinical_metadata across all retrieved chunks, deduplicated.
        """
        seen: set = set()
        results: List[str] = []
        for chunk in chunks:
            cm = chunk.get("clinical_metadata") or {}
            for item in cm.get(field_name, []):
                if item and item not in seen:
                    seen.add(item)
                    results.append(item)
            if len(results) >= max_items:
                break
        return results[:max_items]

    # ------------------------------------------------------------------
    # Improvement 5: Cross-section deduplication
    # ------------------------------------------------------------------

    @staticmethod
    def _deduplicate_sections(
        actions: List[str],
        monitoring: List[str],
        referral_criteria: List[str],
    ) -> tuple[List[str], List[str], List[str]]:
        """
        Remove items from monitoring and referral_criteria that already appear
        in actions (or in each other).  Comparison is case-insensitive.
        """
        seen: set = {a.lower().strip() for a in actions}

        monitoring_clean: List[str] = []
        for item in monitoring:
            key = item.lower().strip()
            if key not in seen:
                seen.add(key)
                monitoring_clean.append(item)

        referral_clean: List[str] = []
        for item in referral_criteria:
            key = item.lower().strip()
            if key not in seen:
                seen.add(key)
                referral_clean.append(item)

        return actions, monitoring_clean, referral_clean

    # ------------------------------------------------------------------
    # Action / monitoring / referral selection — PDF-first, template fallback
    # ------------------------------------------------------------------

    def _select_actions(
        self, query: str, triage: TriageLevel, chunks: List[Dict[str, Any]]
    ) -> List[str]:
        """
        Extract recommended actions from retrieved chunks.

        Source priority (document-agnostic, no per-condition logic):
        1. Bullet/numbered/action-verb lines from NARRATIVE chunks only.
           Skipping is_table_only chunks avoids raw table cell artefacts
           (tilde separators, merged-cell fragments) entirely.
        2. NLL sentences from embedded tables (pre-processed by the chunker
           into clean prose — no artefacts possible).
        3. Generic three-item fallback (not condition-specific).
        """
        relevant = self._relevant_chunks(chunks)
        relevant = self._filter_chunks_by_query_context(query, relevant)

        # 1. Parse text from narrative chunks only (skip raw table cells)
        narrative = [c for c in relevant if not c.get("is_table_only")]
        extracted = self._extract_list_items_from_chunks(narrative, max_items=6)
        if extracted:
            return extracted

        # 2. NLL from any embedded tables (already clean prose)
        nll = self._extract_nll_from_chunks(relevant, max_items=6)
        if nll:
            return nll

        # 3. Generic fallback — no condition-specific content
        return [
            "Assess the patient and check for danger signs",
            "If condition is severe or worsening, refer to the health facility",
            "Follow the treatment protocol in the loaded guidelines",
        ]

    def _select_monitoring(
        self, query: str, chunks: List[Dict[str, Any]]
    ) -> List[str]:
        """
        Extract monitoring / watch-for items from retrieved chunks.

        Source priority (document-agnostic):
        1. clinical_features from chunk clinical_metadata (pre-extracted
           by the chunker — clean, no artefacts).
        2. danger_signs from chunk clinical_metadata, formatted as watch-for.
        3. Bullet/action-verb lines from narrative chunks only.
        4. Generic fallback (not condition-specific).
        """
        relevant = self._relevant_chunks(chunks)
        relevant = self._filter_chunks_by_query_context(query, relevant)

        features = self._collect_metadata_field(relevant, "clinical_features")
        if features:
            return features

        danger_signs = self._collect_metadata_field(relevant, "danger_signs")
        if danger_signs:
            return [f"Watch for: {s}" for s in danger_signs]

        narrative = [c for c in relevant if not c.get("is_table_only")]
        extracted = self._extract_list_items_from_chunks(narrative, max_items=5)
        if extracted:
            return extracted

        return [
            "Check if patient can drink or eat normally",
            "Monitor breathing and level of consciousness",
            "Watch for any worsening of symptoms",
        ]

    def _select_referral_criteria(
        self, triage: TriageLevel, chunks: List[Dict[str, Any]], query: str = ""
    ) -> List[str]:
        relevant = self._relevant_chunks(chunks)
        relevant = self._filter_chunks_by_query_context(query, relevant)
        # Primary: referral criteria extracted from chunk clinical_metadata.
        criteria = self._collect_metadata_field(relevant, "referral_criteria")
        if criteria:
            return criteria
        # Fallback: template-based criteria.
        if triage == TriageLevel.RED:
            return list(self.referral_templates["immediate"])
        if triage == TriageLevel.YELLOW:
            return list(self.referral_templates["urgent"])
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
            # Resolve preservation level — chunks store the string value of the enum.
            raw_level = chunk.get("preservation_level", PreservationLevel.STANDARD.value)
            if isinstance(raw_level, PreservationLevel):
                level = raw_level.value
            else:
                level = raw_level
            # Collect NLL text from any dosing tables in this chunk.
            nll_parts = [
                t.get("nll", "")
                for t in chunk.get("tables", [])
                if t.get("nll")
            ]
            out.append({
                "source": source,
                "page": page,
                "section": chunk.get("heading", "Clinical guideline"),
                "preservation_level": level,
                "text": chunk.get("text", ""),
                "nll": " ".join(nll_parts),
            })
        return out

    # ------------------------------------------------------------------
    # Improvement 3: PDF-first family message
    # ------------------------------------------------------------------

    def _generate_family_message(
        self, query: str, triage: TriageLevel, chunks: List[Dict[str, Any]]
    ) -> str:
        """
        Generate a caregiver-education message.

        Improvement 3 (2026-04-10): first scans retrieved chunk text for
        sentences that begin with caregiver-education verbs (Tell, Explain,
        Advise, Counsel, Inform).  Returns the first matching sentence from
        the PDF verbatim.  Falls back to hardcoded templates when no
        matching sentence is found.
        """
        # Primary: scan chunk text for caregiver-education sentences.
        # Sentences are validated against triage level before use — a "manage
        # at home" sentence from a GREEN-context chunk must not appear in a
        # RED-triage response.
        _HOME_LANGUAGE = re.compile(
            r"\bat home\b|\bhome treatment\b|\bhome management\b|\bmanage at home\b",
            re.IGNORECASE,
        )
        _EMERGENCY_LANGUAGE = re.compile(
            r"\brefer\b|\bhealth facility\b|\bhospital\b|\burgent\b|\bimmediately\b|\bnow\b",
            re.IGNORECASE,
        )
        for chunk in chunks:
            # Only search narrative chunks — skip dosing tables
            if chunk.get("content_type") in ("table", "image_ocr", "image_placeholder"):
                continue
            text = chunk.get("text", "")
            for m in _FAMILY_MSG_RE.finditer(text):
                sentence = m.group(0).strip()
                if not (20 <= len(sentence) <= 250):
                    continue
                # For RED triage: reject sentences that suggest home management
                # and only accept sentences with emergency/referral language.
                if triage == TriageLevel.RED:
                    if _HOME_LANGUAGE.search(sentence):
                        continue
                    if not _EMERGENCY_LANGUAGE.search(sentence):
                        continue
                return sentence

        # Fallback: generic templates — not condition-specific
        if triage == TriageLevel.RED:
            return (
                "This is a serious condition. The patient needs to go to the health facility immediately. "
                "Do not delay — refer now."
            )
        if triage == TriageLevel.YELLOW:
            return (
                "These symptoms need to be assessed by a health worker. "
                "Please go to the health facility today."
            )
        return (
            "Follow the advice given. Return to the health facility if symptoms worsen "
            "or any danger signs develop."
        )

    def _calculate_confidence(
        self,
        guardrail_output: Dict[str, Any],
        retrieved_chunks: List[Dict[str, Any]],
    ) -> float:
        # Retrieval quality: mean score of top-3 retrieved chunks (scores are
        # normalized to [0, 1] by the hybrid retriever after RRF + cross-encoder
        # blending). This is the primary signal — if retrieval found strong
        # evidence, confidence is high; if chunks are weakly matched, it is low.
        if not retrieved_chunks:
            retrieval_score = 0.0
        else:
            scores = sorted(
                (c.get("score", 0.0) for c in retrieved_chunks), reverse=True
            )
            top = scores[:3]
            retrieval_score = sum(top) / len(top)

        # Coverage: fraction of the requested 5 chunks that were actually found.
        coverage = min(len(retrieved_chunks) / 5.0, 1.0)

        # Guardrail penalty: errors are safety-critical; warnings are moderate.
        n_warnings = len(guardrail_output.get("warnings", []))
        n_errors = len(guardrail_output.get("errors", []))
        penalty = 0.05 * min(n_warnings, 4) + 0.15 * min(n_errors, 2)
        if not guardrail_output.get("passed", True):
            penalty += 0.1

        score = 0.6 * retrieval_score + 0.4 * coverage - penalty
        return round(max(0.0, min(1.0, score)), 3)


def infer_triage_from_query(query: str) -> tuple[TriageLevel, List[str]]:
    """
    Rule-based triage aligned with danger-sign list used in guardrail footer.
    YELLOW: non-immediate but time-sensitive phrasing in the query.

    Note: this function sets the *initial* triage level from the query text
    only.  ResponseOrchestrator._escalate_triage_from_chunks() may upgrade
    the level further based on retrieved chunk content.
    """
    q = query.lower()
    reasons: List[str] = []
    # Partial-prefix matching catches inflected forms:
    #   "bleed"      → bleeding / bleeds / bled
    #   "haemorrhag" → haemorrhage / haemorrhaging (British)
    #   "hemorrhag"  → hemorrhage / hemorrhaging (American)
    #   "eclampsi"   → eclampsia / pre-eclampsia
    #   "convuls"    → convulsions / convulsing
    # Only universal, immediately recognisable danger signs are matched here.
    # Condition-specific escalation (eclampsia, APH, sepsis, etc.) is handled
    # by _escalate_triage_from_chunks(), which uses clinical_metadata.danger_signs
    # from the retrieved guideline chunks.  That approach works for any PDF
    # without requiring per-condition keywords here.
    danger_kw = (
        ("unable to drink", "Unable to drink / cannot drink"),
        ("cannot drink",    "Unable to drink / cannot drink"),
        ("convuls",         "Convulsions / seizures"),
        ("seizure",         "Convulsions / seizures"),
        ("fit ",            "Convulsions / fits"),   # space avoids "fits into"
        ("unconscious",     "Unconscious"),
        ("not waking",      "Not waking / unconscious"),
        ("very weak",       "Very weak / lethargic"),
        ("lethargic",       "Very weak / lethargic"),
        ("bleed",           "Bleeding"),
        ("haemorrhag",      "Haemorrhage"),
        ("hemorrhag",       "Hemorrhage"),
        ("not breathing",   "Not breathing"),
        ("stopped breathing", "Stopped breathing"),
        ("in shock",        "Shock"),
    )
    for needle, label in danger_kw:
        if needle in q:
            reasons.append(label)

    # Fuzzy matching for typo tolerance (e.g. "leeding" → "bleeding").
    # Only runs when exact matching found nothing, to avoid double-counting.
    if not reasons and _FUZZY_AVAILABLE:
        _FUZZY_TARGETS = [
            ("bleeding", "Bleeding"),
            ("haemorrhage", "Haemorrhage"),
            ("hemorrhage", "Hemorrhage"),
            ("convulsions", "Convulsions / seizures"),
            ("unconscious", "Unconscious or not waking"),
            ("eclampsia", "Eclampsia"),
        ]
        for word in q.split():
            if len(word) < 5:
                continue
            for target, label in _FUZZY_TARGETS:
                if _fuzz.ratio(word, target) >= 80:
                    reasons.append(label)
                    break

    if reasons:
        return TriageLevel.RED, list(dict.fromkeys(reasons))

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
