"""
Test Suite for Webhook Ingestion Endpoints.
"""

from fastapi.testclient import TestClient


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


def test_github_webhook_ignored_empty_repo(client: TestClient) -> None:
    """Asserts that events without repository information are cleanly ignored without error."""
    response = client.post(
        "/api/v1/webhooks/github",
        json={"action": "ping"},
        headers={"X-GitHub-Event": "ping"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "ignored"
