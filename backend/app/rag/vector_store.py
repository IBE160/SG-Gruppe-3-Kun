import chromadb
from chromadb.api import ClientAPI
from chromadb.api.models.Collection import Collection
from app.core.config import settings

def get_chroma_client() -> ClientAPI:
    """
    Returns a persistent ChromaDB client.
    Persistence path is configured via settings.CHROMA_PERSIST_DIRECTORY.
    """
    return chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIRECTORY)

def get_collection(name: str = "hmsreg_docs") -> Collection:
    """
    Returns the specific collection for HMSREG docs.
    Creates it if it doesn't exist.
    """
    client = get_chroma_client()
    # get_or_create_collection is the standard way to ensure it exists
    return client.get_or_create_collection(name=name)
