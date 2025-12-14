import uuid
import logging
from contextvars import ContextVar
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

# Context variable to hold the correlation ID for the current request
correlation_id_ctx: ContextVar[str | None] = ContextVar("correlation_id_ctx", default=None)

class CorrelationIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        _correlation_id = str(uuid.uuid4())
        
        # Set the correlation ID in the context variable
        token = correlation_id_ctx.set(_correlation_id)
        
        # Add to request headers
        request.headers.__dict__["_list"].append(
            (b"x-correlation-id", _correlation_id.encode())
        )
        # Add to response headers
        try:
            response = await call_next(request)
            response.headers["X-Correlation-ID"] = _correlation_id
            return response
        finally:
            # Reset the context variable
            correlation_id_ctx.reset(token)

class CorrelationIdFilter(logging.Filter):
    def filter(self, record):
        record.correlation_id = correlation_id_ctx.get()
        return True

# Ensure the filter is added to all loggers
def add_correlation_id_filter():
    for handler in logging.root.handlers:
        handler.addFilter(CorrelationIdFilter())
    logging.getLogger().addFilter(CorrelationIdFilter())
