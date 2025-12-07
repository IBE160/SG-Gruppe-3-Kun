# Epics & Stories for ibe160

This document breaks down the requirements from the PRD into actionable epics and user stories, incorporating specific design patterns from the UX Specification and technical decisions from the Architecture.

---

## Proposed Epic Structure

Here is a summary of the proposed epics to build the HMSREG Documentation Chatbot.

### Epic 1: Project Foundation & Deployment Pipeline

-   **Value:** Establishes the core infrastructure, CI/CD pipeline, and development environment. This enables all future development and ensures the project is built on a solid, deployable foundation from day one.
-   **Scope:** Set up Git repository, Next.js frontend project, FastAPI backend project, connect to Supabase, configure Vercel/Railway for CI/CD, and create initial "hello world" deployments.

### Epic 2: Core Conversational Experience & RAG Pipeline

-   **Value:** Implements the fundamental ability for a user to ask a question and receive an answer from the documentation. This is the core "magic" of the product.
-   **Related Functional Requirements:** FR1.1, FR1.2, FR1.3, FR1.4
-   **Scope:** Build the data ingestion pipeline to process `docs.hmsreg.com`, set up the ChromaDB vector store, implement the Pydantic AI-centric RAG pipeline in the FastAPI backend, and create the basic chat UI in the frontend.

### Epic 3: User Context & Personalization

-   **Value:** Makes the chatbot's answers more relevant and useful by tailoring them to the user's specific role.
-   **Related Functional Requirements:** FR2.1, FR2.2
-   **Scope:** Implement the role selection UI at the start of a session, pass the role context to the backend, and modify the RAG prompt to incorporate the user's role.

### Epic 4: Robustness, Reliability & Feedback

-   **Value:** Ensures the chatbot is helpful even when it doesn't know the answer and provides a mechanism for continuous improvement.
-   **Related Functional Requirements:** FR3.1, FR3.2, FR4.1
-   **Scope:** Implement the fallback mechanism for unknown questions, add source citation links to answers, and build the user feedback (thumbs up/down) system.

### Epic 5: Production Readiness & Accessibility

-   **Value:** Prepares the application for public launch by implementing essential non-functional requirements.
-   **Related Functional Requirements:** FR5.1
-   **Scope:** Implement API rate limiting, ensure WCAG 2.1 AA accessibility standards are met, and conduct final testing.

---

## Epic 1: Project Foundation & Deployment Pipeline

**Epic Title:** Project Foundation & Deployment Pipeline
**Epic Goal:** Establish the core infrastructure, CI/CD pipeline, and development environment to enable efficient and continuous development and deployment.

### Story 1.1: Initialize Project Repositories and Core Structure

**As a** developer,
**I want to** set up the foundational project repositories and core directory structure,
**So that** all team members have a consistent and organized starting point for development.

**Acceptance Criteria:**
Given a new project,
When I initialize the project,
Then a monorepo structure is created with separate `frontend` (Next.js) and `backend` (FastAPI) directories.
And the backend directory structure includes `app/api`, `app/core`, `app/services`, `app/db`, `app/rag`, and `app/schemas`.
And the frontend directory structure includes `app/api`, `components`, `hooks`, `lib`, and `types`.
And a `.gitignore` file is configured for each project to exclude unnecessary files.
And a `README.md` is present at the root with basic project setup instructions.

**Prerequisites:** None
**Technical Notes:**
- Follow `Project Structure` in Architecture.
- Use `create-next-app` for frontend.
- Use `poetry new` for backend.
- Ensure `pyproject.toml` and `package.json` are created.

### Story 1.2: Configure Frontend Development Environment

**As a** frontend developer,
**I want to** set up the Next.js development environment with TypeScript, Tailwind CSS, and shadcn/ui,
**So that** I can efficiently build the user interface with a consistent and modern design system.

**Acceptance Criteria:**
Given the frontend directory,
When I set up the development environment,
Then Next.js 14 (App Router) is configured with TypeScript.
And Tailwind CSS is integrated with the project's color palette (Deep Blue/Teal primary).
And shadcn/ui is initialized.
And essential dependencies are installed: `lucide-react`, `clsx`, `tailwind-merge`.
And a basic "Hello World" page is rendered successfully.

