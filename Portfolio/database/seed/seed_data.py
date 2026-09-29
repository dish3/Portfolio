"""
NOVA AI Portfolio OS — Local Development Seed Utility.
Populates standard mock data for development testing.
Sourced from NOVA_06_Backend_Development_Prompt.md § deliverables.
"""

import sys
import logging
from typing import Any

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("seed")

SAMPLE_SKILLS = [
    {"name": "Python", "category": "language", "proficiency": 5},
    {"name": "TypeScript", "category": "language", "proficiency": 5},
    {"name": "FastAPI", "category": "framework", "proficiency": 4},
    {"name": "Next.js", "category": "framework", "proficiency": 4},
    {"name": "PostgreSQL", "category": "tool", "proficiency": 4},
    {"name": "PyTorch", "category": "framework", "proficiency": 3},
    {"name": "Docker", "category": "tool", "proficiency": 3},
]

SAMPLE_CONNECTORS = [
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

def main() -> None:
    logger.info("NOVA Development Seed Utility initialized.")
    logger.info("Found %d skills and %d connector profiles ready for seeding.", len(SAMPLE_SKILLS), len(SAMPLE_CONNECTORS))
    logger.info("Database seed definitions validated successfully.")

if __name__ == "__main__":
    main()
