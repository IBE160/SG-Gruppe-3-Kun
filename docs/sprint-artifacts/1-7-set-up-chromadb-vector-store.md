# Story 1.7: Set up ChromaDB Vector Store

Status: done

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

-   [x] **Install and Configure ChromaDB** (AC: 1)
    -   [x] Add `chromadb` to `pyproject.toml` (already should be there, verify).
    -   [x] Configure settings in `app/core/config.py` (e.g., `CHROMA_PERSIST_DIRECTORY`).
-   [x] **Implement Vector Store Module** (AC: 3)
    -   [x] Create `app/rag/vector_store.py`.
    -   [x] Implement `get_chroma_client()` function.
    -   [x] Define the collection name (e.g., `hmsreg_docs`).
-   [x] **Configure Persistence** (AC: 2)
    -   [x] For local dev: Use local file path.
    -   [x] For Railway (Staging): Determine strategy (Docker volume or ephemeral for now if POC). _Note: Tech Spec implies persistent storage is required._
-   [x] **Verify Functionality** (AC: 4)
    -   [x] Create a test script `tests/test_chroma_init.py`.
    -   [x] Insert a mock vector.
    -   [x] Query the mock vector.
    -   [x] Assert results match.

### Review Follow-ups (AI)

-   [x] [AI-Review][Med] Refactor `get_chroma_client` in `backend/app/rag/vector_store.py` to leverage FastAPI's dependency injection system (e.g., using `Depends` or a lifecycle event handler `app.on_event("startup")`) for managing the `chromadb.PersistentClient` instance. This will improve testability and align with FastAPI best practices.

## Dev Notes

-   **Client Mode:** Use `chromadb.PersistentClient(path=...)` for local/server-based persistence.
-   **Embeddings:** This story focuses on the _store_, not the _embedding generation_. However, testing it might require a dummy embedding function or just passing raw float lists.
-   **Deployment Consideration:** On Railway, file-based persistence will be lost on redeploy unless a Volume is attached. For this story, setting up the _code_ to handle a persistence path is sufficient. Adding the actual Volume can be a deployment task or noted in `README.md`.
-   **Architecture Reference:** "Backend (FastAPI)" section mentions ChromaDB.

### Project Structure Notes

-   `app/rag/vector_store.py`: New module for RAG specific infrastructure.
-   `tests/`: Ensure tests are placed here.

### References

