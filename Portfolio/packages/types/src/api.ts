/**
 * API communication and authentication contracts.
 */

export interface HealthResponse {
  status: 'ok';
  service?: string;
  version?: string;
  timestamp?: string;
}

export interface AdminUser {
  id: string;
  email: string;
  role: 'admin';
}

export interface AuthSession {
  user: AdminUser;
  token: string;
  expires_at: number;
}

export interface RevalidationPayload {
  secret: string;
  path: string;
}

export interface ApiResponse<T = unknown> {
  data?: T;
  error?: string;
  message?: string;
}
