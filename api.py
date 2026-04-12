"""
FastAPI wrapper around MedicalQASystem.

Run from repo root:
  pip install -r requirements-api.txt
  uvicorn api:app --host 0.0.0.0 --port 8000

Endpoints:
  GET  /health     — liveness + initialization flag
  GET  /metadata   — loaded preset, paths, chunk count
  POST /initialize — build or load KB from preset (+ optional paths)
  POST /ask        — run query (simple or full VHT layer)

Local VHT simplifier (optional, see requirements-local-llm.txt):
  SAFEAI_USE_LOCAL_LLM=1
  SAFEAI_LLM_GGUF=path/to/model.gguf
  POST /ask body: "use_local_llm": true (or omit and rely on env)
"""

from __future__ import annotations

import os
import sys
from dataclasses import asdict
from typing import Any, Dict, List, Optional


# Repo root on path for `pipeline` imports when uvicorn loads api:app
_ROOT = os.path.abspath(os.path.dirname(__file__))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from pipeline.compat import fix_stdio_encoding

fix_stdio_encoding()

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from pipeline.config import (
    ExtractionConfig,
    extraction_config_uganda_clinical_2023,
    extraction_config_who_malaria_nih,
)
from pipeline.orchestrator import MedicalQASystem

app = FastAPI(
    title="SafeAI Clinical Pipeline API",
    description="WHO Malaria & Uganda Clinical Guidelines — BM25 + guardrail + optional VHT response layer",
    version="1.0.0",
)

_qa: Optional[MedicalQASystem] = None
_loaded: Optional[Dict[str, Any]] = None

_PRESET_ALIASES = {
    "who-malaria": "who-malaria",
    "who-malaria-nih": "who-malaria",
    "malaria": "who-malaria",
    "uganda": "uganda",
    "uganda-clinical-2023": "uganda",
    "uganda_clinical": "uganda",
}


def _normalize_preset(name: str) -> str:
    key = (name or "").strip().lower().replace(" ", "-")
    if key not in _PRESET_ALIASES:
        allowed = sorted(set(_PRESET_ALIASES.keys()))
        raise HTTPException(
            status_code=400,
            detail=f"Unknown preset '{name}'. Use one of: {allowed}",
        )
    return _PRESET_ALIASES[key]


def _build_config(preset: str, pdf_path: Optional[str], output_dir: Optional[str]) -> ExtractionConfig:
    """Do not pass pdf_path=None — that would override factory defaults."""

    def _kwargs() -> Dict[str, Any]:
        kw: Dict[str, Any] = {}
        if pdf_path:
            kw["pdf_path"] = pdf_path
        if output_dir:
            kw["output_dir"] = output_dir
        return kw

    kw = _kwargs()
    if preset == "who-malaria":
        return extraction_config_who_malaria_nih(**kw) if kw else extraction_config_who_malaria_nih()
    return extraction_config_uganda_clinical_2023(**kw) if kw else extraction_config_uganda_clinical_2023()


def _serialize_structured(obj: Any) -> Dict[str, Any]:
    d = asdict(obj)
    if "triage" in d and hasattr(obj.triage, "name"):
        d["triage"] = obj.triage.name
    return d


def _serialize_ask_result(result: Dict[str, Any]) -> Dict[str, Any]:
    """JSON-safe copy of answer_with_response()."""
    out: Dict[str, Any] = {}
    for k, v in result.items():
        if k == "structured" and v is not None:
            out[k] = _serialize_structured(v)
        elif k == "triage" and hasattr(v, "name"):
            out[k] = v.name
        else:
            out[k] = v
    return out


class InitializeRequest(BaseModel):
    """Load preset and paths; builds KB unless reuse_existing_kb and KB already on disk."""

    preset: str = Field(
        default="who-malaria",
        description="who-malaria | uganda (aliases: who-malaria-nih, uganda-clinical-2023)",
    )
    pdf_path: Optional[str] = Field(
        default=None,
        description="Override PDF path; default uses preset factory paths",
    )
    output_dir: Optional[str] = Field(
        default=None,
        description="Override KB output directory",
    )
    reuse_existing_kb: bool = Field(
        default=True,
        description="If true and knowledge_base.json exists under output_dir, load only (fast)",
    )


