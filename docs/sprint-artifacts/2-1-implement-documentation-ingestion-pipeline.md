# Story 2.1: Implement Documentation Ingestion Pipeline

Status: drafted

## Story

As a backend developer,
I want to create a pipeline to scrape and process official HMSREG documentation from `docs.hmsreg.com`,
so that the chatbot has a comprehensive and up-to-date knowledge base to draw answers from.

## Acceptance Criteria

1. The ingestion script successfully scrapes all linked articles from `docs.hmsreg.com`.
2. Text is split into chunks of appropriate size (e.g., 500-1000 chars) with overlap using `LangChain`.
3. Each chunk is embedded using `text-embedding-004`.
4. The embeddings and metadata are stored in ChromaDB and persisted.

## Tasks / Subtasks

- [ ] Implement Scraper (`app/rag/ingestion.py`)
  - [ ] Configure `BeautifulSoup` or `Playwright` to crawl `docs.hmsreg.com`.
  - [ ] Implement robust selectors to extract article content (excluding nav/footer).
  - [ ] Add "health check" to verify site structure hasn't changed.
- [ ] Implement Text Splitting
  - [ ] Use `LangChain` text splitters (e.g., `RecursiveCharacterTextSplitter`).
  - [ ] Configure chunk size (~500-1000 chars) and overlap (~100 chars).
- [ ] Implement Embedding Generation
  - [ ] Integrate `text-embedding-004` (via Google Gen AI SDK).
  - [ ] Handle API rate limits and errors.
- [ ] Implement Vector Storage (`app/rag/vector_store.py`)
  - [ ] Configure `ChromaDB` client for persistent storage (local disk for MVP).
  - [ ] Implement `add_texts` method to store embeddings + metadata (URL, title).
- [ ] Create Ingestion Script Entry Point
  - [ ] Create a runnable script/CLI command to trigger full ingestion.
  - [ ] Add logging for success/failure of pages.

## Dev Notes

- **Architecture**:
  - `app/rag/ingestion.py`: Main logic for scraping/chunking.
  - `app/rag/vector_store.py`: Wrapper for ChromaDB interactions.
- **Dependencies**: `beautifulsoup4`, `langchain-text-splitters`, `chromadb`, `google-generativeai`.
- **Testing**:
  - Verify ingestion count > 0.
  - Test `vector_store` with a mock embedding.

### Project Structure Notes

- Ensure `app/rag/` directory exists.
- `ingestion.py` should be independent of the main API application logic (runnable as a job).

### References

- [Source: docs/sprint-artifacts/tech-spec-epic-2.md#Detailed-Design]
- [Source: docs/epics.md#Story-2.1]

## Dev Agent Record

### Context Reference

### Agent Model Used

Gemini 2.5 Flash

### Debug Log References

### Completion Notes List

### File List
