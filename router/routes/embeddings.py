from fastapi import APIRouter, Request
import httpx
import os

router = APIRouter()

@router.post("/v1/embeddings")
async def embeddings(request: Request):
    body = await request.json()
    model = body.get("model", "text-embedding-ada-002")
    proxy_url = "https://api.openai.com/v1/embeddings"
    headers = {
        "Authorization": f"Bearer {os.environ.get('OPENAI_API_KEY')}",
        "Content-Type": "application/json"
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(proxy_url, headers=headers, json=body)
        return resp.json()
