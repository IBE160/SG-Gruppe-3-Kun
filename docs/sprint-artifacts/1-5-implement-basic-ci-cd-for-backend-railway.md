# Story 1.5: Implement Basic CI/CD for Backend (Railway)

**Epic:** 1 - Project Foundation & Deployment Pipeline
**Story Key:** 1-5-implement-basic-ci-cd-for-backend-railway
**Status:** Drafted

## User Story

**As a** DevOps engineer,
**I want to** configure a continuous integration and deployment pipeline for the backend,
**So that** changes are automatically built and deployed to a staging environment upon commit.

## Context & Scope

- **Goal:** Establish an automated deployment pipeline for the FastAPI backend using Railway.
- **Preceding Story:** Story 1.3 (Backend Setup) must be complete to have a deployable artifact.
- **Target Environment:** Staging (Railway).
- **Repository Structure:** Monorepo. Backend code is in `backend/` directory.

## Acceptance Criteria

### AC 1: Automated Deployment Trigger
- **Given** the FastAPI backend repository is connected to Railway,
- **When** a commit is pushed to the `main` branch,
- **Then** Railway automatically detects the change and triggers a new build.

### AC 2: Successful Build and Start
- **Given** a new build is triggered,
- **When** the build process completes,
- **Then** the application starts successfully using `poetry run uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
- **And** no startup errors occur.

### AC 3: Public Accessibility
- **Given** a successful deployment,
- **When** I access the provided Railway staging URL,
- **Then** the application is reachable.
- **And** the `/health` endpoint returns a `200 OK` JSON response.

## Technical Implementation

### Deployment Configuration
- **Platform:** Railway
- **Root Directory:** `backend` (Critical for monorepo)
- **Build System:** Railway Nixpacks (auto-detects `pyproject.toml`)
- **Start Command:** `poetry run uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Environment Variables:**
  - `PORT`: Provided by Railway
  - `PYTHON_VERSION`: Ensure 3.11+ is selected if manual config required.

### Configuration Files
- Consider adding a `Procfile` in `backend/` to strictly define the start command:
  ```text
  web: poetry run uvicorn app.main:app --host 0.0.0.0 --port $PORT
  ```
  *Note: Railway works well without this if `pyproject.toml` is present, but `Procfile` is explicit.*

## Tasks

- [ ] **Configure Railway Project**
    - [ ] Create new project in Railway.
    - [ ] Connect to GitHub repository.
    - [ ] Set "Root Directory" to `/backend` in Service Settings.
- [ ] **Define Start Command**
    - [ ] Configure Start Command in Railway Settings OR add `backend/Procfile`.
    - [ ] Command: `poetry run uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- [ ] **Verify Build**
    - [ ] Trigger a deployment.
    - [ ] Monitor build logs for Poetry installation and dependency resolution.
- [ ] **Verify Deployment**
    - [ ] Access the generated public URL.
    - [ ] Test `GET /health` endpoint.

## Dev Notes

- **Monorepo Handling:** Ensure Railway watches only the `backend` folder or rebuilds appropriately. The "Root Directory" setting is key.
- **Port Binding:** FastAPI must listen on `0.0.0.0` and the port provided by the environment variable `$PORT`. Uvicorn handles this with the command flags.
- **Secrets:** No secrets required for this basic setup yet, but be prepared to add `DATABASE_URL` in future stories (Story 1.6).

## Definition of Done

- [ ] Railway project created and linked.
- [ ] Auto-deployment on push to `main` verified.
- [ ] Application is running and accessible via public URL.
- [ ] `/health` returns 200.
