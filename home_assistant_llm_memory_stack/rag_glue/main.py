from fastapi import FastAPI, Request
from ha_tools.memory_loader import search_ha_memory

app = FastAPI()

@app.post("/rag")
async def rag_endpoint(request: Request):
    body = await request.json()
    query = body.get("query")

    if not query:
        return {"status": "error", "error": "Missing query"}

    results = await search_ha_memory(query)

    context = []
    for item in results:
        area = item.get("area", "unknown area")
        device = item.get("device", "unknown device")
        entities = ", ".join(e["entity_id"] for e in item.get("entities", []))
        context.append(f"In {area}, the device {device} has entities: {entities}.")

    full_context = "\n".join(context)
    return {
        "status": "ok",
        "context": full_context
    }
