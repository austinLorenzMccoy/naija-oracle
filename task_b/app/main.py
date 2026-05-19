"""
Naija Oracle — Task B: Recommendation Engine
FastAPI service for hyper-personalised Nigerian consumer recommendations
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from dotenv import load_dotenv

from app.routers import recommend
from app.database import init_db
from app.services.supabase_client import SupabaseClient

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    try:
        app.state.supabase = SupabaseClient()
    except ValueError as e:
        print(f"Warning: Supabase not configured — running in demo mode: {e}")
        app.state.supabase = None
    yield


app = FastAPI(
    title="Naija Oracle — Task B: Recommendation Engine",
    description=(
        "LLM agent that delivers hyper-personalised recommendations with Nigerian cultural context. "
        "Implements the R4 pipeline: Reason → Retrieve → Rank → Refine. "
        "Handles cold-start via 3-question lifestyle onboarding. "
        "Covers food, fashion, fintech, entertainment, and tech domains."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(recommend.router, prefix="/api/v1", tags=["Task B — Recommendation Engine"])


@app.get("/")
async def root():
    return {
        "task": "Task B — Recommendation Engine",
        "description": "Hyper-personalised Nigerian consumer recommendations via R4 pipeline",
        "docs": "/docs",
        "version": "1.0.0",
        "pipeline": "Reason → Retrieve → Rank → Refine",
        "endpoints": {
            "recommend": "POST /api/v1/recommend",
            "cold_start": "POST /api/v1/recommend/cold-start",
            "catalog": "GET /api/v1/recommend/catalog",
        },
    }


@app.get("/health")
async def health_check():
    from datetime import datetime
    return {
        "status": "healthy",
        "service": "Naija Oracle — Task B",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
    }
