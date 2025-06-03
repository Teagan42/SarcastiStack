import aiohttp
import hashlib
import json
import os
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct

HA_WS_URL = "ws://homeassistant.local:8123/api/websocket"
QDRANT_URL = "http://qdrant:6333"
COLLECTION = "ha_knowledge"
CACHE_PATH = "/tmp/memory_cache.json"

model = SentenceTransformer("all-MiniLM-L6-v2")
qdrant = QdrantClient(url=QDRANT_URL)

async def get_ha_registry_data():
    return [{
        "area": "Living Room",
        "device": "Thermostat",
        "entities": [{"entity_id": "climate.living_room", "services": ["set_temperature", "turn_off"]}]
    }]

def make_contextual_string(item):
    entities = ", ".join(e["entity_id"] for e in item["entities"])
    return f"The {item['area']} has device {item['device']} with entities: {entities}"

def embed(text):
    return model.encode(text).tolist()

def hash_payload(payload):
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()

def load_cache():
    if os.path.exists(CACHE_PATH):
        with open(CACHE_PATH, "r") as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open(CACHE_PATH, "w") as f:
        json.dump(cache, f)

async def build_and_store_vectors():
    data = await get_ha_registry_data()
    cache = load_cache()
    new_cache = {}
    points = []

    for item in data:
        desc = make_contextual_string(item)
        uid = str(int(hashlib.md5(desc.encode()).hexdigest()[:8], 16))
        payload_hash = hash_payload(item)

        if cache.get(uid) == payload_hash:
            continue

        vec = embed(desc)
        points.append(PointStruct(id=uid, vector=vec, payload=item))
        new_cache[uid] = payload_hash

    if points:
        qdrant.upsert(collection_name=COLLECTION, points=points)

    save_cache(new_cache)

async def search_ha_memory(query: str):
    vec = embed(query)
    search_result = qdrant.search(collection_name=COLLECTION, query_vector=vec, limit=5)
    return [point.payload for point in search_result]
