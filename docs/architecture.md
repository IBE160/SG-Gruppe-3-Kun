# Architecture

## Executive Summary

The **HMSREG Documentation Chatbot** is a modern, responsive web application and API backend designed to empower construction industry professionals with instant, accurate, and role-based answers from official documentation.

Leveraging **Next.js 14+** for a high-performance frontend and **FastAPI** for a robust, AI-ready backend, the system implements a scalable **RAG (Retrieval-Augmented Generation)** pipeline. Core technologies include **PostgreSQL** with **SQLAlchemy** for reliable data persistence, **ChromaDB** for efficient vector search, and **Google Gemini 2.5 Pro** for intelligent response generation. The architecture prioritizes **real-time responsiveness** via Server-Sent Events (SSE), **user-centric design** through role-based personalization, and **operational reliability** with comprehensive testing and monitoring, all while maintaining a strong commitment to simplicity and "boring technology" principles.

## Project Initialization

### Backend (FastAPI)

First implementation story should execute:
```bash
# Initialize FastAPI project with Poetry
poetry new backend
cd backend
poetry add fastapi uvicorn[standard] sqlalchemy asyncpg python-multipart
```

### Frontend (Next.js)

First implementation story should execute:
```bash
npx create-next-app@latest frontend --typescript --tailwind --eslint --app --no-src-dir --import-alias "@/*"
```
*Followed by manual `shadcn/ui` initialization as per UX spec.*

This establishes the base architecture with these decisions:
- **Next.js Framework:** Standard setup for optimal performance and developer experience.
- **TypeScript:** Ensuring type safety across the frontend codebase.
- **Tailwind CSS:** For rapid, utility-first styling.
- **ESLint:** To maintain code quality and consistency.

## Decision Summary

| Category | Decision | Version | Affects Epics | Rationale |
| -------- | -------- | ------- | ------------- | --------- |
| **Data Persistence** | **SQLAlchemy** with **asyncpg** | SQLAlchemy 2.0.44, asyncpg 0.31.0 | Project Foundation, Core Conversational Experience | Robust, flexible, and well-established ORM for Python with strong async support, ideal for FastAPI and PostgreSQL. |
| **API Backend** | **FastAPI** with **Uvicorn** | FastAPI 0.123.9, Uvicorn 0.38.0 | Project Foundation, Core Conversational Experience | High-performance, modern Python framework with excellent async support and automatic docs, served by a robust ASGI server. |
| **Authentication** | **Supabase Auth** | v2.39.0 (JS), v2.3.0 (Py) | Project Foundation, User Context | Integrated seamlessly with the chosen database (Supabase). Provides robust JWT-based auth without managing a separate auth infrastructure. |
| **Real-time Comms** | **Server-Sent Events (SSE)** | Standard (FastAPI StreamingResponse) | Core Conversational Experience, User Context | Lightweight, standard solution perfect for unidirectional text streaming (LLM responses), simpler than WebSockets. |
| **Project Init (Backend)** | **Poetry** | Poetry 1.8.0 | Project Foundation | Modern dependency management and packaging tool ensuring consistent environments and simplified workflows. |
| **Error Handling** | **Centralized Strategy** | N/A | Robustness & Reliability | Ensures consistent error messages for users and streamlined logging/debugging for developers. |
| **Logging** | **Standard `logging`** (Structured in Prod) | Python built-in | Production Readiness | Flexible standard logging for dev, structured (JSON) for prod to facilitate efficient monitoring and analysis. |
| **Date/Time** | **UTC Storage** | `datetime` (Py), `date-fns` (JS) | Robustness & Reliability, User Context | Standardizing on UTC eliminates timezone ambiguities and ensures data integrity globally. |
| **API Response** | **Direct JSON** | N/A | Core Conversational Experience | Simple, efficient, and consistent communication contract leveraging FastAPI's native capabilities. |
| **Testing** | **Unit + Integration + E2E + Accessibility** | Pytest, Jest/RTL, Playwright | Production Readiness, Robustness | Comprehensive multi-layered strategy to ensure reliability, compliance, and user confidence. |

## Project Structure

