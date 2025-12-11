# Epic Technical Specification: Project Foundation & Deployment Pipeline

Date: Monday, 8 December 2025
Author: BIP
Epic ID: 1
Status: Draft

---

## Overview

This epic focuses on establishing the core infrastructure for the HMSREG Documentation Chatbot. It involves setting up the monorepo structure, initializing the Next.js frontend and FastAPI backend projects, configuring the database connection (Supabase) and vector store (ChromaDB), and implementing a CI/CD pipeline. The goal is to provide a solid, consistent, and deployable foundation for all subsequent development, ensuring that team members can work efficiently and that changes can be safely and automatically deployed to a staging environment. This aligns with the PRD's goal of building a robust web application and API backend.

## Objectives and Scope

**Objectives:**
*   Initialize a clean, monorepo project structure.
*   Set up a modern, type-safe frontend environment with Next.js, TypeScript, and Tailwind CSS.
*   Set up a high-performance, async backend environment with FastAPI and Python 3.11+.
*   Establish database connectivity for relational data (PostgreSQL) and vector data (ChromaDB).
*   Automate build and deployment processes for both frontend and backend.

**In-Scope:**
*   Git repository initialization and `.gitignore` configuration.
*   Frontend project creation (Next.js 14, TypeScript, Tailwind, shadcn/ui).
*   Backend project creation (FastAPI, Poetry, SQLAlchemy, Pydantic).
*   CI/CD pipeline configuration (Vercel for frontend, Railway for backend).
*   Supabase project setup and connection.
*   ChromaDB initialization and client configuration.
*   Basic "Hello World" / Health check endpoints.

**Out-of-Scope:**
*   Implementation of the actual chat interface (Epic 2).
*   Data ingestion logic (Epic 2).
*   User authentication (Future).
*   Production-grade logging and monitoring (Epic 5).

## System Architecture Alignment

This epic directly implements the "Project Structure" and "Technology Stack" defined in the Architecture document. It establishes the `frontend/` and `backend/` directories, configures the specified technologies (Next.js, FastAPI, SQLAlchemy, asyncpg), and sets up the integration points for the database and vector store. It adheres to the decision to use Vercel and Railway for deployment.

## Detailed Design

### Services and Modules

| Module / Service | Responsibilities | Inputs | Outputs | Owner |
| :--- | :--- | :--- | :--- | :--- |
| **Frontend (Next.js)** | User Interface, API proxying | User interactions | UI rendering, API calls | Frontend Dev |
| **Backend (FastAPI)** | API endpoints, business logic, DB access | HTTP Requests | JSON Responses | Backend Dev |
| **Database (Supabase)** | Relational data persistence | SQL queries | Data rows | Backend Dev |
| **Vector Store (ChromaDB)** | Embedding storage & retrieval | Vectors, Metadata | Similar vectors | Backend Dev |
| **CI/CD (Vercel)** | Build & deploy frontend | Git push | Deployed URL | DevOps |
| **CI/CD (Railway)** | Build & deploy backend | Git push | Deployed URL | DevOps |

### Data Models and Contracts

**Relational Database (PostgreSQL - Initial Setup)**
*   No specific tables are required for the "Hello World" setup, but the connection infrastructure must be ready.
*   `app/core/config.py` will define `DATABASE_URL`.
*   `app/db/session.py` will export the `AsyncSession` generator.

**Vector Store (ChromaDB)**
*   Collection name: `hmsreg_docs` (tentative).
*   Schema:
    *   `id`: String (Chunk ID)
    *   `embedding`: List[float] (768 dimensions for `text-embedding-004`)
    *   `document`: String (Text content)
    *   `metadata`: Map (Source URL, Title, Last Updated)

### APIs and Interfaces

**Backend Health Check**
*   **Endpoint:** `GET /health`
*   **Response:** `200 OK`
    ```json
    {
      "status": "ok",
      "version": "0.1.0"
    }
    ```

**Frontend Health Check**
*   **Route:** `/` (Root page)
*   **Content:** Renders a basic "Hello World" or "HMSREG Chatbot" title to verify build success.

### Workflows and Sequencing

**CI/CD Pipeline Flow:**
1.  Developer pushes code to `main` branch.
2.  **Frontend:** Vercel detects change -> Triggers Build -> Deploys to Staging URL.
3.  **Backend:** Railway detects change -> Builds Docker image (or uses Buildpack) -> Deploys to Staging URL.

**Database Connection Flow:**
1.  FastAPI app starts (`app/main.py`).
2.  `lifespan` event triggers.
3.  Database engine initializes (`app/db/session.py`).
4.  Connection test performed (optional but recommended).

## Non-Functional Requirements

