# Story 2.2.c: Implement Mobile Tabbed-Interface Layout

Status: drafted

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

- [ ] Implement Mobile Layout Wrapper
  - [ ] Use `block lg:hidden` to show only on mobile.
  - [ ] Create state: `activeTab` ('links' | 'article' | 'chat').
- [ ] Implement Tab Navigation Component
  - [ ] Create fixed tab bar (bottom favored for thumb access).
  - [ ] Style active tab to highlight current selection (Teal).
- [ ] Implement View Switching Logic
  - [ ] Conditionally render components based on `activeTab`.
  - [ ] `Links` -> Nav placeholder.
  - [ ] `Article` -> Content placeholder.
  - [ ] `Chat` -> `ChatWindow`.
- [ ] Integration
  - [ ] Ensure seamless switch between this and desktop layout when resizing.

## Dev Notes

- **Components**: `shadcn/ui` Tabs component might be useful, or a custom sticky footer.
- **State**: React `useState` for tab selection.

### Project Structure Notes

- Can be part of the main `app/page.tsx` logic or a dedicated `components/MobileLayout.tsx`.

### References

- [Source: docs/sprint-artifacts/tech-spec-epic-2.md#Detailed-Design]
- [Source: docs/epics.md#Story-2.2.c]

## Dev Agent Record

### Context Reference

### Agent Model Used

Gemini 2.5 Flash

### Debug Log References

### Completion Notes List

### File List
