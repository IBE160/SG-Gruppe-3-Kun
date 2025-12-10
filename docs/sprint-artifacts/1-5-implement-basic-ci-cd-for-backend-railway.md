# Story 1.5: Implement Basic CI/CD for Backend (Railway)

Status: drafted

## Story

As a DevOps engineer,
I want to configure a continuous integration and deployment pipeline for the backend,
so that changes are automatically built and deployed to a staging environment upon commit.

## Acceptance Criteria

1.  **Automated Deployment Trigger:** Push to `main` triggers Railway deployment.
2.  **Successful Build:** The build process completes without errors using `poetry`.
3.  **Application Startup:** The application starts successfully using `uvicorn` on the host/port provided by Railway.
4.  **Public Accessibility:** Staging API URL is reachable and the `/health` endpoint returns a `200 OK` JSON response.

## Tasks / Subtasks

- [ ] **Configure Railway Project** (AC: 1)
    - [ ] Create new project in Railway.
    - [ ] Connect to GitHub repository.
    - [ ] Set "Root Directory" to `/backend` in Service Settings.
- [ ] **Define Start Command** (AC: 2, 3)
    - [ ] Configure Start Command in Railway Settings OR add `backend/Procfile`.
    - [ ] Command: `poetry run uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- [ ] **Verify Build** (AC: 2)
    - [ ] Trigger a deployment.
    - [ ] Monitor build logs for Poetry installation and dependency resolution.
- [ ] **Verify Deployment** (AC: 4)
    - [ ] Access the generated public URL.
    - [ ] Test `GET /health` endpoint.

## Dev Notes

- **Monorepo Handling:** Ensure Railway watches only the `backend` folder or rebuilds appropriately. The "Root Directory" setting is key.
- **Port Binding:** FastAPI must listen on `0.0.0.0` and the port provided by the environment variable `$PORT`. Uvicorn handles this with the command flags.
- **Secrets:** No secrets required for this basic setup yet, but be prepared to add `DATABASE_URL` in future stories (Story 1.6).

### Project Structure Notes
- **Root Directory:** The backend code lives in `backend/`, so deployment configuration must specify this as the root.

### References
- [Source: docs/epics.md#Story-1.5-Implement-Basic-CI/CD-for-Backend-(Railway)]
- [Source: docs/architecture.md#Deployment-Architecture]
- [Source: docs/sprint-artifacts/tech-spec-epic-1.md#Story-1.5:-Backend-CI/CD]

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
| 2025-12-10 | BIP | Added AC references to tasks, added References section with citations, added Dev Agent Record, and initialized Change Log. |