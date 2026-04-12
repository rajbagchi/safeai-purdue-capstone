# Pipeline Viewer (WPF)

Windows desktop UI for the repo’s **FastAPI** service (`api.py` at repo root).

Architecture (components, HTTP mapping, data flow): **[pipelineviewer.md](pipelineviewer.md)**.

- **Source**: WHO Malaria vs Uganda preset (same as `/initialize` `preset`).
- **Create index**: `POST /initialize` (respects “reuse existing KB”).
- **Test query**: dropdown lists all **25** evaluation queries per source, matching `scripts/who_malaria_pipeline_report.py` (`MALARIA_SEARCH_QUERIES` / `UGANDA_SEARCH_QUERIES`).

## Prerequisites

- [.NET 8 SDK](https://dotnet.microsoft.com/download/dotnet/8.0)
- Python API running from repo root, PDFs available at the preset default paths (see `pipeline/README.md`).

```powershell
cd C:\temp\capstone\safeai-purdue-capstone
pip install -r requirements-api.txt
uvicorn api:app --host 127.0.0.1 --port 8000
```

## Run the app

```powershell
cd windows\PipelineViewer
dotnet run --project PipelineViewer
```

Or open `PipelineViewer.sln` in Visual Studio and start **PipelineViewer**.

Default API URL is `http://127.0.0.1:8000`. Change it if your server uses another host or port.

## Local Qwen2.5-3B GGUF (optional)

The API can rewrite VHT text with **llama-cpp-python** + a **GGUF** file. On the **machine that runs uvicorn**, install and set env, then restart the API:

```powershell
cd C:\temp\capstone\safeai-purdue-capstone
pip install -r requirements-api.txt
pip install -r requirements-local-llm.txt
# If needed on Windows CPU:
# pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu

# Optional: from repo root, dot-source env (expects C:\models\Qwen2.5-3B-Instruct-Q4_K_M.gguf)
#   . .\windows\set_local_qwen_env.ps1

$env:SAFEAI_USE_LOCAL_LLM = "1"
$env:SAFEAI_LLM_GGUF = "C:\models\Qwen2.5-3B-Instruct-Q4_K_M.gguf"
python -m uvicorn api:app --host 127.0.0.1 --port 8000 --reload
```

Smoke-test the model only (no KB):

```powershell
$env:SAFEAI_LLM_GGUF = "C:\path\to\your.gguf"
python scripts\smoke_local_llm.py
```

In **Pipeline Viewer**, leave **“Use local Qwen2.5-3B GGUF…”** checked to send `use_local_llm: true` on **Run query**. **Health** refreshes the line under the checkbox (`local_llm_gguf_configured` / `local_llm_env_enabled` from `/health`).
