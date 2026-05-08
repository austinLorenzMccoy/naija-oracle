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

engine = create_async_engine(
    database_url,
    echo=True,
    poolclass=StaticPool,
    connect_args={"check_same_thread": False} if "sqlite" in database_url else {}
)

# Session factory
async_session_maker = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def init_db():
    """Initialize database tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

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
