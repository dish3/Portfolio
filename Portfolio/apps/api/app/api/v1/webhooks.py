"""
GitHub Webhook Ingestion Router.
Sourced from NOVA_01 §2 and NOVA_07 §1.
"""

from typing import Dict, Any
from fastapi import APIRouter, Header, Request, HTTPException, status
from app.core.config import settings
from app.core.logging import logger
from app.connectors.github import verify_github_signature
from app.agents.github_agent import GitHubAgent

router = APIRouter(prefix="/webhooks", tags=["Webhooks"])


@router.post("/github")
async def handle_github_webhook(
    request: Request,
    x_hub_signature_256: str = Header(None, alias="X-Hub-Signature-256"),
    x_github_event: str = Header("push", alias="X-GitHub-Event"),
) -> Dict[str, Any]:
    body_bytes = await request.body()
    webhook_secret = getattr(settings, "GITHUB_WEBHOOK_SECRET", "")

    if webhook_secret and webhook_secret != "NOT_CONFIGURED" and not settings.ENVIRONMENT == "test":
        if not verify_github_signature(body_bytes, x_hub_signature_256, webhook_secret):
            logger.warning("Rejected GitHub webhook with invalid HMAC signature.")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid webhook signature.",
            )

    try:
        payload = await request.json()
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid JSON payload") from e

    repo_data = payload.get("repository", {})
    repo_name = repo_data.get("name")

    if not repo_name:
        return {"status": "ignored", "reason": "No repository payload found."}

    logger.info("Received GitHub '%s' event for '%s'", x_github_event, repo_name)

    repo_payload = {
        "name": repo_name,
        "full_name": repo_data.get("full_name"),
        "description": repo_data.get("description"),
        "html_url": repo_data.get("html_url"),
        "topics": repo_data.get("topics", []),
        "languages": [repo_data.get("language")] if repo_data.get("language") else [],
        "readme": "README from webhook push event.",
        "recent_commits": [c.get("message") for c in payload.get("commits", [])[:5]],
    }

    proposal = await GitHubAgent.process_repository(repo_payload)

    return {
        "status": "queued_for_approval",
        "event": x_github_event,
        "proposal_agent": proposal.get("agent"),
        "entity_type": proposal.get("entity_type"),
    }
