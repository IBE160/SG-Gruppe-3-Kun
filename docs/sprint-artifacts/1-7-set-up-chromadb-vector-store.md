# Story 1.7: Set up ChromaDB Vector Store

Status: ready-for-dev

## Story

As a backend developer,
I want to set up and configure the ChromaDB vector store,
so that I can efficiently store and retrieve document embeddings for the RAG pipeline.

## Acceptance Criteria

1. **ChromaDB Initialized:** The `chromadb` client library is integrated and configured.
2. **Persistent Storage:** The vector store is configured to persist data (e.g., to disk or a persistent volume, depending on environment).
3. **Manager Module:** `app/rag/vector_store.py` is created to encapsulate ChromaDB client interactions.
4. **Verification:** A basic test script or endpoint can successfully add a dummy embedding and retrieve it.

## Tasks / Subtasks

- [ ] **Install and Configure ChromaDB** (AC: 1)
  - [ ] Add `chromadb` to `pyproject.toml` (already should be there, verify).
  - [ ] Configure settings in `app/core/config.py` (e.g., `CHROMA_PERSIST_DIRECTORY`).
- [ ] **Implement Vector Store Module** (AC: 3)
  - [ ] Create `app/rag/vector_store.py`.
  - [ ] Implement `get_chroma_client()` function.
  - [ ] Define the collection name (e.g., `hmsreg_docs`).
- [ ] **Configure Persistence** (AC: 2)
  - [ ] For local dev: Use local file path.
  - [ ] For Railway (Staging): Determine strategy (Docker volume or ephemeral for now if POC). *Note: Tech Spec implies persistent storage is required.*
- [ ] **Verify Functionality** (AC: 4)
  - [ ] Create a test script `tests/test_chroma_init.py`.
  - [ ] Insert a mock vector.
  - [ ] Query the mock vector.
  - [ ] Assert results match.

## Dev Notes

- **Client Mode:** Use `chromadb.PersistentClient(path=...)` for local/server-based persistence.
- **Embeddings:** This story focuses on the *store*, not the *embedding generation*. However, testing it might require a dummy embedding function or just passing raw float lists.
- **Deployment Consideration:** On Railway, file-based persistence will be lost on redeploy unless a Volume is attached. For this story, setting up the *code* to handle a persistence path is sufficient. Adding the actual Volume can be a deployment task or noted in `README.md`.
- **Architecture Reference:** "Backend (FastAPI)" section mentions ChromaDB.

### Project Structure Notes

- `app/rag/vector_store.py`: New module for RAG specific infrastructure.
- `tests/`: Ensure tests are placed here.

### References

- [Source: docs/epics.md#Story-1.7-Set-up-ChromaDB-Vector-Store]
- [Source: docs/sprint-artifacts/tech-spec-epic-1.md#detailed-design]
- [Source: docs/architecture.md#backend-stack]

## Dev Agent Record

### Context Reference

- docs/sprint-artifacts/1-7-set-up-chromadb-vector-store.context.xml

### Agent Model Used

Gemini-2.5-Flash

### Debug Log References

### Completion Notes List

### File List

## Change Log

| Date | Author | Description |
|---|---|---|
| 2025-12-10 | BIP | Added Epics citation, Dev Agent Record, and initialized Change Log. |
