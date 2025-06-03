from pathlib import Path

base_path = Path("./home_assistant_llm_memory_stack")

# Define folder structure
folders = [
    base_path / "mcp_home_memory_cached" / "ha_tools",
    base_path / "rag_glue",
    base_path / "user_memory" / "memory_tools"
]

# Define key files
files = {
    base_path / "docker-compose.yml": """\
version: "3.9"
services:
  mcp-memory:
    build: ./user_memory
    ports:
      - "8200:8000"
    networks:
      - internal

  mcp-tools:
    build: ./mcp_home_memory_cached
    ports:
      - "8100:8000"
    networks:
      - internal

  rag-glue:
    build: ./rag_glue
    ports:
      - "8000:8000"
    networks:
      - internal
    volumes:
      - ./mcp_home_memory_cached:/app/ha_tools

networks:
  internal:
    driver: bridge
""",

    base_path / "rag_glue" / "main.py": """\
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

    full_context = "\\n".join(context)
    return {
        "status": "ok",
        "context": full_context
    }
""",

    base_path / "rag_glue" / "Dockerfile": """\
FROM python:3.11-slim

WORKDIR /app
COPY . /app
RUN pip install --upgrade pip && pip install fastapi uvicorn aiohttp qdrant-client sentence-transformers

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
""",

    base_path / "user_memory" / "Dockerfile": """\
FROM python:3.11-slim

WORKDIR /app
COPY . /app
RUN pip install --upgrade pip && pip install fastapi uvicorn

EXPOSE 8000
CMD ["uvicorn", "memory_tools.main:app", "--host", "0.0.0.0", "--port", "8000"]
""",

    base_path / "user_memory" / "memory_tools" / "main.py": """\
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
"""
}

# Create folders and write files
for folder in folders:
    folder.mkdir(parents=True, exist_ok=True)

for file_path, content in files.items():
    file_path.write_text(content)

base_path
