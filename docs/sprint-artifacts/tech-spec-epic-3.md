# Epic Technical Specification: Robustness & Reliability

Date: 2025-12-08
Author: BIP
Epic ID: 3
Status: Draft

---

## Overview

This Epic (Epic 3: Robustness & Reliability) focuses on enhancing the chatbot's ability to handle queries where a confident answer cannot be immediately provided. It ensures a robust user experience by implementing fallback mechanisms and suggesting alternative queries, thereby preventing dead ends and guiding users effectively. This aligns with the overall product goal of user empowerment and self-service, as outlined in the PRD, by ensuring continuous assistance even in ambiguous situations.

## Objectives and Scope

**In-Scope:**
*   Implementation of automatic fallback mechanisms when a confident answer cannot be provided.
*   Provision of alternative resources (documentation links, support contact) during fallback.
*   Development of a mechanism to suggest alternative or related topics for ambiguous queries.

**Out-of-Scope (for this epic):**
*   Direct implementation of new core RAG pipeline features.
*   User interface design beyond the presentation of fallback options and query suggestions.
*   Performance optimization of the core chat response time.

## System Architecture Alignment

This epic primarily aligns with the 'Robustness & Reliability' aspects highlighted in the architecture, specifically leveraging and extending the `Error Handling Middleware` defined in the backend. The implementation will focus on enriching the application's fault tolerance and user guidance mechanisms when the RAG pipeline cannot provide a direct answer, ensuring the system remains helpful and responsive. This involves integrating new backend logic within the existing `backend/app/services/chat_service.py` to manage fallback scenarios and ambiguous query suggestions, and extending the frontend to display these gracefully.

## Detailed Design

### Services and Modules

*   **`backend/app/services/chat_service.py`**
    *   **Responsibility:** Detect low-confidence answers from the RAG pipeline, trigger appropriate fallback mechanisms (e.g., provide direct documentation links, support contacts), and generate contextually relevant ambiguous query suggestions.
    *   **Inputs:** User query, RAG pipeline result (including confidence score), current chat context.
    *   **Outputs:** Final answer, fallback options, or a list of suggested alternative queries.
    *   **Owner:** Backend Team
*   **`backend/app/api/v1/chat.py`**
    *   **Responsibility:** Expose the main chat endpoint, potentially handling different response structures for answers, fallbacks, and suggestions.
    *   **Inputs:** HTTP POST request with user query and selected role.
    *   **Outputs:** Streaming SSE response containing chat messages, fallback prompts, or query suggestions.
    *   **Owner:** Backend Team
*   **`backend/app/llm/gemini.py`**
    *   **Responsibility:** Utilized by `chat_service` to generate natural language ambiguous query suggestions when RAG results are inconclusive.
    *   **Inputs:** Initial user query, potentially retrieved documents with low relevance.
    *   **Outputs:** List of rephrased or alternative query strings.
    *   **Owner:** Backend Team
*   **`backend/app/rag/*` (RAG Pipeline Components)**
    *   **Responsibility:** Potentially enhanced to return a confidence score alongside the retrieved answer, enabling `chat_service` to make informed decisions about fallback.
    *   **Inputs:** User query, embedded documentation.
    *   **Outputs:** Answer, relevant source citations, confidence score.
    *   **Owner:** Backend Team
*   **`frontend/components/ChatWindow.tsx` (and related UI components)**
    *   **Responsibility:** Render diverse response types from the backend, including streaming answers, clickable fallback links (e.g., to docs or support), and interactive ambiguous query suggestions.
    *   **Inputs:** SSE stream data from backend API.
    *   **Outputs:** Dynamic chat interface.
    *   **Owner:** Frontend Team
*   **`frontend/app/api/chat/route.ts` (Frontend API Route)**
    *   **Responsibility:** Proxy requests to the backend chat API and handle the SSE stream for rendering in the frontend.
    *   **Inputs:** User query from frontend UI.
    *   **Outputs:** Proxied SSE stream.
    *   **Owner:** Frontend Team

