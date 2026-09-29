"""
Health Check Endpoint.
Required: GET /health returns {"status": "ok"}
"""

from fastapi import APIRouter
from app.schemas.models import HealthResponse

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthResponse)
async def get_health() -> dict:
    return {"status": "ok"}
