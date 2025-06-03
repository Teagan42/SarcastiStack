from fastapi import APIRouter, Request
import hashlib

router = APIRouter()
memory_store = {}

def hash_text(text):
    return hashlib.sha256(text.encode()).hexdigest()

@router.post("/v1/memory/save")
async def save_memory(request: Request):
    data = await request.json()
    user_id = data.get("user_id", "default")
    content = data.get("content")
    memory_store.setdefault(user_id, {})
    h = hash_text(content)
    memory_store[user_id][h] = content
    return {"status": "ok", "memory_size": len(memory_store[user_id])}

@router.post("/v1/memory/query")
async def query_memory(request: Request):
    data = await request.json()
    user_id = data.get("user_id", "default")
    query = data.get("query", "")
    return {
        "results": list(memory_store.get(user_id, {}).values())[:5],
        "count": len(memory_store.get(user_id, {}))
    }