**Prerequisites:** Story 1.1
**Technical Notes:**
- Follow Architecture `Frontend (Next.js)` initialization command.
- Configure `tailwind.config.ts` with colors from UX Spec Section 3.1.
- Ensure `app/layout.tsx` applies global styles.

### Story 1.3: Configure Backend Development Environment

**As a** backend developer,
**I want to** set up the FastAPI development environment with Python 3.11+,
**So that** I can efficiently build the API endpoints and integrate the RAG pipeline.

**Acceptance Criteria:**
Given the backend directory,
When I set up the development environment,
Then Python 3.11+ is configured with a virtual environment managed by Poetry.
And FastAPI is installed with Uvicorn.
And essential dependencies are installed: `sqlalchemy`, `asyncpg`, `python-multipart`, `pydantic-ai`.
And a basic "Hello World" endpoint (`/health`) is accessible.
And `app/main.py` is configured as the entry point.

**Prerequisites:** Story 1.1
**Technical Notes:**
- Follow Architecture `Backend (FastAPI)` initialization commands.
- Verify `poetry.lock` is generated.
- Configure `app/core/config.py` for environment variables.

### Story 1.4: Implement Basic CI/CD for Frontend (Vercel)

**As a** DevOps engineer,
**I want to** configure a continuous integration and deployment pipeline for the frontend,
**So that** changes are automatically built and deployed to a staging environment upon commit.

**Acceptance Criteria:**
Given the Next.js frontend repository,
When a commit is pushed to the main branch,
Then Vercel automatically builds and deploys the application.
And a unique URL is provided for the staging deployment.
And the "Hello World" page is accessible via the deployed URL.

**Prerequisites:** Story 1.2
**Technical Notes:** Connect Vercel to the Git repository.

### Story 1.5: Implement Basic CI/CD for Backend (Railway)

**As a** DevOps engineer,
**I want to** configure a continuous integration and deployment pipeline for the backend,
**So that** changes are automatically built and deployed to a staging environment upon commit.

**Acceptance Criteria:**
Given the FastAPI backend repository,
When a commit is pushed to the main branch,
Then Railway automatically builds and deploys the application.
And a unique URL is provided for the staging deployment.
And the `/health` endpoint is accessible via the deployed URL.

**Prerequisites:** Story 1.3
**Technical Notes:** Connect Railway to the Git repository, configure build and start commands (`poetry run uvicorn app.main:app --host 0.0.0.0 --port $PORT`).

### Story 1.6: Set up Supabase Project and Connect to Backend

**As a** backend developer,
**I want to** initialize a Supabase project and connect the FastAPI backend to its PostgreSQL database,
**So that** I can store conversation logs, feedback, and analytics data.

**Acceptance Criteria:**
Given a Supabase account,
When I create a new project,
Then a PostgreSQL database is provisioned.
And the FastAPI backend is configured with `DATABASE_URL` in `app/core/config.py`.
And `app/db/session.py` is implemented using `SQLAlchemy`'s async engine.
And a simple test endpoint can successfully read/write to the DB.

**Prerequisites:** Story 1.3
**Technical Notes:** Use `asyncpg` driver.

### Story 1.7: Set up ChromaDB Vector Store

**As a** backend developer,
**I want to** set up and configure the ChromaDB vector store,
**So that** I can efficiently store and retrieve document embeddings for the RAG pipeline.

**Acceptance Criteria:**
Given the backend environment,
When ChromaDB is initialized,
Then it is configured for persistent storage.
And the `app/rag/vector_store.py` module is created to manage the client.
And a basic test can successfully add and retrieve a vector embedding.

**Prerequisites:** Story 1.3
**Technical Notes:** Integrate `chromadb` client library.

## Epic 2: Core Conversational Experience & RAG Pipeline

**Epic Title:** Core Conversational Experience & RAG Pipeline
**Epic Goal:** Implement the fundamental ability for a user to ask a question and receive an answer from the documentation, forming the core "magic" of the product.

### Story 2.1: Implement Documentation Ingestion Pipeline

**Covers:** FR1.2

**As a** backend developer,
**I want to** create a pipeline to scrape and process official HMSREG documentation from `docs.hmsreg.com`,
**So that** the chatbot has a comprehensive and up-to-date knowledge base to draw answers from.

