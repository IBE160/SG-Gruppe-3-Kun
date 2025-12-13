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
    DOC_URLS = [
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10379",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10380",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10751",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10199",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10318",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10562",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10389",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10687",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10219",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10480",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10765",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10525",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10715",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10089",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10167",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10427",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10435",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10583",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10402",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10446",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10582",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10472",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10313",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10768",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10381",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10188",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10347",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10354",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10743",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10697",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10599",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10317",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10584",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10394",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10742",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10093",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10531",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10086",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10091",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10767",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10766",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10760",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10762",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10763",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10554",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10373",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10226",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10252",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10251",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10088",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10756",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10238",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10625",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10635",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10478",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10512",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10220",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10513",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10509",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10359",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10479",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10754",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10528",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10341",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10510",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10665",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10481",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10482",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10388",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10495",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10498",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10469",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10497",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10496",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10256",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10230",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10376",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10117",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10487",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10259",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10227",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10322",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10358",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10323",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10330",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10483",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10485",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10187",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10457",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10748",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10221",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10657",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10260",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10586",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10232",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10430",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10746",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10342",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10336",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10175",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10649",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10529",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10732",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10699",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10295",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10316",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10639",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10627",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10343",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10346",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10345",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10344",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10249",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10248",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10247",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10243",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10241",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10240",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10239",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10237",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10096",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10236",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10235",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10470",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10664",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10428",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10577",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10542",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10424",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10425",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10426",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10484",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10374",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10736",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10367",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10368",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10369",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10149",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10438",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10234",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10257",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10325",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10553",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10628",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10349",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10356",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10558",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10527",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10524",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10526",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10454",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10728",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10588",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10414",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10413",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10422",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10514",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10589",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10663",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10723",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10541",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10656",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10655",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10533",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10611",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10456",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10453",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10253",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10455",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10544",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10523",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10521",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10520",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10094",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10505",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10504",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10503",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10502",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10473",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10421",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10198",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10197",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10195",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10540",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10178",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10201",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10200",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10146",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10233",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10119",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10087",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10489",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10565",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10539",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10621",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10176",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10452",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10174",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10191",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10189",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10488",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10186",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10296",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10398",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10459",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10458",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10650",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10658",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10392",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10690",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10669",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10499",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10511",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10698",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10691",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10696",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10675",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10676",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10309",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10659",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10652",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10578",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10592",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10310",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10461",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10335",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10222",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10372",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10338",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10223",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10396",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10305",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10306",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10364",
        "https://docs.hmsreg.com/?Area-ID=10000&ID=10304"
    ]
    
    asyncio.run(ingest_documents(DOC_URLS))
