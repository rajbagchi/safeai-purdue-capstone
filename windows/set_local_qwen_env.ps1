# Dot-source before starting uvicorn so /ask can use the local GGUF simplifier:
#   . .\windows\set_local_qwen_env.ps1
#   python -m uvicorn api:app --host 127.0.0.1 --port 8000 --reload

$gguf = "C:\models\Qwen2.5-3B-Instruct-Q4_K_M.gguf"
if (-not (Test-Path -LiteralPath $gguf)) {
    Write-Warning "GGUF not found: $gguf"
    return
}
$env:SAFEAI_LLM_GGUF = $gguf
$env:SAFEAI_USE_LOCAL_LLM = "1"
Write-Host "Set SAFEAI_LLM_GGUF and SAFEAI_USE_LOCAL_LLM=1 for this session."