```
.
├── .github/                     # CI/CD workflows (Vercel for frontend, Railway for backend)
├── docs/                        # Project documentation (PRD, UX, Architecture, etc.)
├── frontend/                    # Next.js 14+ Application
│   ├── public/                  # Static assets
│   ├── app/                     # App Router routes and page components
│   │   ├── api/                 # Frontend API routes (e.g., /api/chat for streaming)
│   │   │   └── chat/
│   │   │       └── route.ts     # Frontend SSE endpoint
│   │   ├── (auth)/              # Authentication-related routes/components
│   │   ├── (main)/              # Main application routes/pages
│   │   │   └── page.tsx
│   │   └── layout.tsx           # Global layout
│   ├── components/              # Reusable React UI components (shadcn/ui based)
│   ├── lib/                     # Client-side utility functions, helpers
│   ├── hooks/                   # Custom React hooks
│   ├── styles/                  # Tailwind CSS configuration and global styles
│   ├── types/                   # Frontend TypeScript types
│   └── tests/                   # Jest/RTL unit and integration tests (co-located)
├── backend/                     # FastAPI Application
│   ├── app/                     # Core application modules
│   │   ├── api/                 # FastAPI routers for API endpoints
│   │   │   └── v1/
│   │   │       ├── chat.py      # Chat functionality (RAG, SSE streaming)
│   │   │       ├── feedback.py  # User feedback endpoints
│   │   │       └── __init__.py
│   │   ├── core/                # Application settings, configurations
│   │   │   └── config.py
│   │   ├── db/                  # Database connection, SQLAlchemy models, migrations
│   │   │   ├── session.py
│   │   │   ├── models.py
│   │   │   └── __init__.py
│   │   ├── services/            # Business logic, service layer
│   │   │   ├── chat_service.py
│   │   │   └── __init__.py
│   │   ├── schemas/             # Pydantic models for request/response validation
│   │   │   ├── chat.py
│   │   │   └── __init__.py
│   │   ├── rag/                 # RAG pipeline implementation (LangChain, ChromaDB)
│   │   │   ├── vector_store.py
│   │   │   ├── ingestion.py
│   │   │   └── __init__.py
│   │   ├── llm/                 # LLM integration and utilities (Gemini)
│   │   │   └── gemini.py
│   │   ├── utils/               # General utility functions
│   │   │   └── datetime_utils.py
│   │   └── main.py              # FastAPI application entry point
│   ├── tests/                   # Pytest tests (co-located with app modules where appropriate)
│   ├── alembic/                 # Alembic configuration for database migrations
│   │   └── versions/            # Migration scripts
│   ├── .env.example             # Example environment variables
│   ├── pyproject.toml           # Poetry project configuration and dependencies
│   └── poetry.lock              # Poetry locked dependencies
├── .gitignore                   # Global Git ignore file
├── README.md                    # Project README
└── package.json                 # Monorepo/workspace package.json
```

## Epic to Architecture Mapping

| Epic | Architecture Components |
| :--- | :--- |
| **Epic 1: Project Foundation & Deployment Pipeline** | `frontend/`, `backend/`, `pyproject.toml`, `.github/` (CI/CD), `app/core/config.py`, `app/db/` |
| **Epic 2: Core Conversational Experience & RAG Pipeline** | `backend/app/rag/`, `backend/app/llm/`, `backend/app/api/v1/chat.py`, `backend/app/services/chat_service.py`, `frontend/app/api/chat/`, `frontend/components/ChatWindow.tsx`, `ChromaDB`, `Gemini API` |
| **Epic 3: User Context & Personalization** | `frontend/components/RoleSelector.tsx`, `backend/app/schemas/chat.py` (request model), `backend/app/services/chat_service.py` (prompt engineering logic) |
| **Epic 4: Robustness, Reliability & Feedback** | `backend/app/api/v1/feedback.py`, `backend/app/db/models.py` (Feedback model), `frontend/components/FeedbackButtons.tsx`, Error Handling Middleware |
| **Epic 5: Production Readiness & Accessibility** | `backend/app/core/logging.py`, `frontend/tests/a11y/`, CI/CD pipelines, `backend/app/middleware/rate_limit.py` |

## Technology Stack Details

### Core Technologies

*   **Frontend Framework:** Next.js 14+ (App Router)
*   **Language:** TypeScript (Frontend), Python 3.11+ (Backend)
*   **Styling:** Tailwind CSS
*   **UI Components:** shadcn/ui
*   **Backend API:** FastAPI
*   **Database:** PostgreSQL (via Supabase)
*   **ORM:** SQLAlchemy (Async)
*   **Vector Store:** ChromaDB
*   **LLM:** Google Gemini 2.5 Pro
*   **Orchestration:** LangChain

### Integration Points

*   **Frontend <-> Backend:** REST API for standard ops, SSE (`/api/v1/chat/stream`) for chat streaming.
*   **Backend <-> Database:** SQLAlchemy async session connecting to Supabase PostgreSQL.
*   **Backend <-> Vector Store:** `chromadb` client for managing embeddings.
*   **Backend <-> LLM:** Google Generative AI SDK (via LangChain) for generation.

## Novel Pattern Designs

*   **Note:** While this project features significant innovation in its application of conversational AI and role-based contextualization, the underlying architectural patterns required to implement these features are well-established. We will be utilizing standard patterns such as Retrieval-Augmented Generation (RAG), Server-Sent Events (SSE) for real-time communication, and a monorepo structure with FastAPI and Next.js, rather than inventing novel architectural patterns.

## Implementation Patterns

These patterns ensure consistent implementation across all AI agents:

### Naming Conventions

