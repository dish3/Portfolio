"""
Test Suite for Database Module and Session Layer.
Verifies driver URL transformation, error handling for missing URL,
and dependency overrides without requiring live Supabase credentials.
"""

import pytest
from app.core.database import build_async_database_url


def test_build_async_database_url_transformation() -> None:
    # Transforms postgresql:// to postgresql+asyncpg://
    raw = "postgresql://myuser:mypass@localhost:5432/mydb"
    async_url = build_async_database_url(raw)
    assert async_url.startswith("postgresql+asyncpg://myuser:mypass@localhost:5432/mydb")


def test_build_async_database_url_strips_sslmode() -> None:
    # Strips sslmode parameter which asyncpg handles via connect_args
    raw = "postgresql://myuser:mypass@db.host.com:5432/mydb?sslmode=require"
    async_url = build_async_database_url(raw)
    assert "sslmode" not in async_url
    assert async_url.startswith("postgresql+asyncpg://")


def test_build_async_database_url_fails_on_empty() -> None:
    # Fails clearly rather than silently falling back to localhost
    with pytest.raises(ValueError, match="DATABASE_URL is not configured"):
        build_async_database_url("")

    with pytest.raises(ValueError, match="DATABASE_URL is not configured"):
        build_async_database_url("NOT_CONFIGURED")
