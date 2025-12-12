# Story 4.1: Implement Automatic Fallback Mechanism

Status: review

## Story

As a backend developer,
I want to implement a mechanism to detect when the chatbot cannot confidently answer a question,
so that it can gracefully inform the user and provide alternative resources.

## Acceptance Criteria

1. **Low Confidence Detection:** The system must accurately detect when the confidence score of a RAG-generated answer falls below a configurable threshold (e.g., 0.7).
2.  **Fallback Message:** When low confidence is detected, the system must return a specific fallback message: "Jeg fant ikke et klart svar i dokumentasjonen for dette spørsmålet. Kan du utdype spørsmålet? ..."
3.  **Support Link:** The fallback response must include a link to the general documentation or a support contact page.
4.  **No Hallucination:** The system must NOT attempt to fabricate an answer when confidence is low.

## Tasks / Subtasks

- [x] **Configure Confidence Threshold** (AC: 1)
  - [x] Add `RAG_CONFIDENCE_THRESHOLD` to `app/core/config.py`.
  - [x] Update `ChatRequest` or internal context to respect this setting.
- [x] **Implement Detection Logic in Chat Service** (AC: 1, 4)
  - [x] Modify `app/services/chat_service.py`.
  - [x] In the Pydantic AI agent or post-processing, check the confidence score of the generated response.
  - [x] If `< threshold`, discard the generated answer text.