-   [Source: docs/epics.md#Story-1.7-Set-up-ChromaDB-Vector-Store]
-   [Source: docs/sprint-artifacts/tech-spec-epic-1.md#detailed-design]
-   [Source: docs/architecture.md#backend-stack]

## Dev Agent Record

### Context Reference

-   docs/sprint-artifacts/1-7-set-up-chromadb-vector-store.context.xml

### Agent Model Used

Gemini-2.5-Flash

### Debug Log References

-   cleanup error on Windows in `test_chroma_init.py` (file lock), but test functionality passed.

### Completion Notes List

-   ChromaDB installed and configured.
-   `vector_store.py` created with `get_chroma_client` and `get_collection`.
-   Persistence configured via `settings.CHROMA_PERSIST_DIRECTORY`.
-   Integration test `test_chroma_init.py` created and passed.
-   ✅ Resolved review finding [Med]: Refactor `get_chroma_client` in `backend/app/rag/vector_store.py` to leverage FastAPI's dependency injection system.

### File List

-   backend/pyproject.toml
-   backend/app/core/config.py
-   backend/app/rag/vector_store.py
-   backend/tests/test_chroma_init.py
-   backend/app/main.py

## Change Log

| Date                     | Author  | Description                                                                    |
| ------------------------ | ------- | ------------------------------------------------------------------------------ |
| 2025-12-10               | BIP     | Added Epics citation, Dev Agent Record, and initialized Change Log.            |
| 2025-12-12               | Amelia  | Implemented ChromaDB integration, vector store module, and verification tests. |
| 2025-12-12               | Amelia  | Senior Developer Review (AI) performed. Outcome: Changes Requested.            |
| Friday, 12 December 2025 | BMM Dev | Senior Developer Review (AI) performed. Outcome: Changes Requested.            |
| Friday, 12 December 2025 | BMM Dev | Addressed code review findings - 1 items resolved.                             |

## Senior Developer Review (AI)

**Summary:**
The story "1.7: Set up ChromaDB Vector Store" has been reviewed. All acceptance criteria and completed tasks are verified as implemented. A MEDIUM severity finding regarding the `ChromaDB` client instantiation in `backend/app/rag/vector_store.py` was identified, recommending the use of FastAPI's dependency injection system for better adherence to best practices.

**Outcome:** Changes Requested

-   **Justification:** While core functionality is implemented, the identified area for improvement in client instantiation warrants a "Changes Requested" status to ensure the solution aligns with optimal FastAPI architectural patterns for maintainability and testability.

**Key Findings:**

    -   **MEDIUM Severity:**
        -   **ChromaDB Client Instantiation (Best Practice Refinement):** The current `get_chroma_client()` function in `backend/app/rag/vector_store.py` utilizes a global variable to manage a singleton `chromadb.PersistentClient` instance. While this ensures a single instance, in a FastAPI application, it is a recommended best practice to manage such external dependencies using FastAPI's dependency injection system (e.g., `Depends`) or a dedicated application lifecycle event handler (e.g., `app.on_event("startup")`). This approach offers improved testability, clearer dependency graphs, and better integration with the application's lifecycle. [file: backend/app/rag/vector_store.py:9]

    -   **LOW Severity:**
        -   **Missing Epic Tech Spec:** No Epic Tech Spec was found for Epic 1. While not directly impacting the code functionality of this story, its absence means a comprehensive cross-check of epic-specific technical requirements against the implementation intent could not be performed. This is an informational note for broader project context.

**Acceptance Criteria Coverage:**

| AC# | Description                                                                                                                              | Status      | Evidence                                                                                                                                            |
| :-- | :--------------------------------------------------------------------------------------------------------------------------------------- | :---------- | :-------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | **ChromaDB Initialized:** The `chromadb` client library is integrated and configured.                                                    | IMPLEMENTED | `backend/pyproject.toml:dependencies`, `backend/app/core/config.py:CHROMA_PERSIST_DIRECTORY`, `backend/app/rag/vector_store.py` (imports and usage) |
| 2   | **Persistent Storage:** The vector store is configured to persist data (e.g., to disk or a persistent volume, depending on environment). | IMPLEMENTED | `backend/app/core/config.py:CHROMA_PERSIST_DIRECTORY`, `backend/app/rag/vector_store.py:chromadb.PersistentClient`                                  |
| 3   | **Manager Module:** `app/rag/vector_store.py` is created to encapsulate ChromaDB client interactions.                                    | IMPLEMENTED | `backend/app/rag/vector_store.py` (file existence and content)                                                                                      |
| 4   | **Verification:** A basic test script or endpoint can successfully add a dummy embedding and retrieve it.                                | IMPLEMENTED | `backend/tests/test_chroma_init.py` (file existence and content)                                                                                    |
|     | **Summary:** 4 of 4 acceptance criteria fully implemented.                                                                               |             |                                                                                                                                                     |

**Task Completion Validation:**

| Task                                             | Marked As                                       | Verified As       | Evidence                                             |
| :----------------------------------------------- | :---------------------------------------------- | :---------------- | :--------------------------------------------------- |
| **Install and Configure ChromaDB** (AC: 1)       | `[x]`                                           | VERIFIED COMPLETE |                                                      |
| Add `chromadb` to `pyproject.toml`               | `[x]`                                           | VERIFIED COMPLETE | `backend/pyproject.toml`                             |
| Configure settings in `app/core/config.py`       | `[x]`                                           | VERIFIED COMPLETE | `backend/app/core/config.py`                         |
| **Implement Vector Store Module** (AC: 3)        | `[x]`                                           | VERIFIED COMPLETE |                                                      |
| Create `app/rag/vector_store.py`                 | `[x]`                                           | VERIFIED COMPLETE | `backend/app/rag/vector_store.py`                    |
| Implement `get_chroma_client()` function         | `[x]`                                           | VERIFIED COMPLETE | `backend/app/rag/vector_store.py:get_chroma_client`  |
| Define the collection name                       | `[x]`                                           | VERIFIED COMPLETE | `backend/app/rag/vector_store.py:get_collection`     |
| **Configure Persistence** (AC: 2)                | `[x]`                                           | VERIFIED COMPLETE |                                                      |
| For local dev: Use local file path               | `[x]`                                           | VERIFIED COMPLETE | `backend/app/core/config.py`                         |
| For Railway (Staging): Determine strategy        | `[x]`                                           | VERIFIED COMPLETE | `backend/app/core/config.py`, story `Dev Notes`      |
| **Verify Functionality** (AC: 4)                 | `[x]`                                           | VERIFIED COMPLETE |                                                      |
| Create a test script `tests/test_chroma_init.py` | `[x]`                                           | VERIFIED COMPLETE | `backend/tests/test_chroma_init.py`                  |
| Insert a mock vector                             | `[x]`                                           | VERIFIED COMPLETE | `backend/tests/test_chroma_init.py:collection.add`   |
| Query the mock vector                            | `[x]`                                           | VERIFIED COMPLETE | `backend/tests/test_chroma_init.py:collection.query` |
| Assert results match                             | `[x]`                                           | VERIFIED COMPLETE | `backend/tests/test_chroma_init.py:assert`           |
|                                                  | **Summary:** 12 of 12 completed tasks verified. |                   |                                                      |

**Test Coverage and Gaps:**

-   **Coverage:** `backend/tests/test_chroma_init.py` provides good integration test coverage for ChromaDB setup, persistence, and basic CRUD operations (add/query).
-   **Gaps (Advisory):** Additional unit tests for edge cases (e.g., empty inputs, error scenarios) in `vector_store.py` could be beneficial but are not strictly required by ACs.

**Architectural Alignment:**

-   The implementation aligns well with the architecture document's specification of ChromaDB for vector storage.
-   **Warning:** No Epic Tech Spec was found for Epic 1, thus a comprehensive cross-check for epic-specific technical requirements could not be performed.

**Security Notes:**

-   No direct security vulnerabilities were identified within the scope of these changes. The use of `pydantic-settings` for configuration and environment variables is a good practice.

**Best-Practices and References:**

-   **Backend (Python/FastAPI):** Adhere to `Poetry` for dependency management. Utilize `SQLAlchemy` with `asyncpg` for async DB operations. Implement `Pydantic` for request/response validation. `ChromaDB` for vector storage. Comprehensive testing with `Pytest`.
-   **Frontend (Next.js/React):** Use `Next.js 14+` (App Router), `TypeScript`, `Tailwind CSS`, and `shadcn/ui` for responsive, accessible UI. `Jest/RTL` for testing.
-   **General:** Maintain consistent Naming Conventions. Implement Centralized Error Handling. Use UTC for Date/Time. Employ SSE for real-time communication. Aim for WCAG 2.1 AA accessibility.

**Action Items:**

**Code Changes Required:**

-   [x] [Med] Refactor `get_chroma_client` in `backend/app/rag/vector_store.py` to leverage FastAPI's dependency injection system (e.g., using `Depends` or a lifecycle event handler `app.on_event("startup")`) for managing the `chromadb.PersistentClient` instance. This will improve testability and align with FastAPI best practices. [file: backend/app/rag/vector_store.py:9]

**Advisory Notes:**

-   Note: No Epic Tech Spec was found for Epic 1. This means a comprehensive cross-check of epic-specific technical requirements against the implementation intent could not be performed.
