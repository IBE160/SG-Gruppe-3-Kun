# Epics & Stories for ibe160

This document breaks down the requirements from the PRD into actionable epics and user stories.

---

## Proposed Epic Structure

Here is a summary of the proposed epics to build the HMSREG Documentation Chatbot.

### Epic 1: Project Foundation & Deployment Pipeline

-   **Value:** Establishes the core infrastructure, CI/CD pipeline, and development environment. This enables all future development and ensures the project is built on a solid, deployable foundation from day one.
-   **Scope:** Set up Git repository, Next.js frontend project, FastAPI backend project, connect to Supabase, configure Vercel/Railway for CI/CD, and create initial "hello world" deployments.

### Epic 2: Core Conversational Experience & RAG Pipeline

-   **Value:** Implements the fundamental ability for a user to ask a question and receive an answer from the documentation. This is the core "magic" of the product.
-   **Related Functional Requirements:** FR1.1, FR1.2, FR1.3, FR1.4
-   **Scope:** Build the data ingestion pipeline to process `docs.hmsreg.com`, set up the ChromaDB vector store, implement the LangChain RAG pipeline in the FastAPI backend, and create the basic chat UI in the frontend.

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
And a `.gitignore` file is configured for each project to exclude unnecessary files.
And a `README.md` is present at the root with basic project setup instructions.

**Prerequisites:** None
**Technical Notes:** Use `create-next-app` for frontend, `poetry new` for backend.

### Story 1.2: Configure Frontend Development Environment

**As a** frontend developer,
**I want to** set up the Next.js development environment with TypeScript, Tailwind CSS, and shadcn/ui,
**So that** I can efficiently build the user interface with a consistent and modern design system.

**Acceptance Criteria:**
Given the frontend directory,
When I set up the development environment,
Then Next.js 14 (App Router) is configured with TypeScript.
And Tailwind CSS is integrated for styling.
And shadcn/ui components are installed and configured.
And a basic "Hello World" page is rendered successfully.

**Prerequisites:** Story 1.1
**Technical Notes:** Follow official Next.js, Tailwind, and shadcn/ui installation guides.

### Story 1.3: Configure Backend Development Environment

**As a** backend developer,
**I want to** set up the FastAPI development environment with Python 3.11+,
**So that** I can efficiently build the API endpoints and integrate the RAG pipeline.

**Acceptance Criteria:**
Given the backend directory,
When I set up the development environment,
Then Python 3.11+ is configured with a virtual environment.
And FastAPI is installed with Uvicorn.
And a basic "Hello World" endpoint (`/health`) is accessible.
And a `requirements.txt` or `pyproject.toml` is created to manage dependencies.

**Prerequisites:** Story 1.1
**Technical Notes:** Use `poetry` for dependency management.

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
**Technical Notes:** Connect Railway to the Git repository, configure build and start commands.

### Story 1.6: Set up Supabase Project and Connect to Backend

**As a** backend developer,
**I want to** initialize a Supabase project and connect the FastAPI backend to its PostgreSQL database,
**So that** I can store conversation logs, feedback, and analytics data.

**Acceptance Criteria:**
Given a Supabase account,
When I create a new project,
Then a PostgreSQL database is provisioned.
And the FastAPI backend is configured with the necessary environment variables to connect to the Supabase database.
And a simple test endpoint in FastAPI can successfully write and read data from a test table in Supabase.

**Prerequisites:** Story 1.3
**Technical Notes:** Use Supabase free tier, configure `DATABASE_URL` environment variable in Railway.

### Story 1.7: Set up ChromaDB Vector Store

**As a** backend developer,
**I want to** set up and configure the ChromaDB vector store,
**So that** I can efficiently store and retrieve document embeddings for the RAG pipeline.

**Acceptance Criteria:**
Given the backend environment,
When ChromaDB is initialized,
Then it is configured for persistent storage (if applicable).
And a basic test can successfully add and retrieve a vector embedding.

