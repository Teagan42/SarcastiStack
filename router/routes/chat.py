from fastapi import APIRouter, Request
import httpx
import os
from .vector_memory import vector_memory, get_embedding, cosine_sim
import json
from pathlib import Path

router = APIRouter()

config_path = Path(__file__).parent.parent / "config" / "prompt_templates.json"
with open(config_path) as f:
    PROMPT_TEMPLATES = json.load(f)

def load_tool_memory():
    tool_config = Path(__file__).parent.parent / "config" / "tool_memory.json"
    if tool_config.exists():
        with open(tool_config) as f:
            return {tool["name"]: tool["memory_context"] for tool in json.load(f).get("tools", [])}
    return {}

tool_memory_lookup = load_tool_memory()

def extract_tool_usage(messages):
    used_tools = []
    for m in messages:
        if m.get("tool_call_id"):
            used_tools.append(m["tool_call_id"])
        elif m.get("function_call"):
            used_tools.append(m["function_call"].get("name"))
    return used_tools

def apply_prompt_template(template_name, memory, user_input):
    tmpl = PROMPT_TEMPLATES.get(template_name, PROMPT_TEMPLATES["default"])
    return tmpl.replace("{{memory_context}}", memory).replace("{{user_input}}", user_input)

async def get_top_memory(user_id, query, limit=3):
    if user_id not in vector_memory:
        return []
    query_emb = await get_embedding(query)
    scored = []
    for uid, mem in vector_memory[user_id].items():
        score = cosine_sim(query_emb, mem["embedding"])
        scored.append((score, mem["content"]))
    scored.sort(reverse=True)
    print("Memory Match Log:", scored[:limit])
    return [c for _, c in scored[:limit]]

@router.post("/v1/chat/completions")
async def chat_completions(request: Request):
    body = await request.json()
    model = body.get("model")
    messages = body.get("messages", [])
    user_id = body.get("user", "default")
    user_msg = next((m for m in reversed(messages) if m["role"] == "user"), None)
    query = user_msg["content"] if user_msg else ""

    memory_results = await get_top_memory(user_id, query)
    tool_names = extract_tool_usage(messages)
    tool_memory_context = "\n".join(tool_memory_lookup.get(t, "") for t in tool_names if t in tool_memory_lookup)
    memory_context = tool_memory_context + "\n" + "\n".join(memory_results)

    templated_prompt = apply_prompt_template(
        "mistral" if model.startswith("mistral") else "gpt" if model.startswith("gpt") else "default",
        memory_context,
        query
    )

    forward_messages = [
        {"role": "system", "content": "Memory injected context."},
        {"role": "user", "content": templated_prompt}
    ]

    if model.startswith("gpt"):
        proxy_url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {os.environ.get('OPENAI_API_KEY')}",
            "Content-Type": "application/json"
        }
        body["messages"] = forward_messages
    elif model.startswith("mistral"):
        proxy_url = "http://ollama:11434/api/chat"
        headers = {"Content-Type": "application/json"}
        body = {
            "model": "mistral",
            "messages": forward_messages
        }
    else:
        return {"error": "Unsupported model"}

    async with httpx.AsyncClient() as client:
        resp = await client.post(proxy_url, headers=headers, json=body)
        return resp.json()
