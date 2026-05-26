"""Markdown export for citation graphs."""

from __future__ import annotations

from turing_research_plus.citation_graph.frontier import frontier_report_markdown
from turing_research_plus.citation_graph.models import CitationGraph


def citation_graph_to_markdown(graph: CitationGraph) -> str:
    """Render a citation graph as compact Markdown."""

    lines = [
        f"# Citation Graph: {graph.graph_id}",
        "",
        f"Retrieval status: `{graph.retrieval_status}`",
        f"Source adapter: `{graph.source_adapter}`",
        f"Expansion depth: `{graph.expansion_depth}`",
        f"Requires human review: `{graph.requires_human_review}`",
        "",
        "## Seed Papers",
    ]
    lines.extend(f"- `{node.paper_id}` {node.title}" for node in graph.seed_papers)
    lines.extend(["", "## Nodes"])
    lines.extend(f"- `{node.paper_id}` {node.title}" for node in graph.nodes)
    lines.extend(["", "## Edges"])
    lines.extend(
        f"- `{edge.source_id}` -[{edge.edge_type}]-> `{edge.target_id}`"
        for edge in graph.edges
    )
    if graph.limitations:
        lines.extend(["", "## Limitations"])
        lines.extend(f"- {item}" for item in graph.limitations)
    return "\n".join(lines) + "\n"


def citation_frontier_to_markdown(graph: CitationGraph, limit: int = 10) -> str:
    """Render frontier report Markdown."""

    return frontier_report_markdown(graph, limit=limit)
