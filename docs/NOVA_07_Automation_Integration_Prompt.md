# AUTOMATION & INTEGRATION PROMPT — paste into Claude Code

Builds on the backend from `NOVA_06_Backend_Development_Prompt.md`. Focus purely on making each platform connector real, correctly scoped, and resilient.

## 1. GitHub
- Use a GitHub App (not a personal token) so it can be scoped to specific repos and survives token rotation more gracefully; OAuth flow for you to install it on your own account.
- Webhook events to subscribe: `push`, `release`, `repository` (created).
- HMAC signature verification on every webhook request — reject anything unsigned.
- Poll fallback every 6h via a GitHub Actions cron workflow calling `POST /internal/poll/github`: list repos, compare `pushed_at` against `connectors.last_synced_at`.
- Rate-limit aware: back off on 403/secondary rate limit responses.

## 2. LeetCode
- Use LeetCode's public GraphQL endpoint for public profile stats (no login required for public data) — verify field availability at implementation time since LeetCode's unofficial API surface changes; build with a clear adapter boundary so a breaking change only requires editing `LeetCodeConnector`, nothing else.
- GitHub Actions cron calls `POST /internal/poll/leetcode` every 12h.
- Store every poll as a `leetcode_snapshots` row (time series) rather than overwriting — this is what powers the "Live Pulse" trend, not just a current number.

## 3. LinkedIn (explicitly NOT a poller)
- Build a single admin-facing endpoint: `POST /admin/linkedin-submission { url, raw_text?, media_url? }`.
- Backend attempts to fetch the URL server-side; if blocked (likely, given LinkedIn's restrictions), the UI must gracefully ask for `raw_text` instead — never show an error dead-end.
- This is a manual trigger, not a scheduled job. Do not build a LinkedIn poller — it will violate platform terms and is unreliable even if attempted.

## 4. X / Twitter — explicitly excluded
**Do not implement any X/Twitter connector, agent trigger, schema field, or admin UI element for X.** It was evaluated and dropped: X removed its free API tier in February 2026 and is pay-per-use only with no free read access, which isn't worth the cost for a personal portfolio. If this is revisited far in the future, it would be added as a manual paste-link submission (identical pattern to LinkedIn §3), never an automatic poller. There is nothing to stub for it now.

## 5. Drive / external demo links
- Single endpoint: `POST /admin/projects/:id/demo-link { url }` — stores permanently on the project, no agent involved, no approval needed (you're directly asserting this fact).

## 6. Future connectors (build the interface now, implement later)
Stub `Connector` classes for Kaggle, Devpost, Hashnode, Medium, Codeforces, HackerRank, Spotify, Instagram that raise `NotImplementedError` but are registered in the `connectors` table with `enabled=false`, so the admin dashboard already shows them as "Coming soon" toggles. When you eventually create accounts on these, implementation is additive — no architecture changes. (X is not in this list — see §4.)

## 7. Scheduling, all via GitHub Actions
No Celery, no Redis, no managed worker. A single `.github/workflows/scheduled-polls.yml` with multiple cron triggers calling the backend's internal endpoints (with a shared-secret header) covers GitHub poll fallback, LeetCode poll, and the nightly analytics digest. This is free and removes an entire infrastructure component.

## 8. Notifications
- When a new `pending_changes` row is created, send yourself a notification (email via Resend/SendGrid, or a Telegram/Slack webhook — pick whichever is least friction for you) so the approval queue isn't something you have to remember to check.

## 9. Testing
- Mock all external API responses in tests (GitHub/LeetCode) — no test should make a real network call.
- Include at least one test per connector simulating a malformed/changed API response, asserting the system logs and skips gracefully rather than crashing the scheduled job.
