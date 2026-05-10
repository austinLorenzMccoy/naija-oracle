# Naija Oracle Frontend

A sophisticated Next.js application for Nigerian consumer insights and persona simulation, built with modern web technologies and designed to integrate seamlessly with the Naija Oracle backend and ML training systems.

## 🏗️ Architecture Overview

### Technology Stack
- **Framework**: Next.js 16.2.4 with App Router
- **Styling**: Tailwind CSS 4.2.0 with custom Oracle color palette
- **UI Components**: Radix UI primitives with shadcn/ui
- **State Management**: React hooks and context
- **Data Visualization**: Recharts
- **Icons**: Lucide React
- **Analytics**: Vercel Analytics
- **Package Manager**: pnpm

### Project Structure
```
frontend/
├── app/                    # Next.js App Router pages
│   ├── dashboard/         # Analytics dashboard
│   ├── simulate/           # Review simulator interface
│   ├── personas/           # Persona management
│   ├── recommend/          # Recommendation engine
│   ├── analytics/          # Performance analytics
│   ├── reports/            # Generated reports
│   └── settings/           # Configuration
├── components/            # Reusable UI components
│   ├── ui/                # Base UI primitives
│   ├── sidebar.tsx        # Navigation sidebar
│   ├── header.tsx         # Page header
│   └── theme-provider.tsx # Theme context
├── lib/                   # Utility functions
├── hooks/                 # Custom React hooks
├── public/               # Static assets
└── styles/               # Global styles
```

## 🎨 Design System

### Oracle Color Palette
The application uses a custom dark theme inspired by Nigerian cultural aesthetics:

- **Oracle Void** (`#0C0B09`) - Primary background
- **Oracle Charcoal** (`#1A1916`) - Secondary background
- **Oracle Amber** (`#F5831F`) - Primary accent
- **Oracle Terra** (`#C94020`) - Secondary accent
- **Oracle Green** (`#2DB37A`) - Success state

### Typography
- **DM Sans**: Primary body font
- **Fraunces**: Display and headings (serif)
- **JetBrains Mono**: Code and data display

## 🚀 Core Features

### 1. Dashboard (`/dashboard`)
Real-time analytics and performance metrics:
- Review generation statistics
- BERTScore and NDCG@10 metrics
- CVI (Cultural Voice Index) hit rates
- Interactive performance charts
- Model version tracking

### 2. Review Simulator (`/simulate`)
Advanced persona-based review generation:
- Product configuration interface
- Persona selection (city, language, pidgin intensity)
- Real-time simulation with visual feedback
- Behavioral fidelity scoring
- Export functionality (JSON, library save)

### 3. Persona Management (`/personas`)
Comprehensive persona library:
- 500+ pre-configured Nigerian personas
- Regional and demographic filtering
- Performance metrics per persona
- Detailed persona profiles
- Cultural context visualization

### 4. Recommendation Engine (`/recommend`)
Hyper-personalized recommendations:
- Context-aware suggestions
- Cultural preference matching
- Location-based recommendations
- Reasoning explanations

### 5. Analytics (`/analytics`)
Deep performance insights:
- Model performance tracking
- User engagement metrics
- Cultural accuracy analysis
- A/B testing results

## 🔌 Backend Integration

### API Configuration
The frontend connects to the Naija Oracle backend through these endpoints:

```typescript
// Environment variables
NEXT_PUBLIC_API_BASE_URL=https://naija-oracle.onrender.com/api/v1
NEXT_PUBLIC_WS_URL=wss://naija-oracle.onrender.com/ws
```

### Key API Endpoints
- `POST /api/v1/simulate` - Generate reviews
- `GET /api/v1/personas` - Fetch persona library
- `POST /api/v1/recommend` - Get recommendations
- `GET /api/v1/analytics` - Performance metrics
- `WebSocket /ws` - Real-time updates

### WebSocket Integration
Real-time updates for:
- Simulation progress
- Live metrics
- Model training status
- System notifications

## 🤖 ML Training Integration

