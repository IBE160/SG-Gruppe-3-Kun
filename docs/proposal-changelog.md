# Proposal Changes Log

**Date:** 2025-10-22
**Purpose:** Document all changes made to proposal.md

---

## Summary of Changes

| # | Change | Reason |
|---|--------|--------|
| 1 | React + Vite → Next.js 14 | Need static documentation pages alongside chat interface |
| 2 | GPT-4o-mini → GPT-5-mini | 45% fewer errors, better Norwegian support (released Aug 2025) |
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

### 2. AI Model: GPT-4o-mini → GPT-5-mini

**Before:** GPT-4o-mini ($0.150/$0.600 per 1M tokens)
**After:** GPT-5-mini (est. $0.60-0.80/$2.50-3.50 per 1M tokens)

**Why:**
- GPT-5 released August 7, 2025
- 45% fewer factual errors than GPT-4o
- Better reasoning (94.6% on AIME 2025)
- Enhanced Norwegian language support
- ~50% cheaper than GPT-5 standard

**Cost Impact:**
- Before: $5-15/month
- After: $8-20/month
- Increase justified by better accuracy and user experience

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
| AI Model | GPT-4o-mini | GPT-5-mini |
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
- Integrate GPT-5-mini
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
- OpenAI API: $8-20/month (was $5-15)
- Railway: Free/$5
- Supabase: Free
- Domain: ~$1
- **Total: $8-25/month** (was $5-20)

Cost increase of $3-5/month justified by 45% fewer errors and better Norwegian support.

---

## Justification Summary

**Next.js:** Required for static documentation pages + chat interface in single codebase

**GPT-5-mini:** Released in 2025, significantly better accuracy, worth slight cost increase

**Supabase:** Best option for managed PostgreSQL with Next.js, excellent free tier

**User Flow:** Better communication of system design than text-based stories

**Rate Limiting:** Essential for public chatbot to prevent abuse

**Static Files:** Pragmatic choice for 6-week timeline, can upgrade later

---

## Files Modified

- `proposal.md` - All sections updated
- `proposal-changelog.md` - This file (new)

---

**Changes Approved:** 2025-10-22
