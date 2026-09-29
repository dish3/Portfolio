"""
Pytest Fixtures for FastAPI Backend Tests.
"""

import pytest
from fastapi.testclient import TestClient
from apps.api.app.main import app
from apps.api.app.core.config import settings


@pytest.fixture(scope="session")
def client() -> TestClient:
    """Provides a synchronous FastAPI TestClient."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="session")
def admin_headers() -> dict:
    """Valid admin API key header for testing protected routes."""
    return {"X-Admin-API-Key": settings.ADMIN_API_KEY}


@pytest.fixture(scope="session")
def internal_poll_headers() -> dict:
    """Valid shared secret header for internal cron jobs."""
    return {"X-Internal-Secret": settings.INTERNAL_POLL_SECRET}
