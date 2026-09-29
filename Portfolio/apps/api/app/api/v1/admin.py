"""
Admin API Endpoints (Protected by Authentication Skeleton).
Sourced from NOVA_01 §6, NOVA_02 §2, and NOVA_06 §17.
"""

from typing import List, Dict, Any
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from app.core.security import verify_admin_access
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
async def list_pending_changes() -> List[PendingChangeResponse]:
    return []


@router.post("/pending/{change_id}/review")
async def review_pending_change(
    change_id: UUID,
    review: ReviewChangeRequest,
) -> Dict[str, Any]:
    return await ApprovalService.review_change(change_id, review)


@router.get("/connectors", response_model=List[ConnectorResponse])
async def list_connectors() -> List[ConnectorResponse]:
    return []
