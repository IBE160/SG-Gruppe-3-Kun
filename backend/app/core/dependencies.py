from fastapi import Request
from chromadb.api import ClientAPI

def get_chroma_client(request: Request) -> ClientAPI:
    """
    Dependency to retrieve the ChromaDB client from the app state.
    """
    client = getattr(request.app.state, "chroma_client", None)
    if client is None:
        raise ValueError("ChromaDB client is not initialized in app state.")
    return client
