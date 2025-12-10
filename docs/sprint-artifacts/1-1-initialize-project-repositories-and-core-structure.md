# Story 1.1: Initialize Project Repositories and Core Structure

Status: ready-for-dev

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

- [ ] Initialize Monorepo Root (AC: 1, 4, 5)
    - [ ] Create root directory (or verify current)
    - [ ] Create global `.gitignore` (merging standard Node, Python, and system ignores)
    - [ ] Create root `README.md`
    - [ ] Initialize git repository (`git init`) if not already present

- [ ] Initialize Backend (FastAPI) (AC: 2)
    - [ ] Install Poetry (`pip install poetry`)
    - [ ] Run `poetry new backend`
    - [ ] Configure `pyproject.toml` with dependencies: `fastapi`, `uvicorn[standard]`, `sqlalchemy`, `asyncpg`, `python-multipart`, `pydantic-ai`
    - [ ] Create directory structure:
        - [ ] `app/api/v1`
        - [ ] `app/core`
        - [ ] `app/services`
        - [ ] `app/db`
        - [ ] `app/rag`
        - [ ] `app/schemas`
        - [ ] `app/utils`
    - [ ] Create `app/main.py` (entry point)
    - [ ] Create `app/core/config.py` (settings)
    - [ ] Create `app/__init__.py` in all subdirectories

- [ ] Initialize Frontend (Next.js) (AC: 3)
    - [ ] Run `npx create-next-app@latest frontend --typescript --tailwind --eslint --app --no-src-dir --import-alias "@/*"`
    - [ ] Verify `tsconfig.json`
    - [ ] Verify `tailwind.config.ts`
    - [ ] Create directory structure:
        - [ ] `app/api`
        - [ ] `components`
        - [ ] `hooks`
        - [ ] `lib`
        - [ ] `types`
        - [ ] `tests`

- [ ] Verification (AC: 1, 2, 3)
    - [ ] Verify backend dependencies install (`poetry install`)
    - [ ] Verify frontend dependencies install (`npm install`)
    - [ ] Verify directory structure matches Architecture spec

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

### File List

## Change Log

| Date | Author | Description |
|---|---|---|
| 2025-12-10 | BIP | Added AC references to tasks and initialized Change Log. |