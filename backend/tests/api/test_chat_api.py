from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app
from app.core.dependencies import get_chroma_client

client = TestClient(app)

def test_stream_chat_endpoint():
    # Mock generator for stream_chat_response
    async def mock_generator(*args, **kwargs):
        tokens = ["Hello", " ", "World"]
        for token in tokens:
            yield token

    # Override ChromaDB client dependency
    app.dependency_overrides[get_chroma_client] = lambda: "mock_chroma_client"

    # Patch the service method
    with patch("app.api.v1.endpoints.chat.chat_service.stream_chat_response", side_effect=mock_generator):
        response = client.post(
            "/api/v1/chat/stream",
            json={"message": "Test message", "role": "user"}
        )

        assert response.status_code == 200
        assert "text/event-stream" in response.headers["content-type"]
        
        content = response.text
        # Check for SSE format
        assert 'data: {"type": "token", "content": "Hello"}\n\n' in content
        assert 'data: {"type": "token", "content": " "}\n\n' in content
        assert 'data: {"type": "token", "content": "World"}\n\n' in content

    # Clean up overrides
    app.dependency_overrides = {}
