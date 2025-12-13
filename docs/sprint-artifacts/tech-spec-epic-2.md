# Epic Technical Specification: Core Conversational Experience & RAG Pipeline

Date: Monday, 8 December 2025
Author: BIP
Epic ID: 2
Status: Draft

---

## Overview

This epic implements the core functionality of the HMSREG Documentation Chatbot: the ability for users to ask questions in natural language and receive accurate, role-aware answers derived strictly from official documentation. It encompasses the end-to-end RAG (Retrieval-Augmented Generation) pipeline—from data ingestion and vector storage to the backend generation logic using Gemini 2.5 Pro—and the user-facing frontend chat interface. This is the foundational "magic" of the product, establishing the primary value proposition of self-service support.

## Objectives and Scope

### In-Scope
*   **Data Ingestion Pipeline:** Automated scraping, chunking, and embedding of documentation from `docs.hmsreg.com`.
*   **Vector Database:** Setup and configuration of ChromaDB for efficient semantic retrieval.
*   **RAG Logic:** Implementation of the Pydantic AI-based backend service to orchestrate retrieval and generation.
*   **Chat Interface:** Development of the responsive React frontend (shadcn/ui) for the chat experience.
*   **Real-time Streaming:** Implementation of Server-Sent Events (SSE) for fluid, typewriter-style response delivery.
*   **Source Citation:** Mechanism to extract and display links to source documentation for every answer.
*   **Responsive Layouts:** Implementation of the specific 3-column (desktop) and tabbed (mobile) layouts defined in the UX Spec.

### Out-of-Scope
*   **Role Selection UI:** While the backend will support role context, the specific UI for *selecting* the role is part of Epic 3.
*   **User Feedback System:** Thumbs up/down logic is part of Epic 4.
*   **Authentication:** The system is public-facing for this MVP.
*   **Advanced Rate Limiting:** Deferred to Epic 5.

## System Architecture Alignment

This implementation strictly adheres to the architecture defined in `docs/architecture.md`:

*   **Frontend:** Next.js 14+ (App Router) using Tailwind CSS and shadcn/ui.
    *   **Components:** `ChatWindow`, `ChatBubble` (custom composition).
    *   **Communication:** Custom `useChat` hook utilizing SSE to consume `POST /api/v1/chat/stream`.
*   **Backend:** FastAPI application utilizing `pydantic-ai` for agent orchestration.
    *   **Service Layer:** `chat_service.py` encapsulates the RAG logic.
    *   **Storage:** `ChromaDB` (local persistence for MVP/Development, ensuring easy transition to server mode).
    *   **LLM:** Google Gemini 2.5 Pro via standard API integration.
*   **Data Flow:**
    1.  User input -> Next.js API Route (Proxy) -> FastAPI `/chat/stream`.
    2.  FastAPI -> `vector_store.py` (Query ChromaDB).
    3.  FastAPI -> `chat_service.py` (Construct Prompt with Context).
    4.  `chat_service.py` -> Gemini API (Generate).
    5.  Gemini API -> `chat_service.py` (Stream) -> Frontend (Render).

## Detailed Design

### Services and Modules

| Module/Service | Responsibility | Inputs | Outputs | Owner |
| :--- | :--- | :--- | :--- | :--- |
| `app/rag/ingestion.py` | Scrapes `docs.hmsreg.com`, splits text, generates embeddings. | URL | ChromaDB Collection Entries | Backend |
| `app/rag/vector_store.py` | Wrapper for ChromaDB client; handles `add_texts` and `similarity_search`. | Text Chunks / Query | Embeddings / Ranked Docs | Backend |
| `app/services/chat_service.py` | Core RAG logic. Defines Pydantic AI Agent, context assembly, and system prompts. | User Query, Role | Streaming Response (Token iterator) | Backend |
| `app/api/v1/chat.py` | FastAPI Endpoint definition. Handles SSE connection management. | `ChatRequest` | `StreamingResponse` | Backend |
| `components/ChatWindow.tsx` | Main chat container. Manages message history state and auto-scrolling. | User Input | UI Rendering | Frontend |
| `hooks/useChat.ts` | Custom hook for SSE connection, state management (loading, error, streaming). | API Endpoint | `messages`, `sendMessage`, `isLoading` | Frontend |

### Data Models and Contracts

**Backend (Pydantic Models):**

```python
# app/schemas/chat.py

class ChatRequest(BaseModel):
    message: str
    role: Optional[str] = "General User" # For Epic 3 context

class SourceCitation(BaseModel):
    title: str
    url: str

class ChatResponseChunk(BaseModel):
    """Event sent via SSE"""
    type: Literal["token", "citation", "error"]
    content: str # The token text or JSON string of citation
```

**Frontend (TypeScript Interfaces):**

```typescript
// types/chat.ts

export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  citations?: SourceCitation[];
}

export interface SourceCitation {
  title: string;
  url: string;
}
```

### APIs and Interfaces

**Endpoint:** `POST /api/v1/chat/stream`

*   **Description:** Initiates a streaming chat generation.
*   **Headers:** `Content-Type: application/json`
*   **Body:** `{"message": "How do I reset my password?", "role": "Worker"}`
*   **Response:** `text/event-stream`
    *   Events:
        *   `data: {"type": "token", "content": "To"}`
        *   `data: {"type": "token", "content": " reset"}`
        *   `data: {"type": "citation", "content": "[{{\"title\": \"Login Help\", \"url\": \"...\"}}]"}`
        *   `data: [DONE]`

