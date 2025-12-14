import logging
import os
import sys
import argparse
from urllib.parse import urljoin, urlparse
from typing import List, Dict, Optional, Set, Any
import asyncio
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(backend_dir))

from playwright.sync_api import sync_playwright, Browser, Page # Playwright imports
from bs4 import BeautifulSoup, Tag, Comment
from langchain_text_splitters import RecursiveCharacterTextSplitter
import google.generativeai as genai
from dotenv import load_dotenv
import re # Added for regex operations
import numpy as np # Added for semantic de-duplication

# Import ChromaDB client
import chromadb

# Import add_chunks_to_collection from vector_store.py
from app.rag.vector_store import add_chunks_to_collection

logger = logging.getLogger(__name__)

load_dotenv()

# --- Configuration for Embeddings ---
EMBEDDING_MODEL_NAME = "models/text-embedding-004"
CHROMA_DB_PATH = "./chroma_data" # Local persistent storage for ChromaDB

class HMSREGDocumentationScraper:
    """
    A scraper for HMSREG documentation, designed to extract article content
    and links, and to perform a basic health check on the site structure.
    Uses Playwright for fetching dynamic content.
    """

    @staticmethod
    def calculate_cosine_similarity(embedding1, embedding2):
        """Calculates the cosine similarity between two embedding vectors."""
        if not isinstance(embedding1, np.ndarray):
            embedding1 = np.array(embedding1)
        if not isinstance(embedding2, np.ndarray):
            embedding2 = np.array(embedding2)
        
        dot_product = np.dot(embedding1, embedding2)
        norm_embedding1 = np.linalg.norm(embedding1)
        norm_embedding2 = np.linalg.norm(embedding2)
        
        if norm_embedding1 == 0 or norm_embedding2 == 0:
            return 0.0 # Handle zero-norm case to avoid division by zero
        return dot_product / (norm_embedding1 * norm_embedding2)

    def __init__(self, base_url: str, browser: Browser, chunk_size: int = 2000, chunk_overlap: int = 400, max_depth: int = 3):
        self.base_url = base_url
        self.visited_urls: Set[str] = set()
        self.domain = urlparse(base_url).netloc
        self.browser = browser # Playwright browser instance
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            is_separator_regex=False,
        )
        self.max_depth = max_depth # maximum crawling depth

        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key is None:
            logger.warning("GOOGLE_API_KEY is not set. Embedding generation will be disabled.")
            self.has_api_key = False
        else:
            genai.configure(api_key=api_key)
            self.has_api_key = True


    def _is_internal_link(self, url: str) -> bool:
        """Checks if a URL belongs to the same domain as the base_url."""
        return urlparse(url).netloc == self.domain

    def _get_absolute_url(self, href: str) -> Optional[str]:
        """Converts a relative URL to an absolute URL and filters for internal links."""
        absolute_url = urljoin(self.base_url, href)
        parsed_url = urlparse(absolute_url)
        clean_url = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path
        if parsed_url.query:
            clean_url += "?" + parsed_url.query

        if self._is_internal_link(clean_url):
            return clean_url
        return None

    def _fetch_page(self, url: str) -> Optional[Page]: # Returns Playwright Page object
        """Fetches a page using Playwright and returns a Page object if successful."""
        if url in self.visited_urls:
            return None

        logger.info(f"Fetching: {url} using Playwright")
        self.visited_urls.add(url)

        page = None
        try:
            page = self.browser.new_page()
            page.goto(url, wait_until="domcontentloaded")
            # Explicitly wait for the main content div to appear
            # Use the specific selector identified: div[data-object-id="dsProcedure"]
            page.wait_for_selector('div[data-object-id="dsProcedure"]', state='visible', timeout=10000)
            
            return page
        except Exception as e:
            logger.error(f"Error fetching {url} with Playwright: {e}")
            if page:
                page.close()
        return None

    def _extract_article_content(self, page: Page) -> Optional[str]: # Takes Playwright Page object
        """
        Extracts the main article content from a Playwright Page object.
        """
        main_content_locator = page.locator('div[data-object-id="dsProcedure"].content')
        if main_content_locator.count() > 0:
            html_content = main_content_locator.first.inner_html()
            soup = BeautifulSoup(html_content, 'html.parser')

            # Remove specific boilerplate/navigation elements
            for selector in ['header', 'footer', 'nav', 'script', 'style', '.skip-link', '.breadcrumb']:
                for tag in soup.find_all(selector):
                    tag.decompose()
            
            # Remove comments
            for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
                comment.extract()

            # Remove any remaining unwanted tags like empty spans or divs that are not structural
            for unwanted_tag in soup.find_all(['span', 'div'], class_=False, id=False):
                if not unwanted_tag.get_text(strip=True): # Remove empty or whitespace-only tags
                    unwanted_tag.decompose()

            text_content = soup.get_text(separator=' ', strip=True) # Use space separator to avoid word concatenation
            text_content = re.sub(r'\s+', ' ', text_content).strip() # Normalize whitespace
            
            if len(text_content) > 50:
                logger.debug(f"Extracted content from div[data-object-id='dsProcedure'] (length: {len(text_content)}).")
                return text_content
            else:
                logger.debug(f"Div[dsProcedure] content too short (length: {len(text_content)}).")

        # Fallback to body content if specific div is not sufficient, with similar cleaning
        body_content_html = page.locator('body').inner_html(timeout=1000)
        if body_content_html:
            soup = BeautifulSoup(body_content_html, 'html.parser')
            for selector in ['header', 'footer', 'nav', 'script', 'style', '.skip-link', '.breadcrumb']:
                for tag in soup.find_all(selector):
                    tag.decompose()
            for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
                comment.extract()
            for unwanted_tag in soup.find_all(['span', 'div'], class_=False, id=False):
                if not unwanted_tag.get_text(strip=True):
                    unwanted_tag.decompose()
            
            text_content = soup.get_text(separator=' ', strip=True)
            text_content = re.sub(r'\s+', ' ', text_content).strip()

            if len(text_content) > 50:
                logger.debug(f"Extracted content from body fallback (length: {len(text_content)}).")
                return text_content
        
        logger.debug(f"No significant content extracted by any selector.")
        return None

    def _parse_links(self, page: Page) -> List[str]: # Takes Playwright Page object
        """Extracts all unique, internal links from a Playwright Page object."""
        links = []
        all_hrefs = page.evaluate("Array.from(document.querySelectorAll('a[href]')).map(a => a.href)")
        logger.debug(f"Found {len(all_hrefs)} raw hrefs via Playwright: {all_hrefs}")

        for href in all_hrefs:
            absolute_url = self._get_absolute_url(href)
            if absolute_url and absolute_url not in self.visited_urls:
                links.append(absolute_url)
        unique_links = list(set(links))
        logger.debug(f"Found {len(unique_links)} unique internal links: {unique_links}")
        return unique_links


    def _split_text(self, text: str) -> List[str]:
        """
        Splits a given text into chunks using the configured text splitter
        and performs semantic de-duplication on the generated chunks.
        """
        initial_chunks = self.text_splitter.split_text(text)
        
        # --- Semantic De-duplication ---
        SIMILARITY_THRESHOLD = 0.95  # Tune this value as needed
        unique_chunks = []

        if not initial_chunks:
            return []
        
        if not self.has_api_key:
            logger.warning("GOOGLE_API_KEY is not set. Skipping semantic de-duplication.")
            return initial_chunks

        try:
            # Generate embeddings for all initial chunks
            all_chunk_embeddings_response = genai.embed_content(
                model=EMBEDDING_MODEL_NAME,
                content=initial_chunks,
                task_type="retrieval_document"
            )
            all_chunk_embeddings = all_chunk_embeddings_response["embedding"]

            if not all_chunk_embeddings:
                logger.warning("No embeddings generated for initial chunks. Skipping semantic de-duplication.")
                return initial_chunks

            # Add the first chunk unconditionally
            unique_chunks.append(initial_chunks[0])
            unique_chunk_embeddings = [all_chunk_embeddings[0]]

            for i in range(1, len(initial_chunks)):
                current_chunk = initial_chunks[i]
                current_embedding = all_chunk_embeddings[i]
                
                is_duplicate = False
                for unique_embedding in unique_chunk_embeddings:
                    similarity = self.calculate_cosine_similarity(current_embedding, unique_embedding)
                    if similarity > SIMILARITY_THRESHOLD:
                        is_duplicate = True
                        break
                
                if not is_duplicate:
                    unique_chunks.append(current_chunk)
                    unique_chunk_embeddings.append(current_embedding)
            
            logger.info(f"De-duplicated chunks: {len(initial_chunks)} initial, {len(unique_chunks)} unique.")
            return unique_chunks
        except Exception as e:
            logger.error(f"Error during semantic de-duplication: {e}. Returning all initial chunks.")
            return initial_chunks

    def _get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generates embeddings for a list of text chunks."""
        if not self.has_api_key:
            logger.error("Embedding model is not initialized (missing GOOGLE_API_KEY). Cannot generate embeddings.")
            return [[] for _ in texts]

        try:
            result = genai.embed_content(
                model=EMBEDDING_MODEL_NAME,
                content=texts,
                task_type="retrieval_document"
            )
            
            embeddings = result.get('embedding', [])
            
            logger.info(f"Generated embeddings for {len(texts)} chunks.")
            return embeddings
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            return [[] for _ in texts]


    def health_check(self) -> Dict[str, bool]:
        """
        Performs a basic health check on the documentation site's structure.
        This checks if key elements (e.g., a main article tag or body) are present on the base page.
        """
        logger.info(f"Performing health check on {self.base_url}")
        page = None
        try:
            page = self.browser.new_page()
            page.goto(self.base_url, wait_until="domcontentloaded")
            page.wait_for_selector('div[data-object-id="dsProcedure"]', state='visible', timeout=10000)
            
            site_reachable = True
            
            has_specific_content_div = page.locator('div[data-object-id="dsProcedure"]').count() > 0
            
            has_article_tag = page.locator('article').count() > 0 or page.locator('main').count() > 0
            has_body_tag = page.locator('body').count() > 0
            has_main_content_div_class = page.locator('.docs-content').count() > 0 or \
                                         page.locator('.article-content').count() > 0 or \
                                         page.locator('.main-content').count() > 0

            structure_ok = has_specific_content_div or has_article_tag or has_body_tag or has_main_content_div_class
            logger.info(f"Health check result for {self.base_url}: reachable={site_reachable}, structure_ok={structure_ok}")
            return {"site_reachable": site_reachable, "structure_ok": structure_ok}
        except Exception as e:
            logger.error(f"Health check failed for {self.base_url}: {e}")
            return {"site_reachable": False, "structure_ok": False}
        finally:
            if page:
                page.close()

    def scrape_site(self, start_url: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Scrapes the documentation site starting from the base_url or a specified start_url.
        Recursively follows internal links to collect all article content, then splits it into chunks and generates embeddings.
        """
        if start_url is None:
            start_url = self.base_url

        # Store (url, depth) tuples
        to_visit = [(start_url, 0)]
        all_processed_chunks: List[Dict[str, Any]] = []

        while to_visit:
            current_url, current_depth = to_visit.pop(0)

            if current_depth > self.max_depth:
                logger.info(f"Skipping {current_url} due to max depth ({self.max_depth}) reached.")
                continue

            if current_url in self.visited_urls:
                continue
            
            page = self._fetch_page(current_url)
            if page:
                title = page.title() if page.title() else "No Title"
                content = self._extract_article_content(page)
                
                if content:
                    # Attempt to extract a more specific title from the content
                    content_soup = BeautifulSoup(content, 'html.parser')
                    article_title_tag = content_soup.find(['h1', 'h2'])
                    article_title = article_title_tag.get_text(strip=True) if article_title_tag else title

                    logger.debug(f"Extracted content (snippet): {content[:200]}...")
                    chunks = self._split_text(content)
                    logger.info(f"Split content from {current_url} into {len(chunks)} chunks.")

                    if chunks:
                        embeddings = self._get_embeddings(chunks)
                        if len(embeddings) != len(chunks):
                            logger.error(f"Mismatch between number of chunks ({len(chunks)}) and embeddings ({len(embeddings)}) for {current_url}. Skipping embeddings.")
                            embeddings = [[] for _ in chunks]
                        
                        for i, chunk in enumerate(chunks):
                            chunk_embedding = embeddings[i] if embeddings and i < len(embeddings) else []
                            all_processed_chunks.append({
                                "url": current_url,
                                "title": article_title, # Use the more specific article title
                                "chunk_id": f"{current_url}#{i}",
                                "content": chunk,
                                "embedding": chunk_embedding,
                            })
                else:
                    logger.warning(f"No significant content extracted from: {current_url}")

                new_links = self._parse_links(page)
                if new_links:
                    logger.debug(f"Found {len(new_links)} new links on {current_url}: {new_links}")
                else:
                    logger.debug(f"No new links found on {current_url}.")
                for link in new_links:
                    if link not in self.visited_urls and link not in [item[0] for item in to_visit]:
                        to_visit.append((link, current_depth + 1))
                
                page.close()
            else:
                logger.error(f"Failed to fetch or parse: {current_url}")

        return all_processed_chunks

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(description="Scrape HMSREG documentation and store embeddings in ChromaDB.")
    parser.add_argument("--base_url", type=str, default="https://docs.hmsreg.com/?Area-ID=10000&ID=10379",
                        help="Base URL of the documentation site to scrape.")
    parser.add_argument("--chroma_path", type=str, default=CHROMA_DB_PATH,
                        help="Path for ChromaDB persistent storage.")
    parser.add_argument("--collection_name", type=str, default="hmsreg_docs",
                        help="Name of the ChromaDB collection.")
    parser.add_argument("--max_depth", type=int, default=3,
                        help="Maximum depth for crawling links. Default is 3.")
    parser.add_argument("--urls_file", type=str,
                        help="Path to a file containing a list of URLs to scrape, one per line. If provided, base_url and max_depth are ignored.")
    args = parser.parse_args()

    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        logger.error("GOOGLE_API_KEY environment variable is not set. Please set it to proceed with embedding generation.")
        exit(1)

    urls_to_scrape: List[str] = []
    if args.urls_file:
        try:
            with open(args.urls_file, 'r') as f:
                urls_to_scrape = [line.strip() for line in f if line.strip()]
            logger.info(f"Loaded {len(urls_to_scrape)} URLs from {args.urls_file}")
        except FileNotFoundError:
            logger.error(f"URLs file not found at {args.urls_file}. Aborting.")
            exit(1)
    else:
        # Use a default set of URLs if no file is provided, to ensure some data is processed
        # In a production setup, this would typically be args.base_url and let the scraper crawl
        urls_to_scrape = [
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
        

    with sync_playwright() as p:
        browser = p.chromium.launch() 
        try:
            # Initialize scraper with the first URL as base_url, but process DEBUG_URLS directly
            scraper = HMSREGDocumentationScraper(args.base_url, browser=browser, max_depth=args.max_depth)

            # Health check on the first URL if not using a urls_file
            if not args.urls_file:
                health_status = scraper.health_check()
                if not health_status["site_reachable"] or not health_status["structure_ok"]:
                    logger.error("Site not reachable or structure not as expected. Aborting ingestion.")
                    exit(1)

            logger.info(f"Starting to scrape {len(urls_to_scrape)} URLs...")
            all_processed_chunks_for_db: List[Dict[str, Any]] = []

            for url_to_process in urls_to_scrape:
                page = scraper._fetch_page(url_to_process)
                if page:
                    title = page.title() if page.title() else "No Title"
                    content = scraper._extract_article_content(page)
                    
                    if content:
                        content_soup = BeautifulSoup(content, 'html.parser')
                        article_title_tag = content_soup.find(['h1', 'h2'])
                        article_title = article_title_tag.get_text(strip=True) if article_title_tag else title

                        logger.debug(f"Extracted content (snippet): {content[:200]}...")
                        chunks = scraper._split_text(content) # This now includes semantic de-duplication
                        logger.info(f"Split content from {url_to_process} into {len(chunks)} chunks.")

                        if chunks:
                            embeddings = scraper._get_embeddings(chunks)
                            if len(embeddings) != len(chunks):
                                logger.error(f"Mismatch between number of chunks ({len(chunks)}) and embeddings ({len(embeddings)}) for {url_to_process}. Skipping embeddings.")
                                embeddings = [[] for _ in chunks]
                            
                            for i, chunk in enumerate(chunks):
                                chunk_embedding = embeddings[i] if embeddings and i < len(embeddings) else []
                                all_processed_chunks_for_db.append({
                                    "url": url_to_process,
                                    "title": article_title, 
                                    "chunk_id": f"{url_to_process}#{i}",
                                    "content": chunk,
                                    "embedding": chunk_embedding,
                                })
                    else:
                        logger.warning(f"No significant content extracted from: {url_to_process}")
                    
                    page.close() # Close page after processing
                else:
                    logger.error(f"Failed to fetch or parse: {url_to_process}")


            if all_processed_chunks_for_db:
                logger.info(f"Scraped, chunked, and embedded {len(all_processed_chunks_for_db)} total chunks for DB ingestion.")

                chroma_client = chromadb.PersistentClient(path=args.chroma_path)
                logger.info(f"ChromaDB client initialized with persistent path: {args.chroma_path}")

                add_chunks_to_collection(
                    client=chroma_client,
                    chunks=all_processed_chunks_for_db,
                    collection_name=args.collection_name
                )
                logger.info("Ingestion process completed successfully for DEBUG_URLS.")
            else:
                logger.warning("No chunks were processed or generated from DEBUG_URLS. ChromaDB not updated. This could mean no content was extracted or no links were found on the starting page.")
        finally:
            browser.close()