- [x] **Implement Fallback Response** (AC: 2, 3)
  - [x] Define the standard fallback message string (localized in Norwegian).
  - [x] Include the support/docs link.
  - [x] Return a `ChatResponse` with `fallback_message` set (or replace `answer` with fallback text if schema doesn't support separate field yet - *Tech spec says schema supports it*).
- [x] **Testing**
  - [x] Unit test: Mock low confidence score -> Verify fallback message returned.
  - [x] Unit test: Mock high confidence score -> Verify normal answer returned.

## Dev Notes

### Architecture patterns and constraints

- **Service Layer Pattern:** Core logic for confidence detection and fallback must reside in `app/services/chat_service.py`, keeping the API layer (`app/api/v1/chat.py`) thin.
- **Pydantic Models:** Use `ChatResponse` in `app/schemas/chat.py` to strictly define the API contract, ensuring the `fallback_message` field is correctly typed.
- **Configuration:** Use `app/core/config.py` for the `RAG_CONFIDENCE_THRESHOLD` to allow easy environment-based tuning.

- **Tech Spec Reference:** This implements the "Automatic Fallback Mechanism" sequence diagram in Tech Spec 4.
- **Pydantic AI:** The confidence score might come from the model metadata or be a self-evaluated score requested in the output model. If the model doesn't natively provide it, prompt engineering ("Rate your confidence 0-1") is required.
- **Message Content:**
  > "Jeg fant ikke et klart svar i dokumentasjonen for dette spørsmålet. Kan du utdype spørsmålet? Du kan også søke direkte i [dokumentasjonen](https://docs.hmsreg.com)."

### Project Structure Notes

- `app/services/chat_service.py`: Core logic location.
- `app/core/config.py`: Configuration.

### Learnings from Previous Story

- **N/A:** This is the first story in Epic 4.

### References

- [Source: docs/sprint-artifacts/tech-spec-epic-4.md#detailed-design]
- [Source: docs/sprint-artifacts/tech-spec-epic-4.md#acceptance-criteria-authoritative]
- [Source: docs/architecture.md]
- [Source: docs/epics.md]
- [Source: docs/PRD.md]

## Dev Agent Record

### Context Reference

- docs/sprint-artifacts/4-1-implement-automatic-fallback-mechanism.context.xml

### Agent Model Used

Gemini-2.5-Flash

### Debug Log References

### Completion Notes List
- Implemented automatic fallback mechanism as per AC 1, 2, 3, and 4.
- Configured RAG_CONFIDENCE_THRESHOLD in `app/core/config.py`.
- Modified `app/services/chat_service.py` to check confidence score and trigger fallback.
- Updated `app/schemas/chat.py` to include `confidence` and `fallback_message` fields.
- Added unit tests in `backend/tests/services/test_chat_service.py` to verify fallback behavior.

### File List
- `backend/app/core/config.py`
- `backend/app/schemas/chat.py`
- `backend/app/services/chat_service.py`
- `backend/tests/services/test_chat_service.py`

## Change Log

### Friday, 12 December 2025
- Senior Developer Review notes appended.

## Senior Developer Review (AI)

### Reviewer: BIP
### Date: Friday, 12 December 2025
### Outcome: Approve

**Summary:** The implementation for Story 4.1, "Implement Automatic Fallback Mechanism," is complete and thoroughly addresses all Acceptance Criteria and tasks. The code adheres to architectural patterns and best practices.

**Key Findings:**
- No HIGH severity issues.
- No MEDIUM severity issues.
- No LOW severity issues.

### Acceptance Criteria Coverage

| AC# | Description                                                                                             | Status      | Evidence                                                                                                                                                                                                                                                                                                |
| :-- | :------------------------------------------------------------------------------------------------------ | :---------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1   | Low Confidence Detection: The system must accurately detect when the confidence score ...               | IMPLEMENTED | `backend/app/core/config.py` (line 4, `RAG_CONFIDENCE_THRESHOLD`), `backend/app/services/chat_service.py` (line ~120, `result.data.confidence < settings.RAG_CONFIDENCE_THRESHOLD`). Tests: `backend/tests/services/test_chat_service.py`.                                                            |
| 2   | Fallback Message: When low confidence is detected, the system must return a specific fallback message... | IMPLEMENTED | `backend/app/services/chat_service.py` (lines ~18-22, `FALLBACK_MESSAGE` definition; line ~123, `result.data.fallback_message = FALLBACK_MESSAGE`). Tests: `backend/tests/services/test_chat_service.py`.                                                                                             |
| 3   | Support Link: The fallback response must include a link to the general documentation or a support page. | IMPLEMENTED | `backend/app/services/chat_service.py` (line ~20, `[dokumentasjonen](https://docs.hmsreg.com)` within `FALLBACK_MESSAGE`). Tests: Implicitly covered by `backend/tests/services/test_chat_service.py`.                                                                                                 |
| 4   | No Hallucination: The system must NOT attempt to fabricate an answer when confidence is low.             | IMPLEMENTED | `backend/app/services/chat_service.py` (line ~121, `result.data.answer = ""`; line ~122, `result.data.citations = []`). Tests: `backend/tests/services/test_chat_service.py` asserts empty answer and citations.                                                                                      |

**Summary: 4 of 4 acceptance criteria fully implemented.**

### Task Completion Validation

| Task/Subtask                                                                                   | Marked As | Verified As       | Evidence                                                                                                                                                                                                                                                                                                   |
| :--------------------------------------------------------------------------------------------- | :-------- | :---------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Configure Confidence Threshold**                                                             | [x]       | VERIFIED COMPLETE |                                                                                                                                                                                                                                                                                                            |
| - Add `RAG_CONFIDENCE_THRESHOLD` to `app/core/config.py`.                                      | [x]       | VERIFIED COMPLETE | `backend/app/core/config.py`, line 4.                                                                                                                                                                                                                                                                      |
| - Update `ChatRequest` or internal context to respect this setting.                            | [x]       | VERIFIED COMPLETE | `backend/app/services/chat_service.py`, line ~120 (usage of `settings.RAG_CONFIDENCE_THRESHOLD`).                                                                                                                                                                                                           |
| **Implement Detection Logic in Chat Service**                                                  | [x]       | VERIFIED COMPLETE |                                                                                                                                                                                                                                                                                                            |
| - Modify `app/services/chat_service.py`.                                                       | [x]       | VERIFIED COMPLETE | `backend/app/services/chat_service.py` modifications as detailed above.                                                                                                                                                                                                                                    |
| - In the Pydantic AI agent or post-processing, check the confidence score.                     | [x]       | VERIFIED COMPLETE | `backend/app/services/chat_service.py`, line ~120.                                                                                                                                                                                                                                                         |
| - If `< threshold`, discard the generated answer text.                                         | [x]       | VERIFIED COMPLETE | `backend/app/services/chat_service.py`, line ~121.                                                                                                                                                                                                                                                         |
| **Implement Fallback Response**                                                                | [x]       | VERIFIED COMPLETE |                                                                                                                                                                                                                                                                                                            |
| - Define the standard fallback message string.                                                 | [x]       | VERIFIED COMPLETE | `backend/app/services/chat_service.py`, lines ~18-22.                                                                                                                                                                                                                                                      |
| - Include the support/docs link.                                                               | [x]       | VERIFIED COMPLETE | `backend/app/services/chat_service.py`, line ~20.                                                                                                                                                                                                                                                          |
| - Return a `ChatResponse` with `fallback_message` set.                                         | [x]       | VERIFIED COMPLETE | `backend/app/services/chat_service.py`, line ~123; `backend/app/schemas/chat.py`, line ~26.                                                                                                                                                                                                               |
| **Testing**                                                                                    | [x]       | VERIFIED COMPLETE |                                                                                                                                                                                                                                                                                                            |
| - Unit test: Mock low confidence score -> Verify fallback message returned.                    | [x]       | VERIFIED COMPLETE | `backend/tests/services/test_chat_service.py`, `test_generate_chat_response_low_confidence_fallback`.                                                                                                                                                                                                      |
| - Unit test: Mock high confidence score -> Verify normal answer returned.                      | [x]       | VERIFIED COMPLETE | `backend/tests/services/test_chat_service.py`, `test_generate_chat_response_high_confidence_no_fallback`.                                                                                                                                                                                                  |

**Summary: All 10 of 10 completed tasks verified.**

### Test Coverage and Gaps
- Comprehensive unit tests were added for the new fallback mechanism in `backend/tests/services/test_chat_service.py`, covering both low and high confidence scenarios. All tests passed.

### Architectural Alignment
- The implementation fully aligns with the specified architectural patterns regarding service layer responsibilities, Pydantic model usage, and configuration management, as detailed in `architecture.md` and `tech_spec_epic-4.md`.

### Security Notes
- No new security vulnerabilities introduced. The confidence-based fallback mechanism helps prevent hallucination, which can be a form of information integrity risk.

### Best-Practices and References
- Adherence to Pydantic AI for structured outputs and FastAPI best practices for backend service logic.

### Action Items

**Advisory Notes:**
- Note: Continue to monitor the confidence score behavior of the Gemini 1.5 Flash model in a live environment to ensure optimal `RAG_CONFIDENCE_THRESHOLD` tuning.
