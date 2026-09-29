# SYSTEM ARCHITECTURE — NOVA

## 1. Services
| Service | Tech | Responsibility |
|---|---|---|
| `web` | Next.js 14 (App Router) + TypeScript | Public site, admin dashboard, API routes for light reads |
| `api` | FastAPI (Python) | Heavy lifting: ingestion, agents, embeddings, scheduled job logic |
| `db` | PostgreSQL + pgvector (Supabase) | Knowledge graph + vector search |
| `scheduler` | GitHub Actions (cron workflows) | Triggers scheduled polls (GitHub fallback, LeetCode) by calling backend endpoints on a schedule — free, no managed worker needed |
| `ai` | Gemini API (Google), Flash / Flash-Lite models | All generation: summaries, tags, resume text, chat answers |
| `storage` | Supabase Storage | Thumbnails, generated OG images, PDF resumes |

**Hosting decision: `web` → Vercel (free Hobby tier), `api` → Render (free tier).** Render's free web services sleep after inactivity and take ~1 min to wake on the next request — acceptable here since the chatbot is the only user-facing real-time path, and scheduled polls don't care about cold starts. If the chatbot's cold-start delay becomes annoying in practice, the fix later is Render's Starter tier ($7/mo), not a platform switch.

**No Celery/Redis.** GitHub Actions cron workflows call backend HTTP endpoints on a schedule (e.g. `POST /internal/poll/github`, `POST /internal/poll/leetcode`) instead of running a persistent task queue. This removes a whole paid-or-managed component for a personal-scale project. Revisit only if scheduled job volume grows enough to need true async fan-out.

## 2. Data Flow Per Source

### GitHub (fully automatic)
1. GitHub webhook (push, release, repo created) → `api/webhooks/github`.
2. Fallback: GitHub Actions cron hits a poll endpoint every 6h in case a webhook is missed.
3. GitHub Agent reads README, languages, topics, commit history → drafts a Project record (or diff against existing one).
4. Draft → Approval Queue.

### LeetCode (automatic)
1. GitHub Actions cron hits a poll endpoint every 12h, which calls LeetCode's public GraphQL endpoint (no auth needed for public profiles).
2. Stats stored as a time series (`leetcode_snapshots`) feeding the live stats widget — no approval needed for raw stats, only for narrative claims like "Top X% globally."

### LinkedIn (semi-automatic — explicit human step)
1. Admin dashboard has a single "New LinkedIn Post" input: paste URL and/or paste text/video link.
2. Backend fetches what's publicly fetchable from the URL (respecting LinkedIn's robots/ToS — if blocked, you paste the caption text manually).
3. Content Agent extracts: project name match, description, media link, date, tags.
4. Drafted Project update → Approval Queue.

### Drive / Demo links (manual, one-time)
1. When a Project has no public live-demo URL, the admin dashboard prompts: "No demo link found — paste one (Drive, YouTube, etc.)."
2. Stored permanently on the Project record; never asked again unless cleared.

### X / Twitter — out of scope
Not implemented anywhere in this system. X removed its free API tier in February 2026 (pay-per-use only, no free read access) — not worth the cost for a personal portfolio. If ever revisited, it would be handled exactly like LinkedIn: manual paste-link submission only, never an automatic poller. No connector, no agent trigger, no schema fields reference it.

## 3. Agent Responsibilities
See `NOVA_04_AI_Agents_Specification.md` for full prompt contracts. Summary:

| Agent | Trigger | Output |
|---|---|---|
| GitHub Agent | Webhook / poll | Draft Project create/update |
| Content Agent | LinkedIn/Drive submission | Draft Update card, extracted media/links |
| Portfolio Agent | Any approved change | Decides which sections/pages to regenerate |
| Resume Agent | Any approved Project/Skill/Cert change | Regenerates resume versions (SWE/AI/ML/Backend + ATS) |
| Recruiter Agent | Visitor enters Recruiter Mode | Selects top N projects/skills relevant to visitor |
| Chat Agent | Visitor chat message | RAG over knowledge graph + live fetch of linked GitHub/demo if asked |
| Analytics Agent | Nightly | Summarizes visitor stats into a digest |

## 4. Approval Queue (Core UX Decision)
Every agent writes to a `pending_changes` table, never directly to the live tables. The admin dashboard shows:
```
[New] GitHub: "authenfluence-ai" pushed v2.3
  AI Summary: "Added vector search to recommendation engine..."
  [ Approve & Publish ]  [ Edit ]  [ Reject ]
```
Approving copies the draft into the live `projects`/`updates`/`resume_versions` table and triggers a Next.js revalidation (ISR) so the public site updates without a redeploy.

## 5. Knowledge Graph Sync Strategy
- Every entity (Project, Skill, Certificate, Post, TimelineEvent) has an embedding stored in pgvector.
- On any approved change, re-embed the changed entity and its direct neighbors (e.g., a new Project re-embeds the Skills it references).
- Chat Agent and Recruiter Agent both query this vector index — single source of truth, no duplicate logic.

## 6. Security & Auth
- Admin dashboard behind your own auth (NextAuth/Supabase Auth) — single user (you).
- Public site fully open, read-only.
- Webhook endpoints verified via GitHub's HMAC signature.
- API keys (Gemini, GitHub) stored as backend env secrets only — never exposed to the `web` client.

## 7. Extensibility for Future Platforms
Build a `Connector` interface from day one:
```python
class Connector(Protocol):
    name: str
    def fetch(self) -> list[RawItem]: ...
    def to_draft(self, item: RawItem) -> DraftChange: ...
```
GitHub and LeetCode are concrete implementations now. Kaggle/Devpost/Medium/Hashnode/Codeforces/HackerRank/Spotify/Instagram become drop-in connectors later without touching the agent or approval-queue logic. X is deliberately not stubbed here — it's not a future connector, it's out of scope.
