import path from 'path'
import { fileURLToPath } from 'url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))

/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  distDir: 'out',
  typescript: {
    ignoreBuildErrors: true,
  },
  images: {
    unoptimized: true,
  },
  trailingSlash: true,

  // ── Turbopack (Next.js 16 default bundler) ──────────────────────────
  // Move the @ alias here — webpack config is ignored when Turbopack is active
  turbopack: {
    resolveAlias: {
      '@': path.resolve(__dirname, '.'),
    },
  },

  // ── Remove the webpack block entirely ───────────────────────────────
  // Next.js 16 with Turbopack enabled will throw:
  //   "This build is using Turbopack, with a webpack config and no turbopack config"
  // The alias above handles what webpack was doing.
}

export default nextConfig
