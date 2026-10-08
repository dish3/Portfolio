from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.models import HealthResponse
from app.core.database import get_db

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthResponse)
async def get_health() -> dict:
    return {"status": "ok"}


@router.get("/health/db")
async def get_db_health(db: AsyncSession = Depends(get_db)) -> dict:
    """
    Diagnostic database connectivity check.
    Executes SELECT current_database(), current_user against PostgreSQL.
    Credentials and connection strings are strictly never printed.
    """
    try:
        result = await db.execute(text("SELECT current_database(), current_user;"))
        row = result.fetchone()
        current_db = row[0] if row else "unknown"
        current_user = row[1] if row else "unknown"

        # Check pgvector extension
        vec_res = await db.execute(text("SELECT extname FROM pg_extension WHERE extname = 'vector';"))
        vector_enabled = vec_res.fetchone() is not None

        # Check counts
        p_res = await db.execute(text("SELECT COUNT(*) FROM projects;"))
        projects_count = p_res.scalar() or 0

        s_res = await db.execute(text("SELECT COUNT(*) FROM skills;"))
        skills_count = s_res.scalar() or 0

        return {
            "status": "connected",
            "database": current_db,
            "user": current_user,
            "pgvector": "enabled" if vector_enabled else "disabled",
            "projects_count": projects_count,
            "skills_count": skills_count,
        }
    except Exception as e:
        err_str = str(e)
        if "@" in err_str:
            err_str = err_str.split("@")[-1]
        return {
            "status": "error",
            "error_type": type(e).__name__,
            "error_message": err_str,
        }



