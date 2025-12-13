import pytest
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.db.base import Base
from app.db.models import Feedback  # Import the model to ensure it's registered
from app.core.config import settings

@pytest.fixture(scope="function")
async def test_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Fixture to create a test database session with an in-memory SQLite DB.
    """
    # Override DATABASE_URL for testing
    original_db_url = settings.DATABASE_URL
    settings.DATABASE_URL = "sqlite+aiosqlite:///:memory:"

    # Create test engine and session
    test_engine = create_async_engine(settings.DATABASE_URL, echo=True)
    TestAsyncSessionLocal = async_sessionmaker(
        bind=test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    # Create tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Yield a session
    async with TestAsyncSessionLocal() as session:
        yield session

    # Drop tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    # Restore original settings
    settings.DATABASE_URL = original_db_url
