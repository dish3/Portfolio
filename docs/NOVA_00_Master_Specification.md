# MASTER SPECIFICATION
## Project Codename: NOVA (suggested — replace with your chosen name)

> An AI-managed personal Operating System whose public face is a 3D, story-driven portfolio. It continuously ingests data from GitHub, LeetCode, LinkedIn (semi-auto), and manual sources, builds a knowledge graph of skills/projects/certificates, and uses AI agents (Gemini) to propose — and on approval, publish — updates to the live site, resume, and project pages.

---

## 1. Naming
Pick one (or propose your own). Used throughout all docs as `{{PROJECT_NAME}}`:
- DishaOS
- NEXUS
- AETHER
- NOVA
- ECHO
- DJ
This doc uses **DJ** as placeholder.

## 2. Core Principles
1. **Zero manual upkeep** — the default path is "AI noticed a change → drafted an update → asked for approval."
2. **Human-in-the-loop, not human-in-the-pipeline** — you approve/reject, you never re-type content.
3. **Realistic automation boundaries** — GitHub and LeetCode are pulled automatically; LinkedIn is semi-automatic (you paste a post URL or text and AI does the rest); anything with no API (Drive links, demo videos) is asked for once and stored permanently.
4. **Single source of truth** — a knowledge graph, not scattered fields, backs every page, every resume version, and the chatbot.
5. **Story over sitemap** — visitors move through a guided sequence, not a nav bar.
6. **Dark, professional, never-seen-before** — see UI/UX spec for the visual language (not generic cyberpunk neon).

## 3. High-Level System Map
```
                 EXTERNAL SOURCES
       GitHub        LeetCode       LinkedIn (manual link)     Drive (manual link)
         │               │                  │                          │
         ▼               ▼                  ▼                          ▼
              ┌─────────────────────────────────────────┐
              │         INGESTION LAYER (Backend)         │
              │  - GitHub webhooks + REST poll             │
              │  - LeetCode public stats poll               │
              │  - LinkedIn URL/text submission endpoint    │
              │  - Drive link submission endpoint           │
              └───────────────────┬─────────────────────┘
                                  ▼
              ┌─────────────────────────────────────────┐
              │        AI AGENT LAYER (Gemini)            │
              │  GitHub Agent · Content Agent · Resume     │
              │  Agent · Recruiter Agent · Chat Agent ·    │
              │  Analytics Agent · Portfolio Agent         │
              └───────────────────┬─────────────────────┘
                                  ▼
              ┌─────────────────────────────────────────┐
              │   APPROVAL QUEUE (Admin Dashboard)        │
              │   "AI drafted this update — Approve?"     │
              └───────────────────┬─────────────────────┘
                                  ▼
              ┌─────────────────────────────────────────┐
              │   KNOWLEDGE GRAPH (Postgres + pgvector)   │
              │   Projects · Skills · Certs · Resume ·    │
              │   Posts · Timeline · Embeddings           │
              └───────────────────┬─────────────────────┘
                                  ▼
              ┌─────────────────────────────────────────┐
              │   PUBLIC SITE (Next.js + R3F, on Vercel)  │
              │  Story-driven 3D portfolio · AI Chatbot ·  │
              │  Recruiter Mode · Dynamic Resume Export    │
              └─────────────────────────────────────────┘
```

