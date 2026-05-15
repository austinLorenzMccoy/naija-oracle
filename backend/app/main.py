"""
Naija Oracle Backend API
FastAPI application for persona simulation and recommendation engine
"""

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

from app.routers import simulate, recommend, personas, auth, evaluation
from app.database import init_db
from app.services.supabase_client import SupabaseClient

# Try to import evaluator, but make it optional
try:
    from app.ml.evaluator import NaijaOracleEvaluator
    evaluator_available = True
except ImportError as e:
    print(f"Warning: ML Evaluator not available: {e}")
    evaluator_available = False

# Load environment variables
load_dotenv()

# Security
security = HTTPBearer()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database and services on startup"""
    await init_db()
    
    # Try to initialize Supabase, but don't fail if credentials are missing
    try:
        app.state.supabase = SupabaseClient()
    except ValueError as e:
        print(f"Warning: Supabase not configured: {e}")
        print("Running in demo mode without database persistence")
        app.state.supabase = None
    
    # Only initialize evaluator if ML dependencies are available
    if evaluator_available:
        app.state.evaluator = NaijaOracleEvaluator()
    
    yield
    # Cleanup if needed

app = FastAPI(
    title="Naija Oracle API",
    description="LLM agents that simulate Nigerian consumer voices and deliver hyper-personalised recommendations",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(simulate.router, prefix="/api/v1", tags=["Task A - Review Simulator"])
app.include_router(recommend.router, prefix="/api/v1", tags=["Task B - Recommendations"])
app.include_router(personas.router, prefix="/api/v1", tags=["Personas"])
app.include_router(evaluation.router, prefix="/api/v1", tags=["Evaluation"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Naija Oracle API",
        "description": "The oracle that speaks Naija",
        "docs": "/docs",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    from datetime import datetime
    return {
        "status": "healthy",
        "service": "Naija Oracle Backend",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
        "ml_available": evaluator_available
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
