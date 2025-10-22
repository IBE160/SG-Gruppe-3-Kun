## Case Title

HMSREG Documentation Chatbot

## Background

HMSREG is an electronic system used in the Norwegian construction industry for workforce registration, documentation, and control of suppliers and working conditions. The system helps prevent labor crime and social dumping by ensuring transparency about who is involved in projects. Users often need quick access to information about documentation requirements, certificates, HMS cards, and system procedures, but navigating extensive documentation can be time-consuming.

## Purpose

The chatbot provides HMSREG users (suppliers, subcontractors, construction workers, project managers, and administrators) with quick and accurate answers to questions about using HMSREG, requirements, procedures, documentation, and troubleshooting. The goal is to reduce support workload, ensure consistent answers, improve user efficiency, and make HMSREG documentation more accessible.

## Target Users

-   **Suppliers and subcontractors** who need to register workforce, certificates, and HMS cards
-   **Construction workers** who check in/out of sites using the app or integrated systems and need information about their documentation requirements
-   **Project managers and construction project owners** who need overview of status, deviations, and documentation
-   **Administrative and support personnel** who handle user inquiries and training

## Core Functionality

### Must Have (MVP)

-   Chat interface where users can ask questions related to HMSREG documentation
-   Knowledge base with HMSREG topics: workforce registration, documentation requirements, certificates, HMS cards, check-in/out procedures
-   Answer questions based on official HMSREG documentation from docs.hmsreg.com
-   Automatic fallback when chatbot doesn't know the answer - provide users with support channels or direct documentation links
-   Search and retrieve relevant information from HMSREG documentation

### Nice to Have (Optional Extensions)

-   Example scenarios / "What do I do if..." guides
-   Interactive troubleshooting based on user's specific situation
-   Clarifying questions to understand user's role and provide context-aware responses
-   Log of common questions for analysis and documentation improvement
-   Multi-language support (Norwegian/English)
-   Improved UI with enhanced user experience
-   Mobile-responsive design for on-site access

## Data Requirements

-   **HMSREG documentation content** - FAQs, user guides, procedures, requirements from docs.hmsreg.com
-   **User conversations** - questions asked, responses given, timestamps, session context
-   **Metadata** - topic categorization (e.g., "workforce registration", "HMS card validity", "check-in/out", "documentation requirements")
-   **Feedback data** - user satisfaction ratings, helpful/not helpful responses
-   **Common question analytics** - frequency of topics, unresolved queries

## User Stories

1. As a supplier, I want to quickly find instructions on how to register workforce and upload all required documentation for compliance audits in HMSREG, so that I can meet project requirements and maintain my status as a verified supplier
2. As a construction worker, I want to understand why my check-in failed, so that I can resolve the issue and access the site
3. As a project manager, I want to understand how to verify that all personnel on site have proper competence certifications and that suppliers meet compliance requirements, so that I can fulfill my obligations under the Construction Client Regulations
4. As a support agent, I want the chatbot to handle common user questions automatically, so that I can focus on more complex support cases
5. As a subcontractor, I want to know how to upload documentation and add new HMS cards to crew lists, so that I can keep my workforce registrations up to date

## Technical Constraints

-   Must be mobile-responsive for on-site access by construction workers and field personnel
-   Must support Norwegian terminology and context specific to HMSREG and the construction industry
-   Must be able to access and process documentation from docs.hmsreg.com
-   Must handle Norwegian and English language queries
-   Should be accessible without requiring HMSREG login credentials (public documentation access)
-   Must provide accurate, up-to-date information reflecting current HMSREG procedures and requirements

## Technical Architecture

This section defines the complete technology stack and system architecture for the HMSREG Documentation Chatbot.

### System Architecture Overview

```
┌─────────────────┐
│  User Browser   │
│  (Mobile/Web)   │
└────────┬────────┘
         │ HTTPS
         ▼
┌─────────────────────────────────────┐
│      Frontend (Next.js 14)          │
│  - Chat UI (shadcn/ui components)   │
│  - Static docs pages (SSG)          │
│  - State management (Context API)   │
│  - Tailwind CSS styling             │
└────────┬────────────────────────────┘
         │ REST API / SSE
         ▼
┌─────────────────────────────────────┐
│     Backend (Python + FastAPI)      │
│  - API endpoints (/chat, /feedback) │
│  - LangChain RAG pipeline           │
│  - Document retrieval logic         │
│  - Prompt engineering layer         │
│  - Rate limiting (slowapi)          │
└────┬────────────────────┬───────────┘
     │                    │
     ▼                    ▼
┌──────────────┐   ┌──────────────────┐
│  Vector DB   │   │  PostgreSQL DB   │
│  (ChromaDB)  │   │   (Supabase)     │
│ - Embeddings │   │ - Conversations  │
│ - Doc chunks │   │ - Feedback       │
└──────────────┘   │ - Analytics      │
     │             │ - Rate limits    │
     │             └──────────────────┘
     ▼
┌─────────────────────────────────────┐
│      OpenAI API (Production)        │
│  - GPT-5-mini (chat responses)      │
│  - text-embedding-3-small (search)  │
└─────────────────────────────────────┘
```

### Frontend Specification

**Framework & Build Tools:**
- **Next.js 14 (App Router)** with **TypeScript** - Modern full-stack React framework with built-in SSG/SSR capabilities and type safety
- **File-based routing** - Automatic routing based on file structure in `/app` directory
- **Static Site Generation (SSG)** - Pre-render documentation pages at build time for optimal performance
- **Server and Client Components** - Separate static content (Server Components) from dynamic chat UI (Client Components)

