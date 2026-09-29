"""
Authentication Skeleton and Security Dependencies.
Sourced from NOVA_01_System_Architecture.md §6 and NOVA_06_Backend_Development_Prompt.md §17.
"""

from typing import Optional
from fastapi import HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, APIKeyHeader
from app.core.config import settings
from app.core.logging import logger

# Headers and bearer schemes
api_key_header = APIKeyHeader(name="X-Admin-API-Key", auto_error=False)
bearer_auth = HTTPBearer(auto_error=False)
internal_secret_header = APIKeyHeader(name="X-Internal-Secret", auto_error=False)


async def verify_admin_access(
    api_key: Optional[str] = Security(api_key_header),
    credentials: Optional[HTTPAuthorizationCredentials] = Security(bearer_auth),
) -> dict:
    """
    Validates admin identity via either API Key or JWT Bearer Token.
    Returns the authenticated admin payload.
    """
    if api_key and api_key == settings.ADMIN_API_KEY:
        return {"sub": "admin", "role": "admin", "auth_method": "api_key"}

    if credentials:
        token = credentials.credentials
        if token == settings.ADMIN_API_KEY or token == settings.JWT_SECRET:
            return {"sub": "admin", "role": "admin", "auth_method": "bearer"}

    logger.warning("Unauthorized admin access attempt.")
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing administrative credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )


async def verify_internal_poll_secret(
    secret: Optional[str] = Security(internal_secret_header),
) -> bool:
    """
    Validates shared secret header for GitHub Actions cron workflows.
    """
    if not secret or secret != settings.INTERNAL_POLL_SECRET:
        logger.warning("Rejected unauthorized internal poll trigger.")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: Invalid internal scheduler secret.",
        )
    return True
