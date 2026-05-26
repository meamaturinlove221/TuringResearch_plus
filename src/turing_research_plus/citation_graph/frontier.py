"""Frontier selection for citation graphs."""

from __future__ import annotations

from turing_research_plus.citation_graph.models import CitationGraph, CitationGraphNode
from turing_research_plus.citation_graph.scoring import sort_frontier_nodes


def select_frontier_nodes(graph: CitationGraph, limit: int = 10) -> list[CitationGraphNode]:
    """Select non-seed nodes that look useful for follow-up reading."""

    seed_ids = {paper.paper_id for paper in graph.seed_papers}
    candidates = [node for node in graph.nodes if node.paper_id not in seed_ids]
    return sort_frontier_nodes(candidates)[:limit]


def frontier_report_markdown(graph: CitationGraph, limit: int = 10) -> str:
    """Render a short frontier report."""

    lines = [
        f"# Citation Frontier: {graph.graph_id}",
        "",
        f"Retrieval status: `{graph.retrieval_status}`",
        f"Source adapter: `{graph.source_adapter}`",
        "",
        "## Frontier Nodes",
    ]
    for node in select_frontier_nodes(graph, limit=limit):
        lines.append(f"- `{node.paper_id}` {node.title} ({node.year or 'unknown year'})")
    if graph.limitations:
        lines.extend(["", "## Limitations"])
        lines.extend(f"- {item}" for item in graph.limitations)
    return "\n".join(lines) + "\n"
