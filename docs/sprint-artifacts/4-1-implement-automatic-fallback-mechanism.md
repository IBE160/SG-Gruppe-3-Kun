# Story 4.1: Implement Automatic Fallback Mechanism

Status: drafted

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

- [ ] **Configure Confidence Threshold** (AC: 1)
  - [ ] Add `RAG_CONFIDENCE_THRESHOLD` to `app/core/config.py`.
  - [ ] Update `ChatRequest` or internal context to respect this setting.
- [ ] **Implement Detection Logic in Chat Service** (AC: 1, 4)
  - [ ] Modify `app/services/chat_service.py`.
  - [ ] In the Pydantic AI agent or post-processing, check the confidence score of the generated response.
  - [ ] If `< threshold`, discard the generated answer text.
- [ ] **Implement Fallback Response** (AC: 2, 3)
  - [ ] Define the standard fallback message string (localized in Norwegian).
  - [ ] Include the support/docs link.
  - [ ] Return a `ChatResponse` with `fallback_message` set (or replace `answer` with fallback text if schema doesn't support separate field yet - *Tech spec says schema supports it*).
- [ ] **Testing**
  - [ ] Unit test: Mock low confidence score -> Verify fallback message returned.
  - [ ] Unit test: Mock high confidence score -> Verify normal answer returned.

## Dev Notes

- **Tech Spec Reference:** This implements the "Automatic Fallback Mechanism" sequence diagram in Tech Spec 4.
- **Pydantic AI:** The confidence score might come from the model metadata or be a self-evaluated score requested in the output model. If the model doesn't natively provide it, prompt engineering ("Rate your confidence 0-1") is required.
- **Message Content:**
  > "Jeg fant ikke et klart svar i dokumentasjonen for dette spørsmålet. Kan du utdype spørsmålet? Du kan også søke direkte i [dokumentasjonen](https://docs.hmsreg.com)."

### Project Structure Notes

- `app/services/chat_service.py`: Core logic location.
- `app/core/config.py`: Configuration.

### References

- [Source: docs/sprint-artifacts/tech-spec-epic-4.md#detailed-design]
- [Source: docs/sprint-artifacts/tech-spec-epic-4.md#acceptance-criteria-authoritative]

## Dev Agent Record

### Context Reference

<!-- Path(s) to story context XML will be added here by context workflow -->

### Agent Model Used

Gemini-2.5-Flash

### Debug Log References

### Completion Notes List

### File List
