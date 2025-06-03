import aiohttp
import hashlib
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct

HA_WS_URL = "ws://homeassistant.local:8123/api/websocket"
QDRANT_URL = "http://qdrant:6333"
COLLECTION = "ha_knowledge"

model = SentenceTransformer("all-MiniLM-L6-v2")
qdrant = QdrantClient(url=QDRANT_URL)

async def get_ha_registry_data():
    # Implement this using Home Assistant WebSocket API
    # Return list of hierarchical relationships
    return [{
        "area": "Living Room",
        "device": "Thermostat",
        "entities": [
            {"entity_id": "climate.living_room", "services": ["set_temperature", "turn_off"]}
        ]
    }]

def make_contextual_string(item):
    entities = ", ".join(e["entity_id"] for e in item["entities"])
    return f"The {item['area']} has device {item['device']} with entities: {entities}"

def embed(text):
    return model.encode(text).tolist()

async def build_and_store_vectors():
    data = await get_ha_registry_data()
    points = []
    for item in data:
        desc = make_contextual_string(item)
        vec = embed(desc)
        uid = int(hashlib.md5(desc.encode()).hexdigest()[:8], 16)
        points.append(PointStruct(id=uid, vector=vec, payload=item))
    qdrant.upsert(collection_name=COLLECTION, points=points)
