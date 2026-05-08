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

from app.routers import simulate, recommend, personas, auth
from app.database import init_db
from app.ml.evaluator import NaijaOracleEvaluator
from app.services.supabase_client import SupabaseClient

# Load environment variables
load_dotenv()

# Security
security = HTTPBearer()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database and services on startup"""
    await init_db()
    app.state.supabase = SupabaseClient()
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
    return {
        "status": "healthy",
        "service": "Naija Oracle Backend",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
