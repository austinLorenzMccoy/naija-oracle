# Frontend Deployment Guide

This guide covers deploying the Naija Oracle frontend to various platforms and integrating it with the backend and ML training systems.

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ installed
- pnpm package manager
- Access to backend API endpoints
- Environment variables configured

### Local Development
```bash
# Clone and setup
git clone <repository-url>
cd frontend
pnpm install

# Configure environment
cp .env.example .env.local
# Edit .env.local with your configuration

# Start development server
pnpm dev
```

## 🌍 Production Deployment

### 1. Vercel (Recommended)

#### Automatic Deployment
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy to Vercel
vercel --prod

# Link to GitHub for automatic deployments
vercel link
```

#### Configuration
Create `vercel.json`:
```json
{
  "version": 2,
  "buildCommand": "pnpm build",
  "outputDirectory": ".next",
  "installCommand": "pnpm install",
  "framework": "nextjs",
  "env": {
    "NEXT_PUBLIC_API_BASE_URL": "https://naija-oracle.onrender.com/api/v1",
    "NEXT_PUBLIC_WS_URL": "wss://naija-oracle.onrender.com/ws"
  }
}
```

### 2. Netlify

#### Static Export
```bash
# Update next.config.mjs for static export
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  trailingSlash: true,
  images: {
    unoptimized: true
  }
}

export default nextConfig
```

#### Deploy
```bash
# Build for static export
pnpm build

# Deploy to Netlify
netlify deploy --prod --dir=out
```

### 3. Render

#### Docker Deployment
```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package.json pnpm-lock.yaml ./
RUN npm install -g pnpm
RUN pnpm install --frozen-lockfile

COPY . .
RUN pnpm build

EXPOSE 3000

CMD ["pnpm", "start"]
```

#### Render Configuration
- **Build Command**: `pnpm build`
- **Start Command**: `pnpm start`
- **Health Check Path**: `/api/health`

### 4. AWS Amplify

#### Amplify Configuration
```yaml
version: 1
frontend:
  phases:
    preBuild:
      commands:
        - npm install -g pnpm
        - pnpm install --frozen-lockfile
    build:
      commands:
        - pnpm build
  artifacts:
    baseDirectory: .next
    files:
      - '**/*'
  cache:
    paths:
      - node_modules/**/*
```

## 🔌 Backend Integration

### Environment Variables
```env
# Production
NEXT_PUBLIC_API_BASE_URL=https://naija-oracle.onrender.com/api/v1
NEXT_PUBLIC_WS_URL=wss://naija-oracle.onrender.com/ws

# Development
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws

# Feature Flags
NEXT_PUBLIC_ENABLE_ANALYTICS=true
NEXT_PUBLIC_ENABLE_WEBSOCKET=true
NEXT_PUBLIC_ENABLE_MOCK_DATA=false
```

### API Client Configuration
```typescript
// lib/api.ts
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api/v1'

