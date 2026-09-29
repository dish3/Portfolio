# AI AGENTS SPECIFICATION — NOVA
All agents call **Gemini** (e.g. `gemini-2.5-flash` for cheap/frequent tasks, `gemini-2.5-flash-lite` for high-volume classification tasks). Every agent writes ONLY to `pending_changes` — never directly to live tables. No agent here handles X/Twitter — it is out of scope for this project.

## 1. GitHub Agent
**Trigger:** webhook (push/release/repo created) or scheduled poll (GitHub Actions cron, every 6h).
**Input:** repo metadata, README content, languages, commit messages since last sync, topics.
**Task:** Decide if this is (a) a new project, (b) an update to an existing one, or (c) noise (e.g. a tiny typo fix — skip).
**Output → `pending_changes`:**
```json
{
  "entity_type": "project",
  "entity_id": "<existing id or null>",
  "diff": {
    "title": "...", "short_description": "...", "long_description": "...",
    "tech_stack": ["..."], "github_repo_url": "...", "status": "draft"
  },
  "ai_rationale": "New repo 'x' pushed with a README describing a FastAPI + React app for ..."
}
```
**Prompt contract (system instruction):**
> You are the GitHub Agent for {{PROJECT_NAME}}. Given a repository's README, file tree summary, languages, and recent commits, write a professional 2-4 sentence project description in third person, identify the tech stack as a list of canonical names (e.g. "React" not "react.js"), and state in one sentence why this looks like a new project vs. an incremental update. Never invent features not evidenced in the README or commits. If information is insufficient, say so in `ai_rationale` rather than guessing.

## 2. Content Agent (LinkedIn / Drive submissions)
**Trigger:** admin pastes a LinkedIn URL/text, or a Drive link.
**Task:** Extract: which existing project this relates to (match by title/keywords against the knowledge graph), description, media URL, date, suggested tags.
**Output:** draft `update` row + (if confidently matched) a `diff` patch onto the related `project` (e.g. attaching `linkedin_post_url`).
**Prompt contract:**
> You are the Content Agent. Given raw text/caption from a LinkedIn post (and optionally a media URL), determine which project in the provided project list it most likely refers to (or "none"), write a one-paragraph professional summary suitable for a portfolio "Updates" feed, and extract any certificate/achievement claims separately. If the match confidence is below your threshold, say "needs_human_match": true instead of guessing.

## 3. Portfolio Agent
**Trigger:** any `pending_changes` row gets approved.
**Task:** Decide downstream effects — which public pages need ISR revalidation, whether a Skill's proficiency score should shift, whether a Timeline event should be auto-created (e.g., approving a Project triggers a "Project launched" timeline entry).
**Output:** revalidation calls + secondary `pending_changes` rows (e.g., timeline event) — secondary rows still require approval unless they are purely structural (revalidation), not content.

## 4. Resume Agent
**Trigger:** any approved Project/Skill/Certificate change.
**Task:** Regenerate resume content for each `role_target` (software_engineer, ai_engineer, ml_engineer, backend_engineer, ats_generic), selecting/prioritizing the most relevant projects and skills per role, writing ATS-safe bullet points (no graphics-dependent formatting, standard section headers) for the `ats_generic` version.
**Output:** new `resume_versions` rows marked `is_current=false` until approved; on approval, render to PDF and mark current.
**Prompt contract:**
> Write resume bullet points in the X-Y-Z format (Accomplished X by doing Y, measured by Z) using only facts present in the knowledge graph. Do not fabricate metrics. If no measurable outcome exists, write an impact statement without inventing numbers. Tailor project/skill selection and ordering to {{role_target}} but never omit a project entirely if it is the candidate's only example of a needed skill for that role.

## 5. Recruiter Agent
**Trigger:** Recruiter Mode activated by a visitor.
**Task:** Given referrer/UTM hints (if any) and the full knowledge graph, select the 3 most relevant projects and a skill summary for a generic technical-recruiter audience (default to broad relevance if no role hint exists).
**Output:** ephemeral — not persisted, just an API response shaping that page render.

## 6. Chat Agent
**Trigger:** visitor message.
**Task:** RAG over knowledge graph embeddings; if the visitor asks something requiring live data not yet in the graph (e.g. "what does the demo actually do"), it may live-fetch the project's `live_demo_url` or `github_repo_url` README server-side and summarize on the fly, but must not modify the knowledge graph itself (read-only agent).
**Prompt contract:**
> You are {{PROJECT_NAME}}'s portfolio assistant, speaking on behalf of {{OWNER_NAME}} in first person plural ("we") or third person ("Disha") — pick one and stay consistent. Answer only from retrieved context plus any live-fetched page content explicitly provided to you. If asked something not answerable from available data, say so and offer to connect the visitor via the contact form. Never claim skills, employers, or outcomes not present in the data.

## 7. Analytics Agent
**Trigger:** GitHub Actions cron, nightly.
**Task:** Summarize the day's `visits`/`chat_messages` into a short digest (top pages, recruiter-mode count, notable chat questions) for the admin dashboard home screen.

## 8. Cross-Agent Rules
- All agents must include an `ai_rationale` string — the admin dashboard always shows *why* before *what*.
- Any agent below a confidence threshold (define explicitly, e.g. <0.6) must set `needs_human_match` or equivalent instead of silently guessing.
- No agent ever deletes data; rejections in the approval queue simply mark the row `rejected` and stop there.
- No agent in this system reads from or writes to X/Twitter in any form.