**Application Structure:**
- `/app/page.tsx` - Landing page with chatbot introduction and navigation
- `/app/chat/page.tsx` - Main chat interface (Client Component with dynamic interaction)
- `/app/docs/` - Static documentation pages (Server Components, pre-rendered at build time)
  - `/app/docs/workforce/page.tsx` - Workforce registration guide
  - `/app/docs/hms-cards/page.tsx` - HMS card information and renewal
  - `/app/docs/check-in/page.tsx` - Check-in procedures and troubleshooting
  - `/app/docs/compliance/page.tsx` - Compliance and regulations
- `/public/articles/` - Markdown files and images for documentation content

**UI & Styling:**
- **Tailwind CSS** - Utility-first CSS framework for rapid styling
- **shadcn/ui** - Pre-built accessible React components (Button, Card, Dialog, etc.)
- **Lucide React** - Icon library for UI elements

**Chat Interface:**
- **Streaming responses** - Server-Sent Events (SSE) for real-time chat output
- **Message history** - Local state management with React Context API or Zustand
- **Mobile-first design** - Responsive breakpoints (sm: 640px, md: 768px, lg: 1024px)
- **Accessibility** - WCAG 2.1 AA compliance for form inputs and navigation
- **Session tracking** - Unique session IDs for rate limiting and analytics

**State Management:**
- **React Context API** - Lightweight solution for conversation state
- **localStorage** - Optional session persistence for conversation history

### Backend Specification

**Framework:**
- **Python 3.11+** - Modern Python with improved performance
- **FastAPI** - High-performance async web framework with automatic OpenAPI docs

**API Design:**
- **REST API** with the following endpoints:
  - `POST /api/chat` - Main chat endpoint (accepts message, returns response with citations)
  - `POST /api/feedback` - User feedback submission (thumbs up/down, rating)
  - `GET /api/health` - Health check for monitoring
  - `GET /api/stats` - (Optional) Analytics dashboard data

**RAG Implementation:**
- **LangChain** - RAG framework for document retrieval and question-answering
  - Document loading and chunking (RecursiveCharacterTextSplitter)
  - Vector store integration (ChromaDB)
  - Retrieval chain with similarity search
  - Prompt templates for Norwegian context

**Document Processing:**
- **Beautiful Soup 4** + **requests** - Web scraping for docs.hmsreg.com
- **Markdown/HTML parsing** - Extract clean text from documentation pages
- **Chunking strategy** - 500-1000 character chunks with 100-character overlap

**Data Collection Strategy for docs.hmsreg.com:**

This outlines the detailed approach for collecting, processing, and maintaining HMSREG documentation.

1. **Source Access Verification (Week 1)**
   - **Check robots.txt**: Verify `https://docs.hmsreg.com/robots.txt` for crawling permissions
   - **Review Terms of Service**: Ensure documentation scraping is permitted for educational purposes
   - **Test page loading**: Identify if pages are static HTML or JavaScript-rendered (SPA)
   - **Contact HMSREG**: If unclear, request permission to use documentation for chatbot training

2. **Documentation Priority List**

   Focus on high-value sections that address user stories:
   - **Getting Started Guide** - New user onboarding, account setup
   - **Workforce Registration** - How to register employees, required fields
   - **HMS Cards** - Validity requirements, renewal process, troubleshooting
   - **Documentation Requirements** - What documents are needed, upload procedures
   - **Check-in/Out Procedures** - App usage, QR codes, troubleshooting failed check-ins
   - **Compliance & Regulations** - Construction Client Regulations, seriøsitetskontroll
   - **FAQ Section** - Common questions and answers
   - **API Documentation** (if available) - For potential future integration

3. **Scraping Tools and Approach**

   **Primary Method: Beautiful Soup + requests (for static HTML)**
   ```python
   # Week 1 implementation
   import requests
   from bs4 import BeautifulSoup

   def scrape_hmsreg_docs():
       base_url = "https://docs.hmsreg.com"
       pages = ["/getting-started", "/workforce", "/hms-cards", ...]

       for page in pages:
           response = requests.get(base_url + page)
           soup = BeautifulSoup(response.text, 'html.parser')
           # Extract main content, ignore navigation/footer
           content = soup.find('main') or soup.find('article')
           # Save to structured format (JSON/Markdown)
   ```

   **Fallback Method: Playwright (for JavaScript-heavy pages)**
   ```python
   # If pages require JavaScript rendering
   from playwright.sync_api import sync_playwright

   def scrape_with_playwright():
       with sync_playwright() as p:
           browser = p.chromium.launch()
           page = browser.new_page()
           page.goto("https://docs.hmsreg.com")
           # Wait for content to load, then extract
   ```

   **Backup Plan: Manual Collection**
   - If scraping is blocked or impractical: Manually copy-paste key documentation
   - Save as structured Markdown files in `data/hmsreg_docs/` directory
   - Prioritize 10-20 most critical pages covering all user stories

4. **Document Processing Pipeline**

   **Step 1: Extract and Clean (Week 1)**
   - Remove navigation menus, footers, sidebars, cookie banners
   - Extract main content area only
   - Preserve headings, links, code blocks (if any)
   - Convert HTML to Markdown for readability

   **Step 2: Structure and Metadata (Week 1)**
   - Tag each document with topic category:
     - `workforce_registration`, `hms_cards`, `check_in`, `compliance`, `troubleshooting`, etc.
   - Store metadata: source URL, last updated date, language (Norwegian/English)
   - Create document hierarchy (parent topics, sub-topics)

   **Step 3: Chunking for Embeddings (Week 2)**
   - Use LangChain's `RecursiveCharacterTextSplitter`
   - **Chunk size**: 500-1000 characters (balance between context and precision)
   - **Overlap**: 100-200 characters (ensure continuity across chunks)
   - **Splitting logic**: Split on paragraphs first, then sentences, then characters
   - Preserve heading context in each chunk (e.g., prepend "HMS Cards > Validity:" to chunks)

   **Step 4: Quality Check**
   - Manually review 10-20 sample chunks to ensure quality
   - Verify that chunks contain coherent information
   - Check that Norwegian characters (æ, ø, å) are preserved correctly

