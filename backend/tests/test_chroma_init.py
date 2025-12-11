import pytest
import shutil
import os
import chromadb
from app.rag.vector_store import get_collection, get_chroma_client
from app.core.config import settings

# Use a separate test directory for persistence to avoid messing up dev data
TEST_PERSIST_DIR = "test_chroma_data"

@pytest.fixture(scope="function")
def setup_test_db():
    # Override settings for the test
    original_persist_dir = settings.CHROMA_PERSIST_DIRECTORY
    settings.CHROMA_PERSIST_DIRECTORY = TEST_PERSIST_DIR
    
    # Ensure clean start
    if os.path.exists(TEST_PERSIST_DIR):
        shutil.rmtree(TEST_PERSIST_DIR)
        
    yield
    
    # Cleanup after test
    if os.path.exists(TEST_PERSIST_DIR):
        shutil.rmtree(TEST_PERSIST_DIR)
    # Restore settings
    settings.CHROMA_PERSIST_DIRECTORY = original_persist_dir

def test_chroma_init_and_persistence(setup_test_db):
    """
    Verifies that we can initialize the client, create a collection,
    add a document, and retrieve it.
    """
    # 1. Initialize and get collection
    collection = get_collection(name="test_integration_collection")
    
    # 2. Insert mock vector/document
    # ChromaDB handles embedding generation by default if none provided, 
    # or we can pass embeddings=... 
    # For this basic test, letting the default embedding function work (if available) 
    # or just checking the add/query mechanism is sufficient.
    # However, default embedding function requires internet or local model download.
    # To be safe and fast, we should provide dummy embeddings.
    
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
    
    # 5. Verify persistence (basic check)
    # Re-initialize client to simulate restart
    client2 = chromadb.PersistentClient(path=TEST_PERSIST_DIR)
    coll2 = client2.get_collection("test_integration_collection")
    assert coll2.count() == 1
