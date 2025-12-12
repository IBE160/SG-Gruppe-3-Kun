from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.v1.endpoints import health, chat
from app.core.config import settings
import chromadb

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context Manager for managing the lifespan of the FastAPI application.
    Initializes and cleans up resources like the ChromaDB client.
    """
    # Startup event
    app.state.chroma_client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIRECTORY)
    print("ChromaDB client initialized.") # For debugging
    yield
    # Shutdown event
    # PersistentClient generally doesn't need explicit closing
    app.state.chroma_client = None
    print("ChromaDB client shutdown.") # For debugging

app = FastAPI(lifespan=lifespan)

app.include_router(health.router, prefix="/api/v1/health", tags=["health"])
app.include_router(chat.router, prefix="/api/v1/chat", tags=["chat"])

@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "0.1.0"}
