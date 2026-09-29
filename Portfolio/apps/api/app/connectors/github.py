"""
GitHub Platform Connector.
Sourced from NOVA_01 §2, §7 and NOVA_07 §1.
"""

import hmac
import hashlib
import logging
from typing import List, Dict, Any, Optional
import httpx
from app.core.config import settings
from app.connectors.base import Connector, RawItem, DraftChange

logger = logging.getLogger("nova.connectors.github")


def verify_github_signature(payload_bytes: bytes, signature_header: Optional[str], secret: str) -> bool:
    if not signature_header or not secret:
        return False

    if not signature_header.startswith("sha256="):
        return False

    expected_sig = "sha256=" + hmac.new(
        key=secret.encode("utf-8"),
        msg=payload_bytes,
        digestmod=hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(expected_sig, signature_header)


class GitHubConnector:
    name: str = "github"

    def __init__(self, username: Optional[str] = None, token: Optional[str] = None):
        self.username = username or settings.GITHUB_USERNAME
        self.token = token or getattr(settings, "GITHUB_CLIENT_SECRET", "")
        self.base_url = "https://api.github.com"

    def _get_headers(self) -> Dict[str, str]:
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "NOVA-Portfolio-OS",
        }
        if self.token:
            headers["Authorization"] = f"token {self.token}"
        return headers

    async def fetch_repository(self, owner: str, repo: str) -> RawItem:
        async with httpx.AsyncClient(timeout=15.0, headers=self._get_headers()) as client:
            repo_res = await client.get(f"{self.base_url}/repos/{owner}/{repo}")
            if repo_res.status_code != 200:
                logger.error("Failed to fetch GitHub repo %s/%s: %d", owner, repo, repo_res.status_code)
                raise RuntimeError(f"GitHub API error: {repo_res.status_code}")

            repo_data = repo_res.json()

            readme_text = ""
            readme_res = await client.get(
                f"{self.base_url}/repos/{owner}/{repo}/readme",
                headers={"Accept": "application/vnd.github.raw+json"}
            )
            if readme_res.status_code == 200:
                readme_text = readme_res.text[:5000]

            languages = {}
            lang_res = await client.get(f"{self.base_url}/repos/{owner}/{repo}/languages")
            if lang_res.status_code == 200:
                languages = lang_res.json()

            commits = []
            commits_res = await client.get(f"{self.base_url}/repos/{owner}/{repo}/commits?per_page=5")
            if commits_res.status_code == 200:
                commits = [c.get("commit", {}).get("message", "") for c in commits_res.json()]

            payload = {
                "name": repo_data.get("name"),
                "full_name": repo_data.get("full_name"),
                "description": repo_data.get("description"),
                "html_url": repo_data.get("html_url"),
                "topics": repo_data.get("topics", []),
                "languages": list(languages.keys()),
                "readme": readme_text,
                "recent_commits": commits,
                "default_branch": repo_data.get("default_branch", "main"),
                "pushed_at": repo_data.get("pushed_at"),
            }

            return RawItem(
                external_id=str(repo_data.get("id")),
                platform="github",
                payload=payload
            )

    def to_draft(self, item: RawItem) -> DraftChange:
        payload = item.payload
        name = payload.get("name", "Unnamed Project")
        slug = name.lower().replace(" ", "-").replace("_", "-")

        diff = {
            "title": name.replace("-", " ").title(),
            "slug": slug,
            "short_description": payload.get("description") or f"A software project built with {', '.join(payload.get('languages', [])[:3])}.",
            "long_description": payload.get("readme")[:500] if payload.get("readme") else None,
            "source": "github",
            "github_repo_url": payload.get("html_url"),
            "tech_stack": payload.get("languages", []) + payload.get("topics", []),
            "status": "draft"
        }

        return DraftChange(
            entity_type="project",
            entity_id=None,
            diff=diff,
            ai_rationale=f"Ingested GitHub repository '{name}' with languages: {', '.join(payload.get('languages', []))}."
        )


github_connector = GitHubConnector()
