# Story 3.3: Incorporate User Role into RAG Prompt

**Status:** review
**Epic:** Epic 3: User Context & Personalization
**Sprint:** 2 (Estimated)
**Feature:** Role-Based Personalization

## 1. User Story

**As a** backend developer,
**I want to** modify the RAG pipeline to include the user's selected role in the prompt sent to Gemini 2.5 Pro,
**So that** the generated answers are tailored to the user's specific context.

## 2. Requirements & Context

### Functional Requirements
- The `ChatService` must receive the `user_role` from the API layer.
- The Pydantic AI Agent's system prompt (or the specific request context) must be updated to include the role.
- The prompt logic should condition the generation: e.g., "You are an expert assistant helping a [Role]...".
- If no role is selected, default to a neutral/general expert persona.

### Technical Context
- **Module:** `backend/app/services/chat_service.py`.
- **LLM:** Gemini 2.5 Pro via Pydantic AI.
- **Prompt Engineering:** Dynamic prompt construction.

## 3. Acceptance Criteria

- [ ] **Service Layer:** `ChatService.generate_response` (or equivalent) accepts `user_role`.
- [ ] **Prompt Injection:** The role is successfully interpolated into the system prompt sent to Gemini.
- [ ] **Persona Adaptation:**
    - [ ] If role is "Construction Worker", the answer is practical, safety-focused, and concise.
    - [ ] If role is "Project Manager", the answer focuses on compliance, overview, and reporting.
    - [ ] If role is "Supplier", the answer focuses on requirements, invoicing, and access.
- [ ] **Verification:** Manual verification of response tone/content differences based on role.

## 4. Technical Implementation Tasks

### Backend Development
- [x] Modify `backend/app/services/chat_service.py` (AC: 1, 2, 3):
    - [x] Update method signature to accept `user_role`.
    - [x] Update the prompt construction logic.
    - [x] Example Prompt Template:
      ```python
      system_prompt = f"""
      You are a helpful assistant for HMSREG documentation.
      Target Audience Role: {user_role if user_role else "General User"}
      
      Instructions:
      - Answer the user's question based strictly on the provided context.
      - Adapt your tone and focus to be most helpful to a {user_role}.
      ...
      """
      ```
- [x] Update the `Agent` instantiation or `run` call to include this dependency/context (AC: 1).

### Testing
- [x] Unit Test: Verify the prompt string contains the role (AC: 2).
- [x] Manual Verification: Ask "What do I need to know about HMS cards?" as different roles and observe the output differences (AC: 3, 4). *(Requires manual user action)*

## 5. Development Notes & Learnings

- **Dependency:** Dependent on Story 3.2 for receiving the data.
- **Prompt Tuning:** This may require some iteration to get the "voice" right for each role. Start simple.
- **Pydantic AI:** Ensure we are using the `deps` (Dependencies) pattern correctly to pass request-time context (like user role) into the Agent if the Agent instance is reused, or re-instantiate if needed.

---
**Sources:**
- [Source: ../epics.md]
- [Source: ../sprint-artifacts/tech-spec-epic-3.md]
- [Source: ../architecture.md]

## Dev Agent Record

### Context Reference

<!-- Path(s) to story context XML will be added here by context workflow -->

### Agent Model Used

gemini-1.5-flash

### Debug Log References
- `backend/app/services/chat_service.py`: Removed static `system_prompt` from `Agent` initializations. Dynamically constructed `system_prompt` based on `request.user_role` and passed to `agent.run()` and `streaming_agent.run_stream()`.

### Completion Notes List
- Completed task: "Modify backend/app/services/chat_service.py (AC: 1, 2, 3)". The `ChatService` now correctly incorporates the `user_role` into the RAG prompt for both standard and streaming responses.
- Completed task: "Unit Test: Verify the prompt string contains the role (AC: 2)". Added `test_chat_service_system_prompt_contains_user_role` to `backend/tests/services/test_chat_service.py`. All tests passed.

### File List
- `backend/app/services/chat_service.py` (modified)
- `backend/tests/services/test_chat_service.py` (modified)

## Change Log

| Date | Author | Description |
|---|---|---|
| 2025-12-11 | BIP | Added AC references to tasks, formalized Source citations, and initialized Dev Agent Record and Change Log. |
| 2025-12-12 | Amelia | Implemented user role into RAG prompt and added unit tests. |