**Prerequisites:** Story 1.3
**Technical Notes:** Integrate ChromaDB client library into the backend project.

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
When the ingestion pipeline is executed,
Then documentation content is scraped and chunked into manageable segments.
And each chunk is embedded using `text-embedding-004`.
And the embeddings are stored in ChromaDB.
And the original text content associated with each embedding is also stored.

**Prerequisites:** Story 1.3, Story 1.7
**Technical Notes:** Use a web scraping library (e.g., BeautifulSoup, Playwright) and LangChain for chunking and embedding.

### Story 2.2.a: Implement Core Chat Interface

**Covers:** FR1.1, FR1.3

**As a** frontend developer,
**I want to** create the foundational chat interface components,
**So that** users have the basic tools to interact with the chatbot.

**Acceptance Criteria:**
Given the frontend application,
When a user navigates to the chat page,
Then a chat history panel is displayed for showing messages.
And user and bot message bubbles are styled distinctly.
And a text input field and "Send" button are present and functional.

**Prerequisites:** Story 1.2
**Technical Notes:** Utilize shadcn/ui components. This story focuses on the core components, not the overall page layout.

### Story 2.2.b: Implement Desktop Three-Column Responsive Layout

**Covers:** FR1.1, FR1.3

**As a** frontend developer,
**I want to** implement the three-column responsive layout for large screens,
**So that** desktop users can efficiently see documentation, articles, and the chatbot simultaneously.

**Acceptance Criteria:**
Given the frontend application on a screen wider than 1024px,
When a user views a page with the chatbot,
Then a three-column grid is displayed: "Documentation Links" (left), "Article Content" (middle), and "Chatbot Interface" (right).
And the layout matches the structure in `ux-showcase.html`.

**Prerequisites:** Story 2.2.a
**Technical Notes:** Use CSS grid and media queries.

### Story 2.2.c: Implement Mobile Tabbed-Interface Layout

**Covers:** FR1.1, FR1.3

**As a** frontend developer,
**I want to** implement the single-column, tabbed interface for mobile screens,
**So that** mobile users can easily navigate between different content views on a small screen.

**Acceptance Criteria:**
Given the frontend application on a screen narrower than 1024px,
When a user views a page with the chatbot,
Then a single-column layout is displayed.
And a tab bar is present at the bottom of the screen with "Links," "Article," and "Chatbot" options.
And clicking a tab switches the main content view to the corresponding panel.
And the functionality matches the `ux-showcase.html` mockup.

**Prerequisites:** Story 2.2.a
**Technical Notes:** This will require state management to handle the active tab.

### Story 2.3: Implement RAG Pipeline in Backend

**Covers:** FR1.2, FR1.3

**As a** backend developer,
**I want to** integrate the LangChain RAG pipeline with Gemini 2.5 Pro,
**So that** user questions can be processed to retrieve relevant documentation and generate informed responses.

**Acceptance Criteria:**
Given a user question,
When the question is sent to the backend,
Then the question is embedded and used to query ChromaDB for relevant document chunks.
And the retrieved chunks are passed to Gemini 2.5 Pro along with the user's question.
And Gemini 2.5 Pro generates a coherent and relevant answer based on the provided context.
And the generated answer is returned to the frontend.

**Prerequisites:** Story 2.1
**Technical Notes:** Use LangChain's RAG capabilities, configure Google AI API key.

### Story 2.4: Connect Frontend Chat to Backend API

**Covers:** FR1.1, FR1.3

**As a** full-stack developer,
**I want to** establish communication between the frontend chat interface and the backend RAG API,
**So that** users can send questions and receive real-time answers from the chatbot.

**Acceptance Criteria:**
Given the chat UI and the RAG backend,
When a user types a question and sends it,
Then the frontend sends the question to the `/api/chat` endpoint.
And the backend processes the question via the RAG pipeline and returns an answer.
And the frontend displays the chatbot's answer in the chat window.

