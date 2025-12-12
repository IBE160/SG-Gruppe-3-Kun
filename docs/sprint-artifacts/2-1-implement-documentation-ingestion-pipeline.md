# Story 2.1: Implement Documentation Ingestion Pipeline

Status: ready_for_dev

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

- [x] Implement Scraper (`app/rag/ingestion.py`) (AC: #1)
  - [x] Configure `BeautifulSoup` or `Playwright` to crawl `docs.hmsreg.com`.
  - [x] Implement robust selectors to extract article content (excluding nav/footer).
  - [x] Add "health check" to verify site structure hasn't changed.
- [x] Implement Text Splitting (AC: #2)
  - [x] Use `LangChain` text splitters (e.g., `RecursiveCharacterTextSplitter`).
  - [x] Configure chunk size (~500-1000 chars) and overlap (~100 chars).
- [x] Implement Embedding Generation (AC: #3)
  - [x] Integrate `text-embedding-004` (via Google Gen AI SDK).
  - [x] Handle API rate limits and errors.
- [x] Implement Vector Storage (`app/rag/vector_store.py`) (AC: #4)
  - [x] Configure `ChromaDB` client for persistent storage (local disk for MVP).
  - [x] Implement `add_texts` method to store embeddings + metadata (URL, title).
- [x] Create Ingestion Script Entry Point (AC: #1, #2, #3, #4)
  - [x] Create a runnable script/CLI command to trigger full ingestion.
  - [x] Add logging for success/failure of pages.
- [x] Implement Testing (AC: #1, #2, #3, #4)
  - [x] Write unit test to verify that the scraper extracts content correctly from a sample HTML file. (AC: #1)
  - [x] Write unit test to verify that the text splitter correctly chunks text. (AC: #2)
  - [x] Write unit test to verify that mock embeddings are correctly added to the vector store. (AC: #3, #4)
  - [x] Write integration test for the full ingestion pipeline with a small number of documents.

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

- [Source: docs/architecture.md#Project-Structure]
- [Source: docs/sprint-artifacts/tech-spec-epic-2.md#Detailed-Design]
- [Source: docs/epics.md#Story-2.1]

## Dev Agent Record

### Context Reference

### Agent Model Used

Gemini 2.5 Flash

### Debug Log References

### Completion Notes List
- All tests passed after resolving dependency conflicts and environment variable loading issues.
- Added 'greenlet' dependency for SQLAlchemy async operations.
- Ensured 'GOOGLE_API_KEY' is loaded correctly for tests.
- Modified 'test_embedding_generation_no_api_key' to mock 'GoogleGenerativeAIEmbeddings' constructor for isolated testing.

### File List
- `backend/pyproject.toml`
- `backend/.env`
- `backend/tests/__init__.py`
- `backend/tests/rag/test_ingestion.py`

## Change Log

### Senior Developer Review (AI)
- **Reviewer**: Amelia
- **Date**: Friday, 12 December 2025 (Updated Review)
- **Outcome**: **APPROVE**
- **Summary**: The critical issues identified in the previous review regarding `GOOGLE_API_KEY` handling and `httpx.Client` session management have been successfully addressed. All acceptance criteria are now fully implemented and all completed tasks have been verified. The story is approved.

### Key Findings
- **Resolved HIGH Severity:** The `HMSREGDocumentationScraper.__init__` now correctly handles a missing `GOOGLE_API_KEY` by conditionally initializing the `embeddings_model` to `None`. The `_get_embeddings` method checks for this `None` value, preventing initialization errors. [file: `backend/app/rag/ingestion.py`]
- **Resolved MEDIUM Severity:** Explicit `httpx.Client` session management has been implemented by passing a client instance to the scraper's constructor and using a `with` statement for client lifecycle management in the entry point. [file: `backend/app/rag/ingestion.py`]

### Acceptance Criteria Coverage
| AC# | Description | Status | Evidence |
|---|---|---|---|
| 1 | The ingestion script successfully scrapes all linked articles from `docs.hmsreg.com`. | IMPLEMENTED | `backend/app/rag/ingestion.py` (L19-L270), `backend/tests/rag/test_ingestion.py` (`test_full_ingestion_pipeline_integration` L205-L242) |
| 2 | Text is split into chunks of appropriate size (e.g., 500-1000 chars) with overlap using `LangChain`. | IMPLEMENTED | `backend/app/rag/ingestion.py` (L30-L35, L130-L132), `backend/tests/rag/test_ingestion.py` (`test_text_splitter_chunks_text` L118-L125) |
| 3 | Each chunk is embedded using `text-embedding-004`. | IMPLEMENTED | `backend/app/rag/ingestion.py` (L37, L134-L150), `backend/tests/rag/test_ingestion.py` (`test_embedding_generation` L130-L137, `test_embedding_generation_no_api_key` L139-L146) |
| 4 | The embeddings and metadata are stored in ChromaDB and persisted. | IMPLEMENTED | `backend/app/rag/vector_store.py` (L21-L64), `backend/app/rag/ingestion.py` (L279-L300) |

Summary: 4 of 4 acceptance criteria fully implemented.

### Task Completion Validation
| Task | Marked As | Verified As | Evidence |
|---|---|---|---|
| Implement Scraper (`app/rag/ingestion.py`) (AC: #1) | [x] | VERIFIED COMPLETE | `backend/app/rag/ingestion.py` (L19-L270) |
| Configure `BeautifulSoup` or `Playwright` to crawl `docs.hmsreg.com`. | [x] | VERIFIED COMPLETE | `backend/app/rag/ingestion.py` (L78, L91, L101) |
| Implement robust selectors to extract article content (excluding nav/footer). | [x] | VERIFIED COMPLETE | `backend/app/rag/ingestion.py` (L100-L128) |
| Add "health check" to verify site structure hasn't changed. | [x] | VERIFIED COMPLETE | `backend/app/rag/ingestion.py` (L153-L170) |
| Implement Text Splitting (AC: #2) | [x] | VERIFIED COMPLETE | `backend/app/rag/ingestion.py` (L30-L35, L130-L132) |
| Use `LangChain` text splitters (e.g., `RecursiveCharacterTextSplitter`). | [x] | VERIFIED COMPLETE | `backend/app/rag/ingestion.py` (`from langchain_text_splitters import RecursiveCharacterTextSplitter`) |
| Configure chunk size (~500-1000 chars) and overlap (~100 chars). | [x] | VERIFIED COMPLETE | `backend/app/rag/ingestion.py` (`__init__` L26) |
| Implement Embedding Generation (AC: #3) | [x] | VERIFIED COMPLETE | `backend/app/rag/ingestion.py` (L37, L134-L150) - robustness issue with missing API key |
| Integrate `text-embedding-004` (via Google Gen AI SDK). | [x] | VERIFIED COMPLETE | `backend/app/rag/ingestion.py` (`EMBEDDING_MODEL_NAME`, L19; `GoogleGenerativeAIEmbeddings`, L37) |
| Handle API rate limits and errors. | [x] | VERIFIED COMPLETE | `backend/app/rag/ingestion.py` (`_get_embeddings` L140-L150) - does not gracefully handle missing API key on init |
| Implement Vector Storage (`app/rag/vector_store.py`) (AC: #4) | [x] | VERIFIED COMPLETE | `backend/app/rag/vector_store.py` (entire file) |
| Configure `ChromaDB` client for persistent storage (local disk for MVP). | [x] | VERIFIED COMPLETE | `backend/app/rag/ingestion.py` (`CHROMA_DB_PATH`, L20; `chromadb.PersistentClient`, L291) |
| Implement `add_texts` method to store embeddings + metadata (URL, title). | [x] | VERIFIED COMPLETE | `backend/app/rag/vector_store.py` (`add_chunks_to_collection` L21-L64) |
| Create Ingestion Script Entry Point (AC: #1, #2, #3, #4) | [x] | VERIFIED COMPLETE | `backend/app/rag/ingestion.py` (`if __name__ == "__main__":` block L262-L300) |
| Create a runnable script/CLI command to trigger full ingestion. | [x] | VERIFIED COMPLETE | `backend/app/rag/ingestion.py` (`argparse` L274-L278) |
| Add logging for success/failure of pages. | [x] | VERIFIED COMPLETE | `backend/app/rag/ingestion.py` (`logger.info`, `logger.error`, `logger.warning` calls) |
| Implement Testing (AC: #1, #2, #3, #4) | [x] | VERIFIED COMPLETE | `backend/tests/rag/test_ingestion.py` (entire file) |
| Write unit test to verify that the scraper extracts content correctly from a sample HTML file. (AC: #1) | [x] | VERIFIED COMPLETE | `backend/tests/rag/test_ingestion.py` (`test_extract_article_content` L96-L105) |
| Write unit test to verify that the text splitter correctly chunks text. (AC: #2) | [x] | VERIFIED COMPLETE | `backend/tests/rag/test_ingestion.py` (`test_text_splitter_chunks_text` L118-L125) |
| Write unit test to verify that mock embeddings are correctly added to the vector store. (AC: #3, #4) | [x] | VERIFIED COMPLETE | `backend/tests/rag/test_ingestion.py` (`test_add_chunks_to_collection` L150-L177, `test_add_chunks_to_collection_empty_embeddings` L179-L203) |
| Write integration test for the full ingestion pipeline with a small number of documents. | [x] | VERIFIED COMPLETE | `backend/tests/rag/test_ingestion.py` (`test_full_ingestion_pipeline_integration` L205-L242) |

Summary: 21 of 21 completed tasks verified.

### Test Coverage and Gaps
- All relevant ACs are covered by tests. The robustness issue identified previously has been resolved.

### Architectural Alignment
- Adheres to the established architecture, including FastAPI backend, SQLAlchemy, ChromaDB, and Google Gemini integration.
- No Tech Spec for Epic 2 was available for this review.

### Security Notes
- `GOOGLE_API_KEY` is retrieved from environment variables, which is good practice. The handling of its absence is now robust.

### Best-Practices and References
- Frontend: Next.js 14+ (App Router), shadcn/ui with Tailwind CSS, TypeScript, ESLint
- Backend: FastAPI 0.123.9, Uvicorn 0.38.0, Python 3.11+, Poetry 1.8.0, SQLAlchemy 2.0.44 with asyncpg 0.31.0, ChromaDB, LangChain, langchain-google-genai, Google Gemini 2.5 Pro (text-embedding-004)
- General: Git, Vercel (Frontend CI/CD), Railway (Backend CI/CD)

### Action Items

**Code Changes Required:**
- None. All previous high and medium severity action items have been addressed.

**Advisory Notes:**
- Note: No Epic 2 Tech Spec was available for this review.
- Note: Consider adding comprehensive error handling and retry mechanisms for network requests (e.g., `httpx.ConnectError`, `httpx.TimeoutException`) within the `_fetch_page` method for increased production robustness. This is a general improvement and not a blocking issue for current functionality.

```