**Acceptance Criteria:**
Given the `docs.hmsreg.com` URL,
When the ingestion pipeline (`app/rag/ingestion.py`) is executed,
Then documentation content is scraped using `BeautifulSoup` or `Playwright`.
And content is chunked into manageable segments using `LangChain`.
And each chunk is embedded using `text-embedding-004`.
And the embeddings and metadata are stored in ChromaDB.

**Prerequisites:** Story 1.3, Story 1.7
**Technical Notes:** Use `LangChain` for text splitting and embedding generation.

### Story 2.2.a: Implement Core Chat Interface

**Covers:** FR1.1, FR1.3

**As a** frontend developer,
**I want to** create the foundational chat interface components,
**So that** users have the basic tools to interact with the chatbot in a clean, professional environment.

**Acceptance Criteria:**
Given the frontend application,
When a user navigates to the chat page,
Then a chat history panel is displayed.
And user and bot message bubbles are visually distinct (User: Primary Color, Bot: Neutral).
And a "Loading..." indicator (subtle animation) appears while waiting for a response.
And a text input field and "Send" button are present and functional.

**Prerequisites:** Story 1.2
**Technical Notes:**
- Use shadcn/ui components (`Input`, `Button`).
- Create `components/ChatWindow.tsx` and `components/ChatBubble.tsx`.
- Follow UX "Novel UX Pattern" for simplicity.

### Story 2.2.b: Implement Desktop Three-Column Responsive Layout

**Covers:** FR1.1, FR1.3

**As a** frontend developer,
**I want to** implement the three-column responsive layout for large screens,
**So that** desktop users can efficiently see documentation, articles, and the chatbot simultaneously.

**Acceptance Criteria:**
Given the frontend application on a screen wider than 1024px,
When a user views a page with the chatbot,
Then a three-column grid is displayed: "Documentation Links" (left), "Article Content" (middle), and "Chatbot Interface" (right).
And the layout matches the structure in `ux-showcase.html` concepts.

**Prerequisites:** Story 2.2.a
**Technical Notes:** Use Tailwind CSS grid (`grid-cols-3`) and media queries.

### Story 2.2.c: Implement Mobile Tabbed-Interface Layout

**Covers:** FR1.1, FR1.3

**As a** frontend developer,
**I want to** implement the single-column, tabbed interface for mobile screens,
**So that** mobile users can easily navigate between different content views on a small screen.

**Acceptance Criteria:**
Given the frontend application on a screen narrower than 1024px,
When a user views a page with the chatbot,
Then a single-column layout is displayed.
And a tab bar is present at the bottom (or top segmented control) with "Links," "Article," and "Chatbot".
And clicking a tab switches the main view.

**Prerequisites:** Story 2.2.a
**Technical Notes:** Use React state to manage active tab visibility.

### Story 2.3: Implement Pydantic AI RAG Pipeline in Backend

**Covers:** FR1.2, FR1.3

**As a** backend developer,
**I want to** integrate the Pydantic AI RAG pipeline with Gemini 2.5 Pro,
**So that** user questions can be processed to retrieve relevant documentation and generate informed responses.

**Acceptance Criteria:**
Given a user question,
When the question is sent to `app/services/chat_service.py`,
Then the question is embedded and used to query ChromaDB (`app/rag/vector_store.py`).
And retrieved chunks are passed to Gemini 2.5 Pro via Pydantic AI agent in `app/services/chat_service.py`.
And the response is validated against a Pydantic model structure (answer, citations, confidence).
And Gemini generates a coherent answer based on context.

**Prerequisites:** Story 2.1
**Technical Notes:**
- Use `pydantic-ai` for the Agent and generation.
- Use `LangChain` *only* for text splitting during ingestion.
- Do NOT use LangChain chains for generation.

### Story 2.4: Connect Frontend Chat to Backend API

**Covers:** FR1.1, FR1.3

**As a** full-stack developer,
**I want to** establish communication between the frontend chat interface and the backend RAG API via SSE,
**So that** users can send questions and receive real-time streaming answers.

**Acceptance Criteria:**
Given the chat UI,
When a user sends a question,
Then the frontend calls the Next.js API route `app/api/chat/route.ts`.
And this route proxies to the backend endpoint `/api/v1/chat/stream`.
And the response is streamed back to the UI token by token using Server-Sent Events (SSE).

