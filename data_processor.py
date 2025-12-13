import os
import requests
from bs4 import BeautifulSoup
from langchain_text_splitters import RecursiveCharacterTextSplitter
import google.generativeai as genai
import numpy as np
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

print("Script execution started.")

def calculate_cosine_similarity(embedding1, embedding2):
    """Calculates the cosine similarity between two embedding vectors."""
    return np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))

def get_and_chunk_text(url: str):
    """
    Fetches text content from a URL, cleans it, splits it into chunks,
    and performs semantic de-duplication on the chunks.
    """
    SIMILARITY_THRESHOLD = 0.95  # Tune this value as needed

    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        if soup.main:
            text = soup.main.get_text(separator='\n', strip=True)
        elif soup.article:
            text = soup.article.get_text(separator='\n', strip=True)
        else:
            text = soup.body.get_text(separator='\n', strip=True)

        text = '\n'.join(line.strip() for line in text.splitlines() if line.strip())

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )

        initial_chunks = text_splitter.split_text(text)
        
        # --- Semantic De-duplication ---
        unique_chunks = []
        unique_chunk_embeddings = []

        if not initial_chunks:
            return []

        # Embed all initial chunks first
        all_chunk_embeddings_response = genai.embed_content(
            model="models/text-embedding-004",
            content=initial_chunks,
            task_type="retrieval_document"
        )
        all_chunk_embeddings = all_chunk_embeddings_response["embedding"]

        # Add the first chunk unconditionally
        unique_chunks.append(initial_chunks[0])
        unique_chunk_embeddings.append(all_chunk_embeddings[0])

        for i in range(1, len(initial_chunks)):
            current_chunk = initial_chunks[i]
            current_embedding = all_chunk_embeddings[i]
            
            is_duplicate = False
            for unique_embedding in unique_chunk_embeddings:
                similarity = calculate_cosine_similarity(current_embedding, unique_embedding)
                if similarity > SIMILARITY_THRESHOLD:
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                unique_chunks.append(current_chunk)
                unique_chunk_embeddings.append(current_embedding)
        
        print(f"Successfully fetched and split content from {url}.")
        print(f"Initial chunks: {len(initial_chunks)}. Unique chunks after de-duplication: {len(unique_chunks)}.")
        
        # Display the first unique chunk as a sample
        if unique_chunks:
            print("\n--- Sample Unique Chunk (First 200 chars) ---")
            print(unique_chunks[0][:200] + "...")
            print("------------------------------------")
            
        return unique_chunks

    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

# --- Example Usage ---
# We'll use the main documentation page as a test.
# In the full implementation, we would loop through all your specified URLs.
test_url = "https://docs.hmsreg.com"
chunks = get_and_chunk_text(test_url)

if chunks is not None:
    print(f"Total chunks returned by function: {len(chunks)}")
else:
    print("No chunks were returned due to an error.")

print("Script execution finished.")