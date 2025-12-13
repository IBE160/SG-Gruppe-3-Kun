import logging
import os
import argparse
from urllib.parse import urljoin, urlparse
from typing import List, Dict, Optional, Set, Any

import httpx
from bs4 import BeautifulSoup, Tag
from langchain_text_splitters import RecursiveCharacterTextSplitter
import google.generativeai as genai
from dotenv import load_dotenv # Add this import

# Import ChromaDB client
import chromadb

# Import add_chunks_to_collection from vector_store.py
from app.rag.vector_store import add_chunks_to_collection

logger = logging.getLogger(__name__)

load_dotenv() # Add this line to load environment variables

# --- Configuration for Embeddings ---
# GOOGLE_API_KEY will be loaded from environment variables or passed during runtime
EMBEDDING_MODEL_NAME = "models/text-embedding-004"
CHROMA_DB_PATH = "./chroma_data" # Local persistent storage for ChromaDB

class HMSREGDocumentationScraper:
    """
    A scraper for HMSREG documentation, designed to extract article content
    and links, and to perform a basic health check on the site structure.
    """

    def __init__(self, base_url: str, client: httpx.Client, chunk_size: int = 800, chunk_overlap: int = 100):
        self.base_url = base_url
        self.visited_urls: Set[str] = set()
        self.domain = urlparse(base_url).netloc
        self.session = client # Use the externally managed httpx.Client
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            is_separator_regex=False,
        )

        api_key = os.getenv("GOOGLE_API_KEY") # Load API key from env variable
        if api_key is None:
            logger.warning("GOOGLE_API_KEY is not set. Embedding generation will be disabled.")
            self.has_api_key = False
        else:
            genai.configure(api_key=api_key) # Use the loaded API key
            self.has_api_key = True


    def _is_internal_link(self, url: str) -> bool:
        """Checks if a URL belongs to the same domain as the base_url."""
        return urlparse(url).netloc == self.domain

    def _get_absolute_url(self, href: str) -> Optional[str]:
        """Converts a relative URL to an absolute URL and filters for internal links."""
        absolute_url = urljoin(self.base_url, href)
        if self._is_internal_link(absolute_url):
            return absolute_url
        return None

    def _fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """Fetches a page and returns a BeautifulSoup object if successful."""
        if url in self.visited_urls:
            return None # Already visited

        logger.info(f"Fetching: {url}")
        self.visited_urls.add(url)

        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
            return BeautifulSoup(response.text, 'html.parser')
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error fetching {url}: {e.response.status_code} - {e.response.text}")
        except httpx.RequestError as e:
            logger.error(f"Request error fetching {url}: {e}")
        return None

    def _parse_links(self, soup: BeautifulSoup) -> List[str]:
        """Extracts all unique, internal links from a BeautifulSoup object."""
        links = []
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            absolute_url = self._get_absolute_url(href)
            if absolute_url and absolute_url not in self.visited_urls:
                links.append(absolute_url)
        return list(set(links)) # Return unique links

    def _extract_article_content(self, soup: BeautifulSoup) -> Optional[str]:
        """
        Extracts the main article content from a BeautifulSoup object.
        This method needs to be robust to the specific structure of docs.hmsreg.com.
        Placeholder implementation: Tries common article content selectors.
        """
        # Prioritize known content areas
        content_tags = soup.find(['article', 'main'], class_=['docs-content', 'article-content', 'main-content'])
        if content_tags:
            for unwanted_class in ['sidebar', 'nav', 'footer', 'header', 'meta-data']:
                for tag in content_tags.find_all(class_=unwanted_class):
                    tag.decompose()
            return content_tags.get_text(separator='\n', strip=True)

        # Fallback to body content, but try to remove common non-article elements
        body = soup.find('body')
        if body:
            # Remove navigation, footer, header, sidebar elements if they are direct children or commonly found
            for selector in ['nav', 'footer', 'header', 'aside', '.sidebar', '#sidebar', '.header', '#header', '.footer', '#footer']:
                for tag in body.find_all(selector):
                    tag.decompose()
            return body.get_text(separator='\n', strip=True)
        logger.debug(f"No significant content extracted by default selectors for {soup.title.string if soup.title else 'Untitled'}.")
        return None

    def _split_text(self, text: str) -> List[str]:
        """Splits a given text into chunks using the configured text splitter."""
        return self.text_splitter.split_text(text)

    def _get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generates embeddings for a list of text chunks."""
        if not self.has_api_key:
            logger.error("Embedding model is not initialized (missing GOOGLE_API_KEY). Cannot generate embeddings.")
            return [[] for _ in texts] # Return empty embeddings

        try:
            # Using genai.embed_content to generate embeddings.
            # Note: For batch processing, we can iterate or use batch methods if available.
            # The API supports batch embedding via embed_content if content is a list?
            # Documentation says content is str or list of str.
            
            result = genai.embed_content(
                model=EMBEDDING_MODEL_NAME,
                content=texts,
                task_type="retrieval_document"
            )
            
            # The result for a list input contains a list of embeddings under 'embedding'
            embeddings = result.get('embedding', [])
            
            logger.info(f"Generated embeddings for {len(texts)} chunks.")
            return embeddings
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            # In a production system, implement retry logic or more robust error handling
            return [[] for _ in texts] # Return empty embeddings on error


    def health_check(self) -> Dict[str, bool]:
        """
        Performs a basic health check on the documentation site's structure.
        This checks if key elements (e.g., a main article tag or body) are present on the base page.
        """
        logger.info(f"Performing health check on {self.base_url}")
        soup = self._fetch_page(self.base_url)
        if not soup:
            return {"site_reachable": False, "structure_ok": False}

        site_reachable = True
        # Check for common article content tags or general body content
        has_article_tag = bool(soup.find(['article', 'main']))
        has_body_tag = bool(soup.find('body'))
        has_main_content_div = bool(soup.find(class_=['docs-content', 'article-content', 'main-content']))

        structure_ok = has_article_tag or has_body_tag or has_main_content_div
        logger.info(f"Health check result for {self.base_url}: reachable={site_reachable}, structure_ok={structure_ok}")
        return {"site_reachable": site_reachable, "structure_ok": structure_ok}

    def scrape_site(self, start_url: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Scrapes the documentation site starting from the base_url or a specified start_url.
        Recursively follows internal links to collect all article content, then splits it into chunks and generates embeddings.
        """
        if start_url is None:
            start_url = self.base_url

        to_visit = [start_url]
        all_processed_chunks: List[Dict[str, Any]] = []

        while to_visit:
            current_url = to_visit.pop(0)
            if current_url in self.visited_urls:
                continue

            soup = self._fetch_page(current_url)
            if soup:
                title_tag = soup.find('title')
                title = title_tag.get_text(strip=True) if title_tag else "No Title"
                content = self._extract_article_content(soup)
                
                if content:
                    logger.debug(f"Extracted content (snippet): {content[:200]}...") # Log snippet
                    chunks = self._split_text(content)
                    logger.info(f"Split content from {current_url} into {len(chunks)} chunks.")

                    if chunks:
                        # Generate embeddings for all chunks from the current page
                        embeddings = self._get_embeddings(chunks)
                        if len(embeddings) != len(chunks):
                            logger.error(f"Mismatch between number of chunks ({len(chunks)}) and embeddings ({len(embeddings)}) for {current_url}. Skipping embeddings.")
                            embeddings = [[] for _ in chunks] # Ensure list of lists for consistency
                        
                        for i, chunk in enumerate(chunks):
                            chunk_embedding = embeddings[i] if embeddings and i < len(embeddings) else [] # Ensure index is valid
                            all_processed_chunks.append({
                                "url": current_url,
                                "title": title,
                                "chunk_id": f"{current_url}#{i}",
                                "content": chunk,
                                "embedding": chunk_embedding, # Add the embedding to the chunk data
                            })
                else:
                    logger.warning(f"No significant content extracted from: {current_url}")

                new_links = self._parse_links(soup)
                if new_links:
                    logger.debug(f"Found {len(new_links)} new links on {current_url}: {new_links}")
                else:
                    logger.debug(f"No new links found on {current_url}.")
                for link in new_links:
                    if link not in self.visited_urls and link not in to_visit:
                        to_visit.append(link)
            else:
                logger.error(f"Failed to fetch or parse: {current_url}")

        return all_processed_chunks

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG) # Change to DEBUG for more verbosity

    parser = argparse.ArgumentParser(description="Scrape HMSREG documentation and store embeddings in ChromaDB.")
    parser.add_argument("--base_url", type=str, default="https://docs.hmsreg.com/",
                        help="Base URL of the documentation site to scrape.")
    parser.add_argument("--chroma_path", type=str, default=CHROMA_DB_PATH,
                        help="Path for ChromaDB persistent storage.")
    parser.add_argument("--collection_name", type=str, default="hmsreg_docs",
                        help="Name of the ChromaDB collection.")
    args = parser.parse_args()

    # Attempt to load GOOGLE_API_KEY from environment variable
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        logger.error("GOOGLE_API_KEY environment variable is not set. Please set it to proceed with embedding generation.")
        exit(1)

    with httpx.Client(follow_redirects=True) as client:
        scraper = HMSREGDocumentationScraper(args.base_url, client=client)

        health_status = scraper.health_check()
        if not health_status["site_reachable"] or not health_status["structure_ok"]:
            logger.error("Site not reachable or structure not as expected. Aborting ingestion.")
            exit(1)

        logger.info(f"Starting to scrape {args.base_url}...")
        processed_chunks = scraper.scrape_site()

        if processed_chunks:
            logger.info(f"Scraped, chunked, and embedded {len(processed_chunks)} total chunks.")

            chroma_client = chromadb.PersistentClient(path=args.chroma_path)
            logger.info(f"ChromaDB client initialized with persistent path: {args.chroma_path}")

            add_chunks_to_collection(
                client=chroma_client,
                chunks=processed_chunks,
                collection_name=args.collection_name
            )
            logger.info("Ingestion process completed successfully.")
        else:
            logger.warning("No chunks were processed or generated. ChromaDB not updated. This could mean no content was extracted or no links were found on the starting page.")
