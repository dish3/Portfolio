"""
Test Suite for Approval Service Invariant Enforcement.
Verifies validation and state transitions.
"""

from uuid import uuid4
import pytest
from app.schemas.models import PendingChangeCreate, ReviewChangeRequest
from app.services.approval import ApprovalService


@pytest.mark.asyncio
async def test_propose_change_validation() -> None:
    # Must reject empty rationale
    with pytest.raises(ValueError, match="non-empty 'ai_rationale'"):
        ApprovalService.validate_proposal(
            PendingChangeCreate(agent="github_agent", entity_type="project", diff={"title": "Test"}, ai_rationale="")
        )

    # Must reject empty diff
    with pytest.raises(ValueError, match="'diff' cannot be empty"):
        ApprovalService.validate_proposal(
            PendingChangeCreate(agent="github_agent", entity_type="project", diff={}, ai_rationale="Adding test")
        )


@pytest.mark.asyncio
async def test_propose_and_review_change_rejection() -> None:
    change_id = uuid4()
    review = ReviewChangeRequest(decision="rejected")
    result = await ApprovalService.review_change(change_id, review)

    assert result["decision"] == "rejected"
    assert result["live_tables_mutated"] is False
