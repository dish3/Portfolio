"""
Public Skills Read API.
Sourced from NOVA_05 §3 and NOVA_06 §16.
"""

from typing import List, Optional
from fastapi import APIRouter, Query
from apps.api.app.schemas.models import SkillResponse

router = APIRouter(prefix="/skills", tags=["Skills"])

INITIAL_PHASE1_SKILLS: List[dict] = [
    {"id": "a1b2c3d4-0001-0000-0000-000000000001", "name": "Python", "category": "language", "proficiency": 5, "first_seen": "2023-01-01"},
    {"id": "a1b2c3d4-0002-0000-0000-000000000002", "name": "TypeScript", "category": "language", "proficiency": 5, "first_seen": "2023-03-01"},
    {"id": "a1b2c3d4-0003-0000-0000-000000000003", "name": "FastAPI", "category": "framework", "proficiency": 4, "first_seen": "2023-06-01"},
    {"id": "a1b2c3d4-0004-0000-0000-000000000004", "name": "Next.js", "category": "framework", "proficiency": 4, "first_seen": "2023-08-01"},
    {"id": "a1b2c3d4-0005-0000-0000-000000000005", "name": "PostgreSQL", "category": "tool", "proficiency": 4, "first_seen": "2023-04-01"},
    {"id": "a1b2c3d4-0006-0000-0000-000000000006", "name": "pgvector", "category": "tool", "proficiency": 4, "first_seen": "2024-01-01"},
]


@router.get("", response_model=List[SkillResponse])
async def list_skills(
    category: Optional[str] = Query(None, description="Filter by skill category"),
) -> List[dict]:
    """
    List skills for knowledge graph badges and proficiency visualizers.
    """
    if category:
        return [s for s in INITIAL_PHASE1_SKILLS if s.get("category") == category]
    return INITIAL_PHASE1_SKILLS
