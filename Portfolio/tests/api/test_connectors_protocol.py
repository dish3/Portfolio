"""
Test Suite for Connector Protocol and Platform Exclusions.
Sourced from NOVA_01 §7 and NOVA_07 §4.
"""

from typing import List
from apps.api.app.connectors.base import Connector, RawItem, DraftChange


class DummyConnector:
    """Mock implementation satisfying Connector protocol."""
    name: str = "mock_source"

    def fetch(self) -> List[RawItem]:
        return [
            RawItem(
                external_id="123",
                platform="mock_source",
                payload={"title": "Test Item"},
            )
        ]

    def to_draft(self, item: RawItem) -> DraftChange:
        return DraftChange(
            entity_type="project",
            entity_id=None,
            diff=item.payload,
            ai_rationale="Simulated connector ingestion.",
        )


def test_connector_protocol_conformance() -> None:
    """Verifies that dummy connector complies with Connector protocol."""
    connector: Connector = DummyConnector()
    assert connector.name == "mock_source"
    items = connector.fetch()
    assert len(items) == 1
    draft = connector.to_draft(items[0])
    assert draft.entity_type == "project"
    assert "Test Item" in draft.diff["title"]
    assert draft.ai_rationale != ""
