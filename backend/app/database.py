"""
Database initialization and connection management
"""

import asyncio
from typing import Optional
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.config import settings

# Database models
Base = declarative_base()

# Create engine
database_url = settings.DATABASE_URL or "sqlite+aiosqlite:///./naija_oracle.db"

# Ensure asyncpg driver for PostgreSQL
if database_url.startswith("postgresql://"):
    database_url = database_url.replace("postgresql://", "postgresql+asyncpg://", 1)
    
    # Fix DuplicatePreparedStatementError with Supabase pooler
    if "pooler.supabase.com" in database_url and ":6543/" in database_url:
        # Switch to direct connection port 5432 and disable prepared statement cache
        database_url = database_url.replace(":6543/", ":5432/")
        database_url += "?prepared_statement_cache_size=0"

# Try to create async engine with proper fallback
try:
    engine = create_async_engine(
        database_url,
        echo=True,
        poolclass=StaticPool,
        connect_args={"check_same_thread": False} if "sqlite" in database_url else {}
    )
except Exception as e:
    print(f"Warning: Could not create async engine: {e}")
    print("Using fallback synchronous engine")
    # Fallback to synchronous engine for testing
    sync_url = database_url.replace("sqlite+aiosqlite://", "sqlite://")
    from sqlalchemy import create_engine as sync_create_engine
    engine = sync_create_engine(
        sync_url,
        echo=True,
        poolclass=StaticPool,
        connect_args={"check_same_thread": False} if "sqlite" in sync_url else {}
    )

# Session factory
async_session_maker = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def init_db():
    """Initialize database tables"""
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except Exception as e:
        print(f"Warning: Could not initialize database: {e}")

async def get_db() -> AsyncSession:
    """Get database session"""
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()

async def close_db():
    """Close database connection"""
    await engine.dispose()
