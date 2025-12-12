import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.services.chat_service import ChatService
from app.schemas.chat import ChatRequest, ChatResponse, SourceCitation
# app.schemas.rag might not exist or QueryResult might be from chromadb directly?
# In chat_service.py: from app.rag.vector_store import query_collection
# Let's assume QueryResult is returned by query_collection. 
# Usually Chroma returns a dict-like object. 
# But let's stick to what we see.

@pytest.fixture
def mock_chroma_client():
    return MagicMock()

@pytest.fixture
def chat_service():
    return ChatService()

@pytest.mark.asyncio
async def test_generate_chat_response_success(chat_service, mock_chroma_client):
    # Mock data
    user_message = "What is safety?"
    mock_embedding = [0.1, 0.2, 0.3]
    # Corrected to list of lists
    mock_documents = [["Safety is priority.", "Wear helmets."]]
    mock_metadatas = [[{"url": "url1", "title": "Doc1"}, {"url": "url2", "title": "Doc2"}]]
    
    mock_agent_response = ChatResponse(
        answer="Safety is important.",
        citations=[SourceCitation(title="Doc1", url="url1")] # Updated to list of SourceCitation objects (or dicts matching model)
    )

    # Patch dependencies
    with patch("app.services.chat_service.genai.embed_content") as mock_embed, \
         patch("app.services.chat_service.query_collection") as mock_query, \
         patch.object(chat_service.agent, "run", new_callable=AsyncMock) as mock_agent_run:
        
        # Setup mocks
        mock_embed.return_value = {"embedding": mock_embedding}
        
        mock_query_result = MagicMock()
        mock_query_result.documents = mock_documents
        mock_query_result.metadatas = mock_metadatas
        mock_query.return_value = mock_query_result

        mock_agent_run.return_value.data = mock_agent_response

        # Execute
        request = ChatRequest(message=user_message, user_role="Project Manager") # Changed to user_role
        response = await chat_service.generate_chat_response(request, mock_chroma_client)

        # Verify assertions
        mock_embed.assert_called_once()
        mock_query.assert_called_once_with(
            client=mock_chroma_client,
            query_embedding=mock_embedding,
            n_results=4
        )
        mock_agent_run.assert_called_once()
        
        # Check if context was passed to agent
        call_args = mock_agent_run.call_args[0][0]
        assert "Safety is priority." in call_args
        assert "Wear helmets." in call_args
        
        assert response.answer == "Safety is important."
        # Verify citation objects
        assert response.citations[0].url == "url1"

@pytest.mark.asyncio
async def test_generate_chat_response_error_handling(chat_service, mock_chroma_client):
    # Patch dependencies to raise an exception
    with patch("app.services.chat_service.genai.embed_content", side_effect=Exception("API Error")):
        
        request = ChatRequest(message="Crash me", user_role="User") # Changed to user_role
        response = await chat_service.generate_chat_response(request, mock_chroma_client)
        
        assert "encountered an error" in response.answer

@pytest.mark.asyncio
async def test_stream_chat_response_yields_citations_and_receives_user_role(chat_service, mock_chroma_client): # Renamed test
    user_message = "What is a reg card?"
    user_role_test = "Construction Worker" # Specific role for this test
    mock_embedding = [0.1, 0.2, 0.3]
    mock_documents = [["Reg card info..."]]
    mock_metadatas = [[{"url": "https://docs.hmsreg.com/reg-card", "title": "Reg Card Guide"}]]
    
    with patch("app.services.chat_service.genai.embed_content") as mock_embed, \
         patch("app.services.chat_service.query_collection") as mock_query, \
         patch.object(chat_service.streaming_agent, "run_stream") as mock_agent_stream, \
         patch.object(chat_service, "_prepare_context", new_callable=AsyncMock) as mock_prepare_context: # Patch _prepare_context
        
        mock_embed.return_value = {"embedding": mock_embedding}
        
        mock_query_result = MagicMock()
        mock_query_result.documents = mock_documents
        mock_query_result.metadatas = mock_metadatas
        mock_query.return_value = mock_query_result

        # Mock _prepare_context to return expected values
        mock_prepare_context.return_value = ("Context: some_context\n\nQuestion: What is a reg card?", [SourceCitation(title="Reg Card Guide", url="https://docs.hmsreg.com/reg-card")])

        mock_stream_result = MagicMock()
        
        async def async_generator():
            yield "To"
            yield " get"
            yield " a"
            yield " reg"
            yield " card..."
        
        mock_stream_result.stream.return_value = async_generator()
        mock_agent_stream.return_value.__aenter__.return_value = mock_stream_result

        request = ChatRequest(message=user_message, user_role=user_role_test) # Pass user_role
        
        events = []
        async for event in chat_service.stream_chat_response(request, mock_chroma_client):
            events.append(event)
        
        # Verify _prepare_context was called with the correct request object
        mock_prepare_context.assert_called_once_with(request, mock_chroma_client)
        assert mock_prepare_context.call_args[0][0].user_role == user_role_test

        # Verify other streaming assertions (citations, tokens)
        assert ("token", "To") in events
        assert ("token", " card...") in events
        
        citation_event = next((e for e in events if e[0] == "citation"), None)
        assert citation_event is not None
        
        citations = citation_event[1]
        assert len(citations) == 1
        assert citations[0]["title"] == "Reg Card Guide"
        assert citations[0]["url"] == "https://docs.hmsreg.com/reg-card"