"""
NOVA AI Portfolio OS — Local Development Seed Utility.
Populates initial development test records for local verification.
All seed records are explicitly marked as development/test data.
"""

import sys
import asyncio
import logging
from pathlib import Path

# Ensure root and apps/api are in sys.path
_current_dir = Path(__file__).resolve().parent
_root_dir = _current_dir.parent.parent
_api_dir = _root_dir / "apps" / "api"
for _p in [str(_root_dir), str(_api_dir)]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

from sqlalchemy import select, func
from app.core.database import get_session_factory
from app.models.db_models import Skill, Project, Connector

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("seed")

DEV_SEED_PROJECT = {
    "slug": "nova-ai-portfolio-os",
    "title": "NOVA AI Portfolio OS (Development)",
    "short_description": "[Development Seed] Autonomous personal Operating System built with Next.js 14, FastAPI, and Supabase.",
    "long_description": (
        "[Development Seed Record]\n\n"
        "NOVA is an intelligent personal operating system designed to ingest developer activity across GitHub, "
        "synthesize project records using Gemini AI models, and preserve a verified knowledge graph with pgvector. "
        "All autonomous proposals pass through an approval state machine before mutating live portfolio entities."
    ),
    "source": "github",
    "github_repo_url": "https://github.com/dish3/ai-portfolio-os",
    "live_demo_url": "https://portfolio.os",
    "tech_stack": ["FastAPI", "Next.js", "Python", "TypeScript", "PostgreSQL", "pgvector", "Tailwind CSS"],
    "status": "published",
    "started_at": "2026-09-01",
}

DEV_SEED_SKILLS = [
    {"name": "Python", "category": "language", "proficiency": 5},
    {"name": "TypeScript", "category": "language", "proficiency": 5},
    {"name": "FastAPI", "category": "framework", "proficiency": 4},
    {"name": "Next.js", "category": "framework", "proficiency": 4},
    {"name": "PostgreSQL", "category": "tool", "proficiency": 4},
    {"name": "pgvector", "category": "tool", "proficiency": 4},
    {"name": "Docker", "category": "tool", "proficiency": 3},
]

DEV_SEED_CONNECTORS = [
    {"platform": "github", "enabled": False},
    {"platform": "leetcode", "enabled": False},
    {"platform": "linkedin", "enabled": False},
    {"platform": "kaggle", "enabled": False},
    {"platform": "devpost", "enabled": False},
    {"platform": "hashnode", "enabled": False},
    {"platform": "medium", "enabled": False},
    {"platform": "codeforces", "enabled": False},
    {"platform": "hackerrank", "enabled": False},
    {"platform": "spotify", "enabled": False},
    {"platform": "instagram", "enabled": False},
]


async def run_seed() -> None:
    session_factory = get_session_factory()
    async with session_factory() as session:
        # 1. Seed Skills if empty
        skills_count = (await session.execute(select(func.count(Skill.id)))).scalar() or 0
        if skills_count == 0:
            logger.info("Seeding %d initial development skills...", len(DEV_SEED_SKILLS))
            for s in DEV_SEED_SKILLS:
                session.add(Skill(**s))
            await session.commit()
            logger.info("Skills seeded successfully.")
        else:
            logger.info("Skills table already contains %d records. Skipping.", skills_count)

        # 2. Seed Project if empty
        projects_count = (await session.execute(select(func.count(Project.id)))).scalar() or 0
        if projects_count == 0:
            logger.info("Seeding development project: %s", DEV_SEED_PROJECT["title"])
            session.add(Project(**DEV_SEED_PROJECT))
            await session.commit()
            logger.info("Development project seeded successfully.")
        else:
            logger.info("Projects table already contains %d records. Skipping.", projects_count)

        # 3. Seed Connectors if empty
        connectors_count = (await session.execute(select(func.count(Connector.platform)))).scalar() or 0
        if connectors_count == 0:
            logger.info("Seeding %d platform connector entries...", len(DEV_SEED_CONNECTORS))
            for c in DEV_SEED_CONNECTORS:
                session.add(Connector(platform=c["platform"], enabled=c["enabled"], config={}))
            await session.commit()
            logger.info("Connectors seeded successfully.")
        else:
            logger.info("Connectors table already contains %d records. Skipping.", connectors_count)


def main() -> None:
    logger.info("Starting NOVA Development Seed Utility...")
    asyncio.run(run_seed())
    logger.info("Development seed completed successfully.")


if __name__ == "__main__":
    main()
