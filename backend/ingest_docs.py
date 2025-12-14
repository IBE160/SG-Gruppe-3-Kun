import sys
import os
import google.generativeai as genai
import chromadb
from dotenv import load_dotenv
import asyncio

# Add the project root to sys.path to resolve module import issues for data_processor.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

print(f"Current working directory: {os.getcwd()}")
load_dotenv() # .env is now in the same directory as this script
print("load_dotenv() called.")
print(f"GOOGLE_API_KEY from environment: {os.getenv('GOOGLE_API_KEY')}")
print(f"DATABASE_URL from environment: {os.getenv('DATABASE_URL')}")

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Assuming data_processor.py is in the project root
from data_processor import get_and_chunk_text
# These imports are now relative within the 'backend' package
from app.rag.vector_store import get_collection, add_chunks_to_collection
from app.core.config import settings

# Initialize ChromaDB client
# This should be PersistentClient if you want to save the data
CHROMA_CLIENT = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIRECTORY)
COLLECTION_NAME = "hmsreg_docs"

async def ingest_documents(urls: list[str]):
    print(f"Starting document ingestion for {len(urls)} URLs...")
    
    all_processed_chunks = []
    
    # Optional: Clear existing collection before re-ingesting
    try:
        CHROMA_CLIENT.delete_collection(name=COLLECTION_NAME)
        print(f"Cleared existing ChromaDB collection: {COLLECTION_NAME}")
    except Exception as e:
        print(f"Could not delete collection (might not exist yet): {e}")

    # Ensure collection exists after potential deletion
    collection = get_collection(CHROMA_CLIENT, COLLECTION_NAME)
    print(f"Using ChromaDB collection: {collection.name}")

    for url in urls:
        print(f"\nProcessing URL: {url}")
        chunks = get_and_chunk_text(url) # This now returns semantically de-duplicated chunks

        if chunks:
            for i, chunk_content in enumerate(chunks):
                # For simplicity, using a basic title extraction and chunk_id
                # In a real scenario, you might extract title more robustly from HTML
                # And create a more stable chunk_id
                title = "Untitled Document" # Placeholder, consider improving this in data_processor or here
                
                # Try to get a better title from the URL if possible, or use the HTML title
                # For this specific URL structure, extracting an ID might be useful for title
                if "ID=" in url:
                    try:
                        title_id = url.split("ID=")[-1]
                        title = f"HMSREG Document {title_id}"
                    except:
                        pass # Fallback to "Untitled Document"
                
                all_processed_chunks.append({
                    "content": chunk_content,
                    "url": url,
                    "title": title,
                    "chunk_id": f"{url}_{i}" # Unique ID for each chunk
                })
        else:
            print(f"No chunks returned for URL: {url}")

    if all_processed_chunks:
        print(f"\nTotal processed unique chunks for indexing: {len(all_processed_chunks)}")
        # Generate embeddings for all chunks in a batch for efficiency
        # Note: genai.embed_content can take a list of strings
        try:
            print("Generating embeddings for all chunks...")
            all_contents = [chunk['content'] for chunk in all_processed_chunks]
            embeddings_response = genai.embed_content(
                model="models/text-embedding-004",
                content=all_contents,
                task_type="retrieval_document"
            )
            all_embeddings = embeddings_response["embedding"]

            # Attach embeddings back to their respective chunks
            for i, chunk in enumerate(all_processed_chunks):
                chunk['embedding'] = all_embeddings[i]
            
            # Now add to ChromaDB
            added_count = add_chunks_to_collection(CHROMA_CLIENT, all_processed_chunks, COLLECTION_NAME)
            print(f"Successfully added {added_count} chunks to ChromaDB collection '{COLLECTION_NAME}'.")
        except Exception as e:
            print(f"Error during embedding generation or adding to ChromaDB: {e}")
    else:
        print("No chunks to add to ChromaDB.")

if __name__ == "__main__":
    # Use a smaller subset of URLs for debugging purposes
    DOC_URLS_SMALL_SUBSET = [
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10379",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10380",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10751",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10199",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10318"
    ]
    
    asyncio.run(ingest_documents(DOC_URLS_SMALL_SUBSET))
