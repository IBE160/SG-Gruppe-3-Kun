# Story 5.1: Implement API Rate Limiting

Status: drafted

## Story

As a backend developer,
I want to implement rate limiting on all API endpoints,
so that the system is protected from abuse and denial-of-service attacks.

## Acceptance Criteria

1. Requests exceeding the limit (e.g., 60/min) must be rejected with HTTP status `429 Too Many Requests`.
2. Responses should include standard rate limit headers (e.g., `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `Retry-After`).
3. Rate limits must be configurable via environment variables without code changes.
4. Internal services or specific whitelisted IPs (if any) should be exempt from rate limiting (optional for MVP).

## Tasks / Subtasks

- [ ] Install and configure `slowapi` (or similar middleware) in FastAPI backend.
  - [ ] Add dependency to `pyproject.toml`.
- [ ] Implement rate limiting logic in `backend/app/middleware/rate_limit.py`.
- [ ] Configure rate limit parameters in `app/core/config.py` (read from environment variables).
- [ ] Apply rate limiting middleware to the FastAPI application instance or specific routers.
- [ ] Create unit/integration tests to verify rate limiting enforcement.
  - [ ] Verify 429 status when limit is exceeded.
  - [ ] Verify headers are present.

## Dev Notes

- **Architecture**: Implements `backend/app/middleware/rate_limit.py` as defined in the Tech Spec.
- **Configuration**: Use `slowapi` which integrates well with FastAPI.
- **Testing**: Ensure tests don't permanently block the test runner (mock limits or use separate test config).

### Project Structure Notes

- **File**: `backend/app/middleware/rate_limit.py`
- **Config**: `backend/app/core/config.py`

### References

- [Source: docs/sprint-artifacts/tech-spec-epic-5.md#Detailed Design]
- [Source: docs/epics.md#Story 5.1: Implement API Rate Limiting]

## Dev Agent Record

### Context Reference

<!-- Path(s) to story context XML will be added here by context workflow -->

### Agent Model Used

gemini-2.0-flash-exp

### Debug Log References

### Completion Notes List

### File List
