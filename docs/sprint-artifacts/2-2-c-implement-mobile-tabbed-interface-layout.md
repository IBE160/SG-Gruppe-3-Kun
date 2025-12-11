# Story 2.2.c: Implement Mobile Tabbed-Interface Layout

Status: ready_for_dev

## Story

As a frontend developer,
I want to implement the single-column, tabbed interface for mobile screens,
so that mobile users can easily navigate between different content views on a small screen.

## Acceptance Criteria

1. On screens narrower than 1024px, a single-column layout is displayed.
2. A tab bar is present (bottom or top) with options: "Links", "Article", "Chatbot".
3. Clicking a tab switches the main view content immediately.
4. "Chatbot" view renders the `ChatWindow` component.

## Tasks / Subtasks

- [ ] Implement Mobile Layout Wrapper (AC: #1)
  - [ ] Use `block lg:hidden` to show only on mobile.
  - [ ] Create state: `activeTab` ('links' | 'article' | 'chat').
- [ ] Implement Tab Navigation Component (AC: #2)
  - [ ] Create fixed tab bar (bottom favored for thumb access).
  - [ ] Style active tab to highlight current selection (Teal).
- [ ] Implement View Switching Logic (AC: #3, #4)
  - [ ] Conditionally render components based on `activeTab`.
  - [ ] `Links` -> Nav placeholder.
  - [ ] `Article` -> Content placeholder.
  - [ ] `Chat` -> `ChatWindow`.
- [ ] Integration (AC: #1)
  - [ ] Ensure seamless switch between this and desktop layout when resizing.
- [ ] Implement Testing (AC: #1, #2, #3, #4)
    - [ ] Write a test to verify that the single-column layout is applied on screens smaller than 1024px. (AC: #1)
    - [ ] Write a test to verify that the tab bar is present and contains the correct options. (AC: #2)
    - [ ] Write a test to verify that clicking a tab switches the main view content. (AC: #3)
    - [ ] Write a test to verify that the `ChatWindow` component is rendered when the "Chatbot" tab is active. (AC: #4)

## Dev Notes

- **Components**: `shadcn/ui` Tabs component might be useful, or a custom sticky footer.
- **State**: React `useState` for tab selection.

### Project Structure Notes

- Can be part of the main `app/page.tsx` logic or a dedicated `components/MobileLayout.tsx`.

### References

- [Source: docs/architecture.md#Project-Structure]
- [Source: docs/sprint-artifacts/tech-spec-epic-2.md#Detailed-Design]
- [Source: docs/epics.md#Story-2.2.c]

## Dev Agent Record

### Context Reference

### Agent Model Used

Gemini 2.5 Flash

### Debug Log References

### Completion Notes List

### File List

## Change Log
