# Story 2.5: Display Source Citations in Chat UI

Status: drafted

## Story

As a frontend developer,
I want to display the source documentation links alongside the chatbot's answers,
so that users can verify the information and explore the original context.

## Acceptance Criteria

1. Backend returns source URLs (citations) in the response metadata.
2. Frontend displays these as clickable links at the bottom of the bot's chat bubble.
3. Links are clearly labeled "Source:".
4. Clicking a link opens the `docs.hmsreg.com` page.

## Tasks / Subtasks

- [ ] Backend: Update `chat_service`
  - [ ] Extract source metadata (URL, Title) from the ChromaDB chunks used in the answer.
  - [ ] Yield a final SSE event: `data: {"type": "citation", "content": [...]}`.
- [ ] Frontend: Update `useChat` Hook
  - [ ] Handle `citation` event type.
  - [ ] Append citations to the current message object.
- [ ] Frontend: Update `ChatBubble` Component
  - [ ] Render a "Sources:" section if citations exist.
  - [ ] Map citations to `<a>` tags (styled as small, distinct links).
- [ ] Testing
  - [ ] Verify links are correct and clickable.

## Dev Notes

- **Data Structure**: `SourceCitation { title: string, url: string }`.
- **UX**: Ensure citations don't clutter the view (small font, maybe collapsible).

### Project Structure Notes

- Modify `components/ChatBubble.tsx` and `types/chat.ts`.

### References

- [Source: docs/sprint-artifacts/tech-spec-epic-2.md#Detailed-Design]
- [Source: docs/epics.md#Story-2.5]

## Dev Agent Record

### Context Reference

### Agent Model Used

Gemini 2.5 Flash

### Debug Log References

### Completion Notes List

### File List
