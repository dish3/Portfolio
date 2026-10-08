"""
Test Suite for Projects and Skills Database-Backed Endpoints.
Verifies that endpoints read from the database session and do NOT
use hardcoded fallback data when the database returns empty results.
"""

from unittest.mock import AsyncMock, MagicMock
import pytest
from fastapi.testclient import TestClient
from apps.api.app.main import app
from apps.api.app.core.database import get_db


@pytest.fixture
def mock_db_empty() -> AsyncMock:
    """Mock database session that returns empty results."""
    mock_session = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = []
    mock_result.scalars.return_value.first.return_value = None
    mock_session.execute.return_value = mock_result
    return mock_session


def test_projects_endpoint_returns_empty_when_no_records_in_db(mock_db_empty: AsyncMock) -> None:
    """
    CRITICAL CHECK: When database has 0 published projects,
    endpoint must return empty array [] rather than the old hardcoded mock data.
    """
    async def override_get_db():
        yield mock_db_empty

    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as client:
            response = client.get("/api/v1/projects")
            assert response.status_code == 200
            data = response.json()
            # Must be empty list, NOT the hardcoded INITIAL_PHASE1_PROJECTS mock
            assert data == []
            assert mock_db_empty.execute.called
    finally:
        app.dependency_overrides.clear()


def test_skills_endpoint_returns_empty_when_no_records_in_db(mock_db_empty: AsyncMock) -> None:
    """
    CRITICAL CHECK: When database has 0 skills,
    endpoint must return empty array [] rather than the old hardcoded mock data.
    """
    async def override_get_db():
        yield mock_db_empty

    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as client:
            response = client.get("/api/v1/skills")
            assert response.status_code == 200
            data = response.json()
            assert data == []
            assert mock_db_empty.execute.called
    finally:
        app.dependency_overrides.clear()