### Model Monitoring
The frontend monitors ML training progress through:
- Real-time training metrics
- Model version tracking
- Performance comparisons
- Hyperparameter visualization

### Training Data Interface
- Upload training datasets
- Validate data quality
- Preview training samples
- Cultural context annotations

### Model Evaluation
- BERTScore tracking
- NDCG@10 measurements
- Cultural Voice Index (CVI)
- A/B testing framework

## 🌍 Deployment

### Environment Setup
```bash
# Install dependencies
pnpm install

# Configure environment variables
cp .env.example .env.local

# Development server
pnpm dev

# Production build
pnpm build
pnpm start
```

### Environment Variables
```env
# API Configuration
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws

# Analytics
NEXT_PUBLIC_VERCEL_ANALYTICS_ID=your_analytics_id

# Feature Flags
NEXT_PUBLIC_ENABLE_ANALYTICS=true
NEXT_PUBLIC_ENABLE_WEBSOCKET=true
```

### Production Deployment
The application is optimized for deployment on:
- **Vercel** (recommended for Next.js)
- **Netlify** (static export)
- **Render** (full-stack)
- **AWS Amplify** (serverless)

## 📊 Performance Optimization

### Code Splitting
- Automatic route-based splitting
- Component-level lazy loading
- Dynamic imports for heavy components

### Caching Strategy
- API response caching
- Static asset optimization
- Image optimization with Next.js Image

### Bundle Optimization
- Tree shaking for unused dependencies
- Minification and compression
- Critical CSS inlining

## 🔧 Development Workflow

### Component Development
```typescript
// Example component structure
import { cn } from '@/lib/utils'

interface ComponentProps {
  // Props definition
}

export default function Component({ props }: ComponentProps) {
  return (
    <div className={cn('base-styles', 'conditional-styles')}>
      {/* Component content */}
    </div>
  )
}
```

### Styling Guidelines
- Use Tailwind CSS classes
- Leverage the Oracle color palette
- Maintain consistency with design tokens
- Responsive design first approach

### State Management
```typescript
// Custom hook example
export function useSimulation() {
  const [state, setState] = useState(initialState)
  
  const simulate = useCallback(async (params) => {
    // Simulation logic
  }, [])
  
  return { state, simulate }
}
```

## 🧪 Testing

### Unit Testing
```bash
# Run tests
pnpm test

# Test coverage
pnpm test:coverage
```

### E2E Testing
```bash
# Playwright tests
pnpm test:e2e

# Visual regression
pnpm test:visual
```

## 📈 Monitoring & Analytics

### Performance Metrics
- Core Web Vitals tracking
- User interaction analytics
- Error boundary reporting
- API response time monitoring

### User Analytics
- Page view tracking
- Feature usage analytics
- Conversion funnel analysis
- User journey mapping

## 🔐 Security

### Data Protection
- Input sanitization and validation
- XSS prevention mechanisms
- CSRF protection
- Secure cookie handling

### API Security
- JWT token authentication
- Rate limiting
- Request validation
- HTTPS enforcement

## 🚀 Future Enhancements

### Planned Features
- Real-time collaboration
- Advanced persona customization
- Multi-language support
- Mobile app development
- API marketplace integration

### Technical Improvements
- Server-side rendering optimization
- Progressive Web App (PWA)
- Offline functionality
- Advanced caching strategies

## 🤝 Contributing

### Development Setup
1. Clone the repository
2. Install dependencies with `pnpm install`
3. Configure environment variables
4. Start development server with `pnpm dev`

### Code Standards
- TypeScript for type safety
- ESLint for code quality
- Prettier for formatting
- Conventional commits

### Pull Request Process
1. Create feature branch
2. Implement changes with tests
3. Submit pull request
4. Code review and approval
5. Merge to main branch

## 📞 Support

For technical support and questions:
- Create an issue in the repository
- Join our Discord community
- Email: support@naijaoracle.com
- Documentation: https://docs.naijaoracle.com

---

**Built with ❤️ for the Nigerian market and global consumers**
