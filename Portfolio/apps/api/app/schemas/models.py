"""
Pydantic v2 Schemas for API Requests, Responses, and Entities.
"""

from datetime import datetime, date
from typing import Optional, List, Dict, Any, Literal
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict


# Health Check Schema
class HealthResponse(BaseModel):
    status: Literal["ok"] = "ok"
    service: str = "nova-api"
    version: str = "0.1.0"
    environment: str = "development"


# Skill Schemas
class SkillBase(BaseModel):
    name: str
    category: Optional[str] = None
    proficiency: Optional[int] = Field(None, ge=1, le=5)
    first_seen: Optional[date] = None


class SkillResponse(SkillBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID


# Project Schemas
class ProjectBase(BaseModel):
    slug: str
    title: str
    short_description: Optional[str] = None
    long_description: Optional[str] = None
    source: str = "github"
    github_repo_url: Optional[str] = None
    live_demo_url: Optional[str] = None
    drive_fallback_url: Optional[str] = None
    linkedin_post_url: Optional[str] = None
    youtube_video_url: Optional[str] = None
    cover_image_url: Optional[str] = None
    tech_stack: List[str] = []
    status: str = "draft"


class ProjectResponse(ProjectBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    updated_at: datetime
    started_at: Optional[date] = None


# Pending Changes & Approval Queue
class PendingChangeBase(BaseModel):
    agent: str
    entity_type: str
    entity_id: Optional[UUID] = None
    diff: Dict[str, Any]
    ai_rationale: str


class PendingChangeCreate(PendingChangeBase):
    pass


class PendingChangeResponse(PendingChangeBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    created_at: datetime
    reviewed_at: Optional[datetime] = None
    decision: Optional[str] = None


class ReviewChangeRequest(BaseModel):
    decision: Literal["approved", "rejected", "edited_then_approved"]
    patch: Optional[Dict[str, Any]] = None


# Connector Schemas
class ConnectorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    platform: str
    enabled: bool
    last_synced_at: Optional[datetime] = None
    config: Optional[Dict[str, Any]] = None
