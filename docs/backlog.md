# Engineering Backlog

This backlog collects cross-cutting or future action items that emerge from reviews and planning.

Routing guidance:

- Use this file for non-urgent optimizations, refactors, or follow-ups that span multiple stories/epics.
- Must-fix items to ship a story belong in that story’s `Tasks / Subtasks`.
- Same-epic improvements may also be captured under the epic Tech Spec `Post-Review Follow-ups` section.

| Date | Story | Epic | Type | Severity | Owner | Status | Notes |
| ---- | ----- | ---- | ---- | -------- | ----- | ------ | ----- |
| 2025-12-12 | 1.7 | 1 | TechDebt | Med | TBD | Completed | Harmonize Python version requirement in `backend/pyproject.toml` with `architecture.md` (`>=3.11`). [file: backend/pyproject.toml:9] |
| 2025-12-12 | 1.7 | 1 | Optimization | Low | TBD | Completed | Consider optimizing `get_chroma_client` to reuse a single instance of `chromadb.PersistentClient` (e.g., using a singleton pattern or FastAPI dependency injection for request scope). [file: backend/app/rag/vector_store.py:9] |
| Friday, 12 December 2025 | 1.7 | 1 | Refactor | Med | TBD | Open | Refactor `get_chroma_client` in `backend/app/rag/vector_store.py` to leverage FastAPI's dependency injection system for managing the `chromadb.PersistentClient` instance. [file: backend/app/rag/vector_store.py:9] |