**Prerequisites:** Story 2.2, Story 2.3
**Technical Notes:**
- Create `hooks/useChat.ts` to handle SSE connection and state.
- Backend uses `StreamingResponse` from FastAPI.

### Story 2.5: Display Source Citations in Chat UI

**Covers:** FR1.4

**As a** frontend developer,
**I want to** display the source documentation links alongside the chatbot's answers,
**So that** users can verify the information and explore the original context.

**Acceptance Criteria:**
Given a chatbot response,
When the response is generated,
Then the backend returns source URLs in the metadata.
And the frontend displays these as clickable links at the bottom of the bot's chat bubble.
And links are clearly labeled "Source:".

**Prerequisites:** Story 2.3, Story 2.4
**Technical Notes:** Modify `ChatBubble` component to render source links.

## Epic 3: User Context & Personalization

**Epic Title:** User Context & Personalization
**Epic Goal:** Make the chatbot's answers more relevant and useful by tailoring them to the user's specific role.

### Story 3.1: Implement Role Selection UI

**Covers:** FR2.1

**As a** frontend developer,
**I want to** provide a clear and intuitive interface for users to select their role at the beginning of a session,
**So that** the chatbot can understand their context and personalize responses.

**Acceptance Criteria:**
Given a new chat session,
When the chatbot greets the user (UX Journey 1),
Then it displays a message: "To provide the most relevant information, please select your role:".
And interactive buttons are shown: `[Construction Worker]`, `[Supplier]`, `[Project Manager]`.
And clicking a button sets the user context.

**Prerequisites:** Story 2.2.a
**Technical Notes:**
- Create `components/RoleSelector.tsx`.
- Use `Button` component from shadcn/ui.

### Story 3.2: Pass User Role to Backend

**Covers:** FR2.2

**As a** full-stack developer,
**I want to** securely transmit the selected user role from the frontend to the backend,
**So that** the backend can use this context for personalized RAG responses.

**Acceptance Criteria:**
Given a selected role,
When a chat request is made,
Then the role is included in the request payload (defined in `backend/app/schemas/chat.py`).
And the backend `ChatRequest` model validates the role.

**Prerequisites:** Story 3.1, Story 2.4
**Technical Notes:** Update `useChat` hook to include role state in API calls.

### Story 3.3: Incorporate User Role into RAG Prompt

**Covers:** FR2.2

**As a** backend developer,
**I want to** modify the RAG pipeline to include the user's selected role in the prompt sent to Gemini 2.5 Pro,
**So that** the generated answers are tailored to the user's specific context.

**Acceptance Criteria:**
Given a user's role and question,
When `app/services/chat_service.py` constructs the prompt,
Then it injects the role: "You are an expert assistant helping a [Role]. Answer based on the context...".
And the response reflects the appropriate tone and detail for that role.

**Prerequisites:** Story 3.2, Story 2.3
**Technical Notes:** Update Pydantic AI Agent system prompt dependencies.

## Epic 4: Robustness, Reliability & Feedback

**Epic Title:** Robustness, Reliability & Feedback
**Epic Goal:** Ensure the chatbot is helpful even when it doesn't know the answer and provide a mechanism for continuous improvement.

### Story 4.1: Implement Automatic Fallback Mechanism

**Covers:** FR3.1

**As a** backend developer,
**I want to** implement a mechanism to detect when the chatbot cannot confidently answer a question,
**So that** it can gracefully inform the user and provide alternative resources.

**Acceptance Criteria:**
Given a low confidence score from RAG,
When the chatbot generates a response,
Then it returns the fallback message: "Jeg fant ikke et klart svar i dokumentasjonen for dette spørsmålet. Kan du utdype spørsmålet? ...".
And it provides a link to general support/docs.

**Prerequisites:** Story 2.3
**Technical Notes:** Use Pydantic AI validation or `fallback` method in Agent logic.

### Story 4.2: Develop User Feedback Mechanism (Thumbs Up/Down)

**Covers:** FR4.1

**As a** full-stack developer,
**I want to** provide a simple way for users to give feedback on each chatbot response,
**So that** we can continuously monitor and improve the chatbot's performance.

**Acceptance Criteria:**
Given a chatbot response,
When the user clicks "Thumbs Up" or "Thumbs Down",
Then the frontend sends a request to `POST /api/v1/feedback`.
And the feedback is stored in the `feedback` table (defined in `app/db/models.py`).
And the UI updates to thank the user.

