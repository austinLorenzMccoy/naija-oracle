/**
 * Centralised API base URL.
 * - Production: always /api/v1 — Netlify proxies to Render via public/_redirects.
 *   This is hardcoded so NEXT_PUBLIC_API_BASE_URL on Netlify cannot accidentally
 *   bypass the proxy and trigger CORS errors.
 * - Local dev: use NEXT_PUBLIC_API_BASE_URL if set, else http://localhost:8000/api/v1
 */
export const API_BASE =
  process.env.NODE_ENV === 'production'
    ? '/api/v1'
    : (process.env.NEXT_PUBLIC_API_BASE_URL ?? 'http://localhost:8000/api/v1')
