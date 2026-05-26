"""Static search index builder for vault UI."""

from __future__ import annotations

from turing_research_plus.vault_graph.models import VaultGraph
from turing_research_plus.vault_ui.models import VaultSearchEntry


def build_vault_search_index(graph: VaultGraph) -> list[VaultSearchEntry]:
    """Build a static search index from vault graph nodes."""

    return [
        VaultSearchEntry(
            entry_id=node.node_id,
            title=node.label,
            node_type=node.node_type,
            text=" ".join(
                [
                    node.label,
                    node.node_type,
                    *node.aliases,
                    *node.source_refs,
                    node.status,
                ]
            ),
            href=f"#node-{node.node_id}",
            requires_human_review=node.requires_human_review,
        )
        for node in graph.nodes
    ]
