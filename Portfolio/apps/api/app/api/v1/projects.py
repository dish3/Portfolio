"""
Public Projects Read API.
Sourced from NOVA_05 §9 and NOVA_06 §16.
"""

from typing import List, Optional
from uuid import UUID, uuid4
from fastapi import APIRouter, HTTPException, Query, status
from apps.api.app.schemas.models import ProjectResponse

router = APIRouter(prefix="/projects", tags=["Projects"])

# Sample published project showcase for Phase 1 if database is in memory/dev
INITIAL_PHASE1_PROJECTS: List[dict] = [
    {
        "id": "e4a2c1b0-9876-4321-b012-3456789abcde",
        "slug": "nova-ai-portfolio-os",
        "title": "NOVA AI Portfolio OS",
        "short_description": "An autonomous AI-managed Operating System and story-driven portfolio built with Next.js 14 and FastAPI.",
        "long_description": (
            "NOVA is an intelligent personal operating system designed to ingest developer activity across GitHub, "
            "synthesize project records using Gemini AI models, and preserve a verified knowledge graph with pgvector. "
            "All autonomous proposals pass through an approval state machine before mutating live portfolio entities."
        ),
        "source": "github",
        "github_repo_url": "https://github.com/dish3/ai-portfolio-os",
        "live_demo_url": "https://portfolio.os",
        "drive_fallback_url": None,
        "linkedin_post_url": None,
        "youtube_video_url": None,
        "cover_image_url": None,
        "tech_stack": ["FastAPI", "Next.js", "Python", "TypeScript", "PostgreSQL", "pgvector", "Tailwind CSS"],
        "status": "published",
        "started_at": "2026-09-01",
        "updated_at": "2026-09-29T20:00:00Z",
    }
]


@router.get("", response_model=List[ProjectResponse])
async def list_published_projects(
    tech: Optional[str] = Query(None, description="Filter by technology tag"),
) -> List[dict]:
    """
    List all published projects for the public portfolio showcase.
    Supports optional tech stack tag filtering.
    """
    if tech:
        return [
            p for p in INITIAL_PHASE1_PROJECTS
            if any(tech.lower() == t.lower() for t in p.get("tech_stack", []))
        ]
    return INITIAL_PHASE1_PROJECTS


@router.get("/{slug}", response_model=ProjectResponse)
async def get_project_by_slug(slug: str) -> dict:
    """
    Retrieve project details by slug for the project detail page (/projects/[slug]).
    """
    for project in INITIAL_PHASE1_PROJECTS:
        if project["slug"] == slug:
            return project

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Project with slug '{slug}' not found.",
    )
