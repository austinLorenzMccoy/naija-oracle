/**
 * Centralised API base URL.
 * - Production (Netlify): requests go to /api/v1 — Netlify proxies to Render
 *   via public/_redirects so CORS is never an issue
 * - Local dev: set NEXT_PUBLIC_API_BASE_URL=http://localhost:8003/api/v1 in .env.local
 */
export const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE_URL || '/api/v1'
