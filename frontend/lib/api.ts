/**
 * Centralised API base URL.
 * - Production (Netlify): set NEXT_PUBLIC_API_BASE_URL in Netlify dashboard
 * - Local dev: set NEXT_PUBLIC_API_BASE_URL=http://localhost:8003/api/v1 in .env.local
 * - Fallback: live Render deployment so the Netlify build works without any env var
 */
export const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE_URL || 'https://naija-oracle.onrender.com/api/v1'
