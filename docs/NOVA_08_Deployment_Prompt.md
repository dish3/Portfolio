# DEPLOYMENT PROMPT — paste into Claude Code

## Targets
- **Frontend (`apps/web`)** → Vercel (free Hobby tier)
- **Backend (`apps/api`)** → Render (free tier)
- **Database** → Supabase (Postgres + pgvector + Storage, free tier)
- **Scheduler** → GitHub Actions cron (free, no separate infra)

## 1. Environments
Set up `development`, `preview` (Vercel preview deployments + a shared staging backend on Render), and `production`.

## 2. Secrets Management
- Gemini API key, GitHub App credentials, Supabase service role key, internal poll shared-secret — all backend-only env vars, set in the Render dashboard, never in the frontend.
- Frontend only gets the public Supabase anon key (if used for any client-side reads) and the public backend API base URL.
- Document every required variable in `.env.example` files in both `apps/web` and `apps/api`.
- No X/Twitter credentials exist anywhere in this system — there is nothing to provision for it.

## 3. CI/CD (GitHub Actions)
- `ci.yml`: on every PR — lint, typecheck, run backend tests (mocked externals per automation doc §9), run frontend build.
- `deploy-web.yml`: Vercel auto-deploys on merge to `main` (standard Vercel GitHub integration — minimal extra config needed).
- `deploy-api.yml`: on merge to `main`, trigger Render's deploy via its GitHub integration (auto-deploy on push) or the Render CLI/Deploy Hook URL in the workflow.
- `scheduled-polls.yml`: cron-triggered workflow calling the backend's internal poll/digest endpoints (see automation doc §7) — this *is* your task scheduler, no separate service needed.
- Migration step: run Alembic/SQL migrations against Supabase as a required step before the API deploy completes, not after.

## 4. Revalidation Wiring
Backend's approval service (see backend prompt §4) must call `POST {VERCEL_DEPLOYMENT_URL}/api/revalidate?secret=...&path=/projects/:slug` after every approved change — confirm this endpoint exists in the frontend before wiring it here.

## 5. Domain & SEO
- Custom domain on Vercel, HTTPS automatic.
- `sitemap.xml` and `robots.txt` generated from the live project/blog list (regenerate on each approval, not just at build time).
- Open Graph images: generate per-project OG images server-side (Vercel `@vercel/og` or a backend-rendered image) so shared links to project pages look polished.

## 6. Monitoring
- Vercel Analytics (or Plausible/PostHog) for frontend visits feeding the `visits` table via a lightweight beacon endpoint.
- Backend error tracking (Sentry free tier) on the FastAPI app — agent failures should alert you, not fail silently into a stuck `pending_changes` row.
- Uptime check (e.g., a free UptimeRobot monitor) on the backend health endpoint — useful on Render's free tier specifically because it tells you when a cold start is about to be hit by a real visitor vs. just sitting asleep.

## 7. Cost Awareness
- Gemini calls: cap per-agent call frequency (already bounded by webhook/poll cadence) and log token usage per agent so costs are visible from day one. Default to Flash/Flash-Lite; Pro is not free-tier eligible.
- Render free tier: expect ~1 minute cold start after 15 minutes of inactivity on the backend. Acceptable for this project's traffic profile; upgrade to Starter ($7/mo) only if it becomes a real annoyance.
- Supabase free tier: set up the GitHub Actions keep-alive ping (per master spec §8) so the project doesn't pause after 7 days of inactivity.

If any hosting choice changes later, update this document — don't let deployment drift silently from what's written here.
