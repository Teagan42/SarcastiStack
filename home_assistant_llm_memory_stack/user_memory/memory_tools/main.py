from fastapi import FastAPI, Request

app = FastAPI()

memory_store = {}

@app.post("/extract")
async def extract_memory(request: Request):
    data = await request.json()
    text = data.get("text", "")

    if "NestJS" in text and "NestJS" not in memory_store.get("tech_stack", []):
        memory_store.setdefault("tech_stack", []).append("NestJS")
    if "RxJS" in text and "RxJS" not in memory_store.get("tech_stack", []):
        memory_store.setdefault("tech_stack", []).append("RxJS")
    if "LibreChat" in text and "LibreChat" not in memory_store.get("projects", []):
        memory_store.setdefault("projects", []).append("LibreChat")

    return {"status": "ok", "memory": memory_store}
