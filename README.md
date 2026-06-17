# Lana KI Monorepo

## Quickstart (PowerShell)
1. `cd apps/api`
2. `python -m venv .venv; .\.venv\Scripts\Activate.ps1`
3. `pip install -r requirements.txt`
4. `uvicorn app.main:app --host 127.0.0.1 --port 8010`

## ASCII
User -> Cloudflare Pages -> Worker -> Tunnel -> FastAPI:8010 -> LM Studio/ComfyUI
