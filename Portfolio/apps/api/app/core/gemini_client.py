"""
Centralized Gemini AI Client.
Sourced from NOVA_01 §1, NOVA_04 §1, and NOVA_06 §9.
"""

import json
import logging
from typing import Dict, Any, List, Optional
import httpx
from app.core.config import settings

logger = logging.getLogger("nova.gemini")

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models"


class GeminiClient:
    """
    Client for Google Gemini API (Flash, Flash-Lite, and text-embedding-004).
    Supports production HTTP calls and simulated fallback for offline/test environments.
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.GEMINI_API_KEY
        self.default_model = settings.GEMINI_MODEL
        self.fast_model = settings.GEMINI_FAST_MODEL
        self.embedding_model = settings.GEMINI_EMBEDDING_MODEL

    async def generate_json(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        model: Optional[str] = None,
    ) -> Dict[str, Any]:
        chosen_model = model or self.default_model

        if not self.api_key or self.api_key.startswith("your_") or self.api_key == "NOT_CONFIGURED" or settings.ENVIRONMENT == "test":
            logger.info("Using simulated Gemini response for development/test mode.")
            return self._mock_generation_response(prompt)

        url = f"{GEMINI_API_URL}/{chosen_model}:generateContent?key={self.api_key}"

        payload: Dict[str, Any] = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "responseMimeType": "application/json",
                "temperature": 0.2,
            },
        }

        if system_instruction:
            payload["systemInstruction"] = {
                "parts": [{"text": system_instruction}]
            }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, json=payload)
            if response.status_code != 200:
                logger.error("Gemini API error %d: %s", response.status_code, response.text)
                raise RuntimeError(f"Gemini API returned error {response.status_code}: {response.text}")

            result = response.json()
            try:
                candidate = result["candidates"][0]["content"]["parts"][0]["text"]
                return json.loads(candidate)
            except (KeyError, IndexError, json.JSONDecodeError) as e:
                logger.error("Failed to parse Gemini JSON output: %s", e)
                raise RuntimeError("Invalid JSON response from Gemini model.") from e

    async def get_embedding(self, text: str) -> List[float]:
        if not self.api_key or self.api_key.startswith("your_") or self.api_key == "NOT_CONFIGURED" or settings.ENVIRONMENT == "test":
            return [0.01 * (i % 50) for i in range(settings.EMBEDDING_DIMENSION)]

        url = f"{GEMINI_API_URL}/{self.embedding_model}:embedContent?key={self.api_key}"
        payload = {
            "model": f"models/{self.embedding_model}",
            "content": {"parts": [{"text": text[:2000]}]},
        }

        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(url, json=payload)
            if response.status_code != 200:
                logger.error("Gemini Embedding API error %d: %s", response.status_code, response.text)
                raise RuntimeError(f"Embedding API error: {response.text}")

            result = response.json()
            embedding_values = result.get("embedding", {}).get("values", [])
            return embedding_values

    def _mock_generation_response(self, prompt: str) -> Dict[str, Any]:
        return {
            "title": "NOVA AI Portfolio OS",
            "short_description": "Autonomous AI portfolio operating system with story-driven presentation.",
            "long_description": (
                "NOVA continuously ingests developer activity from GitHub, LeetCode, and LinkedIn, "
                "orchestrates multi-agent summaries via Gemini, and maintains a pgvector knowledge graph."
            ),
            "tech_stack": ["FastAPI", "Next.js", "Python", "TypeScript", "PostgreSQL", "pgvector", "Tailwind CSS"],
            "github_repo_url": "https://github.com/dish3/ai-portfolio-os",
            "status": "draft",
            "ai_rationale": "Generated via simulated Gemini client in development environment.",
        }


gemini_client = GeminiClient()
