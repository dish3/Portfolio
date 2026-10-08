"""
NOVA Backend Configuration Management.
Built with Pydantic Settings v2.
"""

from typing import List, Union
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


from pathlib import Path

_current_file = Path(__file__).resolve()
_root_env = _current_file.parents[4] / ".env"
_api_env = _current_file.parents[2] / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(_root_env, _api_env, ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # Core Environment
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    PROJECT_NAME: str = "NOVA"
    OWNER_NAME: str = "Disha"

    # Database — strictly loaded from environment/.env, no localhost fallback
    DATABASE_URL: str = ""
    DATABASE_DIRECT_URL: str = ""

    # GitHub sources monitored by webhook fallback polling
    GITHUB_USERNAME: str = "dish3"
    GITHUB_REPOSITORIES: List[str] = ["dish3/ai-portfolio-os"]

    # Supabase Secrets
    SUPABASE_URL: str = ""
    SUPABASE_SERVICE_ROLE_KEY: str = ""

    # AI API Keys & Configuration (Gemini)
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.5-flash"
    GEMINI_FAST_MODEL: str = "gemini-2.5-flash-lite"
    GEMINI_EMBEDDING_MODEL: str = "text-embedding-004"
    EMBEDDING_DIMENSION: int = 768

    # Authentication & Security
    INTERNAL_POLL_SECRET: str = "development_internal_secret_key"
    ADMIN_API_KEY: str = "development_admin_api_key"
    JWT_SECRET: str = "development_jwt_secret_key_32_characters_minimum"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    REVALIDATION_SECRET: str = "development_revalidation_secret"
    FRONTEND_URL: str = "http://localhost:3000"

    # CORS
    CORS_ORIGINS: Union[List[str], str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://*.vercel.app"
    ]

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",") if i.strip()]
        return v

    @field_validator("GITHUB_REPOSITORIES", mode="before")
    @classmethod
    def assemble_github_repositories(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str):
            return [repo.strip() for repo in v.split(",") if repo.strip()]
        return v


settings = Settings()
