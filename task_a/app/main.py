"""
Naija Oracle — Task A: Persona Simulator
FastAPI service for Nigerian consumer voice simulation and authentic review generation
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from dotenv import load_dotenv

from app.routers import simulate, personas
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
    title="Naija Oracle — Task A: Persona Simulator",
    description=(
        "LLM agent that simulates authentic Nigerian consumer voices. "
        "Generates hyper-personalised product reviews grounded in the Cultural Voice Index (CVI). "
        "Covers 15 personas across Lagos, Kano, Abuja, Port Harcourt, Enugu, Ibadan, and Onitsha."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://naija-oracle.netlify.app",
        "http://localhost:3000",
        "http://localhost:3001",
    ],
    allow_origin_regex=r"https://.*\.netlify\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(simulate.router, prefix="/api/v1", tags=["Task A — Review Simulator"])
app.include_router(personas.router, prefix="/api/v1", tags=["Personas"])


@app.get("/")
async def root():
    return {
        "task": "Task A — Persona Simulator",
        "description": "Nigerian consumer voice simulation with Cultural Voice Index",
        "docs": "/docs",
        "version": "1.0.0",
        "endpoints": {
            "simulate_review": "POST /api/v1/simulate-review",
            "personas": "GET /api/v1/personas",
            "persona_detail": "GET /api/v1/personas/{id}",
        },
    }


@app.get("/health")
async def health_check():
    from datetime import datetime
    return {
        "status": "healthy",
        "service": "Naija Oracle — Task A",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
    }