## 4. Scope Confirmed From Requirements Gathering
| Question | Decision |
|---|---|
| Purpose | Personal portfolio (your own brand) |
| Theme | Dark, professional, **original** (not generic cyberpunk) |
| 3D level | Option C — 3D accents where they add value, not a full 3D world |
| Mobile | Required |
| Admin dashboard | Yes, with an **approval queue** (AI proposes, you approve) |
| AI autonomy | Drafts only; nothing publishes without your click |
| Platforms (now) | GitHub (auto), LeetCode (auto), LinkedIn (semi-auto, manual paste) |
| Platforms (explicitly skipped) | **X / Twitter** — dropped permanently from scope. X removed its free API tier in Feb 2026 (pay-per-use only, no free read access); not worth the cost for a personal portfolio. If ever revisited, treat it like LinkedIn — manual paste-link only, never an automatic poller. |
| Platforms (future, no account yet — build extensible) | Kaggle, Devpost, Hashnode, Medium, Codeforces, HackerRank, Spotify, Instagram |
| Sections | All standard sections (About, Projects, Skills, Experience, Education, Hackathons, Research, Certifications, Achievements, Music, Video editing, Photography, Blog, Contact) |
| AI Chat | Yes — fetches/analyzes linked sources (GitHub, demo links) live, not just static text |
| Resume | Dynamic AI-generated + ATS version + role-targeted versions (SWE / AI / ML / Backend) |
| Project pages | Must include GitHub link, live demo link, and a Drive-link fallback you supply once |
| Animations | All of it — scroll storytelling, transitions, particles, holograms, floating cards, interaction, sound |
| Stack | Frontend free choice; **Deploy: Vercel** (frontend) + **Render free tier** (backend); **AI: Gemini** (Flash/Flash-Lite) |
| Auth/visitor actions | Contact, book meeting, download resume, testimonials, sign-in, Recruiter Mode |
| Recruiter Mode | Yes — dedicated "60-second view" |
| Long-term vision | Yes — this becomes your career operating system over time |

## 5. Document Set
1. `NOVA_00_Master_Specification.md` — this file
2. `NOVA_01_System_Architecture.md` — services, data flow, agent responsibilities, sync strategy
3. `NOVA_02_Database_Design.md` — schema, knowledge graph, embeddings
4. `NOVA_03_UIUX_Specification.md` — visual language, story flow, sections, motion design
5. `NOVA_04_AI_Agents_Specification.md` — every agent's prompt contract, triggers, approval flow
6. `NOVA_05_Frontend_Development_Prompt.md` — Claude Code prompt for the Next.js/R3F app
7. `NOVA_06_Backend_Development_Prompt.md` — Claude Code prompt for the FastAPI service
8. `NOVA_07_Automation_Integration_Prompt.md` — webhooks, schedulers, platform connectors
9. `NOVA_08_Deployment_Prompt.md` — Vercel + Render + secrets + CI/CD
10. `NOVA_09_Testing_Documentation_Prompt.md` — test strategy, docs, runbooks

## 6. Build Order (Recommended Phases)
1. **Phase 0** — Repo scaffold, schema, auth skeleton, empty admin dashboard.
2. **Phase 1** — GitHub Agent + Knowledge Graph + Project pages (this alone is a usable portfolio).
3. **Phase 2** — Admin approval queue + manual LinkedIn/Drive link submission flow.
4. **Phase 3** — 3D story-driven homepage + section pages + animations.
5. **Phase 4** — AI Chatbot (RAG over knowledge graph) + Recruiter Mode.
6. **Phase 5** — Resume Agent (multi-version, ATS, PDF export).
7. **Phase 6** — LeetCode connector, Content Agent (auto-draft posts), Analytics Agent.
8. **Phase 7** — Extensible connector framework for future platforms (Kaggle, Medium, etc.).

## 7. Realistic Constraint Reminder
LinkedIn has no general API for reading a personal account's arbitrary posts/videos. The system must **never** assume silent LinkedIn scraping. The supported flow is: you paste/forward a LinkedIn post URL → Content Agent extracts what's publicly fetchable (or you paste the caption text directly if blocked) → AI extracts + drafts → you approve.

## 8. Free-Tier Cost Reality (locked in)
- **Gemini (Flash/Flash-Lite)**: free, no card required, ample for personal-portfolio traffic volume.
- **GitHub API/webhooks**: free.
- **LeetCode public stats**: free.
- **Vercel (frontend)**: free Hobby tier.
- **Render (backend)**: free tier; sleeps after inactivity, ~1 min cold start on next request — acceptable since only the chatbot is real-time-sensitive.
- **Supabase (DB + pgvector + storage)**: free tier; projects pause after 7 days of inactivity — mitigated with a scheduled GitHub Actions ping.
- **No Celery/Redis**: scheduled jobs (GitHub poll fallback, LeetCode poll) run via GitHub Actions cron calling backend endpoints — removes a paid/managed component entirely.
- **X / Twitter**: out of scope — no longer has any free path worth using.

Total to build and run the full MVP: **$0/month**, with the only friction being Render's cold start on the chatbot (fixable later with a $7/mo upgrade if it ever bothers you).
