from __future__ import annotations

from pathlib import Path

from turing_research_plus.vault_graph.edge_audit import audit_vault_graph
from turing_research_plus.vault_graph.edge_builder import build_edge
from turing_research_plus.vault_graph.models import VaultGraph, VaultGraphEdgeType
from turing_research_plus.vault_graph.node_builder import build_concept_node
from turing_research_plus.vault_graph.ontology import run_ontology_sop
from turing_research_plus.vault_graph.wikilink_export import export_wikilink_summary

ROOT = Path(__file__).resolve().parents[2]
EXAMPLE = ROOT / "examples" / "vggt-human-prior-survey" / "vault_graph"


def test_vggt_vault_graph_fake_reports_review_boundaries() -> None:
    graph = VaultGraph(
        graph_id="vggt-method-taxonomy",
        nodes=[
            build_concept_node("vggt", "VGGT", source_refs=["fixture:dogfooding"]),
            build_concept_node("smplx", "SMPL-X", source_refs=["fixture:method-taxonomy"]),
            build_concept_node("sparseconv3d", "SparseConv3D", confidence=0.4),
        ],
        edges=[
            build_edge("smplx", "vggt", VaultGraphEdgeType.MAPS_TO, source_refs=["fixture"]),
            build_edge("sparseconv3d", "vggt", VaultGraphEdgeType.SUPPORTS),
        ],
    )

    report = audit_vault_graph(graph)
    markdown = export_wikilink_summary(graph)
    sop = run_ontology_sop("edge-batch-creation", inputs=["VGGT", "SMPL-X"])

    assert report.missing_edges
    assert "sparseconv3d" in report.low_confidence_nodes
    assert "[[SparseConv3D]]" in markdown
    assert sop.required_human_review is True


def test_vggt_vault_graph_example_docs_exist() -> None:
    assert "[[VGGT]]" in (EXAMPLE / "vggt_method_taxonomy.md").read_text(encoding="utf-8")
    assert "`related_to`" in (EXAMPLE / "vggt_related_work_graph.md").read_text(
        encoding="utf-8"
    )
    assert "not proof" in (EXAMPLE / "edge_audit_report.md").read_text(encoding="utf-8")
