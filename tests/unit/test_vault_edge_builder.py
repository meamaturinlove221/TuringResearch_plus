from __future__ import annotations

from turing_research_plus.vault_graph.edge_builder import build_edge
from turing_research_plus.vault_graph.models import VaultGraphEdgeType


def test_build_edge_preserves_type_and_source_refs() -> None:
    edge = build_edge(
        "neuralbody",
        "sparseconv3d",
        VaultGraphEdgeType.RELATED_TO,
        source_refs=["fixture:method-card"],
    )

    assert edge.edge_type == VaultGraphEdgeType.RELATED_TO
    assert edge.source_refs == ["fixture:method-card"]
    assert edge.requires_human_review is True