5. **Update Strategy**

   **During Development (Weeks 1-6)**
   - Documentation snapshot taken in Week 1 is used throughout development
   - No automatic updates during project to maintain consistency

   **Post-Deployment (Future)**
   - **Manual updates**: Re-run scraper monthly to capture documentation changes
   - **Change detection**: Compare new content with existing chunks, identify diffs
   - **Re-embedding**: Only re-embed changed/new content to minimize API costs
   - **Versioning**: Keep old documentation versions for 30 days to handle rollback

   **Monitoring for Staleness**
   - If users report outdated information, flag for documentation refresh
   - Track "documentation last updated" date in analytics dashboard

6. **Backup and Disaster Recovery**

   - **Local backup**: Save all scraped HTML/Markdown in `data/raw_docs/` directory
   - **Version control**: Commit processed documentation to Git repository
   - **ChromaDB backup**: Export embeddings weekly using `chromadb.dump()` feature
   - **Redundancy**: Store documentation on both local development machine and cloud (GitHub)

   **If Scraping Fails:**
   - Use cached documentation from previous scrape (if available)
   - Manually collect 20-30 most important pages (2-4 hours manual work)
   - Contact HMSREG for documentation export (PDF/API access)
   - Use public FAQ sections as minimum viable knowledge base

7. **Estimated Documentation Size**

   - **Pages**: 50-200 documentation pages (estimated)
   - **Total text**: ~100,000 - 500,000 words
   - **Chunks**: 500-2000 chunks after splitting
   - **Embeddings**: 500-2000 vectors (1536 dimensions each)
   - **Storage**: ~50-200 MB for ChromaDB (including metadata)
   - **One-time embedding cost**: $0.50 - $2.00 (OpenAI text-embedding-3-small)

8. **Documentation Coverage Validation**

   Create a checklist to ensure all user story topics are covered:
   - [ ] Workforce registration procedures (User Story 1)
   - [ ] Compliance audit requirements (User Story 1)
   - [ ] Check-in failure troubleshooting (User Story 2)
   - [ ] Competence certification verification (User Story 3)
   - [ ] Supplier compliance requirements (User Story 3)
   - [ ] HMS card management and crew lists (User Story 5)
   - [ ] Common support questions (User Story 4)

   **If gaps identified**: Supplement with external sources or create synthetic FAQ from requirements

**Additional Libraries:**
- **python-dotenv** - Environment variable management
- **pydantic** - Data validation for API requests/responses
- **uvicorn** - ASGI server for FastAPI

### Database Architecture

**Vector Database (Document Embeddings):**
- **ChromaDB** (Development & Production)
  - **Free and open-source** - No API costs, runs locally or in Docker
  - **Persistent storage** - Saves embeddings to disk
  - **Fast similarity search** - Cosine similarity for semantic retrieval
  - **Collections** - `hmsreg_docs` collection for all documentation chunks

**Relational Database (Structured Data):**
- **PostgreSQL** - Robust relational database
  - **Free tier** - Railway, Supabase, or Neon (1GB storage)
  - **Schema design:**
    ```
    conversations
    ├── id (UUID, primary key)
    ├── session_id (VARCHAR, indexed)
    ├── user_message (TEXT)
    ├── bot_response (TEXT)
    ├── timestamp (TIMESTAMP)
    ├── response_time_ms (INTEGER)
    └── sources_cited (JSONB)

    feedback
    ├── id (UUID, primary key)
    ├── conversation_id (UUID, foreign key)
    ├── rating (INTEGER, 1-5)
    ├── helpful (BOOLEAN)
    ├── comment (TEXT, optional)
    └── timestamp (TIMESTAMP)

    analytics
    ├── id (UUID, primary key)
    ├── topic (VARCHAR)
    ├── question_count (INTEGER)
    ├── avg_satisfaction (DECIMAL)
    └── last_updated (TIMESTAMP)
    ```

**Alternative (Simpler for MVP):**
- **SQLite** - File-based database for rapid prototyping
  - No separate server needed
  - Easy migration to PostgreSQL later

### AI Integration Specification

**Development (Free Tier):**
- **Gemini CLI** - Free tier for development and testing
- **Claude Pro** - Subscription-based access for AI-assisted coding

**Production (API-based):**
- **OpenAI API** - Pay-per-use for deployed chatbot
  - **LLM**: GPT-5-mini (pricing estimated ~$0.60-0.80 per 1M input tokens, ~$2.50-3.50 per 1M output tokens based on GPT-5 being ~50% cheaper than GPT-4o)
  - **Embeddings**: text-embedding-3-small ($0.020 per 1M tokens)
  - **Estimated cost**: ~$8-20/month for moderate usage (100-500 conversations/month)
  - **Benefits**: 45% fewer factual errors than GPT-4o, improved reasoning (94.6% on AIME 2025), better Norwegian language support

**RAG Architecture:**
- **Embedding Model**: text-embedding-3-small (1536 dimensions)
  - Excellent Norwegian language support
  - Cost-effective for production
