from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import settings

# Create Async Engine
# echo=True can be enabled for debugging SQL queries during development
engine = create_async_engine(settings.DATABASE_URL, echo=False)

# Create Async Session Factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for FastAPI routes to get a database session.
    Yields an AsyncSession and ensures it's closed after the request.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