### Data Models and Contracts

To support the robustness and reliability features, the existing `ChatSession` model will be updated, and new models may be introduced for granular logging and analytics. All models will be implemented using SQLAlchemy within `backend/app/db/models.py`.

*   **`ChatSession` Model (Update):**
    *   **Purpose:** Track metadata and key events for each user conversation.
    *   **New Fields:**
        *   `last_query_confidence` (Float, optional): Stores the confidence score of the RAG pipeline's last response, used to determine if a fallback is necessary.
        *   `fallback_triggered_at` (DateTime, optional): UTC timestamp indicating when a fallback mechanism was initiated within the session.
        *   `fallback_type` (String, optional): Categorizes the type of fallback (e.g., 'no_answer', 'low_confidence', 'ambiguous_query').
        *   `suggested_queries` (JSONB, optional): An array of alternative queries presented to the user during an ambiguous query scenario.

*   **`FallbackInteraction` Model (New, optional for detailed analytics):**
    *   **Purpose:** Log specific instances of fallback events, the options presented, and user interactions with those options.
    *   **Fields:** `interaction_id` (UUID PK), `session_id` (UUID FK to `ChatSession`), `query_text` (Text), `fallback_type` (String), `fallback_offered_options` (JSONB), `user_action` (String, e.g., 'clicked_link', 'rephrased'), `timestamp` (DateTime UTC).

*   **`QuerySuggestionLog` Model (New, optional for detailed analytics):**
    *   **Purpose:** Record every ambiguous query suggestion made and whether the user interacted with it.
    *   **Fields:** `log_id` (UUID PK), `session_id` (UUID FK to `ChatSession`), `original_query` (Text), `suggested_query` (Text), `user_selected` (Boolean), `timestamp` (DateTime UTC).

### APIs and Interfaces

The primary API interface affected by this epic is the main chat endpoint. The response mechanism will be enhanced to convey various types of messages, including standard answers, fallback options, and query suggestions.

*   **`POST /api/v1/chat` (Update)**
    *   **Description:** The existing chat endpoint will be enhanced to provide a more robust conversational experience. Its Server-Sent Events (SSE) `StreamingResponse` will now send structured JSON objects, allowing the frontend to intelligently render different types of responses.
    *   **Request Model (`ChatRequest`):** Remains as per current definition (e.g., `query: str, user_role: Optional[str]`).
    *   **Response Stream (Structured JSON via SSE):**
        *   **Standard Answer Segment:**
            ```json
            {"type": "text", "content": "Part of the answer..."}
            ```
        *   **Fallback Response:** Issued when a confident answer cannot be found.
            ```json
            {
              "type": "fallback",
              "message": "I couldn't confidently answer that. You might try:",
              "options": [
                {"label": "Search HMSREG Docs", "url": "https://docs.hmsreg.com/?q={{original_query}}"},
                {"label": "Contact Support", "url": "mailto:support@hmsreg.com"}
              ]
            }
            ```
        *   **Ambiguous Query Suggestions:** Provided when the initial query is unclear.
            ```json
            {
              "type": "suggestions",
              "message": "Perhaps you meant one of these?",
              "suggestions": [
                {"label": "HMS card requirements", "query": "What are the requirements for an HMS card?"},
                {"label": "Register new supplier", "query": "How do I register a new supplier?"}
              ]
            }
            ```
    *   **Error Codes:** Standard HTTP status codes (e.g., 4xx for client errors, 5xx for server errors) will be used for API-level issues. Domain-specific issues (like confidence thresholds) will be communicated within the `fallback` response type.