- **Retrieval Strategy**:
  - Top-k similarity search (k=3-5 most relevant chunks)
  - Minimum similarity threshold: 0.7 (configurable)
  - Context window: ~8000 tokens for GPT-5-mini (improved from previous models)
- **Prompt Engineering**:
  ```
  System: Du er en hjelpsom assistent for HMSREG-dokumentasjon...
  Context: [Retrieved documentation chunks]
  User Question: [User's question]
  Instructions: Svar på norsk, bruk kun informasjon fra konteksten...
  ```

**Fallback Strategy:**

The chatbot implements a multi-level fallback mechanism to handle cases where it cannot provide accurate answers:

1. **Confidence Threshold Detection**
   - **Similarity score < 0.7**: Trigger fallback (configurable threshold)
   - Calculate confidence based on vector similarity between query and retrieved chunks
   - If top-3 chunks all score < 0.7, chatbot admits it doesn't know

2. **Fallback Response Template**
   ```
   "Jeg fant ikke et klart svar i dokumentasjonen for dette spørsmålet.
   Her er noen ressurser som kan hjelpe:

   📚 Relevant dokumentasjon:
   - [Link til nærmeste dokumentasjonsseksjon]
   - [Alternative relaterte emner]

   💬 Kontakt support:
   - E-post: support@hmsreg.no
   - Telefon: [support number]
   - Dokumentasjon: https://docs.hmsreg.com

   💡 Tips: Prøv å omformulere spørsmålet ditt eller spør om spesifikke emner som
   'HMS-kort gyldighet' eller 'registrering av mannskap'."
   ```

3. **"Did You Mean?" Suggestions**
   - When query is unclear, suggest related topics from documentation
   - Example: Query "check-in problem" → Suggest "Check-in procedures", "HMS card errors", "App troubleshooting"
   - Use semantic similarity to find 3 most related topics

4. **Error States and Handling**
   - **OpenAI API timeout (>30s)**: "Systemet tar lengre tid enn vanlig. Vennligst prøv igjen."
   - **OpenAI API failure (500 error)**: "Chatboten er midlertidig utilgjengelig. Kontakt support@hmsreg.no for hjelp."
   - **Rate limit exceeded**: "For mange forespørsler. Vennligst vent et øyeblikk og prøv igjen."
   - **ChromaDB connection error**: Serve cached responses or gracefully inform user of technical issue
   - **Network timeout**: Retry once, then show error message with offline fallback instructions

5. **Escalation Path**
   - All fallback-triggered conversations logged with high priority
   - Analytics dashboard highlights frequently failed queries
   - Weekly review of unresolved questions to improve documentation coverage
   - Option to "Request human support" button that sends query to support team

6. **Search Suggestions on Zero Results**
   - If no chunks match query (even with low threshold), suggest:
     - "Kan du spesifisere hvilken del av HMSREG du trenger hjelp med?"
     - Show common topic categories: "Mannskapsregistrering", "HMS-kort", "Dokumentasjon", "Inn-/utsjekking"

**Norwegian Language Handling:**
- **Model selection**: GPT-5-mini has enhanced Norwegian support with improved multilingual capabilities (Bokmål and Nynorsk)
- **Prompt language**: System prompts and instructions in Norwegian
- **Terminology**: Custom glossary for HMSREG-specific terms (HMS-kort, seriøsitetskontroll, etc.)

### Deployment and Hosting

**Frontend Hosting:**
- **Vercel** (Free tier)
  - Automatic deployments from Git
  - Edge network for fast global access
  - Custom domain support
  - Alternative: Netlify, GitHub Pages

**Backend Hosting:**
- **Railway** (Free tier: 500 hours/month, $5/month after)
  - One-click PostgreSQL + Python deployment
  - Automatic HTTPS
  - Environment variable management
  - Alternative: Render, Fly.io

**Database Hosting:**
- **ChromaDB**: Deployed with backend (Docker container or local persistence)
- **PostgreSQL**: Railway built-in database or Supabase free tier

**Environment Variables:**
```
OPENAI_API_KEY=sk-...
DATABASE_URL=postgresql://...
CHROMA_PERSIST_DIRECTORY=/data/chroma
CORS_ORIGINS=https://chatbot.example.com
```

**CI/CD:**
- **GitHub Actions** (optional)
  - Automated testing on pull requests
  - Automated deployment to production on main branch merge

**Monitoring:**
- **Railway logs** - Basic error tracking and performance monitoring
- **Custom analytics** - Track API usage and costs in PostgreSQL

### Cost Estimation

**Development Phase (6 weeks):**
- **Gemini CLI**: Free tier (unlimited for development)
- **Claude Pro**: $20/month (for AI-assisted coding)
- **Total development cost**: ~$20

**Production Phase (Monthly):**
- **OpenAI API**: $5-15/month (estimated 100-500 conversations)
  - Assuming avg 500 tokens/query × 300 queries = ~$2-5/month
  - Embeddings for documentation: One-time ~$0.50 for 50,000 tokens
- **Railway hosting**: Free tier initially, $5/month if usage exceeds free limits
- **Domain (optional)**: $12/year (~$1/month)
- **Total monthly cost**: $5-20/month

### Technology Justification

**Why These Choices:**
1. **React + TypeScript**: Industry standard, excellent AI coding assistant support, strong ecosystem
2. **FastAPI**: Best Python framework for AI/ML integration, async support, automatic API docs
3. **LangChain**: De facto standard for RAG applications, extensive documentation, active community
4. **ChromaDB**: Free, easy to set up, perfect for course project scale (<10k documents)
5. **OpenAI GPT-4o-mini**: Best Norwegian language support, reliable API, cost-effective for production
6. **PostgreSQL**: Industry standard, free tiers available, easy migration from SQLite