class AskRequest(BaseModel):
    query: str = Field(..., min_length=1, description="User question")
    full_response: bool = Field(
        default=True,
        description="If true, return answer_with_response (VHT + referral + quick). If false, answer() only",
    )
    use_local_llm: Optional[bool] = Field(
        default=None,
        description="If true, run local GGUF simplifier when SAFEAI_LLM_GGUF is set; false forces off; null uses SAFEAI_USE_LOCAL_LLM",
    )


def _local_llm_disk_configured() -> bool:
    p = (os.environ.get("SAFEAI_LLM_GGUF") or "").strip()
    return bool(p and os.path.isfile(p))


@app.get("/health")
def health() -> Dict[str, Any]:
    return {
        "status": "ok",
        "initialized": _qa is not None,
        "preset": (_loaded or {}).get("preset"),
        "document_title": (_loaded or {}).get("document_title"),
        "local_llm_gguf_configured": _local_llm_disk_configured(),
        "local_llm_env_enabled": os.environ.get("SAFEAI_USE_LOCAL_LLM", "").strip().lower()
        in ("1", "true", "yes", "on"),
    }


@app.get("/metadata")
def metadata() -> Dict[str, Any]:
    if _qa is None or _loaded is None:
        raise HTTPException(status_code=400, detail="Pipeline not initialized. POST /initialize first.")
    kb = os.path.join(_qa.output_dir, "knowledge_base.json")
    summ: Dict[str, Any] = {}
    if os.path.isfile(kb):
        import json

        with open(kb, "r", encoding="utf-8") as f:
            data = json.load(f)
        summ = data.get("extraction_summary", {})
    val = _qa.validation_result or {}
    overall = val.get("overall", {}) if isinstance(val, dict) else {}
    return {
        "preset": _loaded.get("preset"),
        "pdf_path": _loaded.get("pdf_path"),
        "output_dir": _loaded.get("output_dir"),
        "document_title": _loaded.get("document_title"),
        "chunk_count": len(_qa.chunks or []),
        "knowledge_base_path": kb,
        "extraction_summary": summ,
        "validation_overall": overall,
    }


@app.post("/initialize")
def initialize(req: InitializeRequest) -> Dict[str, Any]:
    global _qa, _loaded

    preset = _normalize_preset(req.preset)
    cfg = _build_config(preset, req.pdf_path, req.output_dir)

    if not os.path.isfile(cfg.pdf_path):
        raise HTTPException(
            status_code=400,
            detail=f"PDF not found: {cfg.pdf_path}",
        )

    kb_file = os.path.join(cfg.output_dir, "knowledge_base.json")
    if not req.reuse_existing_kb and os.path.isfile(kb_file):
        try:
            os.remove(kb_file)
        except OSError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Could not remove existing KB for rebuild: {e}",
            )

    try:
        qa = MedicalQASystem(config=cfg)
        qa.initialize()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Initialization failed: {e!s}")

    _qa = qa
    _loaded = {
        "preset": preset,
        "pdf_path": cfg.pdf_path,
        "output_dir": cfg.output_dir,
        "document_title": cfg.document_title,
        "reuse_existing_kb": req.reuse_existing_kb,
    }

    return {
        "message": "Pipeline initialized successfully",
        "config": _loaded,
        "chunk_count": len(qa.chunks or []),
    }


@app.post("/ask")
def ask(req: AskRequest) -> Dict[str, Any]:
    if _qa is None:
        raise HTTPException(status_code=400, detail="Pipeline not initialized. POST /initialize first.")

    try:
        if req.full_response:
            raw = _qa.answer_with_response(
                req.query,
                use_local_llm=req.use_local_llm,
            )
            result = _serialize_ask_result(raw)
        else:
            result = _qa.answer(req.query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Q&A failed: {e!s}")

    return {
        "query": req.query,
        "full_response": req.full_response,
        "result": result,
    }
