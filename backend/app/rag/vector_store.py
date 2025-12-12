from typing import List, Dict, Any

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

def add_chunks_to_collection(
    client: ClientAPI,
    chunks: List[Dict[str, Any]],
    collection_name: str = "hmsreg_docs"
) -> int:
    """
    Adds a list of processed text chunks (with embeddings and metadata) to a ChromaDB collection.

    Args:
        client: The ChromaDB client instance.
        chunks: A list of dictionaries, where each dictionary represents a chunk
                and contains 'content', 'url', 'title', 'chunk_id', and 'embedding'.
        collection_name: The name of the ChromaDB collection to add chunks to.

    Returns:
        The number of chunks successfully added to the collection.
    """
    if not chunks:
        return 0

    collection = get_collection(client, collection_name)

    documents = [chunk['content'] for chunk in chunks]
    metadatas = [
        {
            "url": chunk['url'],
            "title": chunk['title'],
            "chunk_id": chunk['chunk_id'], # Keep the original chunk ID
        }
        for chunk in chunks
    ]
    embeddings = [chunk['embedding'] for chunk in chunks]
    ids = [chunk['chunk_id'] for chunk in chunks] # Use chunk_id as the document ID in Chroma

    # Filter out chunks with empty embeddings before adding
    filtered_data = [
        (doc, meta, embed, doc_id)
        for doc, meta, embed, doc_id in zip(documents, metadatas, embeddings, ids)
        if embed # Check if embedding list is not empty
    ]

    if not filtered_data:
        print("No chunks with valid embeddings to add to ChromaDB.")
        return 0

    documents, metadatas, embeddings, ids = zip(*filtered_data)

    try:
        collection.add(
            documents=list(documents),
            metadatas=list(metadatas),
            embeddings=list(embeddings),
            ids=list(ids),
        )
        print(f"Successfully added {len(documents)} chunks to ChromaDB collection '{collection_name}'.")
        return len(documents)
    except Exception as e:
        print(f"Error adding chunks to ChromaDB: {e}")
        return 0
