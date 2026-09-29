"""
Knowledge Graph Sync & Embedding Pipeline.
Sourced from NOVA_01 §5 and NOVA_06 §15.
"""

import logging
from typing import Dict, Any, List, Optional
import httpx
from app.core.config import settings
from app.core.gemini_client import gemini_client

logger = logging.getLogger("nova.knowledge_graph")


class KnowledgeGraphService:
    @staticmethod
    async def embed_entity(entity_type: str, title: str, description: str, tech_stack: List[str]) -> List[float]:
        text_content = f"{title}. {description}. Technologies: {', '.join(tech_stack)}"
        embedding = await gemini_client.get_embedding(text_content)
        return embedding

    @staticmethod
    async def trigger_frontend_revalidation(paths: List[str]) -> Dict[str, Any]:
        results = {}
        async with httpx.AsyncClient(timeout=10.0) as client:
            for path in paths:
                url = f"{settings.FRONTEND_URL}/api/revalidate"
                params = {"secret": settings.REVALIDATION_SECRET, "path": path}
                try:
                    response = await client.post(url, params=params)
                    results[path] = response.status_code == 200
                    logger.info("ISR revalidation for '%s': status %d", path, response.status_code)
                except Exception as e:
                    logger.warning("Failed to trigger revalidation for '%s': %s", path, e)
                    results[path] = False
        return results


knowledge_graph_service = KnowledgeGraphService()
