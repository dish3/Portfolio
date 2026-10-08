"""
Database Engine & Async Session Management.
Uses SQLAlchemy 2.0 and asyncpg for PostgreSQL/Supabase connections.
Sourced from NOVA_01 §2 and NOVA_06 §15.
"""

from typing import AsyncGenerator, Optional
from urllib.parse import urlparse, parse_qs, urlunparse, urlencode
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)
from app.core.config import settings
from app.core.logging import logger


def build_async_database_url(raw_url: str) -> str:
    """
    Transforms standard PostgreSQL URL to postgresql+asyncpg:// format,
    stripping conflicting driver parameters (like sslmode) for asyncpg compatibility.
    """
    if not raw_url or raw_url.strip() in ("", "NOT_CONFIGURED"):
        raise ValueError(
            "DATABASE_URL is not configured. Please define a valid PostgreSQL "
            "connection string in .env (e.g. Supabase connection pooler)."
        )

    url = raw_url.strip()

    # Ensure scheme is postgresql+asyncpg
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql+asyncpg://", 1)
    elif url.startswith("postgresql://") and not url.startswith("postgresql+asyncpg://"):
        url = url.replace("postgresql://", "postgresql+asyncpg://", 1)

    # Parse and strip any sslmode query param which asyncpg handles in connect_args
    parsed = urlparse(url)
    if parsed.query:
        query_params = parse_qs(parsed.query)
        query_params.pop("sslmode", None)
        new_query = urlencode(query_params, doseq=True)
        url = urlunparse(parsed._replace(query=new_query))

    return url


_engine: Optional[AsyncEngine] = None
_session_factory: Optional[async_sessionmaker[AsyncSession]] = None


def get_engine() -> AsyncEngine:
    """
    Lazily creates and returns the singleton AsyncEngine instance.
    Configured for high resilience with Supabase connection pooler.
    """
    global _engine, _session_factory
    if _engine is None:
        async_url = build_async_database_url(settings.DATABASE_URL)
        connect_args = {
            "ssl": "require",
            "server_settings": {
                "statement_cache_size": "0",  # Disables prepared statements for PgBouncer/Supavisor
            },
        }
        _engine = create_async_engine(
            async_url,
            echo=(settings.LOG_LEVEL.upper() == "DEBUG"),
            pool_pre_ping=True,
            connect_args=connect_args,
        )
        _session_factory = async_sessionmaker(
            bind=_engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False,
        )
        logger.info("SQLAlchemy 2.x asyncpg engine initialized successfully.")
    return _engine


def get_session_factory() -> async_sessionmaker[AsyncSession]:
    """Returns the async session factory."""
    get_engine()
    assert _session_factory is not None
    return _session_factory


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency that yields an active async SQLAlchemy session per request.
    Rolls back automatically on unhandled exception and closes cleanly.
    """
    factory = get_session_factory()
    async with factory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
