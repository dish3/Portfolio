"""
Public Projects Read API.
Queries live PostgreSQL/Supabase database via SQLAlchemy 2.0.
Sourced from NOVA_05 §9 and NOVA_06 §16.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.db_models import Project
from app.schemas.models import ProjectResponse
from app.core.database import get_db

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.get("", response_model=List[ProjectResponse])
async def list_published_projects(
    tech: Optional[str] = Query(None, description="Filter by technology tag"),
    db: AsyncSession = Depends(get_db),
) -> List[Project]:
    """
    List all published projects from PostgreSQL for the public portfolio showcase.
    Supports optional tech stack tag filtering.
    """
    query = (
        select(Project)
        .where(Project.status == "published")
        .order_by(Project.updated_at.desc())
    )
    result = await db.execute(query)
    projects = result.scalars().all()

    if tech:
        return [
            p for p in projects
            if any(tech.lower() == str(t).lower() for t in (p.tech_stack or []))
        ]
    return list(projects)


@router.get("/{slug}", response_model=ProjectResponse)
async def get_project_by_slug(
    slug: str,
    db: AsyncSession = Depends(get_db),
) -> Project:
    """
    Retrieve project details by slug from PostgreSQL for the project detail page (/projects/[slug]).
    """
    query = select(Project).where(Project.slug == slug, Project.status == "published")
    result = await db.execute(query)
    project = result.scalars().first()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with slug '{slug}' not found.",
        )

    return project