**Alternatives Considered:**
- ~~Next.js~~ - Adds SSR complexity not needed for chat UI
- ~~LlamaIndex~~ - Similar to LangChain but less mature documentation
- ~~Pinecone~~ - Paid vector DB, unnecessary cost for project scale
- ~~Anthropic Claude API~~ - More expensive than GPT-4o-mini, similar Norwegian support

## Development Timeline and Milestones

This section outlines the 6-week development plan (approximately 1.5 months) with weekly milestones, deliverables, and key tasks.

### Week 1: Environment Setup and Data Collection

**Goals:**
- Set up development environment and project structure
- Collect and process HMSREG documentation
- Initialize version control and project repositories

**Tasks:**
- [ ] Create GitHub repository with initial project structure
- [ ] Set up Python virtual environment (Python 3.11+)
- [ ] Initialize React + Vite frontend project with TypeScript
- [ ] Install core dependencies (FastAPI, LangChain, React, Tailwind CSS)
- [ ] Scrape/download documentation from docs.hmsreg.com
  - Identify key documentation sections (Getting Started, HMS Cards, Check-in Procedures, etc.)
  - Use Beautiful Soup + requests to extract content
  - Parse HTML to clean text format
- [ ] Create initial document collection (save as JSON/markdown files)
- [ ] Set up ChromaDB locally with test data
- [ ] Configure environment variables (.env files)

**Deliverables:**
- Working development environment (frontend + backend)
- Complete HMSREG documentation dataset (50-200 pages)
- Initial ChromaDB collection with sample embeddings
- Project README with setup instructions

**Risks & Contingencies:**
- **Risk**: docs.hmsreg.com may block scraping or have JavaScript-heavy pages
  - **Mitigation**: Use Playwright for JavaScript rendering, or manually collect key documentation as backup
- **Risk**: Documentation may be larger than expected
  - **Mitigation**: Prioritize core user stories (workforce registration, HMS cards, check-in) for MVP

### Week 2: Backend API and RAG Pipeline

**Goals:**
- Build core RAG (Retrieval-Augmented Generation) pipeline
- Implement basic FastAPI backend with chat endpoint
- Process and embed all documentation

**Tasks:**
- [ ] Implement document chunking strategy (RecursiveCharacterTextSplitter, 500-1000 chars)
- [ ] Generate embeddings for all documentation chunks using OpenAI text-embedding-3-small
- [ ] Store embeddings in ChromaDB with metadata (source page, topic category)
- [ ] Create FastAPI application structure
  - `POST /api/chat` endpoint (accept user message, return bot response)
  - `GET /api/health` endpoint
- [ ] Implement LangChain RAG chain
  - Vector similarity search (top-k=3-5 chunks)
  - Prompt template with Norwegian instructions
  - Integration with OpenAI GPT-4o-mini (or Gemini for testing)
- [ ] Test retrieval accuracy with sample questions
- [ ] Implement basic error handling and logging

**Deliverables:**
- Working FastAPI backend with `/api/chat` endpoint
- Fully populated ChromaDB vector store (all HMSREG docs embedded)
- RAG pipeline returning relevant answers to test questions
- API documentation (auto-generated by FastAPI)

**Risks & Contingencies:**
- **Risk**: Embedding costs may be higher than expected
  - **Mitigation**: Use Gemini free tier for development, only switch to OpenAI for final testing
- **Risk**: Retrieval quality may be poor initially
  - **Mitigation**: Iterate on chunk size, overlap, and similarity threshold

### Week 3: Frontend Chat Interface and Integration

**Goals:**
- Build responsive chat UI
- Connect frontend to backend API
- Implement streaming responses and conversation state

**Tasks:**
- [ ] Create React components:
  - ChatWindow (main container)
  - MessageList (displays conversation history)
  - MessageInput (user input field with send button)
  - MessageBubble (individual message component)
- [ ] Style with Tailwind CSS and shadcn/ui components
- [ ] Implement React Context API for conversation state
- [ ] Connect frontend to backend `/api/chat` endpoint
  - Use fetch or axios for API calls
  - Implement Server-Sent Events (SSE) for streaming (optional for MVP)
- [ ] Add loading states and error messages
- [ ] Implement localStorage for session persistence (optional)
- [ ] Test end-to-end flow: user question → API call → response display

**Deliverables:**
- Functional chat interface with message history
- Frontend-backend integration working
- Responsive design (mobile breakpoints tested)
- User can ask questions and receive answers

**Risks & Contingencies:**
- **Risk**: SSE streaming may be complex to implement
  - **Mitigation**: Start with simple request-response, add streaming in Week 5 if time permits
- **Risk**: UI/UX may need multiple iterations
  - **Mitigation**: Use shadcn/ui pre-built components to speed up development

### Week 4: Testing, Refinement, and Mobile Responsiveness

**Goals:**
- Test chatbot with representative questions from user stories
- Refine RAG pipeline for better accuracy
- Ensure mobile responsiveness for on-site workers

**Tasks:**
- [ ] Create test question set (50-100 questions covering all user stories)
  - Workforce registration questions
  - HMS card validity and renewal
  - Check-in/out troubleshooting
  - Documentation requirements
  - Compliance and regulations
- [ ] Evaluate chatbot responses:
  - Accuracy (does answer match documentation?)
  - Relevance (are retrieved chunks appropriate?)
  - Completeness (does answer fully address question?)
