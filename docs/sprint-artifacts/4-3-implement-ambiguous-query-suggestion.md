# Story 4.3: Implement Ambiguous Query Suggestion

Status: ready-for-dev

## Story

As a backend developer,
I want to enable the chatbot to suggest alternative or related topics when a user's query is ambiguous,
so that users can refine their questions and find relevant information more easily.

## Acceptance Criteria

1. **Ambiguity Detection:** The system must identify ambiguous queries (e.g., "Tell me about rules") where multiple distinct topics could apply.
2. **Suggestion Generation:** The system must generate 2-3 specific, relevant follow-up questions or topics based on the ambiguous query.
3. **UI Presentation:** Suggestions must be displayed as clickable buttons or links in the chat interface.
4. **Interaction:** Clicking a suggestion must immediately trigger a new search/chat request with that specific query.

## Tasks / Subtasks

- [ ] **Backend: Suggestion Logic** (AC: 1, 2)
  - [ ] Update `app/services/chat_service.py`.
  - [ ] Modify the Pydantic AI agent system prompt to include instructions for identifying ambiguity.
  - [ ] Define output schema to include `suggested_queries: List[str]`.
  - [ ] Test with ambiguous inputs (e.g., "HMS", "regler", "start").
- [ ] **Backend: API Response Update** (AC: 3)
  - [ ] Ensure `ChatResponse` model includes `suggested_queries`.
  - [ ] Ensure `stream` endpoint correctly serializes this field.
- [ ] **Frontend: Display Suggestions** (AC: 3)
  - [ ] Update `components/ChatBubble.tsx` to render `suggested_queries` if present.
  - [ ] Style as "chips" or small outline buttons below the message text.
- [ ] **Frontend: Interaction Handler** (AC: 4)
  - [ ] Implement click handler for suggestions.
  - [ ] Action: Fill input with suggestion AND auto-submit (or just fill input?). *AC says "trigger new search", so auto-submit.*
- [ ] **Testing**
  - [ ] Unit test (Backend): Verify specific prompts produce suggestions.
  - [ ] E2E (Frontend): Click suggestion -> New message sent.

## Dev Notes

### Architecture patterns and constraints

- **Service Layer Logic:** Implement ambiguity detection and suggestion generation within `app/services/chat_service.py` to maintain separation of concerns.
- **SSE Extension:** Deliver suggested queries via the existing Server-Sent Events stream by extending the `ChatResponse` schema, rather than creating a separate endpoint.
- **Prompt Engineering:** Use the system prompt or a dedicated chain to generate suggestions, ensuring they are strictly relevant to the user's ambiguous input.

- **Tech Spec Reference:** "Ambiguous Query Suggestion" workflow in Tech Spec 4.
- **Prompt Engineering:**
  > "If the user's query is too broad or ambiguous (e.g., 'HMS'), provide 2-3 specific follow-up questions they might be interested in, such as 'Hva er kravene til HMS-kort?' or 'Hvordan registrerer jeg et prosjekt?'."
- **UX:** These suggestions act as "conversation starters" or "repair moves".

### Project Structure Notes

- `app/services/chat_service.py`: Logic.
- `components/ChatBubble.tsx`: UI.

### Learnings from Previous Story

- Previous story (4.2) is currently in drafted state.

### References

- [Source: docs/sprint-artifacts/tech-spec-epic-4.md#detailed-design]
- [Source: docs/sprint-artifacts/tech-spec-epic-4.md#acceptance-criteria-authoritative]
- [Source: docs/architecture.md]
- [Source: docs/epics.md]
- [Source: docs/PRD.md]

## Dev Agent Record

### Context Reference

- docs/sprint-artifacts/4-3-implement-ambiguous-query-suggestion.context.xml

### Agent Model Used

Gemini-2.5-Flash

### Debug Log References

### Completion Notes List

### File List
