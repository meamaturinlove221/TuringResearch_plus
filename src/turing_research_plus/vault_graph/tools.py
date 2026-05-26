"""Tool-style wrappers for vault graph helpers."""

from __future__ import annotations

from turing_research_plus.vault_graph.edge_audit import audit_vault_graph
from turing_research_plus.vault_graph.models import VaultGraph, VaultGraphAuditReport
from turing_research_plus.vault_graph.wikilink_export import export_wikilink_summary


def vault_graph_audit(graph: VaultGraph) -> VaultGraphAuditReport:
    """Audit a vault graph."""

    return audit_vault_graph(graph)


def vault_graph_markdown(graph: VaultGraph) -> str:
    """Export a vault graph as Markdown with wikilinks."""

    return export_wikilink_summary(graph)
