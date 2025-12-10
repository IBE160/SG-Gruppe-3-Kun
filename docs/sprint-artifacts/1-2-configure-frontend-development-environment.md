# Story 1.2: Configure Frontend Development Environment

Status: drafted

## Story

As a frontend developer,
I want to set up the Next.js development environment with TypeScript, Tailwind CSS, and shadcn/ui,
so that I can efficiently build the user interface with a consistent and modern design system.

## Acceptance Criteria

1.  Next.js 14 (App Router) is configured with TypeScript.
2.  Tailwind CSS is integrated with the project's color palette (Deep Blue/Teal primary).
3.  shadcn/ui is initialized.
4.  Essential dependencies are installed: `lucide-react`, `clsx`, `tailwind-merge`.
5.  A basic "Hello World" page is rendered successfully, running locally on port 3000.
6.  TypeScript compiles without errors.
7.  Tailwind classes apply correctly.
8.  shadcn/ui components can be added.

## Tasks / Subtasks

*   [ ] **Initialize Next.js Project** (AC: 1)
    *   [ ] Execute `npx create-next-app@latest frontend --typescript --tailwind --eslint --app --no-src-dir --import-alias "@/*"` command.
    *   [ ] Verify `frontend/` directory structure is created correctly.
    *   [ ] Confirm `tsconfig.json` and `tailwind.config.ts` are generated.
*   [ ] **Configure Tailwind CSS** (AC: 2)
    *   [ ] Locate `tailwind.config.ts` in the `frontend/` directory.
    *   [ ] Update `tailwind.config.ts` to include the Deep Blue/Teal primary color palette as defined in UX Specification Section 3.1 (`docs/ux-design-specification.md`).
    *   [ ] Ensure `frontend/app/layout.tsx` correctly imports and applies global Tailwind styles.
*   [ ] **Initialize shadcn/ui** (AC: 3)
    *   [ ] Follow the manual `shadcn/ui` initialization process as per official documentation.
    *   [ ] Install necessary `shadcn/ui` dependencies (e.g., `postcss`, `autoprefixer`).
*   [ ] **Install Essential Frontend Dependencies** (AC: 4)
    *   [ ] Install `lucide-react`, `clsx`, `tailwind-merge` within the `frontend/` project.
*   [ ] **Create Basic "Hello World" Page** (AC: 5)
    *   [ ] Implement a simple page (e.g., `frontend/app/page.tsx`) that displays "Hello World" or "HMSREG Chatbot".
    *   [ ] Apply at least one Tailwind CSS class to the page to confirm Tailwind integration.
    *   [ ] Verify the application runs successfully locally on `http://localhost:3000`.
*   [ ] **Verification & Testing** (AC: 6, 7, 8)
    *   [ ] Run `npm run dev` in `frontend/` and confirm the "Hello World" page is accessible via the browser.
    *   [ ] Check the console for any TypeScript compilation errors.
    *   [ ] Manually inspect the rendered page in the browser's developer tools to confirm Tailwind CSS classes are applied and styling is correct.
    *   [ ] Add a basic shadcn/ui component (e.g., a `<Button>`) to the "Hello World" page and verify it renders as expected.
    *   [ ] **Test (Unit/Integration):** Create initial component rendering tests for core UI elements (e.g., a placeholder for `ChatWindow`) using `Jest` / `React Testing Library` (as per `docs/sprint-artifacts/tech-spec-epic-1.md`).

## Dev Notes

-   **Relevant architecture patterns and constraints:**
    *   Frontend framework: Next.js 14+ (App Router).
    *   Language: TypeScript.
    *   Styling: Tailwind CSS.
    *   UI Components: shadcn/ui.
    *   Project Structure: `frontend/` directory will contain the Next.js application, with feature-based routing, reusable UI components in `components/`, and logic hooks in `hooks/`.
-   **Source tree components to touch:**
    *   `frontend/` directory (for Next.js project initialization).
    *   `frontend/tailwind.config.ts` (for color palette configuration).
    *   `frontend/app/layout.tsx` (for global styles).
    *   `frontend/app/page.tsx` (for "Hello World" page).
-   **Testing standards summary:**
    *   Unit and Integration tests for component rendering using `Jest` / `React Testing Library`.
    *   Manual verification of local server, TypeScript compilation, and Tailwind application.

### Project Structure Notes

-   Alignment with unified project structure (paths, modules, naming): Frontend project will be initialized in `frontend/` as per the monorepo structure.
-   Detected conflicts or variances (with rationale): None detected; direct adherence to architectural guidelines.

### References

-   [Source: docs/epics.md#Story-1.2-Configure-Frontend-Development-Environment]
-   [Source: docs/architecture.md#Project-Initialization]
-   [Source: docs/architecture.md#Technology-Stack-Details]
-   [Source: docs/architecture.md#Code-Organization]
-   [Source: docs/ux-design-specification.md#1.1-Design-System-Choice]
-   [Source: docs/ux-design-specification.md#3.1-Color-System]
-   [Source: docs/sprint-artifacts/tech-spec-epic-1.md#Story-1.2:-Frontend-Setup]

## Dev Agent Record

### Context Reference

<!-- Path(s) to story context XML will be added here by context workflow -->

### Agent Model Used

Gemini 2.5 Flash

### Debug Log References

### Completion Notes List

### File List

## Change Log

| Date | Author | Description |
|---|---|---|
| 2025-12-10 | BIP | Added AC references to tasks and initialized Change Log. |
