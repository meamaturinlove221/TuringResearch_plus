from __future__ import annotations

from turing_research_plus.vault_graph.dangling_link_report import (
    build_dangling_link_report,
    render_dangling_link_report,
)
from turing_research_plus.vault_graph.edge_builder import build_edge
from turing_research_plus.vault_graph.models import VaultGraph, VaultGraphEdgeType
from turing_research_plus.vault_graph.node_builder import build_concept_node


def test_dangling_link_report_flags_missing_source_or_target() -> None:
    graph = VaultGraph(
        graph_id="dangling-demo",
        nodes=[build_concept_node("claim", "Claim Node")],
        edges=[
            build_edge("claim", "missing-target", VaultGraphEdgeType.SUPPORTS),
            build_edge("missing-source", "claim", VaultGraphEdgeType.RELATED_TO),
        ],
    )

    report = build_dangling_link_report(graph)

    assert report.release_blocker is True
    assert len(report.dangling_links) == 2
    assert {link.target_id for link in report.dangling_links} == {
        "claim",
        "missing-target",
    }

    markdown = render_dangling_link_report(report)
    assert "Release blocker: `true`" in markdown
    assert "`missing-source` -> `claim`" in markdown