*   **Internal Interfaces:**
    *   **`RAG Module` Output:** The RAG pipeline (`backend/app/rag/`) should be modified to return a confidence score along with the generated answer and sources. This score will be critical for the `ChatService` to decide on fallback actions.
        ```python
        class RAGResult(BaseModel):
            answer: str
            sources: List[str]
            confidence_score: float # New field
        ```
    *   **`LLM Module` (for suggestions):** A new utility function or method within `backend/app/llm/gemini.py` to generate alternative queries based on the initial user input and potentially the retrieved (but low-confidence) documents.
        ```python
        def generate_alternate_queries(original_query: str, context_snippets: List[str]) -> List[str]:
            # ... logic to use Gemini to rephrase or suggest related queries
            pass
        ```

### Workflows and Sequencing

The following sequence describes the core user interaction flow, specifically highlighting the enhancements for handling low-confidence answers and ambiguous queries introduced by this epic.

1.  **User Initiates Query:**
    *   **Actors:** Frontend User, `frontend/components/ChatWindow.tsx`
    *   **Action:** User enters a query into the chat interface.
    *   **Flow:** The frontend sends a `POST` request to the `backend/api/v1/chat` endpoint, containing the user's query and selected role.

2.  **Backend Processes Query via RAG Pipeline:**
    *   **Actors:** `backend/app/api/v1/chat.py`, `backend/app/services/chat_service.py`, `backend/app/rag/`
    *   **Action:** The `chat_service` orchestrates the RAG process. The RAG pipeline retrieves relevant documentation chunks, generates an initial answer, and critically, computes a `confidence_score` for the generated response.
    *   **Flow:** The `chat_service` receives a `RAGResult` object containing the `answer`, `sources`, and `confidence_score`.

3.  **Confidence-Based Decision Point:**
    *   **Actor:** `backend/app/services/chat_service.py`
    *   **Action:** The `chat_service` evaluates the `confidence_score` against a predefined configurable threshold.
    *   **Flow:**
        *   **If `confidence_score >= threshold` (High Confidence):** Proceed to Step 4 (Standard Answer).
        *   **If `confidence_score < threshold` (Low Confidence):** Proceed to Step 5 (Fallback / Suggestions).

4.  **Standard Answer (High Confidence Path):**
    *   **Actors:** `backend/app/services/chat_service.py`, `backend/app/api/v1/chat.py`
    *   **Action:** The `chat_service` streams the generated answer (and citations) to the frontend using the structured SSE response (`{"type": "text", "content": "..."}`).
    *   **Flow:** Frontend renders the confident answer.

5.  **Fallback / Suggestions (Low Confidence Path):**
    *   **Actors:** `backend/app/services/chat_service.py`, `backend/app/llm/gemini.py` (potentially)
    *   **Action:** The `chat_service` identifies the nature of the low confidence (e.g., no relevant documents, ambiguous query) and prepares a suitable user-guidance response.
    *   **Flow:**
        *   **Step 5a: Trigger Fallback Message:** `chat_service` streams a `{"type": "fallback", "message": "...", "options": [...]}` object to the frontend, providing alternative resources (e.g., links to broad documentation, support contact).
        *   **Step 5b (Optional): Generate Ambiguous Query Suggestions:** If the query was ambiguous or broad, `chat_service` may leverage `backend/app/llm/gemini.py` to generate a list of related, rephrased queries. These are then streamed as `{"type": "suggestions", "message": "...", "suggestions": [...]}`.

6.  **Frontend Renders Dynamic Response:**
    *   **Actors:** `frontend/components/ChatWindow.tsx`, Frontend User
    *   **Action:** The frontend receives and interprets the structured JSON objects from the SSE stream.
    *   **Flow:**
        *   `{"type": "text"}`: Content is appended to the chat display.
        *   `{"type": "fallback"}`: A distinct UI element displays the fallback message and presents clickable options.
        *   `{"type": "suggestions"}`: A distinct UI element (e.g., interactive chips or buttons) displays the suggested alternative queries.

7.  **User Interaction with Fallback/Suggestions:**
    *   **Actors:** Frontend User
    *   **Action:**
        *   User clicks a link within a fallback message (e.g., navigates to external documentation).
        *   User clicks a suggested query, which then triggers a new query (back to Step 1) with the selected suggestion.
    *   **Logging:** These interactions are logged (e.g., via `FallbackInteraction` or `QuerySuggestionLog` models) for future analysis and improvement of the system.

