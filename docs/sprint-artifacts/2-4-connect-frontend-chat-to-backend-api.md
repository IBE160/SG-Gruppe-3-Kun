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

- [ ] Backend: Create SSE Endpoint (`app/api/v1/chat.py`)
  - [ ] Define `POST /stream` endpoint.
  - [ ] Use `StreamingResponse` to yield tokens from `chat_service`.
  - [ ] Format events: `data: {"type": "token", "content": "..."}`.
- [ ] Frontend: Create API Proxy (`app/api/chat/route.ts`)
  - [ ] Forward request to backend URL.
  - [ ] Handle streaming response forwarding.
- [ ] Frontend: Implement `useChat` Hook (`hooks/useChat.ts`)
  - [ ] Manage `EventSource` or `fetch` with readable stream.
  - [ ] Parse incoming SSE data.
  - [ ] Update message state with appended tokens.
- [ ] Integration
  - [ ] Connect `ChatWindow` to `useChat`.
  - [ ] Verify "typing" effect in UI.

## Dev Notes

- **Protocol**: Server-Sent Events (SSE) is preferred over WebSockets for this simple unidirectional flow.
- **CORS**: Ensure backend allows requests from frontend (or proxy handles it).

### Project Structure Notes

- Frontend API route: `frontend/app/api/chat/route.ts`.
- Backend API route: `backend/app/api/v1/chat.py`.

### References

- [Source: docs/sprint-artifacts/tech-spec-epic-2.md#Detailed-Design]
- [Source: docs/epics.md#Story-2.4]

## Dev Agent Record

### Context Reference

### Agent Model Used

Gemini 2.5 Flash

### Debug Log References

### Completion Notes List

### File List
