"""
Test Suite for Approval Queue & System Invariants.
Sourced from NOVA_01 §4 and NOVA_09 §2.
"""

import uuid
import pytest
from apps.api.app.services.approval import ApprovalService
from apps.api.app.schemas.models import PendingChangeCreate, ReviewChangeRequest


def test_ai_rationale_mandatory() -> None:
    """CRITICAL INVARIANT: Rejects any proposal missing an ai_rationale."""
    with pytest.raises(ValueError, match="ai_rationale"):
        ApprovalService.propose_change(
            PendingChangeCreate(
                agent="github_agent",
                entity_type="project",
                diff={"title": "Test Project"},
                ai_rationale="",  # Empty rationale must fail
            )
        )


def test_diff_mandatory() -> None:
    """Rejects proposals with an empty diff."""
    with pytest.raises(ValueError, match="diff"):
        ApprovalService.propose_change(
            PendingChangeCreate(
                agent="github_agent",
                entity_type="project",
                diff={},
                ai_rationale="Found new repository",
            )
        )


def test_valid_proposal_queued_without_live_mutation() -> None:
    """Verifies that propose_change queues the change with null decision."""
    proposal = PendingChangeCreate(
        agent="github_agent",
        entity_type="project",
        diff={"title": "NOVA OS", "tech_stack": ["FastAPI", "Next.js"]},
        ai_rationale="Analyzed repository README and package dependencies.",
    )
    result = ApprovalService.propose_change(proposal)
    assert result["agent"] == "github_agent"
    assert result["decision"] is None


def test_rejected_change_never_mutates_live_tables() -> None:
    """CRITICAL INVARIANT: Rejections never mutate live tables."""
    fake_id = uuid.uuid4()
    review = ReviewChangeRequest(decision="rejected")
    result = ApprovalService.review_change(fake_id, review)

    assert result["decision"] == "rejected"
    assert result["live_tables_mutated"] is False


def test_approved_change_signals_mutation() -> None:
    """Approvals signal permission for live table mutation and ISR."""
    fake_id = uuid.uuid4()
    review = ReviewChangeRequest(decision="approved")
    result = ApprovalService.review_change(fake_id, review)

    assert result["decision"] == "approved"
    assert result["live_tables_mutated"] is True