## Non-Functional Requirements

### Performance

While the core performance target of **under 5 seconds** average response time for standard queries (as defined in the PRD) remains paramount, this epic introduces additional latency considerations for fallback and suggestion mechanisms. Fallback responses, including the display of alternative resources, should be presented to the user within **2 seconds** of a low-confidence detection. Ambiguous query suggestions, if generated by the LLM, should also be returned within **3 seconds** to maintain a fluid user experience. The asynchronous nature of the FastAPI backend and Server-Sent Events (SSE) will be leveraged to ensure these new interactions remain responsive.

### Security

All new endpoints or modifications to existing endpoints (e.g., `/api/v1/chat` response changes) will adhere to the project's established security architecture, including strict input validation (Pydantic), and **rate limiting** (10 requests/minute, 50/hour per user/IP) as outlined in the PRD and Architecture. No personal or regulated data will be processed or stored in the context of these new features. The generation of ambiguous query suggestions must be carefully managed to prevent prompt injection vulnerabilities and ensure that suggested queries do not expose sensitive information or lead to system abuse. All interactions will be handled over secure channels (HTTPS).

### Reliability/Availability

This epic directly enhances the system's reliability by implementing graceful degradation. When the RAG pipeline cannot provide a high-confidence answer, the system will not fail silently or return irrelevant information. Instead, it will proactively guide the user through fallback mechanisms (e.g., providing links to source documentation or support contact) and ambiguous query suggestions. This ensures that the system remains continuously helpful and prevents dead ends in user interaction. The `ChatService` will be designed with robust error handling for external LLM calls (e.g., for generating suggestions) to ensure service continuity even if external APIs face temporary issues.

### Observability

Detailed logging will be implemented to monitor the effectiveness of the fallback and suggestion mechanisms. The following events will be logged at an appropriate level (INFO for production, DEBUG for development) and structured as JSON in production for efficient analysis:

*   `low_confidence_triggered`: Records instances where a RAG response falls below the confidence threshold, indicating a potential need for fallback.
*   `fallback_presented`: Logs when fallback options (e.g., links to external documentation, support contacts) are displayed to the user.
*   `fallback_action_taken`: Tracks when a user interacts with a presented fallback option (e.g., clicks a provided link).
*   `suggestions_presented`: Records when ambiguous query suggestions are displayed to the user.
*   `suggestion_selected`: Logs when a user selects and re-queries with one of the provided suggestions.

These logs will enable analysis of user interaction patterns within fallback scenarios, common failure points, and the overall effectiveness of the guidance provided, thereby offering valuable insights for continuous system improvement.

### Dependencies and Integrations

This epic primarily leverages existing core dependencies but introduces new integration patterns and enhanced utilization of certain libraries to achieve its goals of improved robustness and reliability.

**Core Dependencies Utilized/Extended:**

*   **Backend (`backend/pyproject.toml`):**
    *   **`FastAPI`**: Continues as the primary web framework for API endpoints.
    *   **`SQLAlchemy`, `asyncpg`**: For potential new data models (`FallbackInteraction`, `QuerySuggestionLog`) to log user interactions with fallback/suggestions.
    *   **`ChromaDB`**: The vector store will likely need to be queried in a way that allows for the extraction or derivation of a confidence score for RAG results.
    *   **`LangChain`**: Will be used to orchestrate the RAG pipeline and potentially integrate the LLM for suggestion generation.
    *   **`google-generativeai` (or `langchain-google-genai`)**: Will be specifically utilized by the `ChatService` for the generation of ambiguous query suggestions.
*   **Frontend (`frontend/package.json`):**
    *   **`Next.js`**, **`React`**: For building the enhanced chat interface.
    *   **`shadcn/ui`**: For consistent and accessible UI components to display fallback options and clickable suggestions.
    *   **`TypeScript`**: Ensures type safety for new API response structures and UI state management.

