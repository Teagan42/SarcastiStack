from fastapi import FastAPI
from ha_tools.memory_loader import build_and_store_vectors

app = FastAPI()

@app.post("/update_ha_memory")
async def update_memory():
    try:
        await build_and_store_vectors()
        return {"status": "ok", "message": "Memory updated"}
    except Exception as e:
        return {"status": "error", "error": str(e)}
