from __future__ import annotations

from turing_research_plus.citation_graph.models import CitationGraphNode
from turing_research_plus.citation_graph.scoring import score_frontier_node, sort_frontier_nodes


def test_frontier_score_rewards_topics_and_recency() -> None:
    low = CitationGraphNode(paper_id="low", title="Low", year=2010)
    high = CitationGraphNode(
        paper_id="high",
        title="High",
        year=2025,
        citation_count=100,
        topics=["VGGT", "SMPL-X"],
    )

    assert score_frontier_node(high) > score_frontier_node(low)
    assert sort_frontier_nodes([low, high])[0] == high
