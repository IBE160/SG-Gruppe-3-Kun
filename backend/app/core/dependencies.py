from fastapi import Request
from chromadb.api import ClientAPI
from app.services.chat_service import ChatService
import logging

logger = logging.getLogger(__name__)

def get_chroma_client(request: Request) -> ClientAPI:
    """
    Dependency to retrieve the ChromaDB client from the app state.
    """
    client = getattr(request.app.state, "chroma_client", None)
    if client is None:
        logger.error("ChromaDB client is NOT initialized in app state!")
        raise ValueError("ChromaDB client is not initialized in app state.")
    return client

def get_chat_service() -> ChatService:
    """
    Dependency to retrieve a ChatService instance.
    This can be expanded to manage service lifecycle if needed.
    """
    # This is a simple factory for now.
    # In a real app, you might have connection pooling or other setup here.
    return ChatService()
