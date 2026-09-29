/**
 * Platform connector types and sync state.
 * Sourced from NOVA_01_System_Architecture.md §7 and NOVA_02_Database_Design.md §4.
 *
 * NOTE: Per project specification, X / Twitter is permanently excluded from this system.
 */

export type SupportedPlatform =
  | 'github'
  | 'leetcode'
  | 'linkedin'
  | 'kaggle'
  | 'devpost'
  | 'hashnode'
  | 'medium'
  | 'codeforces'
  | 'hackerrank'
  | 'spotify'
  | 'instagram';

export interface ConnectorState {
  id: string;
  platform: SupportedPlatform;
  enabled: boolean;
  last_synced_at?: string | null;
  config?: Record<string, unknown> | null;
}

export interface LeetCodeSnapshot {
  id: string;
  captured_at: string;
  total_solved: number;
  easy: number;
  medium: number;
  hard: number;
  contest_rating?: number | null;
  raw?: Record<string, unknown> | null;
}

export interface RawItem {
  id: string;
  platform: SupportedPlatform;
  payload: Record<string, unknown>;
  timestamp: string;
}
