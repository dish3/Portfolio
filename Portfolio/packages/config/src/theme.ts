/**
 * Theme design tokens for NOVA: "Quiet Intelligence" Aesthetic.
 * Sourced directly from NOVA_03_UIUX_Specification.md §1.
 */

export const THEME_TOKENS = {
  colors: {
    background: '#0A0A0F',
    surface: '#12121A',
    surfaceHover: '#181824',
    border: '#1E1E2E',
    borderSubtle: '#161622',

    // Accents
    accentAmber: '#D9A857', // Primary warm amber signature
    accentIceBlue: '#7FE7E0', // Secondary electric ice-blue signature

    // Text & Content
    textPrimary: '#F3F4F6',
    textSecondary: '#9CA3AF',
    textMuted: '#6B7280',

    // Semantic status
    statusApproved: '#10B981',
    statusPending: '#F59E0B',
    statusRejected: '#EF4444',
  },
  typography: {
    fontSans: 'var(--font-sans, Inter, sans-serif)',
    fontMono: 'var(--font-mono, JetBrains Mono, monospace)',
    fontEditorial: 'var(--font-editorial, Playfair Display, serif)',
  },
} as const;
