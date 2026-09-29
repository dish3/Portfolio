"""
NOVA AI Portfolio OS — FastAPI Application Entrypoint.
"""

import sys
from pathlib import Path

# Ensure app package and root are on sys.path
_current_dir = Path(__file__).resolve().parent       # app/
_api_dir = _current_dir.parent                       # apps/api/
_root_dir = _api_dir.parent.parent                   # Portfolio root

for _p in [str(_api_dir), str(_root_dir)]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logging import logger
from app.api.v1.router import api_v1_router
from app.api.v1.health import router as root_health_router


def create_application() -> FastAPI:
    """Creates and configures the FastAPI application instance."""
    app = FastAPI(
        title=f"{settings.PROJECT_NAME} AI Portfolio OS API",
        description=(
            "Autonomous backend operating system for portfolio ingestion, AI agents, "
            "approval workflows, and knowledge graph embeddings."
        ),
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS if isinstance(settings.CORS_ORIGINS, list) else [settings.CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Mount Root health check (required: GET /health -> {"status": "ok"})
    app.include_router(root_health_router)

    # Mount API v1 router under /api/v1
    app.include_router(api_v1_router, prefix="/api/v1")

    @app.on_event("startup")
    async def startup_event() -> None:
        logger.info(
            "Starting %s API in [%s] environment",
            settings.PROJECT_NAME,
            settings.ENVIRONMENT,
        )

    @app.on_event("shutdown")
    async def shutdown_event() -> None:
        logger.info("Shutting down %s API", settings.PROJECT_NAME)

    return app


app = create_application()
