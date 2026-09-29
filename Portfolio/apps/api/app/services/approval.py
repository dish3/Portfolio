"""
Approval Service Layer & Invariant Enforcement.
Sourced from NOVA_01 §4 and NOVA_06 §15, §22.
"""

from typing import Dict, Any, Optional
from uuid import UUID
from datetime import datetime
from app.core.logging import logger
from app.schemas.models import PendingChangeCreate, ReviewChangeRequest
from app.services.knowledge_graph import knowledge_graph_service


class ApprovalService:
    @staticmethod
    def validate_proposal(proposal: PendingChangeCreate) -> None:
        if not proposal.ai_rationale or not proposal.ai_rationale.strip():
            raise ValueError("All proposed changes must include a non-empty 'ai_rationale'.")
        if not proposal.diff:
            raise ValueError("Proposed change 'diff' cannot be empty.")

    @staticmethod
    def propose_change(proposal: PendingChangeCreate) -> Dict[str, Any]:
        ApprovalService.validate_proposal(proposal)
        logger.info(
            "Agent '%s' proposed change for entity '%s' (id: %s)",
            proposal.agent,
            proposal.entity_type,
            proposal.entity_id
        )
        return {
            "agent": proposal.agent,
            "entity_type": proposal.entity_type,
            "entity_id": proposal.entity_id,
            "diff": proposal.diff,
            "ai_rationale": proposal.ai_rationale,
            "decision": None,
            "created_at": datetime.utcnow()
        }

    @staticmethod
    async def review_change(
        change_id: UUID,
        review: ReviewChangeRequest,
        existing_diff: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        logger.info("Change %s reviewed with decision: %s", change_id, review.decision)

        if review.decision == "rejected":
            return {
                "id": change_id,
                "decision": "rejected",
                "reviewed_at": datetime.utcnow(),
                "live_tables_mutated": False
            }

        final_diff = dict(existing_diff or {})
        if review.patch:
            final_diff.update(review.patch)

        slug = final_diff.get("slug")
        revalidation_paths = ["/", "/projects"]
        if slug:
            revalidation_paths.append(f"/projects/{slug}")

        revalidation_status = await knowledge_graph_service.trigger_frontend_revalidation(revalidation_paths)

        return {
            "id": change_id,
            "decision": review.decision,
            "reviewed_at": datetime.utcnow(),
            "live_tables_mutated": True,
            "final_diff": final_diff,
            "revalidation": revalidation_status
        }
