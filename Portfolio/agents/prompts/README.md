# AI Agent Prompt Contracts

This directory contains versioned prompt contracts for all 7 autonomous agents in NOVA.
Per `NOVA_04_AI_Agents_Specification.md` and `NOVA_06_Backend_Development_Prompt.md`:

1. **All Gemini prompts live in versioned prompt template files**, not inlined as raw strings scattered through code.
2. **Every agent writes ONLY to `pending_changes`** — never directly to live tables.
3. **Every agent output MUST include `ai_rationale`** explaining why the change is proposed.
4. **No agent handles X/Twitter** — it is permanently out of scope.

| Agent | Contract File | Trigger | Output |
|---|---|---|---|
| GitHub Agent | `github_agent.md` | Webhook / cron poll | Draft Project create/update |
| Content Agent | `content_agent.md` | Admin LinkedIn/Drive submission | Draft Update card + project patch |
| Portfolio Agent | `portfolio_agent.md` | Any approved change | ISR revalidation + secondary changes |
| Resume Agent | `resume_agent.md` | Any approved entity change | Targeted resume versions + ATS |
| Recruiter Agent | `recruiter_agent.md` | Recruiter Mode activated | Ephemeral top N projects/skills |
| Chat Agent | `chat_agent.md` | Visitor chat message | RAG over knowledge graph + live fetch |
| Analytics Agent | `analytics_agent.md` | Nightly cron | Daily digest of visits and queries |