### Performance
*   **CI/CD:** Build and deploy times should ideally be under 5 minutes for rapid iteration.
*   **API Latency:** Health check endpoint should respond in < 100ms.

### Security
*   **Secrets Management:** API keys (Supabase, OpenAI/Gemini, etc.) must NOT be committed to Git. They must be managed via `.env` files locally and environment variable configurations in Vercel/Railway.
*   **Database Access:** Backend should connect to the database using a secure connection string with appropriate user privileges (least privilege principle).

### Reliability/Availability
*   **Uptime:** The staging environments should be available 99% of the time during development hours.
*   **Health Checks:** Automated health checks should verify service availability post-deployment.

### Observability
*   **Build Logs:** CI/CD platforms must provide accessible build and deployment logs.
*   **Runtime Logs:** Application logs should be output to `stdout`/`stderr` for collection by the hosting platform.

## Dependencies and Integrations

*   **Frontend:**
    *   `next`: ^14.0.0
    *   `react`: ^18.0.0
    *   `typescript`: ^5.0.0
    *   `tailwindcss`: ^3.0.0
    *   `lucide-react`: Latest
    *   `clsx`, `tailwind-merge`: Latest
*   **Backend:**
    *   `python`: ^3.11
    *   `fastapi`: ^0.109.0 (or latest stable)
    *   `uvicorn[standard]`: Latest
    *   `sqlalchemy`: ^2.0.0
    *   `asyncpg`: Latest
    *   `pydantic-settings`: Latest
    *   `chromadb`: Latest client
    *   `poetry`: ^1.7.0
*   **Infrastructure:**
    *   Supabase (PostgreSQL)
    *   Vercel (Frontend Hosting)
    *   Railway (Backend Hosting)

## Acceptance Criteria (Authoritative)

**Story 1.1: Project Init**
1.  Monorepo structure exists with `frontend/` and `backend/`.
2.  `.gitignore` correctly ignores `node_modules`, `__pycache__`, `.env`, `.venv`.
3.  `README.md` details setup steps.

**Story 1.2: Frontend Setup**
1.  Next.js 14+ app runs locally on port 3000.
2.  TypeScript compiles without errors.
3.  Tailwind classes apply correctly.
4.  shadcn/ui components can be added.

**Story 1.3: Backend Setup**
1.  FastAPI app runs locally on port 8000.
2.  `GET /health` returns `{"status": "ok"}`.
3.  Poetry manages dependencies.

**Story 1.4: Frontend CI/CD**
1.  Push to `main` triggers Vercel deployment.
2.  Staging URL is accessible and renders the app.

**Story 1.5: Backend CI/CD**
1.  Push to `main` triggers Railway deployment.
2.  Staging API URL (`/health`) returns 200 OK.

**Story 1.6: Supabase Connection**
1.  `app/core/config.py` loads `DATABASE_URL`.
2.  Test endpoint can execute a simple SQL query (e.g., `SELECT 1`).

**Story 1.7: ChromaDB Setup**
1.  ChromaDB client initializes without error.
2.  Test script can add and query a dummy embedding.

## Traceability Mapping

| AC ID | Spec Section | Component / API | Test Idea |
| :--- | :--- | :--- | :--- |
| 1.1.1 | Detailed Design | Project Root | Verify directory structure manually |
| 1.2.1 | Detailed Design | Frontend | Run `npm run dev` and access localhost:3000 |
| 1.3.2 | APIs and Interfaces | Backend API | `curl localhost:8000/health` |
| 1.4.1 | Detailed Design | Vercel | Check Vercel dashboard for build success |
| 1.5.2 | Detailed Design | Railway | Curl the deployed Railway URL |
| 1.6.2 | Detailed Design | Backend DB Module | Unit test simulating DB connection |
| 1.7.2 | Detailed Design | Backend RAG Module | Script to insert/retrieve mock vector |

## Risks, Assumptions, Open Questions

*   **Assumption:** The developer has accounts for Vercel, Railway, and Supabase.
*   **Risk:** Supabase free tier connection limits might be reached during heavy development. **Mitigation:** Use connection pooling (Supabase provides this).
*   **Question:** Should we use a local Docker container for ChromaDB during development or a managed service? **Decision:** Architecture implies local/embedded for dev, need to clarify for production (likely persistent Docker volume on Railway).

## Test Strategy Summary

*   **Unit Tests:**
    *   Backend: Test configuration loading and basic endpoint responses using `pytest` and `httpx`.
    *   Frontend: Basic component rendering tests using `Jest` / `React Testing Library`.
*   **Integration Tests:**
    *   Verify database connection succeeds.
    *   Verify Vector Store client initialization.
*   **Manual Verification:**
    *   Verify deployment URLs work after git push.