**Prerequisites:** Story 2.2, Story 2.3
**Technical Notes:** Use `fetch` or `axios` in Next.js to call the FastAPI endpoint.

### Story 2.5: Display Source Citations in Chat UI

**Covers:** FR1.4

**As a** frontend developer,
**I want to** display the source documentation links alongside the chatbot's answers,
**So that** users can verify the information and explore the original context.

**Acceptance Criteria:**
Given a chatbot response,
When the response is generated from specific documentation chunks,
Then the frontend receives the source URLs or titles from the backend.
And these sources are displayed clearly (e.g., as clickable links) below the chatbot's answer.

**Prerequisites:** Story 2.3, Story 2.4
**Technical Notes:** The RAG pipeline should be configured to return source metadata along with the generated answer. The links should be displayed at the bottom of the chat bubble with a "Source:" label, as shown in `ux-showcase.html`.

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
When the user starts the chat,
Then a prompt appears asking the user to select their role (e.g., Worker, Supplier, Project Manager).
And a list of predefined roles is presented as clickable options.
And upon selection, the chosen role is clearly displayed to the user.

**Prerequisites:** Story 2.2.a
**Technical Notes:** Use shadcn/ui components for selection (e.g., radio buttons, dropdown). The UI should be a set of buttons presented within the chatbot's initial greeting message, as shown in `ux-showcase.html`.

### Story 3.2: Pass User Role to Backend

**Covers:** FR2.2

**As a** full-stack developer,
**I want to** securely transmit the selected user role from the frontend to the backend,
**So that** the backend can use this context for personalized RAG responses.

**Acceptance Criteria:**
Given a user has selected a role in the frontend,
When a user sends a question,
Then the selected role is included in the API request to the backend.
And the backend successfully receives and parses the user's role.

**Prerequisites:** Story 3.1, Story 2.4
**Technical Notes:** Include the role in the `/api/chat` payload.

### Story 3.3: Incorporate User Role into RAG Prompt

**Covers:** FR2.2

**As a** backend developer,
**I want to** modify the RAG pipeline to include the user's selected role in the prompt sent to Gemini 2.5 Pro,
**So that** the generated answers are tailored to the user's specific context.

**Acceptance Criteria:**
Given a user's question and their selected role,
When the RAG pipeline constructs the prompt for Gemini 2.5 Pro,
Then the prompt explicitly includes the user's role (e.g., "As a [Role], answer the following question...").
And the generated response demonstrates an understanding and application of the specified role.

**Prerequisites:** Story 3.2, Story 2.3
**Technical Notes:** Update the LangChain prompt template to dynamically insert the `user_role` variable.

## Epic 4: Robustness, Reliability & Feedback

**Epic Title:** Robustness, Reliability & Feedback
**Epic Goal:** Ensure the chatbot is helpful even when it doesn't know the answer and provide a mechanism for continuous improvement.

### Story 4.1: Implement Automatic Fallback Mechanism

**Covers:** FR3.1

**As a** backend developer,
**I want to** implement a mechanism to detect when the chatbot cannot confidently answer a question,
**So that** it can gracefully inform the user and provide alternative resources.

**Acceptance Criteria:**
Given a user question,
When the RAG pipeline's confidence score for an answer falls below a predefined threshold,
Then the chatbot responds with a message indicating it cannot confidently answer.
And the response includes links to general HMSREG documentation or support contact information.

**Prerequisites:** Story 2.3
**Technical Notes:** Define a confidence threshold for RAG responses.

### Story 4.2: Develop User Feedback Mechanism (Thumbs Up/Down)

**Covers:** FR4.1

**As a** full-stack developer,
**I want to** provide a simple way for users to give feedback on each chatbot response,
**So that** we can continuously monitor and improve the chatbot's performance.

**Acceptance Criteria:**
Given a chatbot response is displayed,
When the user views the response,
Then "Thumbs Up" and "Thumbs Down" buttons are displayed next to the response.
And clicking either button sends feedback (response ID, feedback type) to the backend.
And the feedback is stored in the Supabase database.

