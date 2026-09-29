# NOVA — AI-Managed Personal Portfolio Operating System

> An autonomous personal Operating System whose public presentation is a story-driven portfolio. NOVA continuously ingests data from GitHub, LeetCode, and LinkedIn (semi-auto), maintains a PostgreSQL + pgvector knowledge graph, and uses Gemini AI agents to propose — and on human approval, publish — updates to the live portfolio, resume, and project showcases.

---

## 1. Project Purpose & Principles
- **Zero manual upkeep**: The default workflow is "AI noticed a change → drafted an update → asked for approval."
- **Human-in-the-loop, not in-the-pipeline**: You approve or edit with one click; you never re-type content.
- **Strict Invariant**: AI agents write **only** to `pending_changes`. Live tables are mutated exclusively upon human approval.
- **Quiet Intelligence Aesthetic**: Dark observatory/lab visual language (`#0A0A0F` background, warm amber `#D9A857` accent, glassmorphic panels).
- **Free-Tier Architecture ($0/month)**: Next.js on Vercel, FastAPI on Render, Supabase (Postgres + pgvector), Google Gemini Flash API, and GitHub Actions cron schedulers. No Celery, no Redis.
- **Scope Discipline**: X / Twitter is permanently excluded from this project due to API paywalling.

---

## 2. Architecture Overview

```
             EXTERNAL PLATFORMS
   GitHub (Auto)   LeetCode (Auto)   LinkedIn (Manual)
        │                 │                  │
        ▼                 ▼                  ▼
   ┌──────────────────────────────────────────────┐
   │         FastAPI INGESTION & SCHEDULER        │
   │  - Webhook HMAC verify & Actions cron poll   │
   │  - LeetCode public GraphQL poller            │
   │  - LinkedIn caption submission endpoint      │
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

---

## 3. Monorepo Repository Structure

```text
ai-portfolio-os/
│
├── apps/
│   ├── web/                     # Next.js 14 App Router frontend & admin dashboard
│   └── api/                     # FastAPI backend, ingestion layer, and agent orchestrators
│
├── packages/
│   ├── types/                   # Shared TypeScript models and API interfaces
│   └── config/                  # Shared theme tokens, constants, and system config
│
├── database/
│   ├── migrations/              # PostgreSQL + pgvector schema migrations (001_initial_schema.sql)
│   └── seed/                    # Seed scripts for connectors and development
│
├── agents/
│   └── prompts/                 # Versioned prompt contracts for all 7 Gemini AI agents
│
├── docs/
│   ├── architecture/            # Architecture diagrams and system topologies
│   ├── database/                # Schema documentation and entity relationships
│   └── decisions/               # Architecture Decision Records (ADRs)
│
├── tests/
│   ├── api/                     # Pytest suite: health, config, schema, approval invariants
│   └── web/                     # Frontend component and route tests
│
├── .github/
│   └── workflows/
│       ├── ci.yml               # Automated CI for linting, typechecking, and testing
│       └── scheduled-polls.yml  # Cron workflow triggering scheduled platform polls
│
├── .env.example                 # Comprehensive master environment variables template
├── .gitignore                   # Ignore rules for secrets, dependencies, and build artifacts
├── README.md                    # Root project documentation
└── package.json                 # Monorepo workspaces definition
```

---

## 4. Prerequisites
- **Node.js**: `>= 20.0.0`
- **npm**: `>= 10.0.0`
- **Python**: `>= 3.11`
- **PostgreSQL**: PostgreSQL 15+ with `pgvector` extension (Supabase free tier recommended)
- **Git**: Git 2.30+

---

## 5. Installation & Setup

### Clone and Install Dependencies
```bash
# Clone the repository
git clone <repo-url>
cd ai-portfolio-os

# Install JavaScript/TypeScript dependencies across all workspaces
npm install

# Setup Python virtual environment for the backend
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# Install backend dependencies
pip install -r apps/api/requirements.txt
```

---

## 6. Environment Configuration
Copy `.env.example` to `.env` in the root (or configure individual `.env` files in `apps/web/` and `apps/api/`):

```bash
cp .env.example .env
```

Key variables:
- `DATABASE_URL`: PostgreSQL connection string with `pgvector` enabled.
- `GEMINI_API_KEY`: Google AI Studio API key (free tier).
- `ADMIN_API_KEY`: Secret key protecting administrative endpoints.
- `INTERNAL_POLL_SECRET`: Shared secret between GitHub Actions cron workflows and FastAPI.
- `NEXT_PUBLIC_API_URL`: Base URL for the FastAPI backend (defaults to `http://localhost:8000`).

---

## 7. Database Migration
Run the initial SQL migration on your PostgreSQL / Supabase database:

```bash
# Using psql or Supabase SQL Editor:
psql "$DATABASE_URL" -f database/migrations/001_initial_schema.sql

# Seed initial connector profiles:
psql "$DATABASE_URL" -f database/seed/seed.sql
```

---

## 8. Local Development

### Run Frontend (`apps/web`)
```bash
npm run dev --workspace=apps/web
# Opens on http://localhost:3000
# Admin Dashboard Shell: http://localhost:3000/admin
```

### Run Backend (`apps/api`)
```bash
cd apps/api
uvicorn app.main:app --reload --port 8000
# OpenAPI Docs: http://localhost:8000/docs
# Health Check: http://localhost:8000/health
```

---

## 9. Testing Foundation

### Backend Tests
```bash
pytest tests/api/ -v
```
Validates:
- `GET /health` returns `{"status": "ok"}`
- Configuration loading and environment fallbacks
- Schema integrity of SQLAlchemy models against `NOVA_02`
- Critical invariant: Live tables cannot be mutated directly without approved pending change
- Platform connector protocol conformance

### Frontend Checks
```bash
npm run typecheck --workspace=apps/web
npm run lint --workspace=apps/web
```

---

## 10. Continuous Integration (CI)
GitHub Actions workflow `.github/workflows/ci.yml` validates on every pull request and push to `main`:
1. **Frontend**: Workspace installation, ESLint linting, TypeScript typechecking, and production build.
2. **Backend**: Python dependencies installation, code linting with Ruff, and Pytest test execution.

---

## 11. Current Status & Phase Roadmap

### Current Status: **PHASE 00 (Foundation Scaffold) — COMPLETE**
- Monorepo structure established.
- Next.js 14 App Router frontend scaffold with under-construction landing page.
- Empty function-first Admin Dashboard shell (`/admin`) with "No pending changes" state.
- FastAPI backend scaffold with structured logging, CORS, configuration, and `/health`.
- PostgreSQL + `pgvector` migration (`001_initial_schema.sql`) matching `NOVA_02_Database_Design.md`.
- Authentication skeleton protecting `/admin/*` and API routes.
- Shared `@nova/types` and `@nova/config` packages.
- CI pipeline in `.github/workflows/ci.yml`.
- All 10 NOVA specifications, ADRs, AGENTS.md, and RUNBOOK.md indexed.

### Upcoming Phases (per Master Specification)
- **Phase 1**: GitHub Agent + Knowledge Graph + Project pages.
- **Phase 2**: Admin approval queue + manual LinkedIn/Drive link submission flow.
- **Phase 3**: 3D story-driven homepage + section pages + animations.
- **Phase 4**: AI Chatbot (RAG over knowledge graph) + Recruiter Mode.
- **Phase 5**: Resume Agent (multi-version, ATS, PDF export).
- **Phase 6**: LeetCode connector, Content Agent, Analytics Agent.
- **Phase 7**: Extensible connector framework for future platforms.
