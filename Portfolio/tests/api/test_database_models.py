"""
Test Suite for Database Models & Schema Structure.
Sourced from NOVA_02_Database_Design.md.
"""

from apps.api.app.models.db_models import (
    Base,
    Skill,
    Project,
    ProjectSkill,
    Certificate,
    TimelineEvent,
    Update,
    PendingChange,
    ResumeVersion,
    Connector,
    LeetCodeSnapshot,
    Visit,
    ChatMessage,
)


def test_required_tables_present() -> None:
    """Verifies that all 12 core tables from NOVA_02 are defined in metadata."""
    table_names = set(Base.metadata.tables.keys())
    expected = {
        "skills",
        "projects",
        "project_skills",
        "certificates",
        "timeline_events",
        "updates",
        "pending_changes",
        "resume_versions",
        "connectors",
        "leetcode_snapshots",
        "visits",
        "chat_messages",
    }
    assert expected.issubset(table_names), f"Missing tables: {expected - table_names}"


def test_no_x_twitter_references_in_schema() -> None:
    """
    CRITICAL INVARIANT TEST:
    Asserts no table name or column name references X or Twitter.
    """
    for table_name, table in Base.metadata.tables.items():
        assert "twitter" not in table_name.lower()
        assert table_name.lower() != "x"
        for column in table.columns:
            assert "twitter" not in column.name.lower()
            assert column.name.lower() != "x"


def test_project_model_structure() -> None:
    """Verifies Project model properties."""
    columns = {c.name for c in Project.__table__.columns}
    required_cols = {
        "id", "slug", "title", "short_description", "long_description",
        "source", "github_repo_url", "live_demo_url", "drive_fallback_url",
        "tech_stack", "status", "started_at", "updated_at"
    }
    assert required_cols.issubset(columns)


def test_pending_changes_structure() -> None:
    """Verifies PendingChange approval queue structure."""
    columns = {c.name for c in PendingChange.__table__.columns}
    required_cols = {
        "id", "agent", "entity_type", "entity_id", "diff",
        "ai_rationale", "created_at", "reviewed_at", "decision"
    }
    assert required_cols.issubset(columns)
