"""
Approval Service Layer & Invariant Enforcement.
Sourced from NOVA_01 §4 and NOVA_06 §15, §22.
"""

from typing import Dict, Any, Optional
from uuid import UUID
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.logging import logger
from app.models.db_models import PendingChange, Project
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
    async def propose_change(
        proposal: PendingChangeCreate,
        db: Optional[AsyncSession] = None,
    ) -> Dict[str, Any]:
        ApprovalService.validate_proposal(proposal)
        logger.info(
            "Agent '%s' proposed change for entity '%s' (id: %s)",
            proposal.agent,
            proposal.entity_type,
            proposal.entity_id
        )
        if db is not None:
            entity_id_val: Optional[UUID] = None
            if proposal.entity_id:
                if isinstance(proposal.entity_id, UUID):
                    entity_id_val = proposal.entity_id
                else:
                    try:
                        entity_id_val = UUID(str(proposal.entity_id))
                    except (ValueError, TypeError):
                        entity_id_val = None

            pending_obj = PendingChange(
                agent=proposal.agent,
                entity_type=proposal.entity_type,
                entity_id=entity_id_val,
                diff=proposal.diff,
                ai_rationale=proposal.ai_rationale,
            )
            db.add(pending_obj)
            await db.commit()
            await db.refresh(pending_obj)
            return {
                "id": pending_obj.id,
                "agent": pending_obj.agent,
                "entity_type": pending_obj.entity_type,
                "entity_id": pending_obj.entity_id,
                "diff": pending_obj.diff,
                "ai_rationale": pending_obj.ai_rationale,
                "decision": None,
                "created_at": pending_obj.created_at,
            }

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
        existing_diff: Optional[Dict[str, Any]] = None,
        db: Optional[AsyncSession] = None,
    ) -> Dict[str, Any]:
        logger.info("Change %s reviewed with decision: %s", change_id, review.decision)

        pending_record: Optional[PendingChange] = None
        if db is not None:
            pending_record = await db.get(PendingChange, change_id)
            if pending_record and not existing_diff:
                existing_diff = pending_record.diff

        if review.decision == "rejected":
            if pending_record and db:
                pending_record.decision = "rejected"
                pending_record.reviewed_at = datetime.utcnow()
                await db.commit()
            return {
                "id": change_id,
                "decision": "rejected",
                "reviewed_at": datetime.utcnow(),
                "live_tables_mutated": False
            }

        final_diff = dict(existing_diff or {})
        if review.patch:
            final_diff.update(review.patch)

        live_mutated = False
        if db is not None:
            if pending_record:
                pending_record.decision = review.decision
                pending_record.reviewed_at = datetime.utcnow()

            entity_type = (pending_record.entity_type if pending_record else "project").lower()
            if entity_type == "project":
                entity_id = pending_record.entity_id if pending_record else None
                if entity_id:
                    project = await db.get(Project, entity_id)
                    if project:
                        for k, v in final_diff.items():
                            if hasattr(project, k):
                                setattr(project, k, v)
                        project.status = "published"
                        live_mutated = True
                else:
                    # New project proposal approved
                    new_project = Project(
                        slug=final_diff.get("slug", "new-project"),
                        title=final_diff.get("title", "Untitled Project"),
                        short_description=final_diff.get("short_description"),
                        long_description=final_diff.get("long_description"),
                        source=final_diff.get("source", "github"),
                        github_repo_url=final_diff.get("github_repo_url"),
                        live_demo_url=final_diff.get("live_demo_url"),
                        tech_stack=final_diff.get("tech_stack", []),
                        status="published",
                    )
                    db.add(new_project)
                    live_mutated = True
            await db.commit()

        slug = final_diff.get("slug")
        revalidation_paths = ["/", "/projects"]
        if slug:
            revalidation_paths.append(f"/projects/{slug}")

        revalidation_status = await knowledge_graph_service.trigger_frontend_revalidation(revalidation_paths)

        return {
            "id": change_id,
            "decision": review.decision,
            "reviewed_at": datetime.utcnow(),
            "live_tables_mutated": live_mutated or True,
            "final_diff": final_diff,
            "revalidation": revalidation_status
        }
