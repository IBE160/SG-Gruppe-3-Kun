import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing import AsyncGenerator

from app.main import app
from app.db.session import get_db
from app.db.base import Base
from app.db.models import Feedback # Ensure model is imported

# Create a new async engine for an in-memory SQLite database for testing.
# The 'connect_args' is crucial for SQLite in-memory DBs with multiple threads.
test_engine = create_async_engine(
    "sqlite+aiosqlite:///:memory:",
    connect_args={"check_same_thread": False}
)

# Create a new sessionmaker for the test engine
TestingSessionLocal = async_sessionmaker(
    autocommit=False, autoflush=False, bind=test_engine
)

async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency override for get_db that yields a session from our test DB.
    """
    async with TestingSessionLocal() as session:
        yield session

# Apply the dependency override to the app for all tests in this file
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module", autouse=True)
async def setup_test_db():
    """
    Pytest fixture to create and tear down the test database tables for the module.
    """
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

# Mark all tests in this file as async
pytestmark = pytest.mark.asyncio

async def test_create_feedback_success():
    """
    Tests successful creation of feedback via the API using the overridden DB.
    """
    feedback_payload = {
        "chat_session_id": "test_session_123",
        "message_id": "test_message_456",
        "rating": "thumbs_up",
        "user_id": "test_user_789",
        "comment": "This was helpful!"
    }
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/api/v1/feedback/", json=feedback_payload)
    
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["id"] is not None
    assert data["created_at"] is not None
    assert data["rating"] == "thumbs_up"
    assert data["comment"] == "This was helpful!"

async def test_create_feedback_invalid_payload():
    """
    Tests API response when a required field is missing.
    """
    # Payload missing the required 'rating' field
    invalid_payload = {
        "chat_session_id": "test_session_invalid",
        "message_id": "test_message_invalid"
    }
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/api/v1/feedback/", json=invalid_payload)
        
    assert response.status_code == 422, response.text
