# Story 1.6: Set up Supabase Project and Connect to Backend

Status: ready-for-dev

## Story

As a backend developer,
I want to initialize a Supabase project and connect the FastAPI backend to its PostgreSQL database,
so that I can store conversation logs, feedback, and analytics data.

## Acceptance Criteria

1. **Supabase Project Initialized:** A new Supabase project is created with a provisioned PostgreSQL database.
2. **Environment Configuration:** The FastAPI backend is configured with the `DATABASE_URL` in `app/core/config.py`, loaded from environment variables.
3. **Database Session Manager:** `app/db/session.py` is implemented using `SQLAlchemy`'s async engine (`create_async_engine`) and `async_sessionmaker`.
4. **Connection Verification:** A simple test endpoint (or script) successfully executes a read/write operation (e.g., `SELECT 1`) to the database.

## Tasks / Subtasks

- [ ] **Initialize Supabase Project** (AC: 1)
  - [ ] Create project in Supabase dashboard.
  - [ ] Retrieve connection strings (Transaction Mode vs Session Mode - use Session mode for direct asyncpg connection if possible, or Transaction with prepared statements disabled).
  - [ ] Add `DATABASE_URL` to local `.env` and Railway variables.
- [ ] **Configure Backend Environment** (AC: 2)
  - [ ] Update `app/core/config.py` to use `pydantic-settings` for `DATABASE_URL`.
  - [ ] Ensure `python-dotenv` is active for local development.
- [ ] **Implement Database Session** (AC: 3)
  - [ ] Create `app/db/session.py`.
  - [ ] Configure `create_async_engine` with `asyncpg` driver.
  - [ ] Create `get_db` dependency for FastAPI routes.
- [ ] **Verify Connection** (AC: 4)
  - [ ] Create a temporary endpoint `GET /db-check` in `app/api/v1/endpoints/health.py` (or similar).
  - [ ] Execute `SELECT 1` via the session.
  - [ ] Verify successful response.

## Dev Notes

- **Driver:** Use `asyncpg` as the underlying driver for SQLAlchemy (`postgresql+asyncpg://...`).
- **Connection Pooling:** Supabase provides an external connection pooler (Supavisor) on port 6543 (usually). For `asyncpg` in a serverless/PaaS environment like Railway, connecting directly to the Postgres port (5432) is often fine if the connection count is managed, but using the pooler in "Session" mode is safer.
- **Architecture Reference:** "Backend (FastAPI)" section specifies SQLAlchemy and asyncpg.
- **Security:** Ensure `DATABASE_URL` is **never** logged or committed.

### Project Structure Notes

- `app/core/config.py`: Centralized config.
- `app/db/session.py`: Database connection logic.
- `app/api/deps.py` (Optional): Location for `get_db` dependency if shared across many modules.

### References

- [Source: docs/epics.md#Story-1.6-Set-up-Supabase-Project-and-Connect-to-Backend]
- [Source: docs/sprint-artifacts/tech-spec-epic-1.md#detailed-design]
- [Source: docs/architecture.md#backend-stack]

## Dev Agent Record

### Context Reference

- docs/sprint-artifacts/1-6-set-up-supabase-project-and-connect-to-backend.context.xml

### Agent Model Used

Gemini-2.5-Flash

### Debug Log References

### Completion Notes List

### File List

## Change Log

| Date | Author | Description |
|---|---|---|
| 2025-12-10 | BIP | Added Epics citation, Dev Agent Record, and initialized Change Log. |
