from fastapi import APIRouter, Request
import hashlib
import os
import httpx
import numpy as np

router = APIRouter()
vector_memory = {}

def hash_text(text):
    return hashlib.sha256(text.encode()).hexdigest()

async def get_embedding(text):
    headers = {
        "Authorization": f"Bearer {os.environ.get('OPENAI_API_KEY')}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "text-embedding-ada-002",
        "input": text
    }
    async with httpx.AsyncClient() as client:
        response = await client.post("https://api.openai.com/v1/embeddings", headers=headers, json=payload)
        return response.json()["data"][0]["embedding"]

@router.post("/v1/memory/vector/save")
async def vector_save(request: Request):
    data = await request.json()
    user_id = data.get("user_id", "default")
    content = data.get("content")
    emb = await get_embedding(content)
    uid = hash_text(content)
    vector_memory.setdefault(user_id, {})
    vector_memory[user_id][uid] = {"embedding": emb, "content": content}
    return {"status": "ok", "memory_size": len(vector_memory[user_id])}

def cosine_sim(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

@router.post("/v1/memory/vector/query")
async def vector_query(request: Request):
    data = await request.json()
    user_id = data.get("user_id", "default")
    query = data.get("query")
    query_emb = await get_embedding(query)
    results = []
    for uid, mem in vector_memory.get(user_id, {}).items():
        score = cosine_sim(query_emb, mem["embedding"])
        results.append((score, mem["content"]))
    results.sort(reverse=True)
    return {
        "results": [c for _, c in results[:5]],
        "count": len(results)
    }
