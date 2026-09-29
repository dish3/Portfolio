# FRONTEND DEVELOPMENT PROMPT — paste into Claude Code

You are building the frontend for **NOVA**, a 3D, story-driven personal portfolio. Follow the attached specs exactly: `NOVA_00_Master_Specification.md`, `NOVA_01_System_Architecture.md`, `NOVA_03_UIUX_Specification.md`. Read all of them before writing any code.

## Stack
- Next.js 14 (App Router), TypeScript, Tailwind CSS, shadcn/ui
- React Three Fiber + drei for 3D accents (not a full 3D world — see UI/UX spec §2)
- GSAP (ScrollTrigger) + Framer Motion for scroll storytelling and transitions
- Data fetched from the FastAPI backend (hosted on Render) via typed fetch clients; use Next.js ISR (`revalidate`) for public pages so admin approvals update the site without redeploy

## Build in this order
1. **Design system first**: color tokens, typography scale (serif/grotesk headline + mono data font per spec §1), spacing scale, base components (Card, Badge, Button) in the "Quiet Intelligence" dark theme — no generic neon defaults.
2. **Layout shell**: persistent AI Assistant orb (bottom-right desktop / bottom-sheet mobile), Recruiter Mode toggle in header, sound toggle.
3. **Section components** in the order from UI/UX spec §2: Arrival, Live Pulse, Projects, Experience (timeline), Skills (hologram cluster, degrades to 2D radial chart on mobile), Music/Editing/Photography, Blog/Updates, Contact.
4. **Project detail page** (`/projects/[slug]`) per spec §5.
5. **Recruiter Mode** alternate render per spec §4.
6. **Chatbot UI** wired to backend `/api/chat` (streaming response). Note: backend is on Render's free tier, so build in a graceful loading state for the first request after idle (cold start, ~1 minute) — show a friendly "waking up" message rather than a blank spinner.
7. **Resume section**: version picker (role_target) + PDF download, calling backend `/api/resume/:role`.

## Hard requirements
- Respect `prefers-reduced-motion` everywhere animation is added.
- All 3D scenes must have a non-WebGL fallback or be skipped entirely below a defined mobile breakpoint — never block page load on WebGL.
- No hardcoded portfolio content — every project/skill/cert/timeline item is fetched from the backend; the frontend has zero knowledge of "what projects exist."
- Use ISR with on-demand revalidation triggered by the backend after an approval (`POST /api/revalidate`), not full redeploys.
- WCAG AA contrast for all body text against the dark background.

## Deliverables for this phase
- `apps/web` Next.js project, deployable to Vercel standalone (env vars documented in a `.env.example`)
- Storybook or a `/design-system` route showing all base components for review before wiring real data
- Lighthouse mobile performance ≥85 even with 3D sections present (lazy-load R3F canvases below the fold)

If anything in the specs is ambiguous or you need a decision only the project owner can make (brand name, exact accent color, copy/tone), stop and ask rather than guessing.
