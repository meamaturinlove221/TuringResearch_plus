from __future__ import annotations

from turing_research_plus.vault_graph.models import VaultGraphNodeType
from turing_research_plus.vault_graph.node_builder import build_concept_node, build_node


def test_build_concept_node_requires_review() -> None:
    node = build_concept_node("smplx", "SMPL-X", aliases=["SMPLX"])

    assert node.node_type == VaultGraphNodeType.CONCEPT
    assert node.requires_human_review is True
    assert "SMPLX" in node.aliases


def test_build_typed_node() -> None:
    node = build_node("route", "Modal route", VaultGraphNodeType.ROUTE, confidence=0.7)

    assert node.node_type == VaultGraphNodeType.ROUTE
    assert node.confidence == 0.7
