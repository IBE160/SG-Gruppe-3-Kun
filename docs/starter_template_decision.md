I found several starter options, but for this project, I recommend sticking to the official and standard "from scratch" initialization to ensure we have full control over the stack without unnecessary bloat.

**Recommendation:**
Use `create-next-app` directly, followed by manual `shadcn/ui` initialization. This matches our requirement for a clean, professional foundation.

**Command:**
```bash
npx create-next-app@latest frontend --typescript --tailwind --eslint --app --no-src-dir --import-alias "@/*"
```
*(We will execute this in the Implementation Phase, Epic 1)*

**Why this choice?**
1.  **Standard & Stable:** It's the official Next.js recommendation.
2.  **Clean:** No extra libraries we didn't ask for (like tRPC or Prisma if we want to add them manually later).
3.  **Shadcn Ready:** Perfect base for adding `shadcn/ui` immediately after.

**Shadcn Init Command (for reference):**
```bash
npx shadcn-ui@latest init
```
*(We will run this interactively to pick our style preferences defined in UX spec)*

**Alternatives considered:**
- **T3 Stack:** Great, but might include things we want to configure differently (like auth or db) since we have specific Supabase requirements.
- **Vercel AI SDK Starter:** Too specific, might lock us into patterns we want to design ourselves for the RAG pipeline.

This aligns with "boring technology" principles - standard tools, standard setup.