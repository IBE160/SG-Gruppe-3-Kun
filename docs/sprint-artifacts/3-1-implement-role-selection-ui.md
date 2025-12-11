# Story 3.1: Implement Role Selection UI

**Status:** ready_for_dev
**Epic:** Epic 3: User Context & Personalization
**Sprint:** 2 (Estimated)
**Feature:** Role-Based Personalization

## 1. User Story

**As a** frontend developer,
**I want to** provide a clear and intuitive interface for users to select their role at the beginning of a session,
**So that** the chatbot can understand their context and personalize responses.

## 2. Requirements & Context

### Functional Requirements
- Display a role selection interface when a new chat session starts.
- Provide three distinct role options: **Construction Worker**, **Supplier**, and **Project Manager**.
- Persist the selected role for the duration of the chat session.
- Hide the role selector once a role is chosen or allow it to be minimized (per UX design).

### UX/UI Design
- **Component:** `RoleSelector`
- **Location:** Initial chat screen (before or as part of the greeting).
- **Style:** Use `shadcn/ui` Button components.
- **Interaction:** Single click selection.
- **Visuals:** Clear labels, potentially icons for each role (optional but recommended).

### Technical Constraints
- **Framework:** Next.js (App Router), React.
- **Styling:** Tailwind CSS, shadcn/ui.
- **State Management:** Local React state or Context (to be consumed by `useChat`).

## 3. Acceptance Criteria

- [ ] **UI Rendering:** The `RoleSelector` component renders correctly on the chat page.
- [ ] **Options:** Three buttons are displayed: "Construction Worker", "Supplier", "Project Manager".
- [ ] **Selection:** Clicking a button updates the application state to reflect the selected role.
- [ ] **Feedback:** The selected role is visually highlighted or the selector dismisses after selection.
- [ ] **Accessibility:** The component is keyboard navigable (Tab/Enter) and screen reader accessible (ARIA labels if needed).
- [ ] **Integration:** The selection event is ready to be passed to the chat hook (preparation for Story 3.2).

## 4. Technical Implementation Tasks

### Frontend Development
- [ ] Create `components/RoleSelector.tsx` (AC: 1, 2).
    - [ ] Import `Button` from `@/components/ui/button`.
    - [ ] Define props: `onSelect: (role: string) => void`.
    - [ ] Render the three role buttons.
- [ ] Update `app/page.tsx` (or the main chat page layout) (AC: 1, 3, 4).
    - [ ] Add state: `const [userRole, setUserRole] = useState<string | null>(null)`.
    - [ ] Conditionally render `RoleSelector` if `userRole` is null.
    - [ ] Pass `setUserRole` handler to `RoleSelector`.
- [ ] Add basic styling/layout to center the selector or place it according to UX guidelines (AC: 1, 4).
- [ ] Verify accessibility (Tab order, focus states) (AC: 5).

### Testing
- [ ] Component Test: Verify `onSelect` is called with the correct string when a button is clicked (AC: 3).
- [ ] Manual Test: Verify UI responsiveness and visual state changes (AC: 4, 5).

## 5. Development Notes & Learnings

- **Previous Learnings:** N/A (First story in Epic 3).
- **State Management:** Consider if `userRole` needs to be global (Context) or if prop drilling is sufficient for now. Given the scope, local state in the page lifting it up to the `ChatWindow` wrapper seems appropriate.
- **Future Considerations:** Story 3.2 will require passing this state to `useChat`. Ensure the state is accessible to where `useChat` is initialized.

---
**Sources:**
- [Source: ../epics.md]
- [Source: ../sprint-artifacts/tech-spec-epic-3.md]
- [Source: ../architecture.md#Project-Structure]

## Dev Agent Record

### Context Reference

<!-- Path(s) to story context XML will be added here by context workflow -->

### Agent Model Used

{{agent_model_name_version}}

### Debug Log References

### Completion Notes List

### File List

## Change Log

| Date | Author | Description |
|---|---|---|
| 2025-12-11 | BIP | Added AC references to tasks, formalized Source citations, and initialized Dev Agent Record and Change Log. |
