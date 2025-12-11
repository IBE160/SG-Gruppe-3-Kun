# Story 2.2.a: Implement Core Chat Interface

Status: ready_for_dev

## Story

As a frontend developer,
I want to create the foundational chat interface components,
so that users have the basic tools to interact with the chatbot in a clean, professional environment.

## Acceptance Criteria

1. A chat history panel is displayed when navigating to the chat page.
2. User and bot message bubbles are visually distinct (User: Primary Color/Teal, Bot: Neutral/Gray).
3. A "Loading..." indicator (subtle animation) appears while waiting for a response.
4. A text input field and "Send" button are present and functional.

## Tasks / Subtasks

- [ ] Create UI Components (AC: #1, #2)
  - [ ] Implement `components/ChatBubble.tsx` with distinct styles for 'user' and 'assistant' roles.
  - [ ] Implement `components/ChatWindow.tsx` as the main container.
  - [ ] Add `Input` and `Button` from `shadcn/ui`.
- [ ] Implement State Management (AC: #1, #3, #4)
  - [ ] Manage message history array (initially empty or mock data).
  - [ ] Handle input change and form submission.
  - [ ] Toggle `isLoading` state on submission.
- [ ] Implement Interactions (AC: #1, #4)
  - [ ] Auto-scroll to bottom when new messages arrive.
  - [ ] Disable input/button while loading.
- [ ] Styling (AC: #2, #3)
  - [ ] Apply Tailwind CSS classes matching UX Spec (Deep Blue/Teal).
  - [ ] Ensure "Loading" animation (e.g., pulsing dots) is visible.
- [ ] Implement Testing (AC: #1, #2, #3, #4)
    - [ ] Write unit test to verify that `ChatBubble` renders different styles for user and assistant. (AC: #2)
    - [ ] Write unit test for `ChatWindow` to ensure that messages are added to the history. (AC: #1)
    - [ ] Write unit test to verify that the loading indicator is displayed when `isLoading` is true. (AC: #3)
    - [ ] Write unit test to ensure the send button is disabled when the input is empty or loading. (AC: #4)

## Dev Notes

- **Components**: `ChatWindow` (container), `ChatBubble` (item).
- **Libraries**: `lucide-react` (icons), `shadcn/ui` (primitives).
- **UX Pattern**: Follow "Novel UX Pattern" for simplicity.
- **Mocking**: Since backend isn't connected yet (Story 2.4), use `setTimeout` to mock a bot response after sending.

### Project Structure Notes

- Place components in `components/`.
- Ensure standard `shadcn/ui` components are available in `components/ui/`.

### References

- [Source: docs/architecture.md#Project-Structure]
- [Source: docs/sprint-artifacts/tech-spec-epic-2.md#Detailed-Design]
- [Source: docs/epics.md#Story-2.2.a]

## Dev Agent Record

### Context Reference

### Agent Model Used

Gemini 2.5 Flash

### Debug Log References

### Completion Notes List

### File List

## Change Log
