"""
Test Suite for GitHub Connector and Webhook HMAC Verification.
Sourced from NOVA_07_Automation_Integration_Prompt.md §1 & §9.
"""

import hmac
import hashlib
from apps.api.app.connectors.github import verify_github_signature, GitHubConnector
from apps.api.app.connectors.base import RawItem


def test_github_webhook_hmac_valid_signature() -> None:
    """Verifies that a valid sha256 HMAC signature passes verification."""
    secret = "test_webhook_secret_key"
    payload = b'{"action": "push", "repository": {"name": "test-repo"}}'

    expected_sig = "sha256=" + hmac.new(
        key=secret.encode("utf-8"),
        msg=payload,
        digestmod=hashlib.sha256
    ).hexdigest()

    assert verify_github_signature(payload, expected_sig, secret) is True


def test_github_webhook_hmac_invalid_signature() -> None:
    """Verifies that tampering with payload or wrong signature fails."""
    secret = "test_webhook_secret_key"
    payload = b'{"action": "push", "repository": {"name": "test-repo"}}'
    fake_sig = "sha256=0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"

    assert verify_github_signature(payload, fake_sig, secret) is False
    assert verify_github_signature(payload, None, secret) is False
    assert verify_github_signature(payload, "invalid_prefix", secret) is False


def test_github_connector_to_draft() -> None:
    """Tests conversion of RawItem to a DraftChange proposal."""
    connector = GitHubConnector()
    raw = RawItem(
        external_id="12345",
        platform="github",
        payload={
            "name": "authenfluence-ai",
            "description": "Vector search engine for authentication",
            "html_url": "https://github.com/disha/authenfluence-ai",
            "languages": ["Python", "FastAPI"],
            "topics": ["vector-search", "pgvector"],
            "readme": "# Authenfluence AI\nVector recommendation engine.",
            "recent_commits": ["Add vector search to recommendation engine"],
        }
    )

    draft = connector.to_draft(raw)
    assert draft.entity_type == "project"
    assert draft.diff["title"] == "Authenfluence Ai"
    assert draft.diff["slug"] == "authenfluence-ai"
    assert "Python" in draft.diff["tech_stack"]
    assert draft.ai_rationale != ""
