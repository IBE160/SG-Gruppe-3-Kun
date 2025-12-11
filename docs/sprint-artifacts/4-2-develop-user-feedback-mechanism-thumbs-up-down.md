# Story 4.2: Develop User Feedback Mechanism (Thumbs Up/Down)

Status: ready-for-dev

## Story

As a full-stack developer,
I want to provide a simple way for users to give feedback on each chatbot response,
so that we can continuously monitor and improve the chatbot's performance.

## Acceptance Criteria

1. **UI Visibility:** Thumbs up and Thumbs down buttons must be visible below every chatbot response bubble.
2. **Submission:** Clicking a button must send a POST request to `/api/v1/feedback` with the correct `message_id`, `chat_session_id`, and `rating`.
3. **Persistence:** The feedback must be successfully stored in the `feedback` database table.
4. **User Confirmation:** The UI must provide immediate visual confirmation (e.g., button state change, "Thank you" toast) after submission.
5. **One Vote Per Message:** Users should be prevented from submitting multiple conflicting votes for the same message.

## Tasks / Subtasks

- [ ] **Database Schema & Model** (AC: 3)
  - [ ] Create `Feedback` model in `app/db/models.py` (id, chat_session_id, message_id, rating, created_at).
  - [ ] Create migration (if using Alembic) or `Base.metadata.create_all` for dev.
- [ ] **Backend API Endpoint** (AC: 2, 3)
  - [ ] Create `app/schemas/feedback.py` with `FeedbackCreate` model.
  - [ ] Create `app/api/v1/feedback.py` with `POST /` endpoint.
  - [ ] Implement persistence logic using `app/db/session.py`.
- [ ] **Frontend Component** (AC: 1, 4, 5)
  - [ ] Create `components/FeedbackButtons.tsx`.
  - [ ] Implement "Thumbs Up" and "Thumbs Down" icons (Lucide React).
  - [ ] Handle click events to call API.
  - [ ] Manage local state (submitted, loading).
- [ ] **Integration** (AC: 1)
  - [ ] Add `FeedbackButtons` to `components/ChatBubble.tsx` (only for bot messages).
  - [ ] Update `useChat` or `ChatWindow` to ensure `message_id` is available for each message.
- [ ] **Testing**
  - [ ] Backend: Test `POST /feedback` stores data.
  - [ ] Frontend: Test button click triggers API call.

## Dev Notes

### Architecture patterns and constraints

- **RESTful API:** Implement feedback submission as a standard `POST` endpoint in `app/api/v1/feedback.py` following the project's API conventions.
- **Database Access:** Use SQLAlchemy models (`app/db/models.py`) and session management (`app/db/session.py`) for persistence, avoiding raw SQL.
- **Data Validation:** Ensure strict validation of the feedback payload using Pydantic models (`app/schemas/feedback.py`).

- **Tech Spec Reference:** "User Feedback Submission" workflow in Tech Spec 4.
- **Data Model:**
  ```python
  class Feedback(Base):
      ...
      rating = Column(String, nullable=False) # "thumbs_up", "thumbs_down"
  ```
- **UX:** Keep it subtle. Small icons next to the timestamp or citations.

### Project Structure Notes

- `app/api/v1/feedback.py`: New API module.
- `components/FeedbackButtons.tsx`: New UI component.

### Learnings from Previous Story

- Previous story (4.1) is currently in drafted state. Ensure to check for any shared configuration changes in `app/core/config.py` if overlapping work occurs.

### References

- [Source: docs/sprint-artifacts/tech-spec-epic-4.md#detailed-design]
- [Source: docs/sprint-artifacts/tech-spec-epic-4.md#acceptance-criteria-authoritative]
- [Source: docs/architecture.md]
- [Source: docs/epics.md]
- [Source: docs/PRD.md]

## Dev Agent Record

### Context Reference

- docs/sprint-artifacts/4-2-develop-user-feedback-mechanism-thumbs-up-down.context.xml

### Agent Model Used

Gemini-2.5-Flash

### Debug Log References

### Completion Notes List

### File List
