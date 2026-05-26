"""Citation graph scoring helpers."""

from __future__ import annotations

from turing_research_plus.citation_graph.models import CitationGraphNode


def score_frontier_node(node: CitationGraphNode) -> float:
    """Score frontier nodes for next-read priority."""

    topic_bonus = 0.2 * len(node.topics)
    citation_component = min(node.citation_count / 1000, 1.0)
    recency_component = 0.0
    if node.year:
        recency_component = max(min((node.year - 2015) / 10, 1.0), 0.0)
    return round(citation_component + recency_component + topic_bonus, 4)


def sort_frontier_nodes(nodes: list[CitationGraphNode]) -> list[CitationGraphNode]:
    """Return nodes ordered by deterministic frontier score."""

    return sorted(nodes, key=lambda node: (score_frontier_node(node), node.title), reverse=True)
