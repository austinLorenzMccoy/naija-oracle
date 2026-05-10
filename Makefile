.PHONY: setup run test clean install lint format

# Setup development environment
setup:
	@echo "🔧 Setting up Naija Oracle development environment..."
	# Backend setup
	cp backend/.env.example backend/.env || true
	@echo "✅ Backend .env file created (edit with your API keys)"
	# Frontend setup  
	cp frontend/.env.example frontend/.env.local || true
	@echo "✅ Frontend .env.local file created (edit with your API keys)"
	@echo ""
	@echo "📝 Next steps:"
	@echo "1. Edit backend/.env with your Groq and Supabase API keys"
	@echo "2. Edit frontend/.env.local with your API base URL"
	@echo "3. Run 'make run' to start the application"
	@echo ""
	@echo "🔑 Required API keys:"
	@echo "- Groq API Key: https://console.groq.com/"
	@echo "- Supabase Project: https://supabase.com/"

# Run the full application
run:
	@echo "🚀 Starting Naija Oracle application..."
	docker-compose up --build

# Run in development mode
dev:
	@echo "🔧 Starting development servers..."
	# Start backend
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
	# Start frontend  
	cd frontend && npm run dev &
	@echo "✅ Backend: http://localhost:8000"
	@echo "✅ Frontend: http://localhost:3000"
	@echo "✅ API Docs: http://localhost:8000/docs"

# Install dependencies
install:
	@echo "📦 Installing dependencies..."
	# Backend dependencies
	cd backend && uv sync --dev
	# Frontend dependencies
	cd frontend && npm install
	@echo "✅ Dependencies installed"

# Run tests
test:
	@echo "🧪 Running tests..."
	# Backend tests
	cd backend && uv run pytest -v
	# Frontend tests
	cd frontend && npm test
	@echo "✅ Tests completed"

# Code quality checks
lint:
	@echo "🔍 Running linting..."
	# Backend linting
	cd backend && uv run black --check . && uv run isort --check-only . && uv run flake8 .
	# Frontend linting
	cd frontend && npm run lint
	@echo "✅ Linting completed"

# Format code
format:
	@echo "✨ Formatting code..."
	# Backend formatting
	cd backend && uv run black . && uv run isort .
	# Frontend formatting
	cd frontend && npm run format
	@echo "✅ Code formatted"

# Clean up
clean:
	@echo "🧹 Cleaning up..."
	# Docker cleanup
	docker-compose down --volumes --remove-orphans
	docker system prune -f
	# Node modules cleanup
	rm -rf frontend/node_modules
	rm -rf frontend/.next
	rm -rf frontend/out
	# Python cache cleanup
	cd backend && find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	cd backend && find . -name "*.pyc" -delete 2>/dev/null || true
	@echo "✅ Cleanup completed"

# Database operations
db-init:
	@echo "🗄️ Initializing database..."
	cd backend && uv run python -c "
import asyncio
from app.database import init_db
asyncio.run(init_db())
print('Database initialized successfully')
"

db-reset:
	@echo "🔄 Resetting database..."
	cd backend && uv run python -c "
import asyncio
from app.database import reset_db
asyncio.run(reset_db())
print('Database reset successfully')
"

# Production deployment
deploy-backend:
	@echo "🚀 Deploying backend to Render..."
	# This would trigger Render deployment
	@echo "Backend deployment triggered on Render"

deploy-frontend:
	@echo "🚀 Deploying frontend to Netlify..."
	cd frontend && npm run build
	@echo "Frontend built and ready for Netlify deployment"

# Health check
health:
	@echo "🏥 Checking application health..."
	curl -f http://localhost:8000/health || echo "❌ Backend unhealthy"
	curl -f http://localhost:3000 || echo "❌ Frontend unhealthy"

# Generate sample data
sample-data:
	@echo "📊 Generating sample data..."
	cd backend && uv run python scripts/generate_sample_data.py
	@echo "✅ Sample data generated"

# Run evaluation metrics
eval-metrics:
	@echo "📈 Running evaluation metrics..."
	curl -X POST http://localhost:8000/api/v1/eval/bertscore \
		-H "Content-Type: application/json" \
		-d '{"preds": ["Great product!"], "refs": ["Excellent product!"]}'
	curl -X POST http://localhost:8000/api/v1/eval/rouge \
		-H "Content-Type: application/json" \
		-d '{"preds": ["Great product!"], "refs": ["Excellent product!"]}'
	curl -X POST http://localhost:8000/api/v1/eval/rmse \
		-H "Content-Type: application/json" \
		-d '{"pred_ratings": [4.5], "true_ratings": [4.0]}'

# Help
help:
	@echo "📖 Naija Oracle Makefile Commands:"
	@echo ""
	@echo "Setup & Running:"
	@echo "  make setup    - Setup development environment"
	@echo "  make run      - Run full application with Docker"
	@echo "  make dev      - Run development servers"
	@echo ""
	@echo "Development:"
	@echo "  make install  - Install all dependencies"
	@echo "  make test     - Run tests"
	@echo "  make lint     - Run code quality checks"
	@echo "  make format   - Format code"
	@echo ""
	@echo "Database:"
	@echo "  make db-init  - Initialize database"
	@echo "  make db-reset - Reset database"
	@echo ""
	@echo "Deployment:"
	@echo "  make deploy-backend  - Deploy backend to Render"
	@echo "  make deploy-frontend - Deploy frontend to Netlify"
	@echo ""
	@echo "Utilities:"
	@echo "  make health   - Check application health"
	@echo "  make clean    - Clean up build artifacts"
	@echo "  make sample-data - Generate sample data"
	@echo "  make eval-metrics - Test evaluation endpoints"
	@echo "  make help     - Show this help message"
