# Database Design & Schema Reference

The database is powered by **PostgreSQL (Supabase)** with the **`pgvector`** extension for high-dimensional semantic search.

## Entity Relationship Overview

```
skills (id, name, category, proficiency, embedding)
  │
  ├──< project_skills >──┐
  │                      │
projects (id, slug, title, tech_stack, embedding)
  │
  ├──< timeline_events (related_project_id)
  │
  └──< updates (related_project_id)

pending_changes (id, agent, entity_type, entity_id, diff, ai_rationale, decision)
  ↳ Isolates all unreviewed changes proposed by AI agents.

connectors (id, platform, enabled, last_synced_at, config)
  ↳ State tracking for GitHub, LeetCode, etc. (Excludes X/Twitter).

leetcode_snapshots (id, captured_at, total_solved, easy, medium, hard, contest_rating)
  ↳ Time-series snapshot of competitive coding stats.

resume_versions (id, role_target, content_json, pdf_url, is_current)
  ↳ Dynamic ATS and role-targeted resumes.

visits / chat_messages
  ↳ Ephemeral visitor and session analytics.
```

## Schema Invariants
1. `vector(768)` dimension matches Google Gemini `text-embedding-004`.
2. Live tables (`projects`, `certificates`, `timeline_events`, `updates`, `resume_versions`) are strictly updated through approved `pending_changes` entries.
3. Cosine distance IVFFLAT indexes are maintained on `projects.embedding` and `skills.embedding`.
