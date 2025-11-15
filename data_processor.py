import requests
from bs4 import BeautifulSoup
from langchain_text_splitters import RecursiveCharacterTextSplitter

print("Script execution started.")

def get_and_chunk_text(url: str):
    """
    Fetches text content from a URL, cleans it, and splits it into chunks.
    """
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()  # Raise an exception for bad status codes

        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract text, trying to find the main content area
        if soup.main:
            text = soup.main.get_text(separator='\n', strip=True)
        elif soup.article:
            text = soup.article.get_text(separator='\n', strip=True)
        else:
            text = soup.body.get_text(separator='\n', strip=True)

        # Clean up extra whitespace
        text = '\n'.join(line.strip() for line in text.splitlines() if line.strip())

        # Initialize the text splitter
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )

        # Split the text into chunks
        chunks = text_splitter.split_text(text)
        
        print(f"Successfully fetched and split content from {url}.")
        print(f"Created {len(chunks)} chunks.")
        
        # Display the first chunk as a sample
        if chunks:
            print("\n--- Sample Chunk (First 200 chars) ---")
            print(chunks[0][:200] + "...")
            print("------------------------------------")
            
        return chunks

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