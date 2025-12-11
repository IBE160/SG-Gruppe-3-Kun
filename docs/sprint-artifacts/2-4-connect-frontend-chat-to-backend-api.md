# Story 2.4: Connect Frontend Chat to Backend API

Status: drafted

## Story

As a full-stack developer,
I want to establish communication between the frontend chat interface and the backend RAG API via SSE,
so that users can send questions and receive real-time streaming answers.

## Acceptance Criteria

1. Frontend calls Next.js API route `app/api/chat/route.ts` on send.
2. Route proxies to backend endpoint `/api/v1/chat/stream`.
3. Backend streams response token-by-token using Server-Sent Events (SSE).
4. UI updates in real-time as tokens arrive.

## Tasks / Subtasks

- [ ] Backend: Create SSE Endpoint (`app/api/v1/chat.py`) (AC: 3)
  - [ ] Define `POST /stream` endpoint.
  - [ ] Use `StreamingResponse` to yield tokens from `chat_service`.
  - [ ] Format events: `data: {"type": "token", "content": "..."}`.
- [ ] Frontend: Create API Proxy (`app/api/chat/route.ts`) (AC: 1, 2)
  - [ ] Forward request to backend URL.
  - [ ] Handle streaming response forwarding.
- [ ] Frontend: Implement `useChat` Hook (`hooks/useChat.ts`) (AC: 4)
  - [ ] Manage `EventSource` or `fetch` with readable stream.
  - [ ] Parse incoming SSE data.
  - [ ] Update message state with appended tokens.
- [ ] Integration
  - [ ] Connect `ChatWindow` to `useChat` (AC: 4).
  - [ ] Verify "typing" effect in UI (AC: 4).
- [ ] Implement Testing
    - [ ] Write integration test for frontend API route to verify it proxies correctly (AC: 1, 2).
    - [ ] Write integration test for backend SSE endpoint to verify streaming (AC: 3).
    - [ ] Write E2E test to verify UI updates in real-time (AC: 4).

## Dev Notes

- **Protocol**: Server-Sent Events (SSE) is preferred over WebSockets for this simple unidirectional flow.
- **CORS**: Ensure backend allows requests from frontend (or proxy handles it).

### Project Structure Notes

- Frontend API route: `frontend/app/api/chat/route.ts`.
- Backend API route: `backend/app/api/v1/chat.py`.

### References

- [Source: docs/sprint-artifacts/tech-spec-epic-2.md#Detailed-Design]
- [Source: docs/epics.md#Story-2.4]
- [Source: docs/architecture.md#API-Backend]

## Dev Agent Record

### Context Reference

### Agent Model Used

Gemini 2.5 Flash

### Debug Log References

### Completion Notes List

### File List

## Change Log

| Date | Author | Description |
|---|---|---|
| 2025-12-11 | BIP | Added AC references to tasks, added detailed testing subtasks, formalized Source citations, and initialized Change Log. |
