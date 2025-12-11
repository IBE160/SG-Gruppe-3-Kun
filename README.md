# HMSREG Documentation Chatbot

Repository for the HMSREG Documentation Chatbot, developed as part of IBE160 Programmering med KI.

This project aims to provide an AI-powered tool for construction industry professionals to get instant, accurate, and role-based answers from official documentation.

## Project Structure

This is a monorepo containing a `frontend` (Next.js) and `backend` (FastAPI) application, along with project documentation in `docs/`.

## Development Setup

### Prerequisites

*   Node.js 18+
*   Python 3.11+
*   Poetry (Python package manager)
*   Git

### 1. Clone the repository

```bash
git clone <repository-url>
cd SG-Gruppe-3-Kun
```
(Replace `<repository-url>` with the actual repository URL)

### 2. Backend Setup (FastAPI)

Navigate to the `backend` directory and set up the Python environment:

```bash
cd backend
poetry install
```

To run the backend application locally:

```bash
poetry run uvicorn app.main:app --reload
```

### 3. Frontend Setup (Next.js)

Navigate to the `frontend` directory and install Node.js dependencies:

```bash
cd frontend
npm install
```

To run the frontend application locally:

```bash
npm run dev
```

### 4. Further Information

*   **Frontend Deployment (Vercel):** https://sg-gruppe-3-kun.vercel.app/
*   **Architecture:** See `docs/architecture.md` for detailed architectural decisions and project structure.
*   **Epics & Stories:** See `docs/epics.md` for a breakdown of features and development stories.
*   **UX Design:** See `docs/ux-design-specification.md` for user experience and design guidelines.