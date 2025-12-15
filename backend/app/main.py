from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import traceback
from app.api.v1.endpoints import health, chat, feedback
from app.core.config import settings
from app.core.logging import configure_logging
from app.db.session import engine
from app.db.base import Base
import chromadb
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from app.middleware.rate_limit import limiter
import logfire

import logging # Add import
from app.core.logging import configure_logging # Add import

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context Manager for managing the lifespan of the FastAPI application.
    Initializes and cleans up resources like the ChromaDB client and DB tables.
    """
    # Initialize Logfire
    if settings.LOGFIRE_TOKEN:
        logfire.configure(token=settings.LOGFIRE_TOKEN)
        logging.info("Logfire initialized with cloud logging enabled.")
    else:
        logfire.configure(send_to_logfire=False)
        logging.info("Logfire initialized with cloud logging disabled.")
    configure_logging() # Call configure_logging

    # Startup event
    app.state.chroma_client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIRECTORY)
    logging.info("ChromaDB client initialized.") # Use standard logging

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logfire.info("Database tables created.")

    yield
    # Shutdown event
    # PersistentClient generally doesn't need explicit closing
    app.state.chroma_client = None
    logfire.info("ChromaDB client shutdown.")

from app.middleware.correlation_id import CorrelationIdMiddleware # Add import

from fastapi.middleware.cors import CORSMiddleware # Add import

app = FastAPI(lifespan=lifespan)
logfire.instrument(app) # Enable automatic instrumentation for FastAPI

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all origins for now, specific domains can be added later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add Correlation ID middleware FIRST
app.add_middleware(CorrelationIdMiddleware)

# Initialize SlowAPI
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

# Exception handler for rate limiting
@app.exception_handler(RateLimitExceeded)
async def rate_limit_exception_handler(request: Request, exc: RateLimitExceeded):
    logging.warning(f"Rate limit exceeded for request from {request.client.host}: {exc}")
    return _rate_limit_exceeded_handler(request, exc)

# Global exception handler for unhandled exceptions
@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logging.error(f"Unhandled exception: {exc}", exc_info=True, extra={"request_url": str(request.url)})
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred"},
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
