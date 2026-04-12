"""
Smoke-test local Qwen GGUF via pipeline LocalSimplifierLLM (no API, no KB).

Usage (repo root):
  set SAFEAI_LLM_GGUF=C:\\path\\to\\Qwen2.5-3B-Instruct-Q4_K_M.gguf
  python scripts/smoke_local_llm.py

Optional:
  set SAFEAI_LLM_N_THREADS=4
"""
from __future__ import annotations

import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


def main() -> int:
    from pipeline.compat import fix_stdio_encoding

    fix_stdio_encoding()

    path = (os.environ.get("SAFEAI_LLM_GGUF") or "").strip()
    if not path or not os.path.isfile(path):
        print("Set SAFEAI_LLM_GGUF to a valid .gguf file path, then re-run.")
        print("Example: Qwen2.5-3B-Instruct-Q4_K_M.gguf from Hugging Face (TheBloke or official quant).")
        return 1

    os.environ.setdefault("SAFEAI_USE_LOCAL_LLM", "1")

    from pipeline.local_simplifier import LocalSimplifierLLM

    sim = LocalSimplifierLLM()
    chunks = [
        {
            "page": 1,
            "heading": "Demo",
            "text": "If fever and danger signs, refer urgently to hospital.",
        }
    ]
    out = sim.simplify_vht_markdown(
        query="When should we refer?",
        document_title="Demo guideline",
        rule_based_vht=(
            "**QUICK SUMMARY: YELLOW**\n\n"
            "Triage Level: YELLOW (assess today)\n\n"
            "Immediate Actions:\n- Check danger signs\n\n"
            "Next Steps / Monitoring:\n- Watch breathing\n\n"
            "When to Refer:\n- If worse\n\n"
            "Citations:\n- Page 1\n"
        ),
        structured_answer=(
            "Question: When should we refer?\n"
            "Triage (approved): YELLOW\n"
            "Actions:\n- Check danger signs\n"
        ),
        evidence_chunks=chunks,
    )
    if not out:
        print("Model returned no text (check llama-cpp-python install and GGUF path).")
        return 2
    print("--- LLM output (first 1200 chars) ---")
    print(out[:1200])
    print("\nOK.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
