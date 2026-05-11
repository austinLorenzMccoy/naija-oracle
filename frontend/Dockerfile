# ── Stage 1: deps ───────────────────────────────────────────────────────────
# Install ALL dependencies (including devDeps) so Tailwind v4 / LightningCSS
# native binaries are present during the build step.
FROM node:20-alpine AS deps

# libc6-compat is needed on Alpine (musl) for some native Node modules
RUN apk add --no-cache libc6-compat

WORKDIR /app

COPY package*.json ./

# DO NOT use --only=production here — LightningCSS is a devDependency
# and its musl-compatible native binary must be installed before `next build`
RUN npm ci

# ── Stage 2: builder ─────────────────────────────────────────────────────────
FROM node:20-alpine AS builder

RUN apk add --no-cache libc6-compat

WORKDIR /app

# Copy installed node_modules (with devDeps + correct musl binaries) from deps stage
COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Disable Next.js telemetry during build
ENV NEXT_TELEMETRY_DISABLED=1

RUN npm run build

# ── Stage 3: runner (production image) ───────────────────────────────────────
FROM node:20-alpine AS runner

RUN apk add --no-cache libc6-compat

WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

RUN addgroup -g 1001 -S nodejs
RUN adduser  -S nextjs -u 1001

# Copy only what's needed to serve the exported static output
# (output: 'export' → files land in /app/out)
COPY --from=builder --chown=nextjs:nodejs /app/out    ./out
COPY --from=builder --chown=nextjs:nodejs /app/public ./public

# If you switch away from `output: 'export'` back to a Node server,
# replace the block above with:
#   COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
#   COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static
#   COPY --from=builder --chown=nextjs:nodejs /app/public ./public

USER nextjs

EXPOSE 3000

# Serve the static export with a lightweight HTTP server.
# `serve` is included in node:20-alpine via npx — no extra install needed.
CMD ["npx", "serve", "out", "-l", "3000"]
