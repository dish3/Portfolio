-- ==============================================================================
-- NOVA AI Portfolio OS — Initial PostgreSQL Schema Migration
-- Sourced directly from NOVA_02_Database_Design.md
-- ==============================================================================

-- 1. Extensions
create extension if not exists vector;
create extension if not exists "uuid-ossp";

-- 2. Core Entities

create table if not exists skills (
  id uuid primary key default gen_random_uuid(),
  name text unique not null,
  category text, -- 'language' | 'framework' | 'tool' | 'concept'
  proficiency smallint, -- 1-5, AI-estimated from frequency across projects
  first_seen date,
  embedding vector(768)
);

create table if not exists projects (
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

create table if not exists project_skills (
  project_id uuid references projects(id) on delete cascade,
  skill_id uuid references skills(id) on delete cascade,
  primary key (project_id, skill_id)
);

create table if not exists certificates (
  id uuid primary key default gen_random_uuid(),
  title text not null,
  issuer text,
  issue_date date,
  credential_url text,
  source_post_url text, -- LinkedIn post it was extracted from, if any
  related_skill_ids uuid[],
  status text default 'draft'
);

create table if not exists timeline_events (
  id uuid primary key default gen_random_uuid(),
  type text, -- 'hackathon' | 'internship' | 'project' | 'certificate' | 'achievement' | 'conference'
  title text,
  description text,
  date date,
  related_project_id uuid references projects(id) on delete set null,
  status text default 'draft'
);

create table if not exists updates ( -- the "social post" style cards on the homepage
  id uuid primary key default gen_random_uuid(),
  source text, -- 'linkedin' | 'github' | 'manual'
  raw_content text,
  ai_summary text,
  media_url text,
  related_project_id uuid references projects(id) on delete set null,
  published_at timestamptz,
  status text default 'draft'
);

-- 3. Approval Queue (AI agents propose, human approves)

create table if not exists pending_changes (
  id uuid primary key default gen_random_uuid(),
  agent text not null, -- 'github_agent' | 'content_agent' | 'resume_agent' ...
  entity_type text not null, -- 'project' | 'certificate' | 'timeline_event' | 'update' | 'resume_version'
  entity_id uuid, -- null if this is a brand-new entity
  diff jsonb not null, -- proposed fields
  ai_rationale text not null, -- "why I'm suggesting this"
  created_at timestamptz default now(),
  reviewed_at timestamptz,
  decision text -- 'approved' | 'rejected' | 'edited_then_approved'
);

-- 4. Resume Versions

create table if not exists resume_versions (
  id uuid primary key default gen_random_uuid(),
  role_target text not null, -- 'software_engineer' | 'ai_engineer' | 'ml_engineer' | 'backend_engineer' | 'ats_generic'
  content_json jsonb not null, -- structured resume content
  pdf_url text,
  generated_at timestamptz default now(),
  is_current boolean default false
);

-- 5. Platform Sync State (Connectors)

create table if not exists connectors (
  id uuid primary key default gen_random_uuid(),
  platform text unique not null, -- 'github' | 'leetcode' | 'linkedin' | 'kaggle' | ... (NOT 'x' — out of scope)
  enabled boolean default false,
  last_synced_at timestamptz,
  config jsonb -- API tokens reference, usernames, etc.
);

create table if not exists leetcode_snapshots (
  id uuid primary key default gen_random_uuid(),
  captured_at timestamptz default now(),
  total_solved int,
  easy int,
  medium int,
  hard int,
  contest_rating numeric,
  raw jsonb
);

-- 6. Visitor Analytics & Chat Logs

create table if not exists visits (
  id uuid primary key default gen_random_uuid(),
  visited_at timestamptz default now(),
  path text,
  country text,
  referrer text,
  is_recruiter_mode boolean default false,
  session_id text
);

create table if not exists chat_messages (
  id uuid primary key default gen_random_uuid(),
  session_id text,
  role text, -- 'user' | 'assistant'
  content text,
  created_at timestamptz default now()
);

-- 7. Performance & Vector Indexing

create index if not exists idx_projects_status on projects (status);
create index if not exists idx_pending_changes_decision on pending_changes (decision);
create index if not exists idx_pending_changes_created_at on pending_changes (created_at desc);
create index if not exists idx_timeline_events_date on timeline_events (date desc);
create index if not exists idx_updates_published_at on updates (published_at desc);

-- Vector indexes using cosine distance
-- Note: ivfflat index is typically built after initial rows exist; in Postgres we define it with lists parameter.
do $$
begin
  if not exists (select 1 from pg_indexes where indexname = 'idx_projects_embedding') then
    create index idx_projects_embedding on projects using ivfflat (embedding vector_cosine_ops) with (lists = 10);
  end if;
  if not exists (select 1 from pg_indexes where indexname = 'idx_skills_embedding') then
    create index idx_skills_embedding on skills using ivfflat (embedding vector_cosine_ops) with (lists = 10);
  end if;
end $$;
