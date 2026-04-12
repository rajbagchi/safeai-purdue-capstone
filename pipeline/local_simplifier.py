"""
Local GGUF simplifier (e.g. Qwen2.5-3B-Instruct) via llama-cpp-python.

Rewrites the rule-based VHT draft using only the approved structured answer and
retrieved excerpts. Output is re-validated with MedicalGuardrailBrain before use.
"""

from __future__ import annotations

import os
import threading
from typing import Any, Dict, List, Optional

from .config import MedicalSource, TriageLevel

_LOCK = threading.Lock()
_LLAMA = None
_LLAMA_PATH: Optional[str] = None


def local_llm_enabled(explicit: Optional[bool] = None) -> bool:
    """
    ``explicit`` overrides env: ``False`` off; ``True`` on only if GGUF path exists;
    ``None`` uses ``SAFEAI_USE_LOCAL_LLM`` plus path.
    """
    path = (os.environ.get("SAFEAI_LLM_GGUF") or "").strip()
    if not path or not os.path.isfile(path):
        return False if explicit is not True else False
    if explicit is False:
        return False
    if explicit is True:
        return True
    v = os.environ.get("SAFEAI_USE_LOCAL_LLM", "").strip().lower()
    return v in ("1", "true", "yes", "on")


def _evidence_block(chunks: List[Dict[str, Any]], max_chars: int = 1200) -> str:
    parts: List[str] = []
    for i, ch in enumerate(chunks, 1):
        h = str(ch.get("heading", "")).strip()
        p = ch.get("page", "?")
        t = (ch.get("text") or "")[:max_chars]
        parts.append(f"[{i}] Page {p} | {h}\n{t}")
    return "\n\n".join(parts)


def structured_answer_for_prompt(
    *,
    query: str,
    document_title: str,
    triage: TriageLevel,
    triage_reasons: List[str],
    actions: List[str],
    monitoring: List[str],
    referral_criteria: List[str],
    citations: List[Dict[str, Any]],
    family_message: Optional[str],
) -> str:
    """Deterministic text the model must not contradict (facts + triage intent)."""
    tri = triage.name if hasattr(triage, "name") else str(triage)
    lines = [
        f"Question: {query}",
        f"Guideline title: {document_title}",
        f"Triage (approved): {tri}",
        f"Triage reasons: {', '.join(triage_reasons) if triage_reasons else 'n/a'}",
        "",
        "Approved actions:",
        *[f"- {a}" for a in actions],
        "",
        "Monitoring:",
        *[f"- {m}" for m in monitoring],
        "",
        "Referral criteria:",
        *[f"- {r}" for r in referral_criteria],
        "",
        "Citations (from retrieval):",
    ]
    for c in citations[:8]:
        src = c.get("source", "")
        if isinstance(src, MedicalSource):
            src = src.value
        lines.append(f"- {src} Page {c.get('page', '?')}: {c.get('section', '')}")
    if family_message:
        lines.extend(["", "Family-facing line (approved):", family_message])
    return "\n".join(lines)


SYSTEM_PROMPT = """You rewrite medically approved material for Village Health Team (VHT) workers with low literacy.

Hard rules:
- Do NOT add new medical facts, drugs, doses, or diagnoses.
- Do NOT change the triage level meaning: keep the same RED, YELLOW, or GREEN as in the approved answer.
- Use only the approved structured answer and the evidence excerpts for factual grounding.
- Short, simple sentences. Prefer bullet lines. Do not use emoji.
- If danger signs apply (per approved triage), put urgent referral language first.

You MUST output plain markdown using exactly these section headings in this order (each heading on its own line, then content):
Triage Level:
Immediate Actions:
Next Steps / Monitoring:
When to Refer:
Citations:

Under "Triage Level:" write the level (RED, YELLOW, or GREEN) and a one-line plain reason matching the approved triage.
Under "Citations:" list relevant pages/sections from the evidence (e.g. Page 96)."""


def _load_llama(model_path: str):
    global _LLAMA, _LLAMA_PATH

    from llama_cpp import Llama  # type: ignore[import-not-found]

    with _LOCK:
        if _LLAMA is not None and _LLAMA_PATH == model_path:
            return _LLAMA
        n_ctx = int(os.environ.get("SAFEAI_LLM_N_CTX", "4096"))
        n_threads = int(os.environ.get("SAFEAI_LLM_N_THREADS", str(max(1, (os.cpu_count() or 4) // 2))))
        n_gpu = int(os.environ.get("SAFEAI_LLM_N_GPU_LAYERS", "0"))
        _LLAMA = Llama(
            model_path=model_path,
            n_ctx=n_ctx,
            n_threads=n_threads,
            n_gpu_layers=n_gpu,
            verbose=os.environ.get("SAFEAI_LLM_VERBOSE", "").strip().lower() in ("1", "true", "yes"),
        )
        _LLAMA_PATH = model_path
        return _LLAMA


def structured_answer_from_content(
    structured: Any,
    *,
    query: str,
    document_title: str,
) -> str:
    """Build the approved structured packet from ``ResponseContent``."""
    return structured_answer_for_prompt(
        query=query,
        document_title=document_title,
        triage=structured.triage,
        triage_reasons=structured.triage_reasons,
        actions=structured.actions,
        monitoring=structured.monitoring,
        referral_criteria=structured.referral_criteria,
        citations=structured.citations,
        family_message=structured.family_message,
    )


class LocalSimplifierLLM:
    """
    Controlled rewriting layer: readability only, not a second clinical brain.
    """

    def __init__(self, model_path: Optional[str] = None) -> None:
        self.model_path = (model_path or os.environ.get("SAFEAI_LLM_GGUF") or "").strip()

    @property
    def available(self) -> bool:
        return bool(self.model_path) and os.path.isfile(self.model_path)

    def simplify_vht_markdown(
        self,
        *,
        query: str,
        document_title: str,
        rule_based_vht: str,
        structured_answer: str,
        evidence_chunks: List[Dict[str, Any]],
    ) -> Optional[str]:
        """
        Returns rewritten markdown including required guardrail sections, or None.
        """
        if not self.available:
            return None
        user = (
            f"{structured_answer}\n\n"
            "---\nRule-based draft (tone reference; do not contradict approved facts above):\n"
            f"{rule_based_vht[:6000]}\n\n"
            "---\nEvidence excerpts:\n"
            f"{_evidence_block(evidence_chunks)}\n\n"
            "Rewrite for VHT readers following the system rules. Output markdown only."
        )
        max_tokens = int(os.environ.get("SAFEAI_LLM_MAX_TOKENS", "2048"))
        temperature = float(os.environ.get("SAFEAI_LLM_TEMPERATURE", "0.15"))

        try:
            llm = _load_llama(self.model_path)
            with _LOCK:
                out = llm.create_chat_completion(
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": f"User question:\n{query}\n\n{user}"},
                    ],
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
            text = out["choices"][0]["message"]["content"]
        except Exception:
            return None

        text = (text or "").strip()
        if not text:
            return None
        return text
