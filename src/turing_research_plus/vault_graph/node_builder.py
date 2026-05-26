"""Node builders for lightweight vault graphs."""

from __future__ import annotations

from turing_research_plus.vault_graph.models import VaultGraphNode, VaultGraphNodeType


def build_concept_node(
    node_id: str,
    label: str,
    *,
    source_refs: list[str] | None = None,
    confidence: float = 0.5,
    aliases: list[str] | None = None,
) -> VaultGraphNode:
    """Build a concept node that requires human review by default."""

    return VaultGraphNode(
        node_id=node_id,
        label=label,
        node_type=VaultGraphNodeType.CONCEPT,
        source_refs=source_refs or [],
        confidence=confidence,
        aliases=aliases or [],
        requires_human_review=True,
    )


def build_node(
    node_id: str,
    label: str,
    node_type: VaultGraphNodeType,
    *,
    source_refs: list[str] | None = None,
    confidence: float = 0.5,
) -> VaultGraphNode:
    """Build a typed node."""

    return VaultGraphNode(
        node_id=node_id,
        label=label,
        node_type=node_type,
        source_refs=source_refs or [],
        confidence=confidence,
        requires_human_review=True,
    )
