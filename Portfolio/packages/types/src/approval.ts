/**
 * Approval queue and agent change proposal types.
 * Sourced from NOVA_02_Database_Design.md §2 and NOVA_04_AI_Agents_Specification.md.
 */

export type AgentName =
  | 'github_agent'
  | 'content_agent'
  | 'portfolio_agent'
  | 'resume_agent'
  | 'recruiter_agent'
  | 'chat_agent'
  | 'analytics_agent';

export type ChangeEntityType =
  | 'project'
  | 'certificate'
  | 'timeline_event'
  | 'update'
  | 'resume_version';

export type ApprovalDecision =
  | 'approved'
  | 'rejected'
  | 'edited_then_approved';

export interface PendingChange<T = Record<string, unknown>> {
  id: string;
  agent: AgentName;
  entity_type: ChangeEntityType;
  entity_id?: string | null;
  diff: T;
  ai_rationale: string;
  created_at: string;
  reviewed_at?: string | null;
  decision?: ApprovalDecision | null;
}

export interface ReviewChangePayload<T = Record<string, unknown>> {
  decision: ApprovalDecision;
  patch?: Partial<T>;
}
