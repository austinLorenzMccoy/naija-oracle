# Naija Oracle Backend

FastAPI backend implementing dual-agent LLM system for Nigerian consumer intelligence.

## Core Components

### **Task A - Persona Simulator**
Generates authentic Nigerian reviews with cultural voice patterns:
- Cultural Voice Index (CVI) with 13+ Nigerian phrases
- Tribe/region mapping (Yoruba, Igbo, Hausa, Pan-Nigerian)
- Pidgin intensity modeling (0.0-1.0 scale)
- Real-time streaming output
- Behavioral fidelity scoring

### **Task B - Recommendation Engine**
Hyper-personalised recommendations with contextual reasoning:
- R4 Pipeline: Reason → Retrieve → Rank → Refine
- Cold-start handling with cultural onboarding
- Multi-turn conversation support
- Cross-domain transfer learning
- Contextual boost factors

### **Cultural Voice Index**
Authentic Nigerian linguistic patterns for cultural authenticity:

| Phrase | Tribe | Context | Sentiment | Rating |
|--------|-------|---------|----------|--------|
| "E sweet me die" | Yoruba | Food | Strong Positive | 5.0⭐ |
| "Wahala be like bicycle" | Pan-Nigerian | Service | Negative | 1.5⭐ |
| "E dey manage" | Pan-Nigerian | General | Mixed | 2.5⭐ |
| "Dem cheat me" | Pan-Nigerian | Price | Strong Negative | 1.0⭐ |
| "The vibe no catch me" | Pan-Nigerian | Ambience | Neutral | 3.0⭐ |
| "Gbam!" | Pan-Nigerian | General | Strong Positive | 4.5⭐ |
| "Slow like NEPA" | Pan-Nigerian | Service | Negative | 2.0⭐ |

## Setup with UV

### Prerequisites
- Python 3.11+
- UV package manager
- Groq API key
- Supabase account

### Installation
```bash
# Install UV (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and setup
cd backend
uv sync

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Activate virtual environment
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows
```

### Development Commands
```bash
# Install with dev dependencies
uv sync --dev

# Run development server
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run tests
uv run pytest

# Code formatting
uv run black .
uv run isort .

# Type checking
uv run mypy app/
```

## API Endpoints

### Task A - Review Simulator
```http
POST /api/v1/simulate-review
Content-Type: application/json
Authorization: Bearer <token>

{
  "user_id": "usr_NG_001",
  "persona_id": "emeka",
  "product": {
    "name": "Chicken Republic Spicy Wings",
    "category": "fast_food",
    "location": "Ikeja",
    "price_tier": "mid"
  },
  "context": {
    "time_of_day": "late_night",
    "occasion": "after_work",
    "recency_of_visit": "first_time"
  }
}
```

### Task B - Recommendations
```http
POST /api/v1/recommend
Content-Type: application/json
Authorization: Bearer <token>

{
  "user_id": "usr_NG_001",
  "persona_id": "emeka",
  "domain": "food",
  "context": {
    "current_time": "Saturday 8PM",
    "location": "Lekki Phase 1",
    "mood_signal": "celebratory",
    "budget_naira": 5000
  },
  "max_recommendations": 5
}
```

### Persona Management
```http
POST /api/v1/personas          # Create persona
GET /api/v1/personas/{id}      # Get persona
PUT /api/v1/personas/{id}      # Update persona
DELETE /api/v1/personas/{id}   # Delete persona
GET /api/v1/personas/{id}/history  # Get persona history
```

## Database Schema

### Personas Table
```sql
CREATE TABLE personas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    name VARCHAR(255) NOT NULL,
    age_range VARCHAR(50),
    city VARCHAR(100),
    lga VARCHAR(100),
    primary_language VARCHAR(50),
    review_style VARCHAR(50),
    avg_rating DECIMAL(3,1),
    pidgin_intensity DECIMAL(3,2),
    cultural_markers TEXT[],
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### Review Generations Table
```sql
CREATE TABLE review_generations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    persona_id UUID NOT NULL,
    product JSONB,
    context JSONB,
    generation JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);
```

## Performance Metrics

### Task A Targets
- BERTScore F1: > 0.82
- ROUGE-L: > 0.35
- RMSE: < 0.75
- CVI Hit Rate: > 60%

### Task B Targets
- NDCG@10: > 0.847
- Hit Rate @5: > 0.78
- Cold-start NDCG: > 0.72

## Services Architecture

### **GroqClient**
- LLaMA-3.1-70B-Versatile model
- Sub-200ms latency
- Streaming support
- Cultural prompt engineering

### **SupabaseClient**
- PostgreSQL database with pgvector
- Row-level security (RLS)
- Real-time subscriptions
- Auto-generated REST APIs

### **CulturalVoiceIndex**
- 13+ Nigerian linguistic patterns
- Tribe/region mapping
- Pidgin intensity scoring
- Cultural authenticity evaluation

### **EmbeddingService**
- SentenceTransformer embeddings
- Vector similarity search
- Persona clustering
- Cross-domain transfer

## Docker Configuration

### Backend Container
```dockerfile
FROM python:3.11-slim
WORKDIR /app

# Install UV
RUN pip install uv

# Install dependencies
COPY pyproject.toml ./
RUN uv pip install --system -e .

# Copy application
COPY . .

# Run server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose
```yaml
backend:
  build: ./backend
  environment:
    - GROQ_API_KEY=${GROQ_API_KEY}
    - SUPABASE_URL=${SUPABASE_URL}
    - SUPABASE_SERVICE_KEY=${SUPABASE_SERVICE_KEY}
  ports:
    - "8000:8000"
  depends_on:
    - database
```

## Testing

### Unit Tests
```bash
# Run all tests
uv run pytest tests/ -v

# With coverage
uv run pytest tests/ -v --cov=app --cov-report=html

# Specific test
uv run pytest tests/test_persona_simulator.py -v
```

### Integration Tests
```bash
# Test API endpoints
uv run pytest tests/integration/ -v

# Test database operations
uv run pytest tests/test_database.py -v
```

### Load Testing
```bash
# Performance testing
uv run locust -f tests/locustfile.py --host=http://localhost:8000
```

## Monitoring

### Health Checks
```bash
# Application health
curl http://localhost:8000/health

# Database health
curl http://localhost:8000/health/db

# External services
curl http://localhost:8000/health/groq
curl http://localhost:8000/health/supabase
```

### Metrics Collection
- Response times
- Error rates
- Token usage
- Database performance
- Cultural fidelity scores

## Troubleshooting

### Common Issues

**Groq API Rate Limits**
```bash
# Check rate limit status
curl -H "Authorization: Bearer $GROQ_API_KEY" https://api.groq.com/v1/rate_limits
```

**Database Connection**
```bash
# Test database connection
uv run python -c "from app.database import init_db; import asyncio; asyncio.run(init_db())"
```

**Cultural Voice Index**
```bash
# Test CVI anchors
uv run python -c "from app.services.cultural_voice_index import CulturalVoiceIndex; cvi = CulturalVoiceIndex(); print(len(cvi.get_all_anchors()))"
```

### Debug Mode
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
uv run uvicorn app.main:app --reload --log-level debug
```

## Contributing

1. Follow PEP 8 style guidelines
2. Add type hints to all functions
3. Write comprehensive tests
4. Update documentation
5. Submit pull requests with clear descriptions

## License

Apache 2.0 - See LICENSE file for details
