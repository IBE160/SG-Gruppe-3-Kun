import logging
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from chromadb.api import ClientAPI
import json

from app.schemas.chat import ChatRequest
from app.services.chat_service import ChatService
from app.core.dependencies import get_chroma_client

router = APIRouter()
chat_service = ChatService()
logger = logging.getLogger(__name__) # Initialize logger

@router.post("/stream")
async def stream_chat(
    request: ChatRequest,
    chroma_client: ClientAPI = Depends(get_chroma_client)
):
    """
    Streaming endpoint for chat.
    Uses Server-Sent Events (SSE) to stream the response token-by-token.
    """
    logger.debug(f"Received chat request for user_role: {request.user_role}") # Log the user_role
    async def event_generator():
        try:
            async for event_type, content in chat_service.stream_chat_response(request, chroma_client):
                # Format as SSE
                data = json.dumps({"type": event_type, "content": content})
                yield f"data: {data}\n\n"
        except Exception as e:
            # Yield an error event
            error_data = json.dumps({"type": "error", "content": str(e)})
            yield f"data: {error_data}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
