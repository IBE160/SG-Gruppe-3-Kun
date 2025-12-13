import os
from typing import List, Tuple, Any
import google.generativeai as genai
from dotenv import load_dotenv
from chromadb.api import ClientAPI

from pydantic_ai import Agent
from app.schemas.chat import ChatRequest, ChatResponse, SourceCitation
from app.rag.vector_store import query_collection
from app.core.config import settings # Import settings

load_dotenv()

# Configure the generative AI model
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

FALLBACK_MESSAGE = (
    "Jeg fant ikke et klart svar i dokumentasjonen for dette spørsmålet. "
    "Kan du utdype spørsmålet? Du kan også søke direkte i "
    "[dokumentasjonen](https://docs.hmsreg.com)."
)

class ChatService:
    def __init__(self):
        # Initialize the PydanticAI Agent
        # We use a static system prompt here, but context will be injected dynamically.
        self.agent = Agent(
            'google-gla:gemini-2.5-flash',
            output_type=ChatResponse,
        )
        # Agent for streaming (returns text)
        self.streaming_agent = Agent(
            'google-gla:gemini-2.5-flash',
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
        seen_chunks_content = set() # To track unique chunk content

        if query_result.documents:
            for doc, meta in zip(query_result.documents, query_result.metadatas):
                if doc and meta: # Ensure doc and meta are not None/empty
                    source = meta.get('url', 'Unknown')
                    title = meta.get('title', 'Untitled')
                    
                    # Create a unique representation of the chunk content for de-duplication
                    chunk_content = f"Title: {title}\nSource: {source}\nContent: {doc}"
                    if chunk_content not in seen_chunks_content:
                        formatted_chunks.append(chunk_content)
                        seen_chunks_content.add(chunk_content)
                        
                        if source not in seen_urls and source != 'Unknown':
                            retrieved_citations.append(SourceCitation(title=title, url=source))
                            seen_urls.add(source)

        context_str = "\n\n".join(formatted_chunks)

        # 4. Construct the prompt with context
        prompt_with_context = (
            f"Context:\n{context_str}\n\n"
            f"Question: {request.message}\n\n"
            f"Answer the question using ONLY the provided context. "
            f"Synthesize information from multiple sources if necessary to provide a comprehensive answer, "
            f"but avoid direct repetition or verbatim copying of content. Be concise and to the point."
        )
        
        return prompt_with_context, retrieved_citations

    async def generate_chat_response(self, request: ChatRequest, chroma_client: ClientAPI) -> ChatResponse:
        """
        Orchestrates the RAG pipeline: Embedding -> Retrieval -> Generation.
        """
        try:
            prompt_with_context, _ = await self._prepare_context(request, chroma_client)
            
            # No need to append specific instruction for JSON format, output_type handles it.
            # prompt_with_context += " Provide citations as a list of source URLs used."

            user_role = request.user_role.value if request.user_role else "General User"

            system_prompt = (
                f"You are a helpful assistant for HMSREG documentation.\n"
                f"Target Audience Role: {user_role}\n\n"
                f"Instructions:\n"
                f"- Answer the user's question in the same language as the question. "
                f"Synthesize and fully rephrase information from the provided context. "
                f"UNDER NO CIRCUMSTANCES should you directly copy sentences or paragraphs verbatim from the context. "
                f"Avoid any repetition. Be concise and to the point.\n"
                f"- Adapt your tone and focus to be most helpful to a {user_role}.\n"
                f"- If the user's query is too broad or ambiguous, identify it as such.\n"
                f"- Populate the 'suggested_queries' field of the ChatResponse with 2-3 specific, relevant follow-up questions or topics if ambiguity is detected.\n"
                f"- If 'suggested_queries' are provided, the 'answer' field should be a concise statement acknowledging the ambiguity and guiding the user to the suggestions.\n"
                f"If you don't know the answer based on the context, just say that you don't know. "
                f"You must output a JSON object matching the ChatResponse schema."
            )
            result = await self.agent.run(prompt_with_context, instructions=system_prompt)
            
            # Check confidence score as per AC 1 and 4
            if result.output.confidence is not None and result.output.confidence < settings.RAG_CONFIDENCE_THRESHOLD:
                result.output.answer = ""
                result.output.citations = [] # Discard citations if answer is not confident
                result.output.fallback_message = FALLBACK_MESSAGE # Set fallback message
            
            return result.output

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
            
            user_role = request.user_role.value if request.user_role else "General User"

            system_prompt = (
                f"You are a helpful assistant for HMSREG documentation.\n"
                f"Target Audience Role: {user_role}\n\n"
                f"Instructions:\n"
                f"- Answer the user's question based strictly on the provided context. "
                f"Synthesize information from multiple sources if necessary to provide a comprehensive answer, "
                f"but avoid direct repetition or verbatim copying of content. Be concise and to the point.\n"
                f"- Adapt your tone and focus to be most helpful to a {user_role}.\n"
                f"- If the user's query is too broad or ambiguous, identify it as such.\n"
                f"- Populate the 'suggested_queries' field of the ChatResponse with 2-3 specific, relevant follow-up questions or topics if ambiguity is detected.\n"
                f"- If 'suggested_queries' are provided, the 'answer' field should be a concise statement acknowledging the ambiguity and guiding the user to the suggestions.\n"
                f"If you don't know the answer based on the context, just say that you don't know. "
                f"You must output a JSON object matching the ChatResponse schema."
            )
            
            # First, get a complete ChatResponse object to check for fallback or suggestions
            full_response_result = await self.agent.run(prompt_with_context, instructions=system_prompt)
            full_response = full_response_result.output # Changed from .data

            # Handle fallback message
            if full_response.fallback_message:
                yield ("fallback", full_response.fallback_message)
                return

            # Handle suggested queries
            if full_response.suggested_queries:
                yield ("suggestions", full_response.suggested_queries)
                # If suggestions are provided, the answer might be very short or empty,
                # so we might not need to stream anything further, or just stream the short answer.
                # For now, let's assume if suggestions are primary, the main answer streaming is secondary/empty.
                if full_response.answer:
                    # Yield a very short answer if any, before citations
                    yield ("token", full_response.answer)
                citations_data = [c.model_dump() for c in retrieved_citations]
                yield ("citation", citations_data)
                return

            # If no fallback or suggestions, proceed with streaming the main answer
            # We still need a system prompt that doesn't expect a Pydantic object for the streaming agent
            streaming_system_prompt = (
                f"You are a helpful assistant for HMSREG documentation.\n"
                f"Target Audience Role: {user_role}\n\n"
                f"Instructions:\n"
                f"- Answer the user's question in the same language as the question. "
                f"Synthesize and fully rephrase information from the provided context. "
                f"UNDER NO CIRCUMSTANCES should you directly copy sentences or paragraphs verbatim from the context. "
                f"Avoid any repetition. Be concise and to the point.\n"
                f"- Adapt your tone and focus to be most helpful to a {user_role}.\n"
                f"If you don't know the answer, just say that you don't know."
            )

            async with self.streaming_agent.run_stream(prompt_with_context, instructions=streaming_system_prompt) as result:
                async for chunk in result.stream():
                    print(f"Raw stream chunk: '{chunk}'") # Temporary debug print
                    yield ("token", chunk)

            # Yield citations after streaming is complete
            citations_data = [c.model_dump() for c in retrieved_citations]
            yield ("citation", citations_data)
            
        except Exception as e:
            print(f"Error in streaming RAG pipeline: {e}")
            yield ("error", f"I encountered an error while processing your request: {str(e)}")