- [ ] Iterate on RAG pipeline:
  - Adjust similarity threshold (test 0.6, 0.7, 0.8)
  - Refine prompt engineering for Norwegian context
  - Add HMSREG-specific terminology to prompts
- [ ] Improve chunking strategy if needed
- [ ] Test mobile responsiveness:
  - Test on various screen sizes (320px, 375px, 768px)
  - Ensure touch-friendly UI elements
  - Optimize for slow connections
- [ ] Add Norwegian language handling:
  - Test with Norwegian Bokmål queries
  - Ensure responses are in Norwegian
  - Handle English technical terms appropriately

**Deliverables:**
- Test results documenting accuracy rate (target: ≥80%)
- Refined RAG pipeline with optimized parameters
- Mobile-responsive chat interface tested on multiple devices
- Norwegian language support verified

**Risks & Contingencies:**
- **Risk**: Accuracy may be below 80% target
  - **Mitigation**: Identify failing question types, improve documentation coverage or prompt engineering
- **Risk**: Mobile testing may reveal UI issues
  - **Mitigation**: Allocate extra time in Week 5 for mobile fixes

### Week 5: Fallback Handling, Feedback System, and Analytics

**Goals:**
- Implement fallback mechanism for low-confidence responses
- Add user feedback system (thumbs up/down, ratings)
- Set up analytics tracking and PostgreSQL database

**Tasks:**
- [ ] Implement confidence threshold logic:
  - If similarity score < 0.7, trigger fallback response
  - Fallback message: "I couldn't find a clear answer in the documentation. Here are some helpful resources: [links]"
  - Include HMSREG support contact information
- [ ] Add "Did you mean...?" suggestions for unclear queries
- [ ] Implement feedback system:
  - Add thumbs up/down buttons to each response
  - Create `POST /api/feedback` endpoint
  - Store feedback in database
- [ ] Set up PostgreSQL database:
  - Deploy on Railway or Supabase free tier
  - Create schema (conversations, feedback, analytics tables)
  - Implement database models with SQLAlchemy/Pydantic
- [ ] Log all conversations:
  - Store user messages, bot responses, timestamps
  - Record similarity scores and sources cited
  - Track response time
- [ ] Create basic analytics:
  - Count questions by topic category
  - Calculate average satisfaction rating
  - Identify most common unresolved queries
- [ ] Error handling improvements:
  - API timeout handling
  - Graceful degradation if OpenAI API fails
  - Rate limiting protection

**Deliverables:**
- Fallback mechanism working for low-confidence queries
- User feedback system integrated into chat UI
- PostgreSQL database deployed and storing conversation data
- Analytics tracking common questions and satisfaction

**Risks & Contingencies:**
- **Risk**: Database setup may take longer than expected
  - **Mitigation**: Start with SQLite for MVP, migrate to PostgreSQL in Week 6 if needed
- **Risk**: Analytics implementation may be complex
  - **Mitigation**: Focus on basic metrics (question count, avg rating), defer dashboard to optional extensions

### Week 6: Final Testing, Deployment, and Documentation

**Goals:**
- Deploy chatbot to production (Vercel + Railway)
- Conduct final testing and quality assurance
- Prepare project documentation and presentation

**Tasks:**
- [ ] Deploy frontend to Vercel:
  - Connect GitHub repository
  - Configure environment variables
  - Set up custom domain (optional)
- [ ] Deploy backend to Railway:
  - Configure Python + FastAPI deployment
  - Set up PostgreSQL database connection
  - Configure CORS for frontend domain
  - Mount ChromaDB persistent storage
- [ ] Final end-to-end testing:
  - Test all user stories (5 scenarios)
  - Verify mobile responsiveness in production
  - Test fallback scenarios
  - Verify feedback submission works
  - Check analytics data collection
- [ ] Performance testing:
  - Measure response time (<5 seconds target)
  - Test concurrent users (simulate 5-10 users)
  - Monitor API costs
- [ ] Documentation:
  - Update README with deployment URLs and usage instructions
  - Document API endpoints and request/response formats
  - Create user guide for chatbot (how to ask questions effectively)
  - Document known limitations and future improvements
- [ ] Prepare final presentation:
  - Demo script with example questions
  - Architecture diagram and tech stack overview
  - Test results and metrics (accuracy, satisfaction, response time)
  - Reflection on challenges and learnings

**Deliverables:**
- Live chatbot deployed and accessible via URL
- All success criteria met (80% accuracy, <5s response time, feedback working)
- Complete project documentation (README, API docs, user guide)
- Final presentation materials ready

**Risks & Contingencies:**
- **Risk**: Deployment issues may arise
  - **Mitigation**: Test deployment early in week, allocate buffer time for troubleshooting
- **Risk**: Success criteria may not be fully met
  - **Mitigation**: Document any gaps and explain mitigation strategies

### Milestone Summary

| Week | Key Milestone | Success Metric |
|------|---------------|----------------|
| 1 | Environment & Data Ready | HMSREG docs collected, ChromaDB initialized |
| 2 | Backend API Working | `/api/chat` endpoint returns relevant answers |
| 3 | Full-Stack Integration | User can chat with bot via web interface |
| 4 | Quality & Mobile Tested | ≥80% accuracy, mobile-responsive |
| 5 | Production-Ready Features | Feedback system, analytics, fallback working |
| 6 | Deployed & Documented | Live URL, all success criteria met |

### Risk Management

**Top Risks:**
1. **Documentation scraping complexity** - May require manual collection or alternative tools (Playwright)
2. **RAG accuracy below 80%** - May need iterative prompt engineering and chunking refinement
3. **Norwegian language quality** - GPT-4o-mini performance may vary; test thoroughly
4. **API cost overruns** - Use free tiers (Gemini) during development, monitor OpenAI usage closely
5. **Deployment challenges** - Test early, use well-documented platforms (Vercel, Railway)

