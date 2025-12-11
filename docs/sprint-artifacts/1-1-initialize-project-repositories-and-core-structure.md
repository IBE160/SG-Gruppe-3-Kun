# Story 1.1: Initialize Project Repositories and Core Structure

Status: review

## Story

As a developer,
I want to set up the foundational project repositories and core directory structure,
so that all team members have a consistent and organized starting point for development.

## Acceptance Criteria

1. Monorepo structure exists with separate `frontend` (Next.js) and `backend` (FastAPI) directories.
2. The backend directory structure includes `app/api`, `app/core`, `app/services`, `app/db`, `app/rag`, and `app/schemas`.
3. The frontend directory structure includes `app/api`, `components`, `hooks`, `lib`, and `types`.
4. A `.gitignore` file is configured for each project to exclude unnecessary files.
5. A `README.md` is present at the root with basic project setup instructions.

## Tasks / Subtasks

- [x] Initialize Monorepo Root (AC: 1, 4, 5)
    - [x] Create root directory (or verify current)
    - [x] Create global `.gitignore` (merging standard Node, Python, and system ignores)
    - [x] Create root `README.md`
    - [x] Initialize git repository (`git init`) if not already present

- [x] Initialize Backend (FastAPI) (AC: 2)
    - [x] Install Poetry (`pip install poetry`)
    - [x] Run `poetry new backend`
    - [x] Configure `pyproject.toml` with dependencies: `fastapi`, `uvicorn[standard]`, `sqlalchemy`, `asyncpg`, `python-multipart`, `pydantic-ai`
    - [x] Create directory structure:
        - [x] `app/api/v1`
        - [x] `app/core`
        - [x] `app/services`
        - [x] `app/db`
        - [x] `app/rag`
        - [x] `app/schemas`
        - [x] `app/utils`
    - [x] Create `app/main.py` (entry point)
    - [x] Create `app/core/config.py` (settings)
    - [x] Create `app/__init__.py` in all subdirectories

- [x] Initialize Frontend (Next.js) (AC: 3)
    - [x] Run `npx create-next-app@latest frontend --typescript --tailwind --eslint --app --no-src-dir --import-alias "@/*"`
    - [x] Verify `tsconfig.json`
    - [x] Verify `tailwind.config.ts`
    - [x] Create directory structure:
        - [x] `app/api`
        - [x] `components`
        - [x] `hooks`
        - [x] `lib`
        - [x] `types`
        - [x] `tests`

- [x] Verification (AC: 1, 2, 3)
    - [x] Verify backend dependencies install (`poetry install`)
    - [x] Verify frontend dependencies install (`npm install`)
    - [x] Verify directory structure matches Architecture spec

## Dev Notes

- **Architecture Compliance:** Strict adherence to "Project Structure" in `docs/architecture.md`.
- **Backend Init:** Use `poetry new backend` to ensure standard layout.
- **Frontend Init:** Use the specific `create-next-app` command from Architecture to ensure TypeScript and App Router are set up correctly.
- **Version Control:** Ensure `.gitignore` is comprehensive (node_modules, __pycache__, .env, .venv, .DS_Store).

### Project Structure Notes

- **Unified Structure:** The project uses a monorepo approach.
- **Backend:** Python/FastAPI in `backend/`.
- **Frontend:** TypeScript/Next.js in `frontend/`.
- **Docs:** Documentation lives in `docs/`.
- **Config:** Core config in `backend/app/core/config.py` (Backend) and `frontend/next.config.mjs` / `tailwind.config.ts` (Frontend).

### References

- [Source: docs/epics.md#Story-1.1-Initialize-Project-Repositories-and-Core-Structure]
- [Source: docs/architecture.md#Project-Initialization]
- [Source: docs/sprint-artifacts/tech-spec-epic-1.md#Detailed-Design]

## Dev Agent Record

### Context Reference

- docs/sprint-artifacts/1-1-initialize-project-repositories-and-core-structure.context.xml

### Agent Model Used

Gemini 2.5 Flash

### Debug Log References

### Completion Notes List
- Initialized monorepo root: Verified project root, updated global .gitignore with Python-specific rules, and enhanced root README.md with basic project setup instructions. No new git repo initialization was needed as one was already present.
- Initialized backend (FastAPI): Installed Poetry, created 'backend' project, configured 'pyproject.toml' with core dependencies, created application directory structure, and added '__init__.py' files where necessary, including a basic 'main.py' and 'core/config.py'.
- Initialized frontend (Next.js): Created 'frontend' project using `create-next-app` with TypeScript, Tailwind CSS, ESLint, App Router. Verified `tsconfig.json`. Noted absence of `tailwind.config.ts` (expected to be handled during `shadcn/ui` setup). Created necessary application directory structure.
- Verified project setup: Successfully installed backend (Poetry) and frontend (npm) dependencies. Refactored backend project structure from Poetry's default to match the specified 'backend/app' architecture. Verified overall directory structure for both frontend and backend against the Architecture Specification.

### File List
- .gitignore
- README.md
- backend/pyproject.toml
- backend/app/main.py
- backend/app/core/config.py
- backend/app/__init__.py
- backend/app/api/__init__.py
- backend/app/api/v1/__init__.py
- backend/app/core/__init__.py
- backend/app/services/__init__.py
- backend/app/db/__init__.py
- backend/app/rag/__init__.py
- backend/app/schemas/__init__.py
- backend/app/utils/__init__.py
- frontend/.next
- frontend/app
- frontend/public
- frontend/eslint.config.mjs
- frontend/next.config.ts
- frontend/package-lock.json
- frontend/package.json
- frontend/postcss.config.mjs
- frontend/README.md
- frontend/tsconfig.json
- frontend/app/api
- frontend/components
- frontend/hooks
- frontend/lib
- frontend/types
- frontend/tests
- (deleted) backend/src
- (deleted) backend/README.md

## Change Log

| Date | Author | Description |
|---|---|---|
| 2025-12-10 | BIP | Added AC references to tasks and initialized Change Log. |