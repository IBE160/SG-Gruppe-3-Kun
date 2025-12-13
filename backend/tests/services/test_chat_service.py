import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.services.chat_service import ChatService, FALLBACK_MESSAGE
from app.schemas.chat import ChatRequest, ChatResponse, SourceCitation
from app.core.config import settings

@pytest.fixture
def mock_chroma_client():
    """Mocks a ChromaDB client."""
    return MagicMock()

@pytest.fixture
def chat_service():
    """Provides a ChatService instance with mocked dependencies."""
    with patch('app.services.chat_service.genai'), \
         patch('app.services.chat_service.Agent') as MockAgent:
        
        # Configure the mock agent for generate_chat_response
        mock_agent_instance = MockAgent.return_value
        mock_agent_instance.run = AsyncMock()

        # Configure the mock streaming_agent for stream_chat_response
        mock_streaming_agent_instance = MagicMock()
        mock_streaming_agent_instance.run_stream = MagicMock()
        MockAgent.return_value = mock_agent_instance # ensure the same mock instance is used

        service = ChatService()
        service.agent = mock_agent_instance # Assign the mock instance
        service.streaming_agent = mock_streaming_agent_instance # Assign the mock streaming instance
        yield service

@pytest.mark.asyncio
async def test_generate_chat_response_low_confidence_fallback(chat_service, mock_chroma_client):
    """
    Test that low confidence responses trigger the fallback mechanism.
    """
    # Mocking the _prepare_context to return a dummy prompt and no citations initially
    chat_service._prepare_context = AsyncMock(return_value=("dummy prompt", []))

    # Mock the agent.run to return a ChatResponse with low confidence
    mock_chat_response_data = ChatResponse(
        answer="This is a fabricated answer.",
        citations=[SourceCitation(title="Test", url="http://test.com")],
        confidence=settings.RAG_CONFIDENCE_THRESHOLD - 0.1,  # Below threshold
        fallback_message=None
    )
    chat_service.agent.run.return_value.data = mock_chat_response_data

    request = ChatRequest(message="What is a low confidence query?")
    response = await chat_service.generate_chat_response(request, mock_chroma_client)

    assert response.answer == ""
    assert response.citations == []
    assert response.fallback_message == FALLBACK_MESSAGE
    assert response.confidence is not None
    assert response.confidence < settings.RAG_CONFIDENCE_THRESHOLD

@pytest.mark.asyncio
async def test_generate_chat_response_high_confidence_no_fallback(chat_service, mock_chroma_client):
    """
    Test that high confidence responses do NOT trigger the fallback mechanism.
    """
    # Mocking the _prepare_context to return a dummy prompt and some citations
    mock_citations = [SourceCitation(title="High Conf Doc", url="http://highconf.com")]
    chat_service._prepare_context = AsyncMock(return_value=("dummy prompt", mock_citations))

    # Mock the agent.run to return a ChatResponse with high confidence
    expected_answer = "This is a confident answer based on documentation."
    mock_chat_response_data = ChatResponse(
        answer=expected_answer,
        citations=mock_citations,
        confidence=settings.RAG_CONFIDENCE_THRESHOLD + 0.1,  # Above threshold
        fallback_message=None
    )
    chat_service.agent.run.return_value.data = mock_chat_response_data

    request = ChatRequest(message="What is a high confidence query?")
    response = await chat_service.generate_chat_response(request, mock_chroma_client)

    assert response.answer == expected_answer
    assert response.citations == mock_citations
    assert response.fallback_message is None
    assert response.confidence is not None
    assert response.confidence >= settings.RAG_CONFIDENCE_THRESHOLD

@pytest.mark.asyncio
async def test_generate_chat_response_ambiguous_query_suggestions(chat_service, mock_chroma_client):
    """
    Test that ambiguous queries trigger suggestion generation.
    """
    # Mocking the _prepare_context to return a dummy prompt and no citations initially
    chat_service._prepare_context = AsyncMock(return_value=("dummy prompt for ambiguous query", []))

    # Mock the agent.run to return a ChatResponse with suggested queries
    expected_suggestions = [
        "What are the rules for vehicle access on site?",
        "How do I properly dispose of chemical waste?"
    ]
    expected_answer = "Your query is broad. Here are some suggestions:"
    mock_chat_response_data = ChatResponse(
        answer=expected_answer,
        citations=[],
        confidence=0.8, # Confidence can be anything if suggestions are present
        fallback_message=None,
        suggested_queries=expected_suggestions
    )
    chat_service.agent.run.return_value.data = mock_chat_response_data

    request = ChatRequest(message="Tell me about rules")
    response = await chat_service.generate_chat_response(request, mock_chroma_client)

    assert response.answer == expected_answer
    assert response.citations == []
    assert response.fallback_message is None
    assert response.suggested_queries == expected_suggestions
    assert response.confidence == 0.8
