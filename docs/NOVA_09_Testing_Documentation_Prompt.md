# TESTING & DOCUMENTATION PROMPT — paste into Claude Code

## 1. Test Strategy
| Layer | Approach |
|---|---|
| Backend unit | pytest, mock all external APIs and Gemini calls (use recorded fixture responses) |
| Backend integration | spin up a test Postgres (docker) per CI run, run real migrations, test the full propose→approve→publish flow end to end against it |
| Agent prompt regression | snapshot tests — given a fixed fake README/post, assert the agent's structured output shape (not exact wording, since LLM output varies) matches the expected schema and includes `ai_rationale` |
| Frontend unit | Vitest/Jest for components, especially the resume version picker and chatbot streaming UI |
| Frontend e2e | Playwright — at minimum: homepage loads, a project page loads, chatbot answers a canned question (including the Render cold-start loading state), Recruiter Mode toggles correctly |
| Accessibility | automated axe-core pass in CI on key pages + manual screen-reader pass before launch |

## 2. Critical Invariants to Test Explicitly
- No agent or connector writes directly to a live table (static/lint check, not just a runtime test).
- Every `pending_changes` row has a non-empty `ai_rationale`.
- Rejecting a pending change never mutates live tables.
- LinkedIn submission endpoint never silently fails — if URL fetch is blocked, the response explicitly asks for raw text rather than erroring out blankly.
- Resume Agent never invents a metric not present in source data (test with a fixture project that has no measurable outcome — assert the generated bullet has no fabricated number).
- No code path anywhere references X/Twitter — a simple grep-based CI check for stray X/Twitter API calls or credentials is a cheap guardrail against scope creep.

## 3. Documentation to Produce
- `README.md` (root): project overview, links to all spec docs, local dev setup for both `apps/web` and `apps/api`.
- `RUNBOOK.md`: what to do when — a webhook stops firing, a connector starts erroring, Gemini quota is hit, Render's free tier cold start is too slow, a bad approval gets published (rollback steps).
- `AGENTS.md`: the prompt contracts from `NOVA_04_AI_Agents_Specification.md` kept in sync with the actual prompt template files — this should be the living reference, updated whenever a prompt changes.
- `CHANGELOG.md`: auto-updated or manually maintained per release.
- API docs: FastAPI's auto-generated `/docs` is sufficient for the backend; no separate Postman collection needed unless you want one.

## 4. Definition of Done (per phase, referencing master spec §6 build order)
A phase is not "done" until:
1. Tests above pass in CI.
2. The relevant spec doc section is updated if anything deviated during implementation.
3. It is deployed and demoable on the live (or preview) URL — not just "works locally."

## 5. Ongoing Maintenance Cadence
- Weekly: review any stuck `pending_changes` older than 7 days.
- Monthly: review Gemini token spend per agent and LeetCode endpoint stability (unofficial API may break).
- Quarterly: revisit which "future" connectors (Kaggle, Medium, etc.) are now worth implementing as your platform usage grows. X/Twitter is not on this revisit list unless its pricing model fundamentally changes back to a usable free tier.
