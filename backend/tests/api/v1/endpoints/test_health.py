import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.core.config import settings

# Skip this test if DATABASE_URL is not configured (e.g. in CI without secrets)
# But for local dev with .env, it should run.
@pytest.mark.asyncio
async def test_db_check():
    # Only run if not placeholder
    if "user:password" in settings.DATABASE_URL:
        pytest.skip("DATABASE_URL not configured")
        
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/v1/health/db-check")
    
    # If connection fails, it returns 200 with status: error
    assert response.status_code == 200
    data = response.json()
    
    if data["status"] == "error":
         pytest.fail(f"Database connection failed: {data.get('detail')}")
         
    assert data["status"] == "ok"
    assert data["db_response"] == 1
