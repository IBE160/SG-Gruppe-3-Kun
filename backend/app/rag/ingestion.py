import logging
import os
import argparse
from urllib.parse import urljoin, urlparse
from typing import List, Dict, Optional, Set, Any
import asyncio

from playwright.sync_api import sync_playwright, Browser, Page # Playwright imports
from bs4 import BeautifulSoup, Tag, Comment
from langchain_text_splitters import RecursiveCharacterTextSplitter
import google.generativeai as genai
from dotenv import load_dotenv
import re # Added for regex operations

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

    def __init__(self, base_url: str, browser: Browser, chunk_size: int = 800, chunk_overlap: int = 100, max_depth: int = 3):
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
        """Splits a given text into chunks using the configured text splitter."""
        return self.text_splitter.split_text(text)

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
    parser.add_argument("--base_url", type=str, default="https://docs.hmsreg.com/?Area-ID=10000&ID=10296",
                        help="Base URL of the documentation site to scrape.")
    parser.add_argument("--chroma_path", type=str, default=CHROMA_DB_PATH,
                        help="Path for ChromaDB persistent storage.")
    parser.add_argument("--collection_name", type=str, default="hmsreg_docs",
                        help="Name of the ChromaDB collection.")
    parser.add_argument("--max_depth", type=int, default=3,
                        help="Maximum depth for crawling links. Default is 3.")
    args = parser.parse_args()

    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        logger.error("GOOGLE_API_KEY environment variable is not set. Please set it to proceed with embedding generation.")
        exit(1)

    with sync_playwright() as p:
        browser = p.chromium.launch() # Use chromium, can be headless=True/False
        try:
            scraper = HMSREGDocumentationScraper(args.base_url, browser=browser, max_depth=args.max_depth)

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
        finally:
            browser.close()
