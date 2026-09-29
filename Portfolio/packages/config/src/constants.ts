/**
 * Core constants for the NOVA AI Portfolio OS.
 * Sourced from NOVA specifications.
 */

export const PLATFORM_CONSTANTS = {
  PROJECT_NAME: 'NOVA',
  OWNER_NAME: 'Disha',
  DEFAULT_ROLE_TARGET: 'software_engineer',

  // Gemini AI Models (free-tier optimized)
  GEMINI_DEFAULT_MODEL: 'gemini-2.5-flash',
  GEMINI_FAST_MODEL: 'gemini-2.5-flash-lite',
  GEMINI_EMBEDDING_MODEL: 'text-embedding-004',
  EMBEDDING_DIMENSION: 768,

  // Thresholds & Invariants
  CONFIDENCE_MATCH_THRESHOLD: 0.6,
  STALE_PENDING_DAYS_LIMIT: 7,

  // ISR & Cache
  DEFAULT_ISR_REVALIDATE_SECONDS: 3600,
} as const;

export const ADMIN_NAV_ITEMS = [
  { name: 'Dashboard', href: '/admin' },
  { name: 'Pending Approvals', href: '/admin/pending' },
  { name: 'Projects', href: '/admin/projects' },
  { name: 'Certificates', href: '/admin/certificates' },
  { name: 'Timeline', href: '/admin/timeline' },
  { name: 'Resume Versions', href: '/admin/resume' },
  { name: 'Connectors', href: '/admin/connectors' },
  { name: 'Analytics', href: '/admin/analytics' },
  { name: 'Settings', href: '/admin/settings' },
] as const;