**Prerequisites:** Story 2.4, Story 1.6
**Technical Notes:**
- Create `components/FeedbackButtons.tsx`.
- Create `backend/app/api/v1/feedback.py`.

### Story 4.3: Implement Ambiguous Query Suggestion

**Covers:** FR3.2

**As a** backend developer,
**I want to** enable the chatbot to suggest alternative or related topics when a user's query is ambiguous,
**So that** users can refine their questions and find relevant information more easily.

**Acceptance Criteria:**
Given an ambiguous query,
When the RAG pipeline processes it,
Then it generates 2-3 clarification suggestions (UX Journey: Ambiguous Question).
And these are displayed as clickable options in the chat UI.

**Prerequisites:** Story 2.3
**Technical Notes:** Leverage Gemini's capabilities to identify related topics or use a keyword extraction and suggestion mechanism.

## Epic 5: Production Readiness & Accessibility

**Epic Title:** Production Readiness & Accessibility
**Epic Goal:** Prepare the application for public launch by implementing essential non-functional requirements, ensuring it is robust, secure, and usable by all.

### Story 5.1: Implement API Rate Limiting

**As a** backend developer,
**I want to** implement rate limiting on all API endpoints,
**So that** the system is protected from abuse and denial-of-service attacks.

**Acceptance Criteria:**
Given an API endpoint,
When requests exceed the limit (e.g., 60/min),
Then a 429 Too Many Requests error is returned.
And limits are configurable via `app/core/config.py`.

**Prerequisites:** Story 1.3
**Technical Notes:** Use `slowapi` or custom middleware in FastAPI.

### Story 5.2: Ensure WCAG 2.1 AA Compliance for Frontend

**Covers:** FR5.1

**As a** frontend developer,
**I want to** ensure the web interface adheres to WCAG 2.1 AA accessibility standards,
**So that** the chatbot is usable by individuals with disabilities.

**Acceptance Criteria:**
Given the frontend,
When audited with Axe DevTools,
Then no critical violations are found.
And all interactive elements (inputs, buttons) are navigable via keyboard (Tab/Enter).
And screen readers correctly announce chat messages and role selections.
And color contrast meets AA standards (checked against UX palette).

**Prerequisites:** Story 2.2
**Technical Notes:** Use `radix-ui` primitives (via shadcn) which handle many a11y primitives out of the box.

### Story 5.3: Implement Comprehensive Logging and Monitoring

**As a** DevOps engineer,
**I want to** set up comprehensive logging and monitoring for both frontend and backend,
**So that** operational issues can be quickly identified, diagnosed, and resolved.

**Acceptance Criteria:**
Given the application in production,
When an error occurs,
Then it is logged as structured JSON (Backend) or reported (Frontend).
And `app/core/logging.py` configures the log format.

**Prerequisites:** Story 1.4, Story 1.5
**Technical Notes:** Use Python's `logging` module with a JSON formatter for backend.

### Story 5.4: Conduct Final End-to-End Testing

**As a** QA engineer,
**I want to** perform comprehensive end-to-end testing of the entire application,
**So that** all features and integrations function correctly before launch.

**Acceptance Criteria:**
Given the deployed app,
When I run the E2E test suite (Playwright),
Then critical flows (Role Selection -> Chat -> Feedback) pass.
And integration with Supabase and ChromaDB is verified.

**Prerequisites:** All previous stories
**Technical Notes:** Set up `tests/e2e` folder with Playwright tests.

---

## Epic Breakdown Summary

The epic breakdown has been enhanced with specific technical details from the Architecture document and user experience patterns from the UX Design Specification.

**Key Enhancements:**
- **Project Structure:** Specific file paths and module organizations (e.g., `app/services`, `components/ChatWindow`) are now explicit in the stories.
- **Technology Stack:** Precise libraries and tools (SQLAlchemy, asyncpg, LangChain, shadcn/ui, Tailwind) are mandated in the Acceptance Criteria and Technical Notes.
- **UX Patterns:** The specific user journeys (Role Selection buttons, Fallback messages, Feedback flow) are directly integrated into the stories.
- **Accessibility:** Explicit requirements for keyboard navigation and screen reader support are added.

This detailed plan provides a clear, technically robust, and user-centered roadmap for the implementation phase.
