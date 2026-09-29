"""
GitHub Agent Implementation.
Sourced strictly from NOVA_04_AI_Agents_Specification.md §1 and NOVA_06 §13.
"""

import logging
from typing import Dict, Any, Optional
from app.core.config import settings
from app.core.gemini_client import gemini_client
from app.schemas.models import PendingChangeCreate
from app.services.approval import ApprovalService

logger = logging.getLogger("nova.agents.github")

GITHUB_AGENT_SYSTEM_PROMPT = """
You are the GitHub Agent for {project_name}. Given a repository's README, file tree summary, languages, and recent commits, write a professional 2-4 sentence project description in third person, identify the tech stack as a list of canonical names (e.g. "React" not "react.js"), and state in one sentence why this looks like a new project vs. an incremental update. Never invent features not evidenced in the README or commits. If information is insufficient, say so in ai_rationale rather than guessing.

Output strictly as a valid JSON object matching:
{{
  "title": "Clean Project Title",
  "short_description": "2-3 sentences summary",
  "long_description": "Professional 1-2 paragraph description based strictly on the README",
  "tech_stack": ["CanonicalTechnologyName"],
  "ai_rationale": "Why this looks like a new project or update, and evidence from README/commits"
}}
""".strip()


class GitHubAgent:
    @staticmethod
    async def process_repository(
        repo_payload: Dict[str, Any],
        existing_project_id: Optional[str] = None
    ) -> Dict[str, Any]:
        repo_name = repo_payload.get("name", "Unknown Repo")
        logger.info("GitHub Agent analyzing repository: %s", repo_name)

        prompt = f"""
Repository Metadata:
- Name: {repo_payload.get('name')}
- Description: {repo_payload.get('description')}
- URL: {repo_payload.get('html_url')}
- Primary Languages: {', '.join(repo_payload.get('languages', []))}
- Topics: {', '.join(repo_payload.get('topics', []))}

README Excerpt:
{repo_payload.get('readme', 'No README content provided.')[:3000]}

Recent Commits:
{chr(10).join(f"- {c}" for c in repo_payload.get('recent_commits', []))}
"""

        system_instruction = GITHUB_AGENT_SYSTEM_PROMPT.format(
            project_name=settings.PROJECT_NAME
        )

        analysis = await gemini_client.generate_json(
            prompt=prompt,
            system_instruction=system_instruction,
            model=settings.GEMINI_MODEL
        )

        title = analysis.get("title") or repo_name.replace("-", " ").title()
        slug = repo_name.lower().replace(" ", "-").replace("_", "-")

        diff = {
            "slug": slug,
            "title": title,
            "short_description": analysis.get("short_description") or repo_payload.get("description"),
            "long_description": analysis.get("long_description"),
            "source": "github",
            "github_repo_url": repo_payload.get("html_url"),
            "tech_stack": analysis.get("tech_stack", repo_payload.get("languages", [])),
            "status": "draft",
        }

        ai_rationale = analysis.get("ai_rationale") or f"Analyzed repository {repo_name} commits and README."

        proposal = PendingChangeCreate(
            agent="github_agent",
            entity_type="project",
            entity_id=existing_project_id,
            diff=diff,
            ai_rationale=ai_rationale,
        )

        queued_change = ApprovalService.propose_change(proposal)
        return queued_change
