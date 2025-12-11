# Story 2.3: Implement Pydantic AI RAG Pipeline in Backend

Status: drafted

## Story

As a backend developer,
I want to integrate the Pydantic AI RAG pipeline with Gemini 2.5 Pro,
so that user questions can be processed to retrieve relevant documentation and generate informed responses.

## Acceptance Criteria

1. Questions sent to `app/services/chat_service.py` are embedded and used to query ChromaDB.
2. Retrieved chunks are passed to a `pydantic-ai` Agent configured with Gemini 2.5 Pro.
3. The response matches a defined Pydantic model (answer, confidence).
4. Gemini generates a coherent answer based *only* on the provided context (grounded).

## Tasks / Subtasks

- [ ] Define Data Models (`app/schemas/chat.py`) (AC: #3)
  - [ ] `ChatRequest` (message, role).
  - [ ] `ChatResponse` (answer, citations).
- [ ] Implement Chat Service (`app/services/chat_service.py`) (AC: #2, #4)
  - [ ] Initialize `pydantic-ai` Agent with Gemini 2.5 Pro model.
  - [ ] Define system prompt: "You are a helpful assistant. Use the following context..."
  - [ ] Implement `generate_response(message: str)` function.
- [ ] Implement Retrieval Logic (AC: #1)
  - [ ] Embed user query using `text-embedding-004`.
  - [ ] Query ChromaDB via `vector_store` for top K chunks.
  - [ ] Format chunks into the Agent's context.
- [ ] Implement Testing (AC: #1, #2, #3, #4)
  - [ ] Write unit test for `chat_service.py` to verify that a mock response is correctly generated. (AC: #2, #3, #4)
  - [ ] Write unit test to verify that the retrieval logic correctly queries the vector store. (AC: #1)
  - [ ] Write integration test for the full RAG pipeline with a mock vector store.

## Dev Notes

- **Libraries**: `pydantic-ai`, `google-generativeai`.
- **Constraint**: Do NOT use LangChain for the generation phase. Use `pydantic-ai` natively.
- **Env**: Ensure `GOOGLE_API_KEY` is loaded.

### Project Structure Notes

- Logic belongs in `app/services/chat_service.py`.

### References

- [Source: docs/architecture.md#Backend-FastAPI]
- [Source: docs/sprint-artifacts/tech-spec-epic-2.md#Detailed-Design]
- [Source: docs/epics.md#Story-2.3]

## Dev Agent Record

### Context Reference

### Agent Model Used

Gemini 2.5 Flash

### Debug Log References

### Completion Notes List

### File List

## Change Log
