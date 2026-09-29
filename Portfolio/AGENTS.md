# Autonomous Agents Reference — NOVA OS

Living reference of the 7 autonomous Gemini AI agents operating in the system.
Prompt contracts are versioned in `agents/prompts/*.md`.

---

## 1. GitHub Agent (`github_agent.md`)
- **Trigger**: Webhook (`push`, `release`, `repository`) or 6-hour cron fallback.
- **Model**: `gemini-2.5-flash`
- **Output**: Proposed Project record or diff to `pending_changes`.
- **Constraint**: Must never invent features not present in README or commits.

## 2. Content Agent (`content_agent.md`)
- **Trigger**: Admin pastes a LinkedIn post URL/text or Drive demo link.
- **Model**: `gemini-2.5-flash`
- **Output**: Proposed Update card and project relationship patch to `pending_changes`.
- **Constraint**: Confidence threshold < 0.6 flags `needs_human_match: true`.

## 3. Portfolio Agent (`portfolio_agent.md`)
- **Trigger**: Any approved change in `pending_changes`.
- **Model**: `gemini-2.5-flash`
- **Output**: On-demand ISR revalidation calls + secondary Timeline proposals.

## 4. Resume Agent (`resume_agent.md`)
- **Trigger**: Approved Project, Skill, or Certificate update.
- **Model**: `gemini-2.5-flash`
- **Output**: Synthesized `resume_versions` (SWE, AI, ML, Backend, ATS) in X-Y-Z format.

## 5. Recruiter Agent (`recruiter_agent.md`)
- **Trigger**: Visitor activates Recruiter Mode or lands from recruiting domain.
- **Model**: `gemini-2.5-flash-lite`
- **Output**: Ephemeral top 3 projects, skill summary, and tailored pitch.

## 6. Chat Agent (`chat_agent.md`)
- **Trigger**: Visitor sends a message to the persistent assistant orb.
- **Model**: `gemini-2.5-flash`
- **Output**: Streaming RAG response grounded in knowledge graph embeddings.

## 7. Analytics Agent (`analytics_agent.md`)
- **Trigger**: Nightly GitHub Actions cron.
- **Model**: `gemini-2.5-flash-lite`
- **Output**: Daily traffic and chat conversation executive digest.
