# ADR 0001: Architecture Foundations & Core Invariants

## Status
Accepted

## Date
2026-09-29

## Context
Project NOVA is an AI-managed personal Operating System whose public presentation is a 3D, story-driven portfolio. The system autonomously monitors external developer and professional platforms (GitHub, LeetCode, LinkedIn), synthesizes updates via Google Gemini AI agents, and manages a PostgreSQL + pgvector knowledge graph.

To ensure long-term stability, zero data corruption, predictable operation, and compliance with platform terms, five foundational architectural invariants were established for Phase 00.

---

## Decisions & Rationales

### 1. Why Frontend (`apps/web`) and Backend (`apps/api`) are Separated
- **Hosting Tier Optimization**: The frontend (Next.js 14) is deployed on Vercel's edge network for optimal global asset delivery, instant TTFB, and on-demand ISR. The backend (FastAPI) handles long-running ingestion, webhook verification, vector calculations, and LLM orchestration, deployed on Render.
- **Security Isolation**: Browser clients must never possess secrets (Gemini API keys, Supabase Service Role keys, GitHub App private keys, webhook HMAC secrets). Isolating the backend guarantees that secrets remain strictly in backend server environments.
- **Independent Scaling & Cold Start Decoupling**: On Render's free tier, the backend sleeps after inactivity. The public frontend continues serving cached, pre-rendered ISR pages instantly from Vercel edge nodes without incurring cold-start latency for standard portfolio visitors.

### 2. Why AI Agents Cannot Directly Modify Live Tables
- **Human-in-the-Loop Principle**: Autonomous models (even state-of-the-art LLMs) can hallucinate, fabricate metrics, or misinterpret minor commit messages as full feature launches.
- **Zero Silent Data Corruption**: If an agent directly mutated `projects`, `skills`, or `resume_versions`, correcting errors would require manual database surgery. By preventing direct writes, live portfolio tables represent verified, immutable truths.
- **Enforced via Service Layer**: Direct table access is blocked at the software boundary. Agents are provided only with a `propose_change()` service interface; only the `ApprovalService` has permission to write to live entities upon human confirmation.

### 3. Why `pending_changes` Exists
- **Auditable Proposal Queue**: Every agent proposal is stored in `pending_changes` with the generating agent's identity, the target entity, the proposed JSON diff, and a mandatory `ai_rationale`.
- **Review and Diff Editing**: The admin dashboard renders the proposed diff alongside the AI rationale. The owner can choose `approved`, `rejected`, or `edited_then_approved`.
- **Downstream Decoupling**: Rejections are non-destructive (simply marked `rejected`), leaving live data intact and preserving an audit log of agent suggestions.

### 4. Why Gemini is Isolated Behind a Service
- **Model Version Swapping & Fallbacks**: Wrapping all Gemini calls in a centralized service (`gemini_client.py`) allows model swapping (e.g., between `gemini-2.5-flash` and `gemini-2.5-flash-lite`) without altering agent domain logic.
- **Strict Free-Tier Cost Management**: Centralizing LLM invocation allows per-agent token metering, prompt template caching, and rate-limit backoff handling in one location.
- **Zero Client Exposure**: No client-side code interacts with Gemini directly, eliminating unauthorized prompt injection and key theft.

### 5. Why External Platforms are Accessed Through Connector Interfaces
- **Uniform Protocol Boundary**: By establishing a formal `Connector` protocol (`fetch() -> list[RawItem]`, `to_draft(item) -> DraftChange`), every external service is treated as an asynchronous producer of draft proposals.
- **Resilience to Upstream API Changes**: Unofficial or scraping-resistant platforms (e.g. LeetCode public GraphQL) can break without affecting the rest of the application. Upstream changes only require updating the concrete connector class.
- **Future Extensibility**: Future platforms (Kaggle, Devpost, Medium, Codeforces, Spotify) can be added as drop-in connector modules without altering approval queue logic or database schemas.
- **Scope Discipline (Exclusion of X/Twitter)**: Explicit connector boundaries ensure that platforms with unsustainable pricing models (such as X/Twitter after its February 2026 free API deprecation) are cleanly excluded from the system architecture.

---

## Consequences
- Requires an explicit approval step in the admin UI before external activity reflects on the public site.
- Development requires maintaining type synchronization across TypeScript and Python, satisfied via `@nova/types` and Pydantic schemas.
- Prevents accidental regressions and ensures $0/month maintenance cost on free-tier infrastructure.
