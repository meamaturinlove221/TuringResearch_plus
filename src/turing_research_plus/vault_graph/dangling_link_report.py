"""Dangling link report for lightweight vault graphs."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from turing_research_plus.vault_graph.models import VaultGraph


class DanglingLink(BaseModel):
    """One graph edge that points to a missing node."""

    model_config = ConfigDict(extra="forbid")

    source_id: str = Field(min_length=1)
    target_id: str = Field(min_length=1)
    edge_type: str = Field(min_length=1)
    severity: str = "high"
    requires_human_review: bool = True


class DanglingLinkReport(BaseModel):
    """Review-only dangling link report."""

    model_config = ConfigDict(extra="forbid")

    graph_id: str = Field(min_length=1)
    dangling_links: list[DanglingLink] = Field(default_factory=list)
    release_blocker: bool = False
    requires_human_review: bool = True


def build_dangling_link_report(graph: VaultGraph) -> DanglingLinkReport:
    """Return dangling edges where source or target node is missing."""

    node_ids = {node.node_id for node in graph.nodes}
    dangling = [
        DanglingLink(
            source_id=edge.source_id,
            target_id=edge.target_id,
            edge_type=edge.edge_type.value,
        )
        for edge in graph.edges
        if edge.source_id not in node_ids or edge.target_id not in node_ids
    ]
    return DanglingLinkReport(
        graph_id=graph.graph_id,
        dangling_links=dangling,
        release_blocker=bool(dangling),
    )


def render_dangling_link_report(report: DanglingLinkReport) -> str:
    """Render dangling link report as Markdown."""

    lines = [
        f"# Dangling Link Report: {report.graph_id}",
        "",
        f"- Release blocker: `{str(report.release_blocker).lower()}`",
        f"- Requires human review: `{str(report.requires_human_review).lower()}`",
        "",
        "## Dangling Links",
        "",
    ]
    lines.extend(
        [
            f"- `{link.source_id}` -> `{link.target_id}` (`{link.edge_type}`)"
            for link in report.dangling_links
        ]
        or ["- none"]
    )
    return "\n".join(lines) + "\n"
