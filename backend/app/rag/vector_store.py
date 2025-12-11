from chromadb.api import ClientAPI
from chromadb.api.models.Collection import Collection

# Note: The ChromaDB client is now initialized and managed by FastAPI's lifecycle events
# in app.main.py, and provided via dependency injection.

def get_collection(client: ClientAPI, name: str = "hmsreg_docs") -> Collection:
    """
    Returns the specific collection for HMSREG docs.
    Creates it if it doesn't exist.
    The ChromaDB client is provided via FastAPI's dependency injection.
    """
    # get_or_create_collection is the standard way to ensure it exists
    return client.get_or_create_collection(name=name)

