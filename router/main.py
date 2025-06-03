from fastapi import FastAPI
from routes.chat import router as chat_router
from routes.embeddings import router as embed_router
from routes.memory import router as memory_router
from routes.vector_memory import router as vector_router

app = FastAPI()
app.include_router(chat_router)
app.include_router(embed_router)
app.include_router(memory_router)
app.include_router(vector_router)
