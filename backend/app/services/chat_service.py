import os
from typing import List, Tuple, Any
import google.generativeai as genai
from dotenv import load_dotenv
from chromadb.api import ClientAPI

from pydantic_ai import Agent
from app.schemas.chat import ChatRequest, ChatResponse, SourceCitation
from app.rag.vector_store import query_collection

load_dotenv()

# Configure the generative AI model
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

class ChatService:
    def __init__(self):
        # Initialize the PydanticAI Agent
        # We use a static system prompt here, but context will be injected dynamically.
        self.agent = Agent(
            'google-gla:gemini-1.5-flash',
            result_type=ChatResponse,
            system_prompt=(
                "You are a helpful assistant. Use the provided context to answer the user's question. "
                "If you don't know the answer, just say that you don't know. "
                "You must output a JSON object matching the ChatResponse schema."
            ),
        )
        # Agent for streaming (returns text)
        self.streaming_agent = Agent(
            'google-gla:gemini-1.5-flash',
            system_prompt=(
                "You are a helpful assistant. Use the provided context to answer the user's question. "
                "If you don't know the answer, just say that you don't know."
            ),
        )

    async def _prepare_context(self, request: ChatRequest, chroma_client: ClientAPI) -> tuple[str, List[SourceCitation]]:
        """
        Shared logic to embed query and retrieve context.
        Returns (prompt_with_context, retrieved_citations)
        """
        # 1. Embed the user's query
        embedding_result = genai.embed_content(
            model="models/text-embedding-004",
            content=request.message,
            task_type="retrieval_query"
        )
        query_embedding = embedding_result["embedding"]

        # 2. Retrieve relevant chunks from ChromaDB
        query_result = query_collection(
            client=chroma_client,
            query_embedding=query_embedding,
            n_results=4
        )
        
        # 3. Format context with source metadata for the model
        formatted_chunks = []
        retrieved_citations: List[SourceCitation] = []
        seen_urls = set()

        if query_result.documents:
            for i, doc_list in enumerate(query_result.documents):
                # query_result.documents is a list of lists (one per query)
                # Since we query one embedding, we take the first list
                metas = query_result.metadatas[i]
                for doc, meta in zip(doc_list, metas):
                    source = meta.get('url', 'Unknown')
                    title = meta.get('title', 'Untitled')
                    formatted_chunks.append(f"Source: {title} ({source})\nContent: {doc}")
                    
                    if source not in seen_urls and source != 'Unknown':
                        retrieved_citations.append(SourceCitation(title=title, url=source))
                        seen_urls.add(source)

        context_str = "\n\n".join(formatted_chunks)

        # 4. Construct the prompt with context
        prompt_with_context = (
            f"Context:\n{context_str}\n\n"
            f"Question: {request.message}\n\n"
            f"Answer the question using the context above."
        )
        
        return prompt_with_context, retrieved_citations

    async def generate_chat_response(self, request: ChatRequest, chroma_client: ClientAPI) -> ChatResponse:
        """
        Orchestrates the RAG pipeline: Embedding -> Retrieval -> Generation.
        """
        try:
            prompt_with_context, _ = await self._prepare_context(request, chroma_client)
            
            # Append specific instruction for JSON format if needed, though result_type handles it mostly
            prompt_with_context += " Provide citations as a list of source URLs used."

            # 5. Run the PydanticAI Agent
            result = await self.agent.run(prompt_with_context)
            
            return result.data

        except Exception as e:
            # Fallback for errors
            print(f"Error in RAG pipeline: {e}")
            return ChatResponse(
                answer="I encountered an error while processing your request.",
                citations=[]
            )

    async def stream_chat_response(self, request: ChatRequest, chroma_client: ClientAPI):
        """
        Streams the response using SSE-compatible logic.
        Yields (type, content) tuples.
        """
        try:
            prompt_with_context, retrieved_citations = await self._prepare_context(request, chroma_client)
            
            # Stream the response
            # Note: run_stream returns a context manager or async iterator depending on version. 
            # In v0.0.19 it likely returns a StreamedRunResult which we can iterate.
            async with self.streaming_agent.run_stream(prompt_with_context) as result:
                async for chunk in result.stream():
                    yield ("token", chunk)

            # Yield citations after streaming is complete
            citations_data = [c.model_dump() for c in retrieved_citations]
            yield ("citation", citations_data)
            
        except Exception as e:
            print(f"Error in streaming RAG pipeline: {e}")
            yield ("error", "I encountered an error while processing your request.")