**Prerequisites:** Story 2.4, Story 1.6
**Technical Notes:** Create a new API endpoint (`/api/feedback`) and a table in Supabase for feedback. The feedback buttons should appear directly below each chatbot response that is eligible for feedback.

### Story 4.3: Implement Ambiguous Query Suggestion

**Covers:** FR3.2

**As a** backend developer,
**I want to** enable the chatbot to suggest alternative or related topics when a user's query is ambiguous,
**So that** users can refine their questions and find relevant information more easily.

**Acceptance Criteria:**
Given a user query that is deemed ambiguous by the RAG pipeline,
When the chatbot processes the query,
Then it suggests 2-3 related topics or rephrased questions.
And these suggestions are displayed to the user in the chat interface.

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
Given an API endpoint (e.g., `/api/chat`, `/api/feedback`),
When a user exceeds the defined rate limit (e.g., 10 requests/minute, 50 requests/hour),
Then subsequent requests from that user are rejected with an appropriate HTTP status code (e.g., 429 Too Many Requests).
And the rate limits are configurable via environment variables.

**Prerequisites:** Story 1.3
**Technical Notes:** Use a FastAPI middleware or a dedicated rate-limiting library.

### Story 5.2: Ensure WCAG 2.1 AA Compliance for Frontend

**Covers:** FR5.1

**As a** frontend developer,
**I want to** ensure the web interface adheres to WCAG 2.1 AA accessibility standards,
**So that** the chatbot is usable by individuals with disabilities.

**Acceptance Criteria:**
Given the frontend application,
When tested with accessibility tools (e.g., Lighthouse, Axe DevTools),
Then all critical accessibility issues (e.g., sufficient color contrast, proper focus management, semantic HTML) are resolved.
And keyboard navigation is fully functional for all interactive elements.
And screen reader users can effectively interact with the chat interface and understand content.

**Prerequisites:** Story 2.2
**Technical Notes:** Conduct regular accessibility audits throughout development.

### Story 5.3: Implement Comprehensive Logging and Monitoring

**As a** DevOps engineer,
**I want to** set up comprehensive logging and monitoring for both frontend and backend,
**So that** operational issues can be quickly identified, diagnosed, and resolved.

**Acceptance Criteria:**
Given the deployed application,
When errors or significant events occur in the frontend or backend,
Then logs are generated with relevant information (e.g., timestamps, error messages, request details).
And these logs are centralized and accessible for monitoring and analysis.
And basic application health metrics (e.g., API response times, error rates) are collected and visualized.

**Prerequisites:** Story 1.4, Story 1.5
**Technical Notes:** Use a logging library (e.g., `logging` in Python, `console` in JS) and integrate with a monitoring solution (e.g., Sentry, Prometheus/Grafana).

### Story 5.4: Conduct Final End-to-End Testing

**As a** QA engineer,
**I want to** perform comprehensive end-to-end testing of the entire application,
**So that** all features and integrations function correctly before launch.

**Acceptance Criteria:**
Given the fully integrated application,
When a suite of end-to-end tests is executed,
Then all critical user flows (e.g., role selection, asking questions, receiving answers, providing feedback) pass successfully.
And integrations between frontend, backend, Supabase, and ChromaDB are verified.
And performance and security non-functional requirements are validated.

**Prerequisites:** All previous stories
**Technical Notes:** Use a testing framework like Playwright or Cypress.

---

## Epic Breakdown Summary

The proposed epic structure and the detailed stories for each epic appear to be comprehensive, logically sequenced, and actionable. All functional requirements from the PRD are covered, and Epic 1 correctly establishes the necessary foundation. The stories are vertically sliced, appropriately sized for single-session completion, and include clear, testable BDD acceptance criteria. Domain and compliance requirements are addressed, and the overall sequencing supports incremental value delivery.

This breakdown provides a solid plan for the architecture and implementation phases.
