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
        # Initialize the PydanticAI Agent with model settings
        # Lower temperature to reduce repetition
        from pydantic_ai.models.gemini import GeminiModelSettings

        model_settings = GeminiModelSettings(temperature=0.3)

        self.agent = Agent(
            'google-gla:gemini-2.5-flash',
            output_type=ChatResponse,
            model_settings=model_settings,
        )
        # Agent for streaming (returns text)
        self.streaming_agent = Agent(
            'google-gla:gemini-2.5-flash',
            model_settings=model_settings,
        )

        # Domain-specific term expansions for better matching
        self.term_expansions = {
            'kort': ['kort', 'HMS kort', 'HMS-kort', 'HMSREG kort'],
            'register': ['register', 'registrering', 'HMS register'],
            'risiko': ['risiko', 'risikovurdering', 'risikostyring'],
            'underleverandør': ['leverandør', 'underleverandører', 'entreprenør', 'underentreprenør'],
            'hovedentreprenør': ['hovedleverandør', 'hovedbedrift'],
        }

    def _expand_query(self, query: str) -> str:
        """Expand query with domain-specific terms for better matching."""
        query_lower = query.lower()
        expanded_terms = []

        for term, expansions in self.term_expansions.items():
            if term in query_lower:
                # Add all expansion variations
                expanded_terms.extend(expansions)

        if expanded_terms:
            # Combine original query with expansions
            return f"{query} {' '.join(set(expanded_terms))}"

        return query

    async def _prepare_context(self, request: ChatRequest, chroma_client: ClientAPI) -> tuple[str, List[SourceCitation]]:
        """
        Shared logic to embed query and retrieve context.
        Returns (prompt_with_context, retrieved_citations)
        """
        # 1. Expand the query for better matching
        expanded_query = self._expand_query(request.message)

        # 2. Embed the expanded query
        embedding_result = genai.embed_content(
            model="models/text-embedding-004",
            content=expanded_query,
            task_type="retrieval_query"
        )
        query_embedding = embedding_result["embedding"]

        # 3. Retrieve chunks for deduplication (reduced from 15 to 10)
        query_result = query_collection(
            client=chroma_client,
            query_embedding=query_embedding,
            n_results=10
        )
        
        # 4. Smart deduplication: remove similar chunks, not just exact matches
        formatted_chunks = []
        retrieved_citations: List[SourceCitation] = []
        seen_urls = set()
        unique_docs = []

        if query_result.documents:
            for doc, meta in zip(query_result.documents, query_result.metadatas):
                if doc and meta:
                    # Check if this chunk is similar to any already selected chunk
                    is_duplicate = False
                    doc_normalized = doc.lower().strip()

                    for existing_doc in unique_docs:
                        existing_normalized = existing_doc.lower().strip()

                        # Check for exact match
                        if doc_normalized == existing_normalized:
                            is_duplicate = True
                            break

                        # Check if one is a substring of the other (likely duplicate)
                        if (doc_normalized in existing_normalized or
                            existing_normalized in doc_normalized):
                            is_duplicate = True
                            break

                        # Check for high word overlap (lowered from 85% to 60%)
                        doc_words = set(doc_normalized.split())
                        existing_words = set(existing_normalized.split())
                        if doc_words and existing_words:
                            overlap = len(doc_words & existing_words) / len(doc_words | existing_words)
                            if overlap > 0.60:  # 60% word overlap = likely duplicate
                                is_duplicate = True
                                break

                        # Check for sentence-level duplication (first sentence match)
                        doc_sentences = [s.strip() for s in doc_normalized.split('.') if s.strip()]
                        existing_sentences = [s.strip() for s in existing_normalized.split('.') if s.strip()]
                        if doc_sentences and existing_sentences:
                            # If first sentences are very similar, likely duplicate
                            if doc_sentences[0] == existing_sentences[0]:
                                is_duplicate = True
                                break

                    if not is_duplicate:
                        source = meta.get('url', 'Unknown')
                        title = meta.get('title', 'Untitled')

                        chunk_content = f"Title: {title}\nSource: {source}\nContent: {doc}"
                        formatted_chunks.append(chunk_content)
                        unique_docs.append(doc)

                        if source not in seen_urls and source != 'Unknown':
                            retrieved_citations.append(SourceCitation(title=title, url=source))
                            seen_urls.add(source)

                # Limit to best 3 chunks after deduplication (further reduced to test)
                if len(formatted_chunks) >= 3:
                    break

        # Debug: Log how many chunks we're actually using
        print(f"[DEBUG] Retrieved {len(query_result.documents) if query_result.documents else 0} chunks from DB")
        print(f"[DEBUG] After deduplication: {len(formatted_chunks)} unique chunks")
        print(f"[DEBUG] First chunk preview: {formatted_chunks[0][:200] if formatted_chunks else 'No chunks'}...")

        context_str = "\n\n".join(formatted_chunks)

        # 5. Construct the prompt with context
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
                f"CRITICAL INSTRUCTIONS:\n"
                f"- Answer the user's question in the same language as the question.\n"
                f"- Synthesize information from ALL context sources into ONE cohesive, flowing answer.\n"
                f"- DO NOT repeat the same information multiple times, even if it appears in multiple context sources.\n"
                f"- Each piece of information should appear ONLY ONCE in your answer.\n"
                f"- NEVER copy sentences or paragraphs verbatim from the context.\n"
                f"- Be concise, clear, and to the point. Avoid redundancy.\n"
                f"- If the context contains overlapping information, merge it into a single coherent explanation.\n"
                f"- Complete your sentences - never cut off mid-sentence.\n\n"
                f"Additional Guidelines:\n"
                f"- Adapt your tone and focus to be most helpful to a {user_role}.\n"
                f"- If the user's query is too broad or ambiguous, identify it as such and populate 'suggested_queries' with 2-3 specific follow-up questions.\n"
                f"- If you don't know the answer based on the context, say so.\n"
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
                f"CRITICAL INSTRUCTIONS:\n"
                f"- Answer the user's question in the same language as the question.\n"
                f"- Synthesize information from ALL context sources into ONE cohesive, flowing answer.\n"
                f"- DO NOT repeat the same information multiple times, even if it appears in multiple context sources.\n"
                f"- Each piece of information should appear ONLY ONCE in your answer.\n"
                f"- NEVER copy sentences or paragraphs verbatim from the context.\n"
                f"- Be concise, clear, and to the point. Avoid redundancy.\n"
                f"- If the context contains overlapping information, merge it into a single coherent explanation.\n"
                f"- Complete your sentences - never cut off mid-sentence.\n"
                f"- Adapt your tone and focus to be most helpful to a {user_role}.\n"
                f"If you don't know the answer, just say that you don't know."
            )

            # Track accumulated text to only send new portions
            accumulated_text = ""

            async with self.streaming_agent.run_stream(prompt_with_context, instructions=streaming_system_prompt) as result:
                async for chunk in result.stream():
                    # Gemini returns full accumulated text, not deltas
                    # We need to extract only the new portion
                    if chunk and len(chunk) > len(accumulated_text):
                        new_text = chunk[len(accumulated_text):]
                        accumulated_text = chunk
                        print(f"New chunk (delta): '{new_text}'") # Debug
                        yield ("token", new_text)
                    elif chunk != accumulated_text:
                        # In case of unexpected format, send the chunk
                        print(f"Unexpected chunk format: '{chunk}'")
                        yield ("token", chunk)
                        accumulated_text = chunk

            # Yield citations after streaming is complete
            citations_data = [c.model_dump() for c in retrieved_citations]
            yield ("citation", citations_data)
            
        except Exception as e:
            print(f"Error in streaming RAG pipeline: {e}")
            yield ("error", f"I encountered an error while processing your request: {str(e)}")