**Key Integration Points (New & Enhanced):**

*   **`ChatService` (Backend) <-> RAG Pipeline (Backend):**
    *   **Integration:** The RAG pipeline's output will be enhanced to include a `confidence_score` alongside the answer and sources.
    *   **Impact:** `ChatService` will use this score to determine whether to provide a direct answer or initiate a fallback/suggestion mechanism.
*   **`ChatService` (Backend) <-> LLM (Gemini) (Backend):**
    *   **Integration:** Direct invocation of the Google Gemini LLM API (via `google-generativeai` or `LangChain` wrappers) to formulate contextually relevant alternative queries when the primary RAG search is ambiguous.
    *   **Impact:** Enables the chatbot to offer proactive guidance instead of a simple "I don't know" response.
*   **`/api/v1/chat` Endpoint (Backend) <-> `ChatWindow.tsx` (Frontend):**
    *   **Integration:** The Server-Sent Events (SSE) stream will now carry structured JSON objects (`{"type": "fallback", ...}`, `{"type": "suggestions", ...}`) to differentiate between standard answers, fallback options, and query suggestions.
    *   **Impact:** The frontend will dynamically render different UI elements based on the `type` field in the streamed JSON, offering a more interactive experience.
*   **Frontend UI <-> External Documentation/Support Channels:**
    *   **Integration:** The frontend will render clickable links within fallback messages that direct users to external HMSREG documentation or email support.
    *   **Impact:** Provides clear "escape hatches" for users when the chatbot cannot directly assist.
*   **Frontend UI (Suggested Queries) <-> `/api/v1/chat` (Backend):**
    *   **Integration:** Users will be able to click on a suggested query, which will trigger a new `POST /api/v1/chat` request with the selected suggestion as the new `query`.
    *   **Impact:** Allows users to easily explore alternative avenues of inquiry.

### Acceptance Criteria (Authoritative)

1.  **AC1.1:** When the RAG pipeline returns an answer with a confidence score below a defined threshold, the chatbot SHALL NOT provide the low-confidence answer.
2.  **AC1.2:** Instead of a low-confidence answer, the chatbot SHALL inform the user that it could not confidently answer the question via a clear message.
3.  **AC1.3:** The chatbot SHALL present the user with at least two alternative resources:
    *   A clickable link to the general HMSREG documentation search page, pre-populated with the user's original query.
    *   A clickable link to contact support (e.g., mailto: link).
4.  **AC1.4:** The fallback message and alternative resources SHALL be displayed to the user within **2 seconds** of the low-confidence detection.
5.  **AC1.5:** When a user's query is deemed ambiguous (e.g., leading to multiple low-confidence answers or no clear intent), the chatbot SHALL offer a list of **2-4 alternative or rephrased queries**.
6.  **AC1.6:** The alternative/rephrased queries SHALL be generated by the LLM and presented to the user within **3 seconds** of the ambiguous query being processed.
7.  **AC1.7:** Users SHALL be able to click on a suggested alternative query, which will then be submitted as a new query to the chatbot.
8.  **AC1.8:** The system SHALL log every instance where a low-confidence threshold triggers a fallback mechanism.
9.  **AC1.9:** The system SHALL log every instance where ambiguous query suggestions are presented to the user.
10. **AC1.10:** The system SHALL log when a user interacts with a presented fallback option (e.g., clicks a link within the fallback message).
11. **AC1.11:** The system SHALL log when a user selects one of the suggested alternative queries from the displayed list.

### Traceability Mapping

