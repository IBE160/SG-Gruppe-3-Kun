import pytest
import shutil
import os
import chromadb
from app.rag.vector_store import get_collection
from app.core.config import settings

@pytest.fixture(scope="function")
def chroma_client_fixture(tmp_path_factory):
    # Use pytest's tmp_path_factory for a temporary directory
    test_persist_dir = tmp_path_factory.mktemp("chroma_data")
    
    # Override settings for the test
    original_persist_dir = settings.CHROMA_PERSIST_DIRECTORY
    settings.CHROMA_PERSIST_DIRECTORY = str(test_persist_dir)
    
    # Initialize client and yield it
    client = chromadb.PersistentClient(path=str(test_persist_dir))
    yield client
    
    # Cleanup after test - tmp_path_factory handles directory removal
    client = None # Explicitly dereference
    # Restore settings
    settings.CHROMA_PERSIST_DIRECTORY = original_persist_dir

def test_chroma_init_and_persistence(chroma_client_fixture):
    """
    Verifies that we can initialize the client, create a collection,
    add a document, and retrieve it.
    """
    test_client = chroma_client_fixture
    # 1. Get collection using the test client
    collection = get_collection(client=test_client, name="test_integration_collection")
    
    # 2. Insert mock vector/document
    collection.add(
        embeddings=[[0.1, 0.2, 0.3]], # Dummy 3D embedding
        documents=["This is a test document"],
        metadatas=[{"source": "test_script"}],
        ids=["test_id_1"]
    )
    
    # 3. Query the mock vector
    results = collection.query(
        query_embeddings=[[0.1, 0.2, 0.3]],
        n_results=1
    )
    
    # 4. Assert results match
    assert len(results['ids']) > 0
    assert results['ids'][0][0] == "test_id_1"
    assert results['documents'][0][0] == "This is a test document"
    
    # Explicitly delete collection reference
    del collection
    
    # 5. Verify persistence (basic check)
    # Re-initialize client to simulate restart (needs a new client instance)
    # Use the same path as the fixture to simulate restart on the same data
    client2 = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIRECTORY) 
    coll2 = get_collection(client=client2, name="test_integration_collection")
    assert coll2.count() == 1
    
    # Explicitly delete client references
    del client2
    del coll2
