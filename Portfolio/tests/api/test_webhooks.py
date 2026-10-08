"""
Test Suite for Webhook Ingestion Endpoints.
"""

from uuid import UUID
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from app.models.db_models import PendingChange, Project
from app.agents.github_agent import GitHubAgent
from app.core.database import get_session_factory


def test_github_webhook_push_event(client: TestClient) -> None:
    """Asserts that valid push webhook events queue a proposal for human approval."""
    payload = {
        "repository": {
            "name": "autonomous-scheduler",
            "full_name": "disha/autonomous-scheduler",
            "description": "Cron-driven serverless scheduler",
            "html_url": "https://github.com/disha/autonomous-scheduler",
            "language": "Python",
            "topics": ["cron", "scheduler"],
        },
        "commits": [
            {"message": "Add retry backoff logic"}
        ]
    }

    response = client.post(
        "/api/v1/webhooks/github",
        json=payload,
        headers={"X-GitHub-Event": "push"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "queued_for_approval"
    assert data["proposal_agent"] == "github_agent"
    assert data["entity_type"] == "project"
    assert "proposal_id" in data


def test_github_webhook_ignored_empty_repo(client: TestClient) -> None:
    """Asserts that events without repository information are cleanly ignored without error."""
    response = client.post(
        "/api/v1/webhooks/github",
        json={"action": "ping"},
        headers={"X-GitHub-Event": "ping"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "ignored"


@pytest.mark.asyncio
async def test_github_agent_persists_to_pending_changes_only() -> None:
    """
    Asserts that GitHubAgent.process_repository creates a record in pending_changes
    and strictly does NOT write directly to live portfolio tables (e.g. projects).
    """
    factory = get_session_factory()
    test_slug = "test-agent-persistence-repo"
    repo_payload = {
        "name": test_slug,
        "full_name": f"disha/{test_slug}",
        "description": "Test repository for persistence verification",
        "html_url": f"https://github.com/disha/{test_slug}",
        "language": "Python",
        "topics": ["ai", "testing"],
        "readme": "A test README for persistence verification.",
        "recent_commits": ["Initial commit", "Feature added"],
    }

    async with factory() as db:
        result = await GitHubAgent.process_repository(repo_payload, db=db)
        assert result is not None
        assert result.get("agent") == "github_agent"
        assert result.get("entity_type") == "project"
        assert result.get("id") is not None
        change_id = UUID(str(result["id"]))

        # Verify PendingChange is persisted
        pending_record = await db.get(PendingChange, change_id)
        assert pending_record is not None
        assert pending_record.agent == "github_agent"
        assert pending_record.decision is None
        assert pending_record.diff.get("slug") == test_slug

        # Verify Project table was NOT written to directly by the agent
        proj_res = await db.execute(select(Project).where(Project.slug == test_slug))
        project_record = proj_res.scalar_one_or_none()
        assert project_record is None, "AI Agent must NEVER write directly to live tables"

        # Cleanup test pending_change
        await db.delete(pending_record)
        await db.commit()