export const apiClient = {
  simulate: async (params: SimulationParams) => {
    const response = await fetch(`${API_BASE_URL}/simulate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(params)
    })
    return response.json()
  },
  
  getPersonas: async () => {
    const response = await fetch(`${API_BASE_URL}/personas`)
    return response.json()
  }
}
```

### WebSocket Integration
```typescript
// hooks/useWebSocket.ts
export function useWebSocket(url: string) {
  const [socket, setSocket] = useState<WebSocket | null>(null)
  
  useEffect(() => {
    const ws = new WebSocket(url)
    setSocket(ws)
    
    return () => ws.close()
  }, [url])
  
  return socket
}
```

## 🤖 ML Training Integration

### Training Progress Monitoring
```typescript
// hooks/useTrainingProgress.ts
export function useTrainingProgress(modelId: string) {
  const [progress, setProgress] = useState(0)
  const [metrics, setMetrics] = useState({})
  
  useEffect(() => {
    const ws = new WebSocket(`${WS_URL}/training/${modelId}`)
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data)
      setProgress(data.progress)
      setMetrics(data.metrics)
    }
    
    return () => ws.close()
  }, [modelId])
  
  return { progress, metrics }
}
```

### Model Performance Tracking
```typescript
// components/ModelMetrics.tsx
export function ModelMetrics({ modelId }: { modelId: string }) {
  const { data: metrics } = useSWR(
    `/api/models/${modelId}/metrics`,
    fetcher
  )
  
  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      <MetricCard
        label="BERTScore"
        value={metrics?.bertScore}
        format="decimal"
      />
      <MetricCard
        label="NDCG@10"
        value={metrics?.ndcg}
        format="decimal"
      />
      <MetricCard
        label="CVI"
        value={metrics?.cvi}
        format="percentage"
      />
      <MetricCard
        label="Latency"
        value={metrics?.latency}
        format="duration"
      />
    </div>
  )
}
```

## 📊 Performance Optimization

### Build Optimization
```javascript
// next.config.mjs
/** @type {import('next').NextConfig} */
const nextConfig = {
  // Optimization
  swcMinify: true,
  compiler: {
    removeConsole: process.env.NODE_ENV === 'production'
  },
  
  // Image optimization
  images: {
    domains: ['example.com'],
    formats: ['image/webp', 'image/avif']
  },
  
  // Bundle analysis
  webpack: (config, { dev, isServer }) => {
    if (!dev && !isServer) {
      config.optimization.splitChunks.cacheGroups = {
        ...config.optimization.splitChunks.cacheGroups,
        vendor: {
          test: /[\\/]node_modules[\\/]/,
          name: 'vendors',
          chunks: 'all',
        }
      }
    }
    return config
  }
}

export default nextConfig
```

### Caching Strategy
```typescript
// lib/cache.ts
export const cacheConfig = {
  // API responses
  api: {
    ttl: 5 * 60 * 1000, // 5 minutes
    staleWhileRevalidate: 60 * 1000, // 1 minute
  },
  
  // Static assets
  static: {
    ttl: 24 * 60 * 60 * 1000, // 24 hours
  },
  
  // User data
  user: {
    ttl: 30 * 60 * 1000, // 30 minutes
  }
}
```

## 🔐 Security Configuration

### CORS Setup
```typescript
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  const response = NextResponse.next()
  
  // CORS headers
  response.headers.set('Access-Control-Allow-Origin', '*')
  response.headers.set('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
  response.headers.set('Access-Control-Allow-Headers', 'Content-Type, Authorization')
  
  // Security headers
  response.headers.set('X-Frame-Options', 'DENY')
  response.headers.set('X-Content-Type-Options', 'nosniff')
  response.headers.set('Referrer-Policy', 'origin-when-cross-origin')
  
  return response
}
```

### Environment Validation
```typescript
// lib/env.ts
import { z } from 'zod'

const envSchema = z.object({
  NEXT_PUBLIC_API_BASE_URL: z.string().url(),
  NEXT_PUBLIC_WS_URL: z.string().url(),
  NEXT_PUBLIC_ENABLE_ANALYTICS: z.boolean().default(false),
})

export const env = envSchema.parse(process.env)
```

## 📈 Monitoring & Analytics

### Performance Monitoring
```typescript
// lib/analytics.ts
export const analytics = {
  track: (event: string, properties?: Record<string, any>) => {
    if (typeof window !== 'undefined' && process.env.NEXT_PUBLIC_ENABLE_ANALYTICS) {
      // Analytics implementation
      window.gtag?.('event', event, properties)
    }
  },
  
  pageView: (path: string) => {
    analytics.track('page_view', { path })
  }
}
```

### Error Tracking
```typescript
// components/ErrorBoundary.tsx
export class ErrorBoundary extends Component {
  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    // Log error to monitoring service
    console.error('Error caught by boundary:', error, errorInfo)
    
    // Track error in analytics
    analytics.track('error', {
      message: error.message,
      stack: error.stack,
      component: errorInfo.componentStack
    })
  }
}
```

## 🧪 Testing Strategy

### Unit Tests
```bash
# Run unit tests
pnpm test

# Run with coverage
pnpm test:coverage

# Watch mode
pnpm test:watch
```

### E2E Tests
```bash
# Run E2E tests
pnpm test:e2e

# Run on specific browser
pnpm test:e2e --browser=chromium

# Run in headed mode
pnpm test:e2e --headed
```

### Performance Tests
```bash
# Lighthouse CI
pnpm lighthouse

# Bundle analysis
pnpm analyze
```

## 🔧 Troubleshooting

### Common Issues

#### Build Failures
```bash
# Clear Next.js cache
rm -rf .next

# Clear node modules
rm -rf node_modules pnpm-lock.yaml
pnpm install

# Rebuild
pnpm build
```

#### API Connection Issues
```bash
# Check API connectivity
curl -X GET http://localhost:8000/api/v1/health

# Check WebSocket connection
wscat -c ws://localhost:8000/ws
```

#### Performance Issues
```bash
# Analyze bundle size
pnpm analyze

# Check Core Web Vitals
pnpm lighthouse
```

### Debug Mode
```typescript
// Enable debug logging
if (process.env.NODE_ENV === 'development') {
  console.log('Debug info:', debugData)
}
```

## 📋 Deployment Checklist

### Pre-deployment
- [ ] Environment variables configured
- [ ] API endpoints tested
- [ ] Build successful locally
- [ ] Tests passing
- [ ] Performance benchmarks met
- [ ] Security audit completed

### Post-deployment
- [ ] Health checks passing
- [ ] Analytics tracking working
- [ ] Error monitoring configured
- [ ] Performance metrics collected
- [ ] User acceptance testing
- [ ] Documentation updated

---

## 📞 Support

For deployment issues:
- Check the troubleshooting section
- Review deployment logs
- Contact the development team
- Create an issue in the repository

**Happy deploying! 🚀**
