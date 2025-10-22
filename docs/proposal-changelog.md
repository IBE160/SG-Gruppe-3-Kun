# Proposal Changes Log

**Date:** 2025-10-22
**Purpose:** Document all changes made to proposal.md

---

## Summary of Changes

| # | Change | Reason |
|---|--------|--------|
| 1 | React + Vite → Next.js 14 | Need static documentation pages alongside chat interface |
| 2 | GPT-4o-mini → GPT-5-mini → Gemini 2.5 Pro | Cost-effective, generous free tier, excellent Norwegian support |
| 3 | PostgreSQL → Supabase | Selected from options, better Next.js integration |
| 4 | User Stories → User Flow | Visual diagram showing interaction patterns |
| 5 | Added rate limiting | Abuse prevention (10/min, 50/hour per IP) |
| 6 | Added static content strategy | Markdown files in `/public/articles/` |

---

## Change Details

### 1. Frontend: React + Vite → Next.js 14

**Before:** React 18 + Vite
**After:** Next.js 14 (App Router)

**Why:**
- Project requires multiple static documentation pages (`/docs/workforce`, `/docs/hms-cards`, etc.)
- Next.js SSG ideal for pre-rendering docs at build time
- File-based routing simplifies multi-page structure
- Chatbot can reference static pages in responses

**Technical Impact:**
- Application structure: `/app/page.tsx`, `/app/chat/`, `/app/docs/`
- Static content in `/public/articles/`
- Deployment: Vercel (optimized for Next.js)

---

### 2. AI Model: GPT-4o-mini → GPT-5-mini → Gemini 2.5 Pro

**Before:** GPT-4o-mini ($0.150/$0.600 per 1M tokens), then GPT-5-mini
**After:** Gemini 2.5 Pro (Free tier: 15 RPM, 1500 RPD; Paid pricing TBD)

**Why:**
- Google Gemini 2.5 Pro offers state-of-the-art capabilities
- Generous free tier (1500 requests/day) - suitable for project scale
- Excellent multilingual support including Norwegian (Bokmål and Nynorsk)
- Large context window for comprehensive RAG
- Cost-effective: Free for moderate usage, competitive paid pricing
- LangChain has excellent Google AI integration

**Cost Impact:**
- Before: $8-20/month (GPT-5-mini)
- After: $0-15/month (likely free within tier limits)
- Significant cost savings while maintaining quality

---

### 3. Database: Specified Supabase for PostgreSQL

**Before:** "Railway, Supabase, or Neon" (options listed)
**After:** Supabase (selected)

**Why:**
- Generous free tier (500MB database, 50k MAU)
- Excellent Next.js integration (TypeScript SDK)
- Python client for FastAPI backend
- Built-in features: REST API, auth, real-time, storage

**Schema Updates:**
- Added `rate_limits` table for abuse prevention
- All tables use Supabase-hosted PostgreSQL

---

### 4. User Stories → User Flow Diagram

**Before:** 5 text-based user stories
**After:** Comprehensive visual flow diagram

**Why:**
- Better visualization of interaction patterns
- Shows technical flow (frontend → backend → RAG → response)
- Includes fallback scenarios
- Demonstrates all system features in context

**Primary Flow:** Construction worker troubleshooting check-in failure

---

### 5. Added Rate Limiting & Abuse Prevention

**New Feature:** Multi-layer protection strategy

**Implementation:**
- IP-based: 10 requests/minute, 50/hour (slowapi)
- Session tracking in Supabase
- Message length limit: 500 characters
- Cost monitoring dashboard

**Why:**
- Public chatbot vulnerable to API cost abuse
- Prevents spam and automated attacks
- Protects OpenAI API budget

---

### 6. Added Static Content Storage Strategy

**New Feature:** Documentation storage approach

**Implementation:**
- Markdown files in `/public/articles/`
- Images in `/public/images/`
- Served via Vercel CDN
- Version controlled in Git

**Why:**
- Faster to implement (6-week timeline)
- Free CDN delivery
- Chatbot can reference articles
- Can migrate to Supabase Storage later if needed

---

## Updated Technology Stack

| Component | Before | After |
|-----------|--------|-------|
| Frontend | React 18 + Vite | Next.js 14 (App Router) |
| AI Model | GPT-4o-mini | Gemini 2.5 Pro |
| Embeddings | OpenAI text-embedding-3-small | Google text-embedding-004 |
| Database | PostgreSQL (options) | Supabase (selected) |
| Rate Limiting | Not specified | slowapi + Supabase |
| Content Storage | Not specified | Static files in `/public/` |

---

## Timeline Adjustments

**Week 1:**
- Initialize Next.js (not React + Vite)
- Set up Supabase project
- Create `/app/` structure
- Save docs as Markdown in `/public/articles/`

**Week 2:**
- Implement rate limiting (slowapi)
- Integrate Gemini 2.5 Pro via LangChain
- Supabase Python client for logging

**Week 3:**
- Create Next.js pages (chat + static docs)
- Integrate Supabase client in frontend

**Week 5:**
- Verify Supabase production-ready
- Test rate limiting

---

## Cost Estimation Update

**Development:** ~$20 (unchanged)

**Production (Monthly):**
- Google AI API: $0-15/month (was $8-20 for GPT-5-mini)
- Railway: Free/$5
- Supabase: Free
- Domain: ~$1
- **Total: $0-20/month** (was $8-25 with GPT-5-mini)

Cost decrease of $8-5/month due to generous free tier while maintaining quality.

---

## Justification Summary

**Next.js:** Required for static documentation pages + chat interface in single codebase

**Gemini 2.5 Pro:** State-of-the-art model with generous free tier, excellent Norwegian support, cost-effective

**Supabase:** Best option for managed PostgreSQL with Next.js, excellent free tier

**User Flow:** Better communication of system design than text-based stories

**Rate Limiting:** Essential for public chatbot to prevent abuse

**Static Files:** Pragmatic choice for 6-week timeline, can upgrade later

---

## Files Modified

- `proposal.md` - All sections updated
- `proposal-changelog.md` - This file (new)

---

---

## Update: 2025-10-22 (Later)

**Change:** GPT-5-mini → Gemini 2.5 Pro

**Reason:**
- Better cost structure with generous free tier (1500 requests/day)
- Potentially free for entire project within API limits
- Excellent multilingual support for Norwegian
- Strong LangChain integration
- Large context window
- State-of-the-art reasoning capabilities

**Impact:**
- Monthly cost: $8-20 → $0-15 (potentially free)
- Embedding cost: $0.50 one-time → Free
- Better budget fit for course project
- No compromise on quality

---

**Changes Approved:** 2025-10-22
