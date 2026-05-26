"""Edge builders for lightweight vault graphs."""

from __future__ import annotations

from turing_research_plus.vault_graph.models import VaultGraphEdge, VaultGraphEdgeType


def build_edge(
    source_id: str,
    target_id: str,
    edge_type: VaultGraphEdgeType,
    *,
    source_refs: list[str] | None = None,
    confidence: float = 0.5,
) -> VaultGraphEdge:
    """Build a typed edge."""

    return VaultGraphEdge(
        source_id=source_id,
        target_id=target_id,
        edge_type=edge_type,
        source_refs=source_refs or [],
        confidence=confidence,
        requires_human_review=True,
    )
