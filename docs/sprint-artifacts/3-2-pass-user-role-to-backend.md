# Story 3.2: Pass User Role to Backend

**Status:** Drafted
**Epic:** Epic 3: User Context & Personalization
**Sprint:** 2 (Estimated)
**Feature:** Role-Based Personalization

## 1. User Story

**As a** full-stack developer,
**I want to** securely transmit the selected user role from the frontend to the backend,
**So that** the backend can use this context for personalized RAG responses.

## 2. Requirements & Context

### Functional Requirements
- The frontend `useChat` hook must include the selected `userRole` in the API request payload.
- The backend API endpoint `/api/v1/chat` must accept an optional `user_role` field.
- The backend Pydantic model `ChatRequest` must validate this new field.

### Technical Context
- **Frontend:** `hooks/useChat.ts` calls `app/api/chat/route.ts` which proxies to Backend.
- **Backend:** FastAPI, Pydantic.
- **Protocol:** HTTP POST (JSON body).

## 3. Acceptance Criteria

- [ ] **Frontend Update:** The `useChat` hook accepts `userRole` as an argument or prop.
- [ ] **API Payload:** The POST request to `/api/v1/chat` includes `{"role": "..."}` (or matching schema field).
- [ ] **Backend Schema:** The `ChatRequest` Pydantic model in `backend/app/schemas/chat.py` includes `user_role: Optional[str]`.
- [ ] **Validation:** The backend validates the role against allowed values (optional but good practice) or at least accepts the string.
- [ ] **Integration:** Sending a message with a selected role results in a successful 200 OK (and SSE stream start), verifying the backend accepted the payload.

## 4. Technical Implementation Tasks

### Backend Development
- [ ] Update `backend/app/schemas/chat.py` (AC: 3):
    - [ ] Add `user_role: Optional[str] = None` to `ChatRequest` class.
    - [ ] (Optional) Define an Enum for allowed roles.
- [ ] Update `backend/app/api/v1/chat.py` (AC: 4, 5):
    - [ ] Ensure the endpoint handler accepts the updated `ChatRequest` model.
    - [ ] Log the received role (DEBUG level) to verify transmission.

### Frontend Development
- [ ] Update `hooks/useChat.ts` (AC: 1, 2):
    - [ ] Add `userRole` to the hook's input or state.
    - [ ] Update the `fetch` call body to include `role: userRole`.
- [ ] Update `app/api/chat/route.ts` (Next.js Proxy) (AC: 2):
    - [ ] Ensure it parses the incoming request body and forwards the `role` field to the Python backend.

### Testing
- [ ] API Test (Backend): Send a curl request with `user_role` and verify response (AC: 4, 5).
- [ ] Integration Test (Frontend): Use the Chat UI with a selected role, inspect Network tab to verify payload (AC: 1, 2, 5).

## 5. Development Notes & Learnings

- **Dependency:** dependent on Story 3.1 for the UI selection.
- **Learnings from 3.1:** Ensure the role string matches exactly what the backend expects (case-sensitivity).
- **Security:** Sanitize the input, although Pydantic handles basic type validation.

---
**Sources:**
- [Source: ../epics.md]
- [Source: ../sprint-artifacts/tech-spec-epic-3.md]
- [Source: ../architecture.md#API-Backend]

## Dev Agent Record

### Context Reference

<!-- Path(s) to story context XML will be added here by context workflow -->

### Agent Model Used

{{agent_model_name_version}}

### Debug Log References

### Completion Notes List

### File List

## Change Log

| Date | Author | Description |
|---|---|---|
| 2025-12-11 | BIP | Added AC references to tasks, formalized Source citations, and initialized Dev Agent Record and Change Log. |
