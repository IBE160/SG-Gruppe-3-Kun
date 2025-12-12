from fastapi.testclient import TestClient
from unittest.mock import MagicMock, AsyncMock
import pytest
import asyncio
from app.main import app
from app.core.dependencies import get_chroma_client, get_chat_service
from app.schemas.chat import UserRole
from app.services.chat_service import ChatService

client = TestClient(app)

# --- Mock Dependencies ---
@pytest.fixture(autouse=True)
def override_dependencies():
    # This fixture will apply the mocks to all tests in this file.
    
    # Mock ChatService for testing API layer in isolation
    mock_chat_service = MagicMock(spec=ChatService)
    mock_chat_service.stream_chat_response = AsyncMock() # Mock the async generator method

    def override_get_chat_service():
        return mock_chat_service

    def override_get_chroma_client():
        return MagicMock()

    original_overrides = app.dependency_overrides.copy()
    app.dependency_overrides[get_chat_service] = override_get_chat_service
    app.dependency_overrides[get_chroma_client] = override_get_chroma_client
    
    yield mock_chat_service # yield the mock to be used in tests

    # Restore original overrides after tests are done
    app.dependency_overrides = original_overrides

# --- Helper for mocking async generator with explicit AsyncIterator ---
class MockAsyncIterator:
    def __init__(self, data):
        self._data = iter(data)

    async def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            return next(self._data)
        except StopIteration:
            raise StopAsyncIteration

# --- Tests ---

def test_stream_chat_with_default_role(override_dependencies):
    """
    Test that the chat stream works correctly and the service is called
    with the default user role when none is provided.
    """
    mock_chat_service = override_dependencies
    mock_chat_service.stream_chat_response.return_value = MockAsyncIterator([("token", "Hello")])
    
    response = client.post(
        "/api/v1/chat/stream",
        json={"message": "Test message"}
    )

    assert response.status_code == 200
    assert "text/event-stream" in response.headers["content-type"]
    
    mock_chat_service.stream_chat_response.assert_called_once()
    request_arg = mock_chat_service.stream_chat_response.call_args[0][0]
    assert request_arg.message == "Test message"
    assert request_arg.user_role is None

def test_stream_chat_with_specific_role(override_dependencies):
    """
    Test that a specific user_role is correctly passed to the chat service.
    """
    mock_chat_service = override_dependencies
    mock_chat_service.stream_chat_response.return_value = MockAsyncIterator([("token", "Role-specific response")])
    
    test_role = UserRole.CONSTRUCTION_WORKER
    response = client.post(
        "/api/v1/chat/stream",
        json={"message": "A role-specific question", "user_role": test_role.value}
    )

    assert response.status_code == 200
    
    mock_chat_service.stream_chat_response.assert_called_once()
    request_arg = mock_chat_service.stream_chat_response.call_args[0][0]
    assert request_arg.message == "A role-specific question"
    assert request_arg.user_role == test_role

def test_stream_chat_with_invalid_role(override_dependencies):
    """
    Test that an invalid user_role returns a validation error.
    """
    mock_chat_service = override_dependencies
    
    response = client.post(
        "/api/v1/chat/stream",
        json={"message": "Test message", "user_role": "invalid-role"}
    )
    assert response.status_code == 422
    assert '"type":"enum"' in response.text
    mock_chat_service.stream_chat_response.assert_not_called()