**Mitigation Strategy:**
- Build MVP features first (Weeks 1-4), add nice-to-haves only if time permits
- Test continuously throughout development, not just at the end
- Use AI-assisted coding (Claude Pro, GitHub Copilot) to accelerate development
- Maintain buffer time in Week 6 for unexpected issues

## Testing Strategy and Evaluation

This section defines the comprehensive approach to testing the chatbot and validating that it meets the 80% accuracy target and other success criteria.

### Test Question Set Development

**Creation Timeline:** Week 3-4

**Structure:**
Create 50-100 representative test questions covering all user stories and documentation topics.

**Question Categories:**

1. **Workforce Registration (15-20 questions)**
   - "Hvordan registrerer jeg mannskap i HMSREG?"
   - "Hvilke opplysninger trengs for å registrere en ansatt?"
   - "Hva gjør jeg hvis registreringen feiler?"
   - "Hvordan oppdaterer jeg informasjon om registrerte arbeidere?"
   - Mix of basic and complex questions

2. **HMS Cards (15-20 questions)**
   - "Hvor lenge er et HMS-kort gyldig?"
   - "Hvordan fornyer jeg et HMS-kort?"
   - "Hva betyr det hvis HMS-kortet er utløpt?"
   - "Hvor finner jeg HMS-kortnummeret?"
   - Include troubleshooting scenarios

3. **Check-in/Out Procedures (10-15 questions)**
   - "Hvorfor feiler innsjekkingen min?"
   - "Hvordan sjekker jeg inn på en byggeplass?"
   - "Kan jeg sjekke inn uten HMS-kort?"
   - "Hva gjør jeg hvis appen ikke fungerer?"
   - Focus on common failure cases

4. **Documentation Requirements (10-15 questions)**
   - "Hvilke dokumenter må jeg laste opp?"
   - "Hva er kravene for å være en seriøs leverandør?"
   - "Hvordan laster jeg opp sertifikater?"
   - "Hvilke kompetansebevis kreves?"

5. **Compliance and Regulations (10-15 questions)**
   - "Hva er byggherreforskriften?"
   - "Hvilke kontraktskrav gjelder for leverandører?"
   - "Hvordan verifiserer jeg at personell har riktig kompetanse?"

6. **Edge Cases and Ambiguous Queries (5-10 questions)**
   - "HMS" (ambiguous single word)
   - "Hjelp med innsjekking" (vague request)
   - "Jeg får feilmelding" (missing context)
   - Test fallback mechanism

**Question Diversity:**
- **Language**: 70% Norwegian Bokmål, 30% English (test bilingual support)
- **Complexity**: 50% simple/direct, 30% medium, 20% complex multi-part
- **Phrasing**: Vary phrasing for same question to test semantic understanding

### Evaluation Metrics

**Primary Metrics (aligned with Success Criteria):**

1. **Accuracy Rate (Target: ≥80%)**
   - **Definition**: Percentage of questions answered correctly and completely
   - **Scoring**:
     - ✅ **Correct (1 point)**: Answer matches documentation, fully addresses question
     - ⚠️ **Partial (0.5 points)**: Answer is relevant but incomplete or imprecise
     - ❌ **Incorrect (0 points)**: Answer is wrong, misleading, or completely off-topic
     - ➖ **No answer (0 points)**: Fallback triggered appropriately
   - **Calculation**: (Correct + 0.5×Partial) / Total Questions × 100%

2. **Relevance Score**
   - Are retrieved document chunks actually relevant to the question?
   - Manual review of top-3 retrieved chunks for 20 sample questions
   - Target: ≥90% of retrieved chunks are relevant

3. **Completeness Score**
   - Does the answer fully address all aspects of the question?
   - Target: ≥75% of answers are complete (not partial)

4. **Response Time (Target: <5 seconds)**
   - Measured from API request to complete response
   - Test under normal load (1 concurrent user) and stress (5-10 concurrent users)

5. **Fallback Accuracy**
   - For ambiguous/out-of-scope questions, does fallback trigger appropriately?
   - Target: 90% appropriate fallback activation (no false positives/negatives)

**Secondary Metrics:**

6. **Source Citation Quality**
   - Do cited sources actually support the answer?
   - Manual check for 20 responses

7. **Norwegian Language Quality**
   - Grammar, spelling, natural phrasing in Norwegian responses
   - Native speaker review for 10-15 responses

8. **Consistency**
   - Same question asked 3 times yields similar answers
   - Test 10 questions for consistency

### Testing Methodology

**Phase 1: Automated Testing (Week 4)**

1. **Create Test Suite**
   - Store test questions in JSON format with expected answer topics
   - Example:
   ```json
   {
     "question": "Hvordan registrerer jeg mannskap?",
     "expected_topics": ["workforce_registration", "employee_data", "process_steps"],
     "language": "no",
     "difficulty": "easy"
   }
   ```

2. **Run Batch Evaluation**
   - Script to send all test questions to chatbot API
   - Record responses, similarity scores, sources, response times
   - Save to CSV for analysis

3. **Automated Scoring (where possible)**
   - Check if expected topics appear in response
   - Measure response time automatically
   - Flag responses below 0.7 similarity for manual review

**Phase 2: Manual Evaluation (Week 4)**

1. **Human Review Process**
   - Two reviewers (ideally including Norwegian speaker) independently score responses
   - Use standardized rubric (Correct/Partial/Incorrect)
   - Resolve disagreements through discussion
   - Time investment: 3-5 hours

