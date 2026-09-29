"""
Consolidated API v1 Router.
"""

from fastapi import APIRouter
from app.api.v1.health import router as health_router
from app.api.v1.admin import router as admin_router
from app.api.v1.projects import router as projects_router
from app.api.v1.skills import router as skills_router
from app.api.v1.webhooks import router as webhooks_router
from app.api.v1.internal import router as internal_router

api_v1_router = APIRouter()

api_v1_router.include_router(health_router)
api_v1_router.include_router(admin_router)
api_v1_router.include_router(projects_router)
api_v1_router.include_router(skills_router)
api_v1_router.include_router(webhooks_router)
api_v1_router.include_router(internal_router)
