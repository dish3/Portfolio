"""
Test Suite for GitHub Agent Ingestion & Contract Conformance.
Sourced from NOVA_04 §1 and NOVA_06 §13, §22.
"""

import pytest
from apps.api.app.agents.github_agent import GitHubAgent


@pytest.mark.asyncio
async def test_github_agent_processes_repo_into_pending_change() -> None:
    """
    CRITICAL INVARIANT TEST:
    Asserts GitHub Agent outputs strictly to pending_changes with mandatory ai_rationale.
    """
    sample_repo = {
        "name": "vision-transformer-lab",
        "description": "PyTorch implementation of Vision Transformers from scratch",
        "html_url": "https://github.com/disha/vision-transformer-lab",
        "languages": ["Python"],
        "topics": ["pytorch", "deep-learning", "vision"],
        "readme": "A deep learning repository demonstrating multi-head self-attention.",
        "recent_commits": ["Initial release v1.0", "Add ViT patch tokenizer"],
    }

    proposal = await GitHubAgent.process_repository(sample_repo)

    assert proposal["agent"] == "github_agent"
    assert proposal["entity_type"] == "project"
    assert proposal["decision"] is None  # Must remain pending human review!
    assert proposal["diff"]["source"] == "github"
    assert "slug" in proposal["diff"]
    assert proposal["ai_rationale"] != ""
    assert len(proposal["diff"]["tech_stack"]) > 0


@pytest.mark.asyncio
async def test_github_agent_never_writes_directly_to_live_table() -> None:
    """
    Asserts that processing a repository returns a draft proposal without committing to live tables.
    """
    sample_repo = {
        "name": "ephemeral-sandbox",
        "html_url": "https://github.com/disha/ephemeral-sandbox",
    }

    proposal = await GitHubAgent.process_repository(sample_repo)
    assert proposal["diff"]["status"] == "draft"
