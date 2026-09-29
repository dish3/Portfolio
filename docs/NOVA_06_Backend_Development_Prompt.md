# BACKEND DEVELOPMENT PROMPT — paste into Claude Code

You are building the backend for **NOVA**. Read `NOVA_00_Master_Specification.md`, `NOVA_01_System_Architecture.md`, `NOVA_02_Database_Design.md`, and `NOVA_04_AI_Agents_Specification.md` fully before writing code.

## Stack
- FastAPI (Python 3.12), Pydantic v2
- PostgreSQL via Supabase (pgvector extension) — use SQLAlchemy or a thin asyncpg layer, your choice, but keep models matching `NOVA_02_Database_Design.md` exactly
- **No Celery/Redis.** Scheduled work (GitHub poll fallback, LeetCode poll, nightly analytics digest) is triggered externally by GitHub Actions cron workflows calling dedicated backend endpoints (e.g. `POST /internal/poll/github`). Protect these endpoints with a shared secret header, not public auth.
- Gemini API for all agent generation calls (wrap every call in a single `gemini_client.py` so model/version is swappable later) — default to `gemini-2.5-flash` or `gemini-2.5-flash-lite`, never assume Pro-tier access is free.

## Build in this order
1. **DB models + migrations** exactly matching `NOVA_02_Database_Design.md`.
2. **Connector interface** (`Connector` protocol from architecture doc §7) + concrete `GitHubConnector`, `LeetCodeConnector`. Stub `LinkedInConnector` as the manual-submission endpoint, not a poller. **Do not build an X/Twitter connector — it is explicitly out of scope.**
3. **Agent implementations** for all 7 agents in `NOVA_04_AI_Agents_Specification.md`, each as its own module under `agents/`, each writing only to `pending_changes` — enforce this with a single `propose_change()` service function agents must call (no direct table writes from agent code).
4. **Approval service**: `approve_change(id)`, `reject_change(id)`, `edit_and_approve(id, patch)` — these are the only functions allowed to write to live tables (`projects`, `certificates`, `timeline_events`, `updates`, `resume_versions`). On approve, trigger re-embedding (pgvector) and call the frontend's `/api/revalidate`.
5. **Public read API**: `/projects`, `/projects/:slug`, `/skills`, `/timeline`, `/updates`, `/resume/:role`, `/chat` (streaming, RAG over embeddings + optional live fetch of a project's demo/repo when the Chat Agent decides it's needed).
6. **Admin API** (auth-protected, single user): CRUD for pending_changes review, connectors config, manual LinkedIn/Drive submission endpoints.
7. **Webhooks**: `/webhooks/github` with HMAC signature verification.
8. **Internal poll endpoints** for GitHub Actions to call: `/internal/poll/github`, `/internal/poll/leetcode`, `/internal/digest/nightly` — all behind a shared-secret header check.

## Hard requirements
- No agent or connector may write directly to a "live" table — only the Approval service may, and only on an approved row. Add a test that asserts this (e.g., a static check that agent modules never import the live-table write functions).
- All Gemini prompts live in versioned prompt template files (`prompts/*.md` or `.jinja`), not inlined as raw strings scattered through code — match the prompt contracts given in `NOVA_04_AI_Agents_Specification.md` verbatim as the starting point.
- Every agent output must include `ai_rationale`; reject any agent function that returns without one.
- Secrets (Gemini key, GitHub token, internal poll secret) only via environment variables, never committed, documented in `.env.example`.
- Confidence thresholds for fuzzy matching (Content Agent project-matching) must be explicit constants, not magic numbers buried in code.
- Build with Render's free-tier cold starts in mind: keep startup time fast (lazy-load heavy ML/embedding libs only on first use where possible) so the post-idle wake-up is as quick as it can be.

## Deliverables for this phase
- `apps/api` FastAPI project, deployable to Render (free tier) via render.yaml or the Render dashboard
- OpenAPI docs auto-generated and reachable at `/docs`
- Seed script to populate a few example projects/skills so the frontend team can develop against real-shaped data before connectors are live
- README documenting every environment variable and the local dev setup (docker-compose for Postgres is preferred for local dev only — production DB is Supabase)

If anything is ambiguous (confidence thresholds, exact polling cadence, which Gemini model per agent), state your assumption explicitly in the README rather than silently picking one with no record.
