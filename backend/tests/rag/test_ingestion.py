import pytest
from unittest.mock import MagicMock, patch
import httpx
from bs4 import BeautifulSoup
import os

from app.rag.ingestion import HMSREGDocumentationScraper
from app.rag.vector_store import add_chunks_to_collection # Import to mock it

# Mock data for testing
MOCK_HTML_CONTENT = """
<!DOCTYPE html>
<html>
<head><title>Test Article</title></head>
<body>
    <header>Nav Header</header>
    <main class="docs-content">
        <h1>Welcome to the HMSREG Documentation</h1>
        <p>This is some content about <a href="/internal-link">internal procedures</a>.</p>
        <p>Here is more text for chunking purposes. It needs to be long enough to be split.
           Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor
           incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis
           nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
           Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore
           eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident,
           sunt in culpa qui officia deserunt mollit anim id est laborum.
           </p>
        <p>Another paragraph. <a href="https://external.com">External Link</a>.</p>
    </main>
    <footer>Footer Content</footer>
</body>
</html>
"""

MOCK_HTML_CONTENT_SHORT = """
<!DOCTYPE html>
<html>
<head><title>Short Article</title></head>
<body>
    <article><h1>Short Content</h1><p>This is short.</p></article>
</body>
</html>
"""

# Define a simple MockHttpResponse class to mimic httpx.Response for side_effect
class MockHttpResponse:
    def __init__(self, status_code, text_content, headers=None):
        self.status_code = status_code
        self._text_content = text_content
        self.headers = headers if headers is not None else {}

    @property
    def text(self):
        return self._text_content

    def raise_for_status(self):
        if 400 <= self.status_code < 600:
            raise httpx.HTTPStatusError("Bad response", request=httpx.Request("GET", "http://test.com"), response=self)

@pytest.fixture
def mock_httpx_client():
    """Mocks the httpx.Client.get method."""
    with patch('httpx.Client') as mock_client:
        mock_client_instance = mock_client.return_value
        mock_response = MagicMock(spec=httpx.Response)
        mock_response.status_code = 200
        mock_response.text = MOCK_HTML_CONTENT
        mock_response.raise_for_status.return_value = None
        mock_client_instance.get.return_value = mock_response
        yield mock_client_instance

@pytest.fixture
def mock_genai_embed_content():
    """Mocks genai.embed_content to return dummy embeddings."""
    with patch('app.rag.ingestion.genai.embed_content') as mock_embed:
        def side_effect(model, content, task_type):
            if isinstance(content, list):
                return {'embedding': [[0.1] * 768 for _ in content]}
            else:
                return {'embedding': [0.1] * 768}
                
        mock_embed.side_effect = side_effect
        yield mock_embed

@pytest.fixture
def mock_chroma_client():
    """Mocks the chromadb.PersistentClient and its collection add method."""
    with patch('chromadb.PersistentClient') as mock_client_class:
        mock_client_instance = mock_client_class.return_value
        mock_collection = MagicMock()
        mock_client_instance.get_or_create_collection.return_value = mock_collection
        mock_collection.add.return_value = None # add method doesn't return anything significant by default
        yield mock_client_instance, mock_collection

# --- Test Scraper ---

def test_scraper_health_check_reachable(mock_httpx_client):
    """Verifies health check for a reachable and structured site."""
    scraper = HMSREGDocumentationScraper(base_url="http://test.com", client=mock_httpx_client)
    status = scraper.health_check()
    assert status["site_reachable"] is True
    assert status["structure_ok"] is True

def test_scraper_health_check_unreachable():
    """Verifies health check for an unreachable site."""
    with patch('httpx.Client') as mock_client:
        mock_client_instance = mock_client.return_value
        mock_client_instance.get.side_effect = httpx.RequestError("Network error", request=httpx.Request("GET", "http://test.com"))
        scraper = HMSREGDocumentationScraper(base_url="http://test.com", client=mock_client_instance)
        status = scraper.health_check()
        assert status["site_reachable"] is False
        assert status["structure_ok"] is False

def test_extract_article_content(mock_httpx_client):
    """Verifies that article content is extracted correctly."""
    scraper = HMSREGDocumentationScraper(base_url="http://test.com", client=mock_httpx_client)
    soup = BeautifulSoup(MOCK_HTML_CONTENT, 'html.parser')
    content = scraper._extract_article_content(soup)
    assert "Welcome to the HMSREG Documentation" in content
    assert "Nav Header" not in content
    assert "Footer Content" not in content
    assert "internal procedures" in content # Ensure links within content are kept
    assert "External Link" in content


def test_parse_links(mock_httpx_client):
    """Verifies that internal links are parsed correctly."""
    scraper = HMSREGDocumentationScraper(base_url="http://test.com", client=mock_httpx_client)
    soup = BeautifulSoup(MOCK_HTML_CONTENT, 'html.parser')
    links = scraper._parse_links(soup)
    expected_link = "http://test.com/internal-link"
    assert expected_link in links
    assert "https://external.com" not in links # External links should be filtered out

# --- Test Text Splitter ---

def test_text_splitter_chunks_text():
    """Verifies that the text splitter correctly chunks text."""
    with httpx.Client(follow_redirects=True) as client:
        scraper = HMSREGDocumentationScraper(base_url="http://test.com", client=client, chunk_size=50, chunk_overlap=10)
        text = "A" * 100 # A long string to ensure splitting
        chunks = scraper._split_text(text)
        assert len(chunks) > 1
        assert all(len(chunk) <= 50 for chunk in chunks)
        assert chunks[0].endswith("A") # Check for overlap if first chunk is long enough