*   **API Endpoints:** Plural for collections (`/users`, `/chats`), singular for specific instances or actions (`/user/{id}`, `/chat/stream`).
*   **Database:**
    *   Tables: Lowercase, plural, snake_case (`chat_sessions`, `user_feedback`).
    *   Columns: Lowercase, singular, snake_case (`user_id`, `created_at`).
*   **Frontend:**
    *   Components: PascalCase (`ChatWindow`, `RoleSelector`).
    *   Files: PascalCase with extension (`ChatWindow.tsx`, `useChat.ts`).

### Role-Based Prompting Pattern

*   **Mechanism:** The user's selected role (from frontend `RoleSelector`) is passed as a header or body parameter (`X-User-Role` or JSON payload) to the `/chat` endpoint.
*   **Injection:** The backend `ChatService` injects this role into the System Prompt:
    ```python
    system_prompt = f"You are an expert assistant for a {user_role}. Tailor your language and technical depth accordingly."
    ```
*   **Fallback:** Default to "General User" if no role is specified.

### Chat UI State Machine

*   **States:**
    *   `IDLE`: User has not sent a message. Input enabled.
    *   `SENDING`: User pressed send. Input disabled. Optimistic UI update.
    *   `STREAMING`: Receiving SSE tokens. Input disabled. Auto-scroll to bottom.
    *   `COMPLETE`: Stream finished. Input enabled. Markdown rendered.
    *   `ERROR`: Network or API error. Input enabled. Retry button visible.

### Code Organization

*   **Frontend:** Feature-based routing (App Router). Reusable UI in `components/`. Logic hooks in `hooks/`.
*   **Backend:** Domain-driven structure (`api/`, `services/`, `schemas/`, `db/`).
*   **Tests:** Co-located with source files (`component.test.tsx`, `test_service.py`).

### Lifecycle Patterns

*   **Loading:** Use skeleton loaders for content areas; spinners for actions. Disable inputs during processing.
*   **Errors:** Centralized handling. User-friendly toast/inline notifications.
*   **Retry:** Auto-retry with backoff for backend idempotent ops. Manual "Retry" button for frontend user actions.

## Consistency Rules

### Error Handling

*   **Backend:** Global exception handler in FastAPI catches all errors, logs them, and returns a standard JSON error response (e.g., `{ "detail": "User friendly message" }`).
*   **Frontend:** Interceptors/hooks catch API errors and trigger the UI notification system.

### Logging Strategy

*   **Development:** Standard Python logging to console (DEBUG level).
*   **Production:** Structured JSON logging (INFO level) enabling ingestion by monitoring tools.

## Data Architecture

*   **Primary Database (PostgreSQL):** Stores relational data like `Feedback`, `ChatSessions` (if persisted), and potential future `Users`.
*   **Vector Database (ChromaDB):** Stores high-dimensional vector embeddings of the chunked documentation content for similarity search.

## API Contracts

*   **Request/Response:** Strict Pydantic models define all API payloads.
*   **Documentation:** Auto-generated OpenAPI (Swagger) documentation available at `/docs` on the backend.

## Security Architecture

*   **Authentication:** **Supabase Auth** manages user identities and issues JWTs.
    *   **Frontend:** Uses `@supabase/auth-helpers-nextjs` for middleware protection and session management.
    *   **Backend:** Validates the Supabase JWT in the `Authorization: Bearer` header for protected routes.
*   **Input Validation:** Strict Pydantic validation on all incoming data.
*   **Rate Limiting:** Implemented on API endpoints to prevent abuse.
*   **Data Protection:** Use of parameterized queries (via ORM) to prevent SQL injection.

## Performance Considerations

*   **Async I/O:** Extensive use of `async`/`await` in FastAPI for non-blocking operations.
*   **Streaming:** SSE for chat responses to minimize perceived latency.
*   **Caching:** Potential future implementation of Redis for caching frequent queries or RAG results.

## Deployment Architecture

*   **Frontend:** Vercel (Edge Network) for global, fast delivery of the Next.js app.
*   **Backend:** Railway (Containerized) for reliable, scalable hosting of the FastAPI service.
*   **Database:** Supabase (Managed PostgreSQL) for robust data storage.

## Development Environment

### Prerequisites

*   Node.js 18+
*   Python 3.11+
*   Docker (optional, for local DB/ChromaDB)
*   Poetry (Python package manager)

### Setup Commands

```bash
# Backend
cd backend
poetry install
poetry run uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

## Architecture Decision Records (ADRs)

*   **ADR-001:** Use FastAPI + Next.js for high-performance AI integration.
*   **ADR-002:** Adopt Server-Sent Events (SSE) for simple, efficient text streaming.
*   **ADR-003:** Use SQLAlchemy + asyncpg for robust, async database interactions.
*   **ADR-004:** Implement comprehensive testing strategy (Unit, Integration, E2E) for reliability.

---

_Generated by BMAD Decision Architecture Workflow v1.0_
_Date: Sunday, 7 December 2025_
_For: BIP_