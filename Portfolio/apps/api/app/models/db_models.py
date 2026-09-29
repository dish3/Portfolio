"""
SQLAlchemy 2.0 Database Models for NOVA.
Sourced strictly from NOVA_02_Database_Design.md.
"""

import uuid
from datetime import datetime, date
from typing import List, Optional, Any
from sqlalchemy import (
    String,
    Text,
    SmallInteger,
    Integer,
    Numeric,
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    JSON,
    func,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB, ARRAY
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

try:
    from pgvector.sqlalchemy import Vector
    HAS_PGVECTOR = True
except ImportError:
    HAS_PGVECTOR = False


class Base(DeclarativeBase):
    pass


class Skill(Base):
    __tablename__ = "skills"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    category: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    proficiency: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    first_seen: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    
    if HAS_PGVECTOR:
        embedding = mapped_column(Vector(768), nullable=True)
    else:
        embedding = mapped_column(JSON, nullable=True)

    projects: Mapped[List["ProjectSkill"]] = relationship(
        "ProjectSkill", back_populates="skill", cascade="all, delete-orphan"
    )


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    slug: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    short_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    long_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    source: Mapped[str] = mapped_column(String, nullable=False, default="github")
    github_repo_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    live_demo_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    drive_fallback_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    linkedin_post_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    youtube_video_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    cover_image_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Denormalized for fast filtering
    tech_stack = mapped_column(JSON, nullable=True, default=list)
    status: Mapped[str] = mapped_column(String, default="draft")
    started_at: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )

    if HAS_PGVECTOR:
        embedding = mapped_column(Vector(768), nullable=True)
    else:
        embedding = mapped_column(JSON, nullable=True)

    skills: Mapped[List["ProjectSkill"]] = relationship(
        "ProjectSkill", back_populates="project", cascade="all, delete-orphan"
    )


class ProjectSkill(Base):
    __tablename__ = "project_skills"

    project_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), primary_key=True
    )
    skill_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("skills.id", ondelete="CASCADE"), primary_key=True
    )

    project: Mapped["Project"] = relationship("Project", back_populates="skills")
    skill: Mapped["Skill"] = relationship("Skill", back_populates="projects")


class Certificate(Base):
    __tablename__ = "certificates"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    title: Mapped[str] = mapped_column(String, nullable=False)
    issuer: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    issue_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    credential_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    source_post_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    related_skill_ids = mapped_column(JSON, nullable=True, default=list)
    status: Mapped[str] = mapped_column(String, default="draft")


class TimelineEvent(Base):
    __tablename__ = "timeline_events"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    type: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    title: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    related_project_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("projects.id", ondelete="SET NULL"), nullable=True
    )
    status: Mapped[str] = mapped_column(String, default="draft")


class Update(Base):
    __tablename__ = "updates"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    source: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    raw_content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    ai_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    media_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    related_project_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("projects.id", ondelete="SET NULL"), nullable=True
    )
    published_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(String, default="draft")


class PendingChange(Base):
    __tablename__ = "pending_changes"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    agent: Mapped[str] = mapped_column(String, nullable=False)
    entity_type: Mapped[str] = mapped_column(String, nullable=False)
    entity_id: Mapped[Optional[uuid.UUID]] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    diff: Mapped[Any] = mapped_column(JSON, nullable=False)
    ai_rationale: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    reviewed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    decision: Mapped[Optional[str]] = mapped_column(String, nullable=True)


class ResumeVersion(Base):
    __tablename__ = "resume_versions"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    role_target: Mapped[str] = mapped_column(String, nullable=False)
    content_json: Mapped[Any] = mapped_column(JSON, nullable=False)
    pdf_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    is_current: Mapped[bool] = mapped_column(Boolean, default=False)


class Connector(Base):
    __tablename__ = "connectors"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    platform: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    last_synced_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    config: Mapped[Optional[Any]] = mapped_column(JSON, nullable=True)


class LeetCodeSnapshot(Base):
    __tablename__ = "leetcode_snapshots"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    captured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    total_solved: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    easy: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    medium: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    hard: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    contest_rating: Mapped[Optional[float]] = mapped_column(Numeric(6, 2), nullable=True)
    raw: Mapped[Optional[Any]] = mapped_column(JSON, nullable=True)


class Visit(Base):
    __tablename__ = "visits"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    visited_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    path: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    country: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    referrer: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    is_recruiter_mode: Mapped[bool] = mapped_column(Boolean, default=False)
    session_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    session_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    role: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
