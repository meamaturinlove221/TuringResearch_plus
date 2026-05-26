from __future__ import annotations

from turing_research_plus.vault_graph.edge_builder import build_edge
from turing_research_plus.vault_graph.models import (
    VaultGraph,
    VaultGraphEdgeType,
    VaultGraphNodeType,
)
from turing_research_plus.vault_graph.node_builder import build_node
from turing_research_plus.vault_graph.ontology_gap_detector import (
    detect_ontology_gaps,
    render_ontology_gap_report,
)


def test_ontology_gap_detector_reports_review_gaps() -> None:
    graph = VaultGraph(
        graph_id="gap-demo",
        nodes=[
            build_node(
                "concept",
                "Concept",
                VaultGraphNodeType.CONCEPT,
                confidence=0.3,
            ),
            build_node(
                "root",
                "Root Concept",
                VaultGraphNodeType.CONCEPT,
                source_refs=["demo"],
            ),
        ],
        edges=[
            build_edge("concept", "missing", VaultGraphEdgeType.RELATED_TO),
        ],
    )

    report = detect_ontology_gaps(graph)

    assert report.release_blocker is True
    assert report.missing_source_ref_nodes == ["concept"]
    assert report.low_confidence_nodes == ["concept"]
    assert report.dangling_edges == ["concept->missing:related_to"]
    assert "concept" in report.missing_hierarchy_edges
    assert "root" in report.orphan_nodes

    markdown = render_ontology_gap_report(report)
    assert "Ontology Gap Report" in markdown
    assert "`dangling_edge`" in markdown
