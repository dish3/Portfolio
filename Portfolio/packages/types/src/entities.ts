/**
 * Core entity models for NOVA AI Portfolio OS.
 * Sourced directly from NOVA_02_Database_Design.md.
 */

export type SkillCategory = 'language' | 'framework' | 'tool' | 'concept';

export interface Skill {
  id: string;
  name: string;
  category: SkillCategory;
  proficiency: number; // 1-5, estimated from project frequency
  first_seen?: string | null;
  embedding?: number[] | null;
}

export type ProjectSource = 'github' | 'manual';
export type EntityStatus = 'draft' | 'published' | 'archived';

export interface Project {
  id: string;
  slug: string;
  title: string;
  short_description?: string | null;
  long_description?: string | null;
  source: ProjectSource;
  github_repo_url?: string | null;
  live_demo_url?: string | null;
  drive_fallback_url?: string | null;
  linkedin_post_url?: string | null;
  youtube_video_url?: string | null;
  cover_image_url?: string | null;
  tech_stack: string[];
  status: EntityStatus;
  started_at?: string | null;
  updated_at: string;
  embedding?: number[] | null;
}

export interface ProjectSkill {
  project_id: string;
  skill_id: string;
}

export interface Certificate {
  id: string;
  title: string;
  issuer?: string | null;
  issue_date?: string | null;
  credential_url?: string | null;
  source_post_url?: string | null;
  related_skill_ids: string[];
  status: EntityStatus;
}

export type TimelineEventType =
  | 'hackathon'
  | 'internship'
  | 'project'
  | 'certificate'
  | 'achievement'
  | 'conference';

export interface TimelineEvent {
  id: string;
  type: TimelineEventType;
  title: string;
  description?: string | null;
  date?: string | null;
  related_project_id?: string | null;
  status: EntityStatus;
}

export type UpdateSource = 'linkedin' | 'github' | 'manual';

export interface Update {
  id: string;
  source: UpdateSource;
  raw_content?: string | null;
  ai_summary?: string | null;
  media_url?: string | null;
  related_project_id?: string | null;
  published_at?: string | null;
  status: EntityStatus;
}

export type ResumeRoleTarget =
  | 'software_engineer'
  | 'ai_engineer'
  | 'ml_engineer'
  | 'backend_engineer'
  | 'ats_generic';

export interface ResumeVersion {
  id: string;
  role_target: ResumeRoleTarget;
  content_json: Record<string, unknown>;
  pdf_url?: string | null;
  generated_at: string;
  is_current: boolean;
}

export interface Visit {
  id: string;
  visited_at: string;
  path?: string | null;
  country?: string | null;
  referrer?: string | null;
  is_recruiter_mode: boolean;
  session_id?: string | null;
}

export interface ChatMessage {
  id: string;
  session_id: string;
  role: 'user' | 'assistant';
  content: string;
  created_at: string;
}
