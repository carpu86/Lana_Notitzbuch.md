import os
from datetime import datetime, timezone

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

app = FastAPI(title="Lana API")

LM_STUDIO_BASE = os.getenv("LM_STUDIO_BASE_URL", "http://127.0.0.1:1234/v1")
COMFYUI_BASE = os.getenv("COMFYUI_BASE_URL", "http://127.0.0.1:8188")
REQUEST_TIMEOUT = float(os.getenv("REQUEST_TIMEOUT_SECONDS", "30"))


class ChatRequest(BaseModel):
    model: str
    messages: list
    stream: bool = True


class ComfyRequest(BaseModel):
    prompt: dict


@app.get("/health")
def health():
    return {"status": "ok", "ts": datetime.now(timezone.utc).isoformat()}


@app.get("/api/v1/models")
async def models():
    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
        try:
            r = await client.get(f"{LM_STUDIO_BASE}/models")
            r.raise_for_status()
            return r.json()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=502, detail=f"LM Studio error: {e}")


@app.post("/api/v1/chat")
async def chat(payload: ChatRequest):
    async def stream_gen():
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
            try:
                async with client.stream("POST", f"{LM_STUDIO_BASE}/chat/completions", json=payload.model_dump()) as r:
                    r.raise_for_status()
                    async for line in r.aiter_lines():
                        if line:
                            yield line + "\n"
            except httpx.HTTPError as e:
                yield f"data: {{\"error\": \"{str(e)}\"}}\n\n"

    return StreamingResponse(stream_gen(), media_type="text/event-stream")


@app.post("/api/v1/comfy")
async def comfy(payload: ComfyRequest):
    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
        try:
            r = await client.post(f"{COMFYUI_BASE}/prompt", json=payload.model_dump())
            r.raise_for_status()
            return r.json()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=502, detail=f"ComfyUI error: {e}")
