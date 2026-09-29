"""
Test Suite for Admin Authentication Skeleton.
"""

from fastapi.testclient import TestClient


def test_admin_routes_require_authentication(client: TestClient) -> None:
    """Asserts that requests without credentials to /api/v1/admin/pending return 401."""
    response = client.get("/api/v1/admin/pending")
    assert response.status_code == 401


def test_admin_routes_accessible_with_valid_api_key(
    client: TestClient, admin_headers: dict
) -> None:
    """Asserts that requests with valid API key return 200."""
    response = client.get("/api/v1/admin/pending", headers=admin_headers)
    assert response.status_code == 200
    assert response.json() == []  # Empty pending changes in Phase 00


def test_admin_connectors_accessible_with_api_key(
    client: TestClient, admin_headers: dict
) -> None:
    """Asserts that connectors list returns 200 with valid key."""
    response = client.get("/api/v1/admin/connectors", headers=admin_headers)
    assert response.status_code == 200
    assert response.json() == []
