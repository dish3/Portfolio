"""
Test Suite for Public Projects and Skills Read API.
"""

from fastapi.testclient import TestClient


def test_list_published_projects(client: TestClient) -> None:
    """Asserts that GET /api/v1/projects returns a list of published projects."""
    response = client.get("/api/v1/projects")
    assert response.status_code == 200
    projects = response.json()
    assert isinstance(projects, list)
    assert len(projects) > 0
    assert "slug" in projects[0]
    assert "tech_stack" in projects[0]


def test_get_project_by_slug_success(client: TestClient) -> None:
    """Asserts that GET /api/v1/projects/nova-ai-portfolio-os returns project details."""
    response = client.get("/api/v1/projects/nova-ai-portfolio-os")
    assert response.status_code == 200
    project = response.json()
    assert project["slug"] == "nova-ai-portfolio-os"
    assert project["source"] == "github"
    assert "tech_stack" in project


def test_get_project_by_slug_not_found(client: TestClient) -> None:
    """Asserts that GET /api/v1/projects/nonexistent returns 404."""
    response = client.get("/api/v1/projects/nonexistent-slug-xyz")
    assert response.status_code == 404


def test_list_skills_endpoint(client: TestClient) -> None:
    """Asserts that GET /api/v1/skills returns skills with proficiency."""
    response = client.get("/api/v1/skills")
    assert response.status_code == 200
    skills = response.json()
    assert isinstance(skills, list)
    assert any(s["name"] == "Python" for s in skills)
