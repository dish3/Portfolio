# System Architecture Overview — NOVA OS

## High-Level Topology

```
             EXTERNAL PLATFORMS
   GitHub (Auto)   LeetCode (Auto)   LinkedIn (Manual)
        │                 │                  │
        ▼                 ▼                  ▼
   ┌──────────────────────────────────────────────┐
   │         FastAPI INGESTION & SCHEDULER        │
   │  - GitHub Webhook HMAC & Actions Cron Poll   │
   │  - LeetCode Public GraphQL Poller            │
   │  - LinkedIn Caption Submission Endpoint      │
   └──────────────────────┬───────────────────────┘
                          │
                          ▼
   ┌──────────────────────────────────────────────┐
   │         GEMINI AI AGENTS (Flash/Flash-Lite)  │
   │  GitHub · Content · Portfolio · Resume ·     │
   │  Recruiter · Chatbot · Analytics             │
   └──────────────────────┬───────────────────────┘
                          │ (Draft proposals only)
                          ▼
   ┌──────────────────────────────────────────────┐
   │      APPROVAL QUEUE (pending_changes)        │
   │   "AI drafted an update — Approve/Edit?"    │
   └──────────────────────┬───────────────────────┘
                          │ (Human Approval)
                          ▼
   ┌──────────────────────────────────────────────┐
   │    KNOWLEDGE GRAPH (PostgreSQL + pgvector)   │
   │  Projects · Skills · Certificates · Resume   │
   └──────────────────────┬───────────────────────┘
                          │ (ISR Revalidation)
                          ▼
   ┌──────────────────────────────────────────────┐
   │     PUBLIC PORTFOLIO (Next.js 14 App Router) │
   │  Quiet Intelligence Theme · Story Sections   │
   │  Recruiter Mode · Dynamic Resume Downloader  │
   └──────────────────────────────────────────────┘
```

## Service Directory Mapping
- `apps/web`: Next.js 14 frontend and admin dashboard.
- `apps/api`: FastAPI backend, ingestion layer, and agent orchestrators.
- `packages/types`: Shared TypeScript definitions.
- `packages/config`: Shared theme tokens, constants, and configuration.
- `database/migrations`: PostgreSQL + pgvector schema scripts.
- `agents/prompts`: Markdown prompt contracts for all 7 Gemini agents.
