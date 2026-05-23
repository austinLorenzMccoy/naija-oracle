/**
 * Centralised API base URL.
 * - Netlify production: NEXT_PUBLIC_API_BASE_URL is unset → /api/v1
 *   Netlify _redirects proxies /api/* to Render, keeping CORS off the frontend.
 * - Docker Compose: NEXT_PUBLIC_API_BASE_URL=http://localhost:9000/api/v1
 *   Baked in at build time via ARG → used directly by the browser.
 * - Local dev: NEXT_PUBLIC_API_BASE_URL if set, else http://localhost:8000/api/v1
 */
export const API_BASE =
  process.env.NODE_ENV === 'production'
    ? (process.env.NEXT_PUBLIC_API_BASE_URL?.startsWith('http')
        ? process.env.NEXT_PUBLIC_API_BASE_URL
        : '/api/v1')
    : (process.env.NEXT_PUBLIC_API_BASE_URL ?? 'http://localhost:8000/api/v1')
