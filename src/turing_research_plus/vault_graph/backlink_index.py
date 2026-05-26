"""Backlink index helpers for lightweight vault graphs."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from turing_research_plus.vault_graph.models import VaultGraph


class BacklinkEntry(BaseModel):
    """Incoming links for one vault node."""

    model_config = ConfigDict(extra="forbid")

    node_id: str = Field(min_length=1)
    label: str = Field(min_length=1)
    backlinks: list[str] = Field(default_factory=list)
    outgoing_links: list[str] = Field(default_factory=list)
    requires_human_review: bool = True


class BacklinkIndex(BaseModel):
    """Review-only backlink index."""

    model_config = ConfigDict(extra="forbid")

    graph_id: str = Field(min_length=1)
    entries: list[BacklinkEntry] = Field(default_factory=list)
    dangling_targets: list[str] = Field(default_factory=list)
    requires_human_review: bool = True

    def by_node_id(self) -> dict[str, BacklinkEntry]:
        """Return entries keyed by node id."""

        return {entry.node_id: entry for entry in self.entries}


def build_backlink_index(graph: VaultGraph) -> BacklinkIndex:
    """Build incoming and outgoing link index for a graph."""

    labels = {node.node_id: node.label for node in graph.nodes}
    incoming: dict[str, list[str]] = {node.node_id: [] for node in graph.nodes}
    outgoing: dict[str, list[str]] = {node.node_id: [] for node in graph.nodes}
    dangling_targets: list[str] = []

    for edge in graph.edges:
        if edge.source_id in outgoing:
            outgoing[edge.source_id].append(edge.target_id)
        if edge.target_id in incoming:
            incoming[edge.target_id].append(edge.source_id)
        else:
            dangling_targets.append(edge.target_id)

    entries = [
        BacklinkEntry(
            node_id=node_id,
            label=labels[node_id],
            backlinks=sorted(set(incoming[node_id])),
            outgoing_links=sorted(set(outgoing[node_id])),
        )
        for node_id in sorted(labels)
    ]
    return BacklinkIndex(
        graph_id=graph.graph_id,
        entries=entries,
        dangling_targets=sorted(set(dangling_targets)),
    )


def render_backlink_index(index: BacklinkIndex) -> str:
    """Render backlink index as Markdown."""

    lines = [
        f"# Backlink Index: {index.graph_id}",
        "",
        f"- Requires human review: `{str(index.requires_human_review).lower()}`",
        "",
        "| Node | Backlinks | Outgoing |",
        "| --- | --- | --- |",
    ]
    for entry in index.entries:
        backlinks = ", ".join(f"`{item}`" for item in entry.backlinks) or "none"
        outgoing = ", ".join(f"`{item}`" for item in entry.outgoing_links) or "none"
        lines.append(f"| `{entry.node_id}` | {backlinks} | {outgoing} |")
    return "\n".join(lines) + "\n"