| Acceptance Criterion | Spec Section(s)                                                                           | Component(s)/API(s)                                                 | Test Idea                                                                                               |
| :------------------- | :---------------------------------------------------------------------------------------- | :------------------------------------------------------------------ | :------------------------------------------------------------------------------------------------------ |
| AC1.1                | FR3.1, NFR-Performance, Workflows                                                         | `backend/app/services/chat_service.py`, RAG Module                  | Unit test `chat_service`: verify no answer returned when RAG confidence is below threshold.             |
| AC1.2                | FR3.1, Workflows                                                                          | `backend/app/services/chat_service.py`, `backend/app/api/v1/chat.py`, Frontend UI | Integration test: Verify backend sends fallback message, frontend displays it.                          |
| AC1.3                | FR3.1, Workflows                                                                          | `backend/app/services/chat_service.py`, `backend/app/api/v1/chat.py`, Frontend UI | Integration test: Verify backend sends correct clickable links, frontend renders them.                  |
| AC1.4                | NFR-Performance                                                                           | `backend/app/services/chat_service.py`, `backend/app/api/v1/chat.py`, Frontend UI | Performance test: Measure time from low-confidence detection to UI display of fallback.                 |
| AC1.5                | FR3.2, Workflows                                                                          | `backend/app/services/chat_service.py`, `backend/app/llm/gemini.py` | Unit test `chat_service`: verify generation of 2-4 suggestions for ambiguous input.                     |
| AC1.6                | FR3.2, NFR-Performance, Workflows                                                         | `backend/app/services/chat_service.py`, `backend/app/llm/gemini.py`, `backend/app/api/v1/chat.py`, Frontend UI | Performance test: Measure time from ambiguous query to UI display of suggestions.                       |
| AC1.7                | FR3.2, Workflows                                                                          | Frontend UI, `backend/app/api/v1/chat.py`                           | E2E test: User clicks suggestion, verify new query is submitted and processed correctly.                |
| AC1.8                | NFR-Observability, Data Models                                                            | `backend/app/services/chat_service.py`, `ChatSession` (updated)     | Integration test: Verify low-confidence event is logged in `ChatSession` or `FallbackInteraction`.      |
| AC1.9                | NFR-Observability, Data Models                                                            | `backend/app/services/chat_service.py`, `ChatSession` (updated)     | Integration test: Verify suggestion presentation event is logged in `ChatSession` or `QuerySuggestionLog`. |
| AC1.10               | NFR-Observability, Data Models                                                            | Frontend UI, `backend/app/api/v1/feedback.py` (potentially)         | E2E test: User clicks fallback link, verify interaction is logged.                                      |
| AC1.11               | NFR-Observability, Data Models                                                            | Frontend UI, `backend/app/api/v1/feedback.py` (potentially)         | E2E test: User selects suggestion, verify selection is logged.                                          |

**Risks:**

*   **R1: Inaccurate or Irrelevant Ambiguous Query Suggestions:** The LLM might generate suggestions that do not accurately reflect the user's intent or are unhelpful, leading to user frustration.
    *   **Mitigation:** Implement rigorous prompt engineering for suggestion generation. Incorporate user feedback mechanisms specifically for suggestion quality. Regularly review logs of generated suggestions and user interactions.
*   **R2: Over-triggering Fallback Mechanisms:** If the confidence threshold for RAG responses is set too high, the system may frequently resort to fallback, even for queries that could have been answered, leading to an inefficient user experience.
    *   **Mitigation:** Calibrate and fine-tune the confidence threshold through iterative testing, A/B testing, and analysis of user feedback.
*   **R3: Under-triggering Fallback Mechanisms:** Conversely, if the confidence threshold is too low, the system might provide low-quality or incorrect answers without initiating a fallback, undermining user trust.
    *   **Mitigation:** Rigorous validation of RAG response quality metrics. Continuous monitoring of user feedback for inaccurate answers.
*   **R4: Performance Degradation from LLM-based Suggestions:** Generating ambiguous query suggestions via an external LLM could introduce significant latency or incur unexpected costs.
    *   **Mitigation:** Implement caching for frequently occurring ambiguous query patterns. Optimize LLM calls to be asynchronous and potentially limit the number of suggestions generated. Explore local models for suggestion generation if latency becomes a critical issue.