# --- Test Embedding Generation ---

def test_embedding_generation(mock_genai_embed_content):
    """Verifies that embeddings are generated and returned using genai."""
    with patch.dict(os.environ, {"GOOGLE_API_KEY": "dummy_key"}):
        with httpx.Client(follow_redirects=True) as client:
            scraper = HMSREGDocumentationScraper(base_url="http://test.com", client=client)
            texts = ["hello world", "how are you"]
            embeddings = scraper._get_embeddings(texts)
            assert len(embeddings) == len(texts)
            assert len(embeddings[0]) == 768
            mock_genai_embed_content.assert_called_once()

def test_embedding_generation_no_api_key():
    """Verifies that embedding generation handles missing API key."""
    with patch.dict(os.environ, {}, clear=True): # Clear GOOGLE_API_KEY from env
        with httpx.Client(follow_redirects=True) as client:
            scraper = HMSREGDocumentationScraper(base_url="http://test.com", client=client)
            texts = ["hello world"]
            embeddings = scraper._get_embeddings(texts)
            assert embeddings == [[]]

# --- Test Vector Storage (Mocked) ---

def test_add_chunks_to_collection(mock_chroma_client):
    """Verifies that add_chunks_to_collection correctly calls ChromaDB client."""
    mock_client_instance, mock_collection = mock_chroma_client
    chunks = [
        {"url": "http://test.com/1", "title": "Title 1", "chunk_id": "id1", "content": "content 1", "embedding": [0.1, 0.2]},
        {"url": "http://test.com/2", "title": "Title 2", "chunk_id": "id2", "content": "content 2", "embedding": [0.3, 0.4]},
    ]
    
    added_count = add_chunks_to_collection(mock_client_instance, chunks)

    assert added_count == 2
    mock_client_instance.get_or_create_collection.assert_called_once_with(name="hmsreg_docs")
    mock_collection.add.assert_called_once()
    args, kwargs = mock_collection.add.call_args
    assert kwargs['documents'] == ["content 1", "content 2"]
    assert kwargs['ids'] == ["id1", "id2"]
    assert kwargs['embeddings'] == [[0.1, 0.2], [0.3, 0.4]]
    assert kwargs['metadatas'] == [
        {"url": "http://test.com/1", "title": "Title 1", "chunk_id": "id1"},
        {"url": "http://test.com/2", "title": "Title 2", "chunk_id": "id2"},
    ]

def test_add_chunks_to_collection_empty_embeddings(mock_chroma_client):
    """Verifies that chunks with empty embeddings are not added."""
    mock_client_instance, mock_collection = mock_chroma_client
    chunks = [
        {"url": "http://test.com/1", "title": "Title 1", "chunk_id": "id1", "content": "content 1", "embedding": [0.1, 0.2]},
        {"url": "http://test.com/2", "title": "Title 2", "chunk_id": "id2", "content": "content 2", "embedding": []}, # Empty embedding
    ]
    
    added_count = add_chunks_to_collection(mock_client_instance, chunks)

    assert added_count == 1 # Only one chunk should be added
    mock_collection.add.assert_called_once()
    args, kwargs = mock_collection.add.call_args
    assert kwargs['documents'] == ["content 1"]
    assert kwargs['ids'] == ["id1"]
    assert kwargs['embeddings'] == [[0.1, 0.2]]
    assert kwargs['metadatas'] == [
        {"url": "http://test.com/1", "title": "Title 1", "chunk_id": "id1"},
    ]

# --- Integration Test ---

def test_full_ingestion_pipeline_integration(
    mock_httpx_client, # This is the mocked client instance from the fixture
    mock_genai_embed_content,
    mock_chroma_client,
):
    """
    Tests the full ingestion pipeline from scraping to adding to ChromaDB
    using mocked external dependencies.
    """
    base_url = "http://test.com"
    # Configure mock_httpx_client.get.side_effect
    mock_httpx_client.get.side_effect = [
        MockHttpResponse(200, MOCK_HTML_CONTENT_SHORT),
        MockHttpResponse(200, MOCK_HTML_CONTENT),
        MockHttpResponse(200, MOCK_HTML_CONTENT_SHORT),
    ]

    mock_chroma_client_instance, mock_collection = mock_chroma_client

    with patch.dict(os.environ, {"GOOGLE_API_KEY": "dummy_key"}):
        # Pass the mocked client from the fixture
        scraper = HMSREGDocumentationScraper(base_url=base_url, client=mock_httpx_client, chunk_size=50, chunk_overlap=10)
            
        # Manually call scrape_site which includes text splitting and embedding
        processed_chunks = scraper.scrape_site()

        # Then call add_chunks_to_collection
        added_count = add_chunks_to_collection(
            client=mock_chroma_client_instance,
            chunks=processed_chunks,
            collection_name="hmsreg_docs"
        )

        assert added_count > 0
        assert mock_collection.add.call_count == 1
        
        # Verify content and embeddings are passed to ChromaDB mock
        args, kwargs = mock_collection.add.call_args
        assert len(kwargs['documents']) == added_count
        assert len(kwargs['embeddings']) == added_count
        assert all(len(e) == 768 for e in kwargs['embeddings']) # Check embedding dimension
