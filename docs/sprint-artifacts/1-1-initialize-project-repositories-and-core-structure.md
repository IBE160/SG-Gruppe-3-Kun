# Story 1.1: Initialize Project Repositories and Core Structure

Status: drafted

## Story

As a developer,
I want to set up the foundational project repositories and core directory structure,
so that all team members have a consistent and organized starting point for development.

## Acceptance Criteria

-   Given a new project,
-   When I initialize the project,
-   Then a monorepo structure is created with separate `frontend` (Next.js) and `backend` (FastAPI) directories.
-   And the backend directory structure includes `app/api`, `app/core`, `app/services`, `app/db`, `app/rag`, and `app/schemas`.
-   And the frontend directory structure includes `app/api`, `components`, `hooks`, `lib`, and `types`.
-   And a `.gitignore` file is configured for each project to exclude unnecessary files.
-   And a `README.md` is present at the root with basic project setup instructions.

## Tasks / Subtasks

-   [ ] **Create Monorepo Root Structure (AC: Monorepo created)**

    -   [ ] Create the top-level project directory.
    -   [ ] Initialize a Git repository at the root.
    -   [ ] Create a root `.gitignore` file.
    -   [ ] Create a root `README.md` with basic setup instructions.

-   [ ] **Initialize Frontend Project (AC: `frontend` dir created, Next.js initialized, `package.json` created)**

    -   [ ] Navigate to the root directory.
    -   [ ] Execute `npx create-next-app@latest frontend --typescript --tailwind --eslint --app --no-src-dir --import-alias "@/*"`
    -   [ ] Verify `frontend/package.json` exists.
    -   [ ] Create core `frontend` subdirectories: `app/api`, `components`, `hooks`, `lib`, `types`.

-   [ ] **Initialize Backend Project (AC: `backend` dir created, FastAPI initialized, `pyproject.toml` created)**

    -   [ ] Navigate to the root directory.
    -   [ ] Execute `poetry new backend`
    -   [ ] Verify `backend/pyproject.toml` exists.
    -   [ ] Create core `backend` subdirectories: `app/api`, `app/core`, `app/services`, `app/db`, `app/rag`, `app/schemas`.
    -   [ ] Add `__init__.py` files to `backend/app/api`, `backend/app/core`, `backend/app/db`, `backend/app/rag`, `backend/app/schemas`, `backend/app/services` to ensure they are recognized as Python packages.

-   [ ] **Initial Verification (AC: Structure alignment)**
    -   [ ] Confirm both `frontend` and `backend` directories exist at the root.
    -   [ ] Confirm the presence of specified subdirectories within `frontend` and `backend`.
    -   [ ] Confirm existence of `.gitignore` at root, `package.json` in `frontend`, and `pyproject.toml` in `backend`.

## Dev Notes

-   **Relevant architecture patterns and constraints:** Monorepo structure, Next.js for frontend, FastAPI for backend. Follow project structure as defined in Architecture.
-   **Source tree components to touch:** Creation of `frontend/` and `backend/` directories and their initial subdirectories, root `.gitignore`, root `README.md`.
-   **Testing standards summary:** Not directly applicable to this story, as it's foundational setup. Subsequent stories will cover environment setup for testing.

### Project Structure Notes

-   Alignment with `docs/architecture.md` Project Structure section.
-   No detected conflicts or variances at this foundational stage.

### References

-   [Source: docs/architecture.md#Project-Initialization]
-   [Source: docs/architecture.md#Project-Structure]
-   [Source: docs/epics.md#Story-1.1:-Initialize-Project-Repositories-and-Core-Structure]

## Dev Agent Record

### Context Reference

<!-- Path(s) to story context XML will be added here by context workflow -->

### Agent Model Used

gemini-2.5-flash-latest

### Debug Log References

### Completion Notes List

### File List
