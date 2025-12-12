# Story 2.2.a: Implement Core Chat Interface

Status: review

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

- [x] Create UI Components (AC: #1, #2)
  - [x] Implement `components/ChatBubble.tsx` with distinct styles for 'user' and 'assistant' roles.
  - [x] Implement `components/ChatWindow.tsx` as the main container.
  - [x] Add `Input` and `Button` from `shadcn/ui`.
- [x] Implement State Management (AC: #1, #3, #4)
  - [x] Manage message history array (initially empty or mock data).
  - [x] Handle input change and form submission.
  - [x] Toggle `isLoading` state on submission.
- [x] Implement Interactions (AC: #1, #4)
  - [x] Auto-scroll to bottom when new messages arrive.
  - [x] Disable input/button while loading.
- [x] Styling (AC: #2, #3)
  - [x] Apply Tailwind CSS classes matching UX Spec (Deep Blue/Teal).
  - [x] Ensure "Loading" animation (e.g., pulsing dots) is visible.
- [x] Implement Testing (AC: #1, #2, #3, #4)
    - [x] Write unit test to verify that `ChatBubble` renders different styles for user and assistant. (AC: #2)
    - [x] Write unit test for `ChatWindow` to ensure that messages are added to the history. (AC: #1)
    - [x] Write unit test to verify that the loading indicator is displayed when `isLoading` is true. (AC: #3)
    - [x] Write unit test to ensure the send button is disabled when the input is empty or loading. (AC: #4)

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

- **2025-12-12 [Amelia]:** Starting implementation.
  - **Plan:**
    1. Install `react-markdown`.
    2. Create `components/ChatBubble.tsx` (User/Assistant styles).
    3. Create `components/ChatWindow.tsx` (State, Auto-scroll, Mock response).
    4. Integrate into `app/page.tsx`.
    5. Add unit tests.

### Completion Notes List

- **2025-12-12 [Amelia]:**
  - Implemented `ChatBubble` with `react-markdown` support and conditional styling.
  - Implemented `ChatWindow` with message state, auto-scroll, mock response logic, and loading state.
  - Integrated `ChatWindow` into `app/page.tsx` replacing placeholder.
  - Added comprehensive unit tests for new components and updated page tests.
  - Handled ESM/Jest config issue by mocking `react-markdown` in `jest.setup.ts`.

### File List

- frontend/components/ChatBubble.tsx
- frontend/components/ChatWindow.tsx
- frontend/components/ui/input.tsx
- frontend/app/page.tsx
- frontend/tests/components/ChatBubble.test.tsx
- frontend/tests/components/ChatWindow.test.tsx
- frontend/tests/page.test.tsx
- frontend/package.json
- frontend/jest.setup.ts

## Change Log

| Date | Author | Description |
|---|---|---|
| 2025-12-12 | Amelia | Implemented Core Chat Interface, components, and tests. Marked ready for review. |

### Senior Developer Review (AI)
- **Reviewer**: Amelia
- **Date**: Friday, 12 December 2025
- **Outcome**: **APPROVE**
- **Summary**: The core chat interface components, including `ChatWindow` and `ChatBubble`, have been successfully implemented. The UI is functional, visually distinct for user and bot messages, and includes a loading indicator. All acceptance criteria and development tasks have been met and verified by accompanying tests.

### Key Findings
- **None**: No high or medium severity findings.

### Acceptance Criteria Coverage
| AC# | Description | Status | Evidence |
|---|---|---|---|
| 1 | A chat history panel is displayed when navigating to the chat page. | IMPLEMENTED | `frontend/components/ChatWindow.tsx` (L50-L60), `frontend/app/page.tsx` (L35-L37) |
| 2 | User and bot message bubbles are visually distinct (User: Primary Color/Teal, Bot: Neutral/Gray). | IMPLEMENTED | `frontend/components/ChatBubble.tsx` (L14-L22) |
| 3 | A "Loading..." indicator (subtle animation) appears while waiting for a response. | IMPLEMENTED | `frontend/components/ChatWindow.tsx` (L62-L70) |
| 4 | A text input field and "Send" button are present and functional. | IMPLEMENTED | `frontend/components/ChatWindow.tsx` (L75-L87) |

Summary: 4 of 4 acceptance criteria fully implemented.

### Task Completion Validation
| Task | Marked As | Verified As | Evidence |
|---|---|---|---|
| Create UI Components (AC: #1, #2) | [x] | VERIFIED COMPLETE | `frontend/components/ChatBubble.tsx`, `frontend/components/ChatWindow.tsx`, `frontend/components/ui/input.tsx` |
| Implement `components/ChatBubble.tsx` with distinct styles for 'user' and 'assistant' roles. | [x] | VERIFIED COMPLETE | `frontend/components/ChatBubble.tsx` |
| Implement `components/ChatWindow.tsx` as the main container. | [x] | VERIFIED COMPLETE | `frontend/components/ChatWindow.tsx` |
| Add `Input` and `Button` from `shadcn/ui`. | [x] | VERIFIED COMPLETE | `frontend/components/ui/input.tsx`, `frontend/components/ui/button.tsx` |
| Implement State Management (AC: #1, #3, #4) | [x] | VERIFIED COMPLETE | `frontend/components/ChatWindow.tsx` (L23-L47) |
| Manage message history array (initially empty or mock data). | [x] | VERIFIED COMPLETE | `frontend/components/ChatWindow.tsx` (L23) |
| Handle input change and form submission. | [x] | VERIFIED COMPLETE | `frontend/components/ChatWindow.tsx` (L38-L47, L76-L80) |
| Toggle `isLoading` state on submission. | [x] | VERIFIED COMPLETE | `frontend/components/ChatWindow.tsx` (L45, L47) |
| Implement Interactions (AC: #1, #4) | [x] | VERIFIED COMPLETE | `frontend/components/ChatWindow.tsx` (L30-L32, L75-L87) |
| Auto-scroll to bottom when new messages arrive. | [x] | VERIFIED COMPLETE | `frontend/components/ChatWindow.tsx` (L30-L32) |
| Disable input/button while loading. | [x] | VERIFIED COMPLETE | `frontend/components/ChatWindow.tsx` (L80, L82) |
| Styling (AC: #2, #3) | [x] | VERIFIED COMPLETE | `frontend/components/ChatBubble.tsx`, `frontend/components/ChatWindow.tsx` |
| Apply Tailwind CSS classes matching UX Spec (Deep Blue/Teal). | [x] | VERIFIED COMPLETE | `frontend/components/ChatBubble.tsx` (L14-L22) |
| Ensure "Loading" animation (e.g., pulsing dots) is visible. | [x] | VERIFIED COMPLETE | `frontend/components/ChatWindow.tsx` (L62-L70) |
| Implement Testing (AC: #1, #2, #3, #4) | [x] | VERIFIED COMPLETE | `frontend/tests/components/ChatBubble.test.tsx`, `frontend/tests/components/ChatWindow.test.tsx` |
| Write unit test to verify that `ChatBubble` renders different styles for user and assistant. (AC: #2) | [x] | VERIFIED COMPLETE | `frontend/tests/components/ChatBubble.test.tsx` (L9-L21) |
| Write unit test for `ChatWindow` to ensure that messages are added to the history. (AC: #1) | [x] | VERIFIED COMPLETE | `frontend/tests/components/ChatWindow.test.tsx` (L26-L50) |
| Write unit test to verify that the loading indicator is displayed when `isLoading` is true. (AC: #3) | [x] | VERIFIED COMPLETE | `frontend/tests/components/ChatWindow.test.tsx` (L26-L50) |
| Write unit test to ensure the send button is disabled when the input is empty or loading. (AC: #4) | [x] | VERIFIED COMPLETE | `frontend/tests/components/ChatWindow.test.tsx` (L26-L50) |

Summary: 19 of 19 completed tasks verified.

### Test Coverage and Gaps
- All relevant ACs are covered by unit tests. The mock for `react-markdown` in `jest.setup.ts` ensures tests run without ESM issues.

### Architectural Alignment
- The implementation aligns with the defined frontend architecture for `ChatWindow` and `ChatBubble` components.

### Security Notes
- No specific security vulnerabilities were identified in this frontend-focused implementation.

### Best-Practices and References
- Follows React component structure and state management. Utilizes shadcn/ui for consistent styling.

### Action Items

**Code Changes Required:**
- None.

**Advisory Notes:**
- Note: This story implements a mock backend response. Story 2-4 will focus on connecting to the actual backend API for real responses.
| Date | Author | Description |
|---|---|---|
| 2025-12-12 | Amelia | Implemented Core Chat Interface, components, and tests. Marked ready for review. |
