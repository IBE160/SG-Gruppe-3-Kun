import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.services.chat_service import ChatService
from app.schemas.chat import ChatRequest, ChatResponse, SourceCitation, UserRole
from app.schemas.rag import QueryResult # Import QueryResult

@pytest.fixture
def mock_chroma_client():
    """Fixture for a mocked ChromaDB client."""
    return MagicMock()

@pytest.fixture
def chat_service():
    """
    Fixture for ChatService with the pydantic_ai.Agent patched to avoid
    instantiating the real Gemini model and requiring an API key.
    """
    with patch("app.services.chat_service.Agent", spec=True) as MockAgent:
        service = ChatService()
        yield service

@pytest.mark.asyncio
async def test_generate_chat_response_success(chat_service, mock_chroma_client):
    user_message = "What is safety?"
    mock_embedding = [0.1, 0.2, 0.3]
    mock_documents = ["Safety is priority.", "Wear helmets."] # List of strings
    mock_metadatas = [{"url": "url1", "title": "Doc1"}, {"url": "url2", "title": "Doc2"}] # List of dicts

    mock_agent_response = ChatResponse(
        answer="Safety is important.",
        citations=[SourceCitation(title="Doc1", url="url1")]
    )

    chat_service.agent.run = AsyncMock(return_value=MagicMock(data=mock_agent_response))

    with patch("app.services.chat_service.genai.embed_content") as mock_embed, \
         patch("app.services.chat_service.query_collection") as mock_query:
        
        mock_embed.return_value = {"embedding": mock_embedding}
        
        # Mock query_collection to return a QueryResult object
        mock_query.return_value = QueryResult(documents=mock_documents, metadatas=mock_metadatas)

        request = ChatRequest(message=user_message, user_role=UserRole.PROJECT_MANAGER_ADMIN)
        response = await chat_service.generate_chat_response(request, mock_chroma_client)

        mock_embed.assert_called_once()
        mock_query.assert_called_once()
        chat_service.agent.run.assert_called_once()
        
        call_args = chat_service.agent.run.call_args[0][0]
        assert "Safety is priority." in call_args
        
        assert response.answer == "Safety is important."
        assert response.citations[0].url == "url1"

@pytest.mark.asyncio
async def test_generate_chat_response_error_handling(chat_service, mock_chroma_client):
    with patch("app.services.chat_service.genai.embed_content", side_effect=Exception("API Error")):
        request = ChatRequest(message="Crash me", user_role=UserRole.CONSTRUCTION_WORKER)
        response = await chat_service.generate_chat_response(request, mock_chroma_client)
        assert "encountered an error" in response.answer

@pytest.mark.asyncio
async def test_stream_chat_response_yields_citations_and_receives_user_role(chat_service, mock_chroma_client):
    user_message = "What is a reg card?"
    user_role_test = UserRole.CONSTRUCTION_WORKER
    
    prepared_context = "Context: some_context\n\nQuestion: What is a reg card?"
    citations = [SourceCitation(title="Reg Card Guide", url="https://docs.hmsreg.com/reg-card")]

    async def async_token_generator():
        yield "To get a reg card..."

    mock_stream_result = MagicMock()
    mock_stream_result.stream = async_token_generator
    chat_service.streaming_agent.run_stream.return_value = MagicMock(__aenter__=AsyncMock(return_value=mock_stream_result))

    with patch.object(chat_service, "_prepare_context", new_callable=AsyncMock) as mock_prepare_context:
        mock_prepare_context.return_value = (prepared_context, citations)
        
        request = ChatRequest(message=user_message, user_role=user_role_test)
        
        events = []
        async for event_type, content in chat_service.stream_chat_response(request, mock_chroma_client):
            events.append((event_type, content))
        
        mock_prepare_context.assert_called_once_with(request, mock_chroma_client)
        assert mock_prepare_context.call_args[0][0].user_role == user_role_test

        chat_service.streaming_agent.run_stream.assert_called_once_with(prepared_context)

        assert ("token", "To get a reg card...") in events
        
        citation_event = next((e for e in events if e[0] == "citation"), None)
        assert citation_event is not None
        assert citation_event[1] == [c.model_dump() for c in citations]