2. **Scoring Criteria**
   - **Correct**: Answer directly addresses question with accurate information from docs
   - **Partial**: Answer is relevant but missing key details or has minor inaccuracies
   - **Incorrect**: Answer is wrong, misleading, or doesn't address the question

3. **Document Findings**
   - Create spreadsheet with:
     - Question | Response | Score | Issues | Suggested Fix
   - Categorize failure types: retrieval failure, LLM hallucination, ambiguous query, missing docs

**Phase 3: Iterative Refinement (Week 4-5)**

Based on test results, iterate on:

1. **If accuracy < 80%:**
   - **Retrieval issues**: Adjust chunk size, overlap, or similarity threshold
   - **Prompt issues**: Refine system prompt, add more Norwegian context
   - **Documentation gaps**: Add missing information or synthetic FAQ entries
   - **LLM hallucination**: Strengthen "use only provided context" instruction

2. **If response time > 5s:**
   - Optimize vector search (reduce k value)
   - Use GPT-4o-mini instead of GPT-4 (faster)
   - Implement caching for common questions
   - Consider async processing

3. **If fallback issues:**
   - Adjust similarity threshold (test 0.6, 0.65, 0.7, 0.75)
   - Improve fallback message clarity
   - Add more "did you mean?" suggestions

**Iteration Cycle:**
1. Run test suite → 2. Analyze failures → 3. Make improvements → 4. Re-test → Repeat until 80% target met

**Target:** 2-3 iteration cycles in Week 4

### User Testing Plan

**Timeline:** Week 5-6

**Recruitment (Optional but Recommended):**
- Recruit 3-5 users from target groups:
  - 1-2 suppliers/subcontractors
  - 1 construction worker
  - 1 project manager
  - 1 support/admin personnel
- Incentive: Free access to tool, acknowledgment in project

**Testing Protocol:**

1. **Brief Introduction (5 min)**
   - Explain chatbot purpose and how to use it
   - Emphasize honest feedback

2. **Task-Based Scenarios (15 min)**
   - Give users 5-7 realistic scenarios from their role:
     - "You need to register a new employee. Ask the chatbot how."
     - "Your HMS card is expiring soon. Find out how to renew it."
     - "A worker's check-in failed. Troubleshoot the issue."
   - Observe: Do they get useful answers? Do they trust the bot?

3. **Free Exploration (10 min)**
   - Let users ask any HMSREG questions they have
   - Note: Questions that chatbot struggles with

4. **Feedback Survey (5 min)**
   - Rate satisfaction (1-5 scale)
   - Would you use this tool in real work? (Yes/No/Maybe)
   - What did you like? What frustrated you?
   - Suggestions for improvement

5. **Debrief Interview (10 min)**
   - What questions did the chatbot answer well?
   - What questions did it fail on?
   - How does this compare to searching docs.hmsreg.com manually?

**Data Collection:**
- Record all user questions and chatbot responses
- Note verbal reactions and observations
- Collect satisfaction scores and qualitative feedback
- Identify common pain points

**Analysis:**
- Calculate user satisfaction average (target: ≥4/5)
- Identify top 3-5 improvement opportunities
- Prioritize fixes for Week 6 if time permits

**If user testing not feasible:**
- Simulate user scenarios internally with colleagues
- Focus on automated testing and manual review

### Feedback Loop and Continuous Improvement

**During Development:**
- Weekly testing every Friday (Weeks 3-6)
- Track accuracy improvement over time (graph Week 3: 60% → Week 4: 75% → Week 5: 85%)
- Document lessons learned in development log

**Post-Deployment:**
- Monitor user feedback (thumbs up/down, ratings)
- Weekly review of conversations flagged as "not helpful"
- Monthly analysis of most common unresolved questions
- Quarterly documentation refresh based on gap analysis

**Improvement Process:**
1. Collect failed queries (low satisfaction, fallback triggered)
2. Identify root cause (missing docs, poor retrieval, LLM issue)
3. Implement fix (add docs, adjust prompts, tune threshold)
4. Re-test with failed queries
5. Deploy updated version

**Metrics Dashboard (Optional):**
- Real-time accuracy rate (based on user feedback)
- Average response time
- Fallback trigger rate
- Top 10 most asked questions
- User satisfaction trend (weekly average)

### Acceptance Criteria for Launch

Before deploying to production (end of Week 6), verify:

- ✅ **Accuracy**: ≥80% on test question set (minimum 80/100 questions correct/partial)
- ✅ **Response time**: <5 seconds for 95% of queries
- ✅ **Fallback**: Triggers appropriately for ambiguous/out-of-scope questions
- ✅ **Norwegian**: Responses are grammatically correct and natural
- ✅ **Mobile**: Works on mobile devices (320px width)
- ✅ **Feedback system**: Users can rate responses
- ✅ **Error handling**: Graceful degradation on API failures
- ✅ **User testing** (if conducted): ≥4/5 average satisfaction

**If criteria not met:**
- Document gaps and known issues
- Create prioritized roadmap for post-launch improvements
- Set realistic expectations with stakeholders

## Success Criteria

-   The chatbot provides accurate and helpful answers to at least 80% of HMSREG documentation questions
-   User satisfaction rating of 4/5 or higher
-   Reduction in support ticket volume related to common HMSREG documentation questions
-   Average response time under 5 seconds for standard queries
-   Chatbot successfully identifies and escalates questions it cannot answer with appropriate fallback options
-   Analytics data identifies documentation gaps and frequently asked topics to improve HMSREG resources
