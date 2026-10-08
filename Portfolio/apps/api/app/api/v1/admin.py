"""
Admin API Endpoints (Protected by Authentication Skeleton).
Sourced from NOVA_01 §6, NOVA_02 §2, and NOVA_06 §17.
"""

from typing import List, Dict, Any
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import verify_admin_access
from app.core.database import get_db
from app.models.db_models import PendingChange, Connector
from app.schemas.models import (
    PendingChangeResponse,
    ReviewChangeRequest,
    ConnectorResponse,
)
from app.services.approval import ApprovalService

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Depends(verify_admin_access)],
)


@router.get("/pending", response_model=List[PendingChangeResponse])
async def list_pending_changes(db: AsyncSession = Depends(get_db)) -> List[PendingChange]:
    query = select(PendingChange).where(PendingChange.decision.is_(None)).order_by(PendingChange.created_at.desc())
    result = await db.execute(query)
    return list(result.scalars().all())


@router.post("/pending/{change_id}/review")
async def review_pending_change(
    change_id: UUID,
    review: ReviewChangeRequest,
    db: AsyncSession = Depends(get_db),
) -> Dict[str, Any]:
    return await ApprovalService.review_change(change_id, review, db=db)


@router.get("/connectors", response_model=List[ConnectorResponse])
async def list_connectors(db: AsyncSession = Depends(get_db)) -> List[Connector]:
    query = select(Connector).order_by(Connector.platform.asc())
    result = await db.execute(query)
    return list(result.scalars().all())