*   **R5: User Interface Complexity:** Presenting multiple types of responses (answer, fallback options, suggestions) simultaneously might overwhelm users or make the interface cluttered.
    *   **Mitigation:** Follow established UX principles for clear visual hierarchy and progressive disclosure. Conduct user testing to ensure intuitive presentation.

**Assumptions:**

*   **A1:** The RAG pipeline is capable of providing a sufficiently accurate and meaningful confidence score alongside its generated answers.
*   **A2:** The chosen LLM (Google Gemini) can reliably generate diverse, relevant, and helpful alternative queries given an ambiguous user input.
*   **A3:** Users will be able to understand the distinction between a chatbot answer, a fallback response, and query suggestions, and will actively utilize the provided options.
*   **A4:** The existing frontend and backend frameworks (Next.js, FastAPI) and UI component library (shadcn/ui) can be extended gracefully to support the new structured response types and interactive elements.

**Open Questions:**

*   **Q1:** What is the optimal, configurable confidence threshold for triggering a fallback? This needs to be determined through testing and observation.
*   **Q2:** What is the precise distinction between a query that triggers a "no confident answer" fallback and one that triggers "ambiguous query suggestions"? How will `chat_service` differentiate these scenarios?
*   **Q3:** What is the maximum number of ambiguous query suggestions to present to the user at any given time to avoid cognitive overload? (Currently set at 2-4 per AC1.5, but needs validation).
*   **Q4:** What are the fallback mechanisms if the LLM fails to generate suggestions (e.g., API error, rate limit)? Should it default to a generic "try rephrasing" message?

### Test Strategy Summary

A comprehensive testing strategy will be employed across multiple levels to ensure the robustness and reliability enhancements introduced by this epic function as expected.

*   **Unit Tests:**
    *   **Focus:** Core logic within `backend/app/services/chat_service.py` responsible for confidence threshold evaluation, triggering fallback logic, and orchestrating LLM calls for suggestion generation. Also, unit test the individual LLM prompting for suggestions.
    *   **Framework:** `Pytest` (Python).
    *   **Coverage:** Validate `AC1.1` (no low-confidence answer), `AC1.5` (suggestion generation), `AC1.8` (logging fallback trigger), `AC1.9` (logging suggestion presentation).
*   **Integration Tests:**
    *   **Focus:** Verify the interactions between `chat_service`, a mocked RAG module (simulating different confidence scores), a mocked LLM (simulating various suggestion outputs), and the `backend/app/api/v1/chat` API endpoint.
    *   **Framework:** `Pytest` (Python).
    *   **Coverage:** Validate the structured SSE responses for fallback messages and suggestions (`AC1.2`, `AC1.3`). Verify logging of interaction events to the database.
*   **End-to-End (E2E) Tests:**
    *   **Focus:** Simulate full user journeys, interacting with the frontend, verifying correct display of fallback messages and suggested queries, and validating the functionality of clickable elements.
    *   **Framework:** `Playwright` (or similar).
    *   **Coverage:** Verify `AC1.2`, `AC1.3` (correct UI display), `AC1.7` (clicking a suggestion submits a new query). Validate `AC1.10` (logging fallback interaction) and `AC1.11` (logging suggestion selection) by checking database entries.
*   **Performance Tests:**
    *   **Focus:** Measure the latency introduced by the fallback and suggestion mechanisms.
    *   **Framework:** Dedicated performance testing tools (e.g., Locust).
    *   **Coverage:** Ensure `AC1.4` (fallback within 2s) and `AC1.6` (suggestions within 3s) performance targets are met.
*   **Edge Cases & Negative Testing:**
    *   Queries that are extremely short, long, or nonsensical.
    *   Queries that are outside the scope of the documentation.
    *   Simulating network failures or API errors during LLM calls for suggestions.
    *   Testing with various confidence threshold configurations.
    *   User repeatedly clicking suggestions or fallback options.

