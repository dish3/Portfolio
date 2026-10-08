"""
Public Skills Read API.
Queries live PostgreSQL/Supabase database via SQLAlchemy 2.0.
Sourced from NOVA_05 §3 and NOVA_06 §16.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.db_models import Skill
from app.schemas.models import SkillResponse
from app.core.database import get_db

router = APIRouter(prefix="/skills", tags=["Skills"])


@router.get("", response_model=List[SkillResponse])
async def list_skills(
    category: Optional[str] = Query(None, description="Filter by skill category"),
    db: AsyncSession = Depends(get_db),
) -> List[Skill]:
    """
    List skills for knowledge graph badges and proficiency visualizers from PostgreSQL.
    """
    query = select(Skill).order_by(Skill.proficiency.desc().nullslast(), Skill.name.asc())
    if category:
        query = query.where(Skill.category == category)

    result = await db.execute(query)
    skills = result.scalars().all()
    return list(skills)
