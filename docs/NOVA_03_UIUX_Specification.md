# UI/UX SPECIFICATION — NOVA

## 1. Visual Direction (dark, professional, original — not generic cyberpunk)
The brief was "something no one has seen before, eye-catching, but dark and professional." Generic neon-cyberpunk is the *opposite* of original now — it's the default everyone reaches for. Instead:

**Direction: "Quiet Intelligence"** — a dark observatory/lab aesthetic, not a neon arcade.
- Background: near-black (#0A0A0F) with very subtle deep-indigo gradients, not pure black.
- Accent: a single signature color (e.g., warm amber `#D9A857` or electric ice-blue `#7FE7E0`) used sparingly — one accent, not a rainbow of neon.
- Typography: a serif or high-contrast grotesk for headlines (signals "professional/editorial," uncommon in tech portfolios) paired with a clean mono for data/stats (signals "engineer").
- Glass panels used sparingly for cards (per your "glassmorphism" interest) but always over a textured dark background (subtle noise/grain), not flat black — this avoids the generic "Apple Vision Pro clone" look.
- Motion is the real differentiator, not color: things should feel like they have weight and physics (GSAP/Framer Motion spring easing), not just fade-ins.

## 2. Structure: Story-Driven, Not Page-Driven
Single scrolling experience with anchor sections (good for SEO, sharing, and mobile) but presented as a *sequence* rather than a flat nav bar:

```
1. Arrival        — full-bleed intro, name, one-line identity, subtle 3D accent (e.g. a slowly rotating abstract object representing "code+AI")
2. AI Assistant    — a small persistent chat orb introduces itself: "Ask me anything about Disha" (this IS the nav — visitors can type instead of scrolling)
3. Live Pulse      — GitHub activity graph, LeetCode stats — "what's happening right now"
4. Projects        — horizontal-scroll or staggered grid of project cards, each opens a full project page
5. Experience      — vertical interactive timeline (hackathons, internships, achievements, certs all merged chronologically)
6. Skills          — grouped badges, sized/colored by proficiency, sourced live from the knowledge graph
7. Music / Editing / Photography — a lighter, more visual section (separate from the engineering sections in tone)
8. Blog/Updates    — AI-drafted posts and approved LinkedIn highlights
9. Contact         — contact form, book-a-meeting, resume download (with version picker), testimonials
```

Each section gets its own anchor route (`/#projects`) for shareability, but the default experience is continuous scroll with scroll-triggered animations (GSAP ScrollTrigger).

## 3. The AI Assistant Orb (signature element)
Persistent small element (bottom-right, mobile: bottom sheet) — always present, not just a "Contact" page chatbot. This doubles as navigation: typing "show me ML projects" filters the Projects section live instead of opening a separate modal. This is the "never seen before" hook — the chatbot IS the nav.

## 4. Recruiter Mode
Toggle in the header ("Recruiter? Tap here") or auto-detected via referrer (LinkedIn/Naukri/company-domain links). On activation:
- Page re-renders to a condensed single-screen layout: photo, one-line pitch, top 3 projects, skills summary, resume download (role-targeted), contact button — explicitly designed to be absorbed in under 60 seconds.
- A subtle banner: "Showing Recruiter View — [See Full Portfolio]" lets them opt out.

## 5. Project Pages
Each project page includes:
- Cover image/video
- AI-written long description
- Tech stack badges (from knowledge graph)
- GitHub link
- Live demo link (or Drive fallback link if no live demo)
- LinkedIn post embed/link (if provided)
- Timeline (started/updated dates)
- "Ask the AI about this project" — deep-links into the chatbot pre-scoped to this project

## 6. Motion & Animation Inventory
- Scroll storytelling: section transforms tied to scroll position (parallax depth, not just opacity fades).
- Page/section transitions: shared-element transitions when opening a project card → project page.
- Particle effects: extremely subtle ambient particles in the Arrival section only — restraint is part of "professional."
- Floating cards: Projects grid has gentle idle float (subtle, <4px) to feel alive without being distracting.
- Holograms: reserved for the Skills section — skill clusters rendered as a soft glowing 3D node cluster (R3F), clickable.
- Mouse interaction: cursor-reactive tilt on project cards (subtle 3D parallax on hover).
- Sound: optional, off by default, toggle in corner — soft UI clicks only, never auto-playing music.

## 7. Mobile
- 3D elements degrade gracefully: Skills hologram becomes a 2D radial chart below a viewport-width breakpoint (no WebGL strain on low-end phones).
- Story sections become simple vertical scroll with lighter animation (transform-only, no heavy particle canvases).
- AI Assistant becomes a bottom sheet, not a floating orb.

## 8. Accessibility
- All animations respect `prefers-reduced-motion`.
- Color contrast of accent-on-dark must hit WCAG AA for body text; decorative glows are exempt.
- Chatbot fully usable via keyboard and screen reader (it's also your nav, so this matters a lot).

## 9. Admin Dashboard (separate, minimal-design, function-first)
Not part of the "wow" brand — built plainly (e.g., shadcn/ui default theme) so it's fast to build and fast to use:
- Sidebar: Pending Approvals · Projects · Certificates · Timeline · Resume Versions · Connectors · Analytics
- Approval Queue is the home screen — this is where most of your time in this system will be spent.
