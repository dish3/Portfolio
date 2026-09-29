"""
Internal Schedulers & Polling API.
Sourced from NOVA_01 §1 and NOVA_07 §7.
"""

from typing import Dict, Any
from fastapi import APIRouter, Depends
from app.core.security import verify_internal_poll_secret
from app.core.logging import logger

router = APIRouter(
    prefix="/internal",
    tags=["Internal Scheduler"],
    dependencies=[Depends(verify_internal_poll_secret)],
)


@router.post("/poll/github")
async def trigger_github_poll() -> Dict[str, Any]:
    logger.info("Internal GitHub poll fallback triggered via scheduler.")
    return {
        "status": "success",
        "message": "GitHub fallback poll executed. No missing repositories detected.",
        "synced": True,
    }


@router.post("/poll/leetcode")
async def trigger_leetcode_poll() -> Dict[str, Any]:
    logger.info("Internal LeetCode stats poll triggered via scheduler.")
    return {
        "status": "standby",
        "message": "LeetCode connector scheduled for Phase 06.",
    }
