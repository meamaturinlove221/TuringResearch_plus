"""Wiki-style export for vault graph parity."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from turing_research_plus.vault_graph.backlink_index import (
    BacklinkIndex,
    build_backlink_index,
)
from turing_research_plus.vault_graph.dangling_link_report import (
    DanglingLinkReport,
    build_dangling_link_report,
)
from turing_research_plus.vault_graph.edge_quality import (
    VaultEdgeQualityReport,
    evaluate_edge_quality,
)
from turing_research_plus.vault_graph.models import VaultGraph
from turing_research_plus.vault_graph.wikilink_export import wikilink


class WikiVaultExport(BaseModel):
    """Review-only wiki/vault export package."""

    model_config = ConfigDict(extra="forbid")

    graph_id: str = Field(min_length=1)
    pages: dict[str, str] = Field(default_factory=dict)
    backlink_index: BacklinkIndex
    dangling_link_report: DanglingLinkReport
    edge_quality_report: VaultEdgeQualityReport
    graph_summary: dict[str, int] = Field(default_factory=dict)
    requires_human_review: bool = True


def build_wiki_vault_export(graph: VaultGraph) -> WikiVaultExport:
    """Build a wiki-style export package from a vault graph."""

    backlinks = build_backlink_index(graph)
    dangling = build_dangling_link_report(graph)
    edge_quality = evaluate_edge_quality(graph)
    pages = {
        _page_name(node.label): _render_node_page(graph, node.node_id)
        for node in graph.nodes
    }
    return WikiVaultExport(
        graph_id=graph.graph_id,
        pages=pages,
        backlink_index=backlinks,
        dangling_link_report=dangling,
        edge_quality_report=edge_quality,
        graph_summary=edge_quality.graph_summary,
    )


def render_wiki_vault_export(export: WikiVaultExport) -> str:
    """Render a compact export index as Markdown."""

    lines = [
        f"# Wiki Vault Export: {export.graph_id}",
        "",
        f"- Requires human review: `{str(export.requires_human_review).lower()}`",
        f"- Pages: `{len(export.pages)}`",
        f"- Dangling links: `{len(export.dangling_link_report.dangling_links)}`",
        f"- Weak edges: `{len(export.edge_quality_report.weak_edges)}`",
        "",
        "## Pages",
        "",
    ]
    lines.extend([f"- {wikilink(page)}" for page in sorted(export.pages)])
    return "\n".join(lines) + "\n"


def _page_name(label: str) -> str:
    return label.strip().replace("/", "-")


def _render_node_page(graph: VaultGraph, node_id: str) -> str:
    labels = {node.node_id: node.label for node in graph.nodes}
    node = next(item for item in graph.nodes if item.node_id == node_id)
    incoming = [
        edge.source_id
        for edge in graph.edges
        if edge.target_id == node_id and edge.source_id in labels
    ]
    outgoing = [
        edge.target_id
        for edge in graph.edges
        if edge.source_id == node_id and edge.target_id in labels
    ]
    backlink_lines = [f"- {wikilink(labels[item])}" for item in incoming] or ["- none"]
    outgoing_lines = [f"- {wikilink(labels[item])}" for item in outgoing] or ["- none"]
    lines = [
        f"# {node.label}",
        "",
        f"- Node id: `{node.node_id}`",
        f"- Type: `{node.node_type.value}`",
        f"- Confidence: `{node.confidence}`",
        f"- Requires human review: `{str(node.requires_human_review).lower()}`",
        "",
        "## Backlinks",
        "",
        *backlink_lines,
        "",
        "## Outgoing",
        "",
        *outgoing_lines,
    ]
    return "\n".join(lines) + "\n"
