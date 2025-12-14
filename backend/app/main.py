from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import traceback
from app.api.v1.endpoints import health, chat, feedback
from app.core.config import settings
from app.db.session import engine
from app.db.base import Base
import chromadb
import redis.asyncio as redis # Import redis.asyncio
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.exceptions import RateLimitExceeded
import logfire # Import logfire

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context Manager for managing the lifespan of the FastAPI application.
    Initializes and cleans up resources like the ChromaDB client and DB tables.
    """
    # Initialize Logfire
    logfire.configure()
    logfire.info("Logfire initialized.")

    # Startup event
    app.state.chroma_client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIRECTORY)
    logfire.info("ChromaDB client initialized.")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logfire.info("Database tables created.")

    # Initialize FastAPI Limiter with Redis
    redis_connection = redis.from_url(settings.REDIS_URL, encoding="utf8", decode_responses=True)
    await FastAPILimiter.init(redis_connection)
    logfire.info("FastAPI Limiter initialized.")

    yield
    # Shutdown event
    # PersistentClient generally doesn't need explicit closing
    app.state.chroma_client = None
    logfire.info("ChromaDB client shutdown.")
    # FastAPI Limiter doesn't require explicit shutdown for RedisBackend
    # as the connection is managed by redis-py

app = FastAPI(lifespan=lifespan)
logfire.instrument(app) # Enable automatic instrumentation for FastAPI

# Exception handler for rate limiting
@app.exception_handler(RateLimitExceeded)
async def rate_limit_exception_handler(request: Request, exc: RateLimitExceeded):
    logfire.warn(f"Rate limit exceeded for request from {request.client.host}: {exc.detail}")
    return JSONResponse(
        status_code=429,
        content={"detail": f"Rate limit exceeded: {exc.detail}"},
    )

app.include_router(health.router, prefix="/api/v1/health", tags=["health"])
app.include_router(chat.router, prefix="/api/v1/chat", tags=["chat"])
app.include_router(feedback.router, prefix="/api/v1/feedback", tags=["feedback"])

@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "0.1.0"}

# Route for favicon.ico to prevent unnecessary 404 errors
@app.get("/favicon.ico")
async def get_favicon():
    return {"message": "No favicon"}