### Workflows and Sequencing

**RAG Pipeline (Runtime):**
1.  **Receive:** API receives `ChatRequest`.
2.  **Embed:** Query is embedded using `text-embedding-004`.
3.  **Retrieve:** `vector_store.search(query_embedding, k=5)` returns top 5 chunks.
4.  **Augment:** `chat_service` constructs prompt:
    > "You are a helpful assistant. Use the following context to answer the user's question. Context: [Chunks] Question: [Query]"
5.  **Generate:** Call `gemini-2.5-pro` with `stream=True`.
6.  **Stream:** Yield tokens to client.
7.  **Finalize:** Yield citations extracted from used chunks.

## Non-Functional Requirements

### Performance
*   **Latency:** Time-to-first-token (TTFT) should be under **2 seconds**.
*   **Throughput:** System should handle simultaneous streams without blocking (asyncio).

### Security
*   **Input Sanitization:** All user input validated via Pydantic.
*   **Output Encoding:** React handles escaping of HTML in markdown rendering to prevent XSS.

### Reliability/Availability
*   **Degradation:** If ChromaDB is unavailable, return a polite "Service unavailable" error rather than crashing.
*   **Timeouts:** LLM requests should timeout after 30 seconds.

### Observability
*   **Logging:** Log every incoming query (anonymized if needed) and the number of chunks retrieved.
*   **Metrics:** Track token usage and latency per request.

## Dependencies and Integrations

*   **Core Libraries:**
    *   Backend: `pydantic-ai`, `fastapi`, `uvicorn`, `chromadb`, `langchain-text-splitters`, `beautifulsoup4`.
    *   Frontend: `react-markdown` (for rendering bot responses), `lucide-react`, `clsx`, `tailwind-merge`.
*   **External APIs:**
    *   **Google Gemini API:** Requires `GOOGLE_API_KEY`.
    *   **HMSREG Documentation:** `docs.hmsreg.com` (Source).

## Acceptance Criteria (Authoritative)

1.  **Ingestion Completeness:**
    *   The ingestion script successfully scrapes all linked articles from `docs.hmsreg.com`.
    *   Text is split into chunks of appropriate size (e.g., 500-1000 chars) with overlap.
    *   Embeddings are stored in ChromaDB and persisted.

2.  **Chat Interface Functionality:**
    *   User can type a message and press Enter/Send.
    *   User message appears immediately (Optimistic UI).
    *   Bot response streams in token-by-token.
    *   Markdown in bot response (bold, lists) is rendered correctly.

3.  **RAG Accuracy (Baseline):**
    *   The bot answers questions correctly based *only* on the provided documentation.
    *   The bot provides a "I don't know" fallback if the info is missing (basic implementation).

4.  **Responsive Layouts:**
    *   **Desktop (>1024px):** Verify 3-column layout (Links | Article | Chat).
    *   **Mobile (<1024px):** Verify single column with Tab bar switching views.

5.  **Citations:**
    *   Every answer generated from documentation includes at least one clickable source link.
    *   Links redirect to the correct page on `docs.hmsreg.com`.

## Traceability Mapping

| Acceptance Criteria | Spec Section | Component/Module | Test Idea |
| :--- | :--- | :--- | :--- |
| Ingestion Completeness | Detailed Design / Workflows | `ingestion.py` | Run script, query ChromaDB for total count > 0. |
| Chat Interface Functionality | Detailed Design / APIs | `ChatWindow.tsx` | Manual test: type "hello", verify stream. |
| RAG Accuracy | Workflows | `chat_service.py` | Unit test: Mock vector store, verify prompt construction. |
| Responsive Layouts | Detailed Design / Workflows | `layout.tsx`, `page.tsx` | Resize browser window, check column/tab visibility. |
| Citations | Data Models | `ChatBubble.tsx`, `chat_service.py` | Ask "What is a reg card?", verify link exists. |

## Risks, Assumptions, Open Questions

*   **Risk:** `docs.hmsreg.com` structure changes, breaking the scraper.
    *   *Mitigation:* Write robust selectors and a "health check" for the scraper.
*   **Assumption:** The documentation site allows scraping (check `robots.txt`).
*   **Question:** Do we need to proxy the images from the docs if the bot references them? (MVP: No, text only).
*   **Risk:** ChromaDB memory usage on railway/vercel free tiers.
    *   *Mitigation:* Use persistent disk mode, keep collection size monitored.

## Test Strategy Summary

*   **Unit Tests:**
    *   Backend: Test `chat_service` prompt generation and Pydantic validation.
    *   Frontend: Test `ChatWindow` state transitions (loading -> streaming -> done).
*   **Integration Tests:**
    *   Test `ingestion.py` against a small subset of pages.
    *   Test API endpoint returns 200 and stream headers.
*   **Manual Validation:**
    *   Verify responsive layout behavior on mobile and desktop.
    *   "Vibe check" the RAG responses for a set of 10 standard questions.

## Post-Review Follow-ups

### Story 2.4: Connect Frontend Chat to Backend API
*   **[High]** Create integration test for frontend API route (`frontend/app/api/chat/route.ts`) to verify proxy logic (AC #1, #2).
*   **[High]** Create E2E test (e.g., Playwright) to verify the full chat flow and real-time updates (AC #4).

