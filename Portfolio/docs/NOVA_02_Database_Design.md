# DATABASE DESIGN — NOVA

PostgreSQL (Supabase) with `pgvector` extension. Naming convention: snake_case tables, UUID primary keys.

## 1. Core Entities

```sql
create extension if not exists vector;

create table skills (
  id uuid primary key default gen_random_uuid(),
  name text unique not null,
  category text, -- 'language' | 'framework' | 'tool' | 'concept'
  proficiency smallint, -- 1-5, AI-estimated from frequency across projects
  first_seen date,
  embedding vector(768)
);

create table projects (
  id uuid primary key default gen_random_uuid(),
  slug text unique not null,
  title text not null,
  short_description text,
  long_description text, -- AI-generated
  source text not null, -- 'github' | 'manual'
  github_repo_url text,
  live_demo_url text,
  drive_fallback_url text,
  linkedin_post_url text,
  youtube_video_url text,
  cover_image_url text,
  tech_stack text[], -- denormalized for fast filtering
  status text default 'draft', -- 'draft' | 'published' | 'archived'
  started_at date,
  updated_at timestamptz default now(),
  embedding vector(768)
);

create table project_skills (
  project_id uuid references projects(id) on delete cascade,
  skill_id uuid references skills(id) on delete cascade,
  primary key (project_id, skill_id)
);

create table certificates (
  id uuid primary key default gen_random_uuid(),
  title text not null,
  issuer text,
  issue_date date,
  credential_url text,
  source_post_url text, -- LinkedIn post it was extracted from, if any
  related_skill_ids uuid[],
  status text default 'draft'
);

create table timeline_events (
  id uuid primary key default gen_random_uuid(),
  type text, -- 'hackathon' | 'internship' | 'project' | 'certificate' | 'achievement' | 'conference'
  title text,
  description text,
  date date,
  related_project_id uuid references projects(id),
  status text default 'draft'
);

create table updates ( -- the "social post" style cards on the homepage
  id uuid primary key default gen_random_uuid(),
  source text, -- 'linkedin' | 'github' | 'manual'
  raw_content text,
  ai_summary text,
  media_url text,
  related_project_id uuid references projects(id),
  published_at timestamptz,
  status text default 'draft'
);
```

## 2. Approval Queue

```sql
create table pending_changes (
  id uuid primary key default gen_random_uuid(),
  agent text not null, -- 'github_agent' | 'content_agent' | 'resume_agent' ...
  entity_type text not null, -- 'project' | 'certificate' | 'timeline_event' | 'update' | 'resume_version'
  entity_id uuid, -- null if this is a brand-new entity
  diff jsonb not null, -- proposed fields
  ai_rationale text, -- "why I'm suggesting this"
  created_at timestamptz default now(),
  reviewed_at timestamptz,
  decision text -- 'approved' | 'rejected' | 'edited_then_approved'
);
```

## 3. Resume Versions

```sql
create table resume_versions (
  id uuid primary key default gen_random_uuid(),
  role_target text, -- 'software_engineer' | 'ai_engineer' | 'ml_engineer' | 'backend_engineer' | 'ats_generic'
  content_json jsonb, -- structured resume content
  pdf_url text,
  generated_at timestamptz default now(),
  is_current boolean default false
);
```

## 4. Platform Sync State

```sql
create table connectors (
  id uuid primary key default gen_random_uuid(),
  platform text unique not null, -- 'github' | 'leetcode' | 'linkedin' | 'kaggle' | ... (NOT 'x' — out of scope)
  enabled boolean default false,
  last_synced_at timestamptz,
  config jsonb -- API tokens reference (store actual secrets in env, not here), usernames, etc.
);

create table leetcode_snapshots (
  id uuid primary key default gen_random_uuid(),
  captured_at timestamptz default now(),
  total_solved int,
  easy int,
  medium int,
  hard int,
  contest_rating numeric,
  raw jsonb
);
```

## 5. Visitor Analytics

```sql
create table visits (
  id uuid primary key default gen_random_uuid(),
  visited_at timestamptz default now(),
  path text,
  country text,
  referrer text,
  is_recruiter_mode boolean default false,
  session_id text
);

create table chat_messages (
  id uuid primary key default gen_random_uuid(),
  session_id text,
  role text, -- 'user' | 'assistant'
  content text,
  created_at timestamptz default now()
);
```

## 6. Indexing
```sql
create index on projects using ivfflat (embedding vector_cosine_ops);
create index on skills using ivfflat (embedding vector_cosine_ops);
create index on projects (status);
create index on pending_changes (decision);
```

## 7. Notes for Implementer
- All "source of truth" tables (`projects`, `certificates`, `timeline_events`, `updates`, `resume_versions`) are only ever written to directly by an **approved** `pending_changes` row — enforce this with a backend service layer, not ad-hoc routes.
- Keep `tech_stack text[]` denormalized on `projects` for fast badge rendering even though `project_skills` is the normalized relation — re-sync it whenever `project_skills` changes.
- `embedding` columns are populated by the Resume/Chat pipeline immediately after any approved write (see architecture doc §5).
- No table, column, or enum value references X/Twitter anywhere in this schema — it is fully out of scope.
