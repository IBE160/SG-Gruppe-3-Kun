from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from app.api.v1.endpoints import health
from app.core.config import settings
import chromadb
from chromadb.api import ClientAPI

# Global variable to hold the ChromaDB client instance managed by FastAPI lifecycle
_chroma_client_instance: ClientAPI | None = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context Manager for managing the lifespan of the FastAPI application.
    Initializes and cleans up resources like the ChromaDB client.
    """
    global _chroma_client_instance
    # Startup event
    _chroma_client_instance = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIRECTORY)
    print("ChromaDB client initialized.") # For debugging
    yield
    # Shutdown event
    if _chroma_client_instance:
        # PersistentClient generally doesn't need explicit closing, but good practice for resources
        _chroma_client_instance = None # Resetting for clarity
    print("ChromaDB client shutdown.") # For debugging

app = FastAPI(lifespan=lifespan)

app.include_router(health.router, prefix="/api/v1/health", tags=["health"])

@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "0.1.0"}

def get_chroma_client_fastapi() -> ClientAPI:
    """Dependency function to provide the ChromaDB client instance."""
    if _chroma_client_instance is None:
        raise ValueError("ChromaDB client not initialized. Ensure startup event ran.")
    return _chroma_client_instance
