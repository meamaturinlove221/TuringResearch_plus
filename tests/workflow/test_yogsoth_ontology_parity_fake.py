from __future__ import annotations

from pathlib import Path

from turing_research_plus.vault_graph.alias_resolver import resolve_aliases
from turing_research_plus.vault_graph.edge_builder import build_edge
from turing_research_plus.vault_graph.models import VaultGraph, VaultGraphEdgeType
from turing_research_plus.vault_graph.node_builder import build_concept_node
from turing_research_plus.vault_graph.ontology_gap_detector import detect_ontology_gaps
from turing_research_plus.vault_graph.ontology_sop_runner import run_ontology_sop_plan

ROOT = Path(__file__).resolve().parents[2]


def test_yogsoth_ontology_parity_fake_workflow_is_review_only() -> None:
    graph = VaultGraph(
        graph_id="ontology-parity-fake",
        nodes=[
            build_concept_node(
                "north-star",
                "North Star",
                aliases=["north star question"],
                source_refs=["demo"],
            ),
            build_concept_node("hypothesis", "Hypothesis", confidence=0.4),
            build_concept_node("catalog", "Research Catalog", source_refs=["demo"]),
        ],
        edges=[
            build_edge("north-star", "catalog", VaultGraphEdgeType.BELONGS_TO),
            build_edge("hypothesis", "missing-node", VaultGraphEdgeType.RELATED_TO),
        ],
    )

    alias_report = resolve_aliases(graph, ["north star question", "unknown"])
    gap_report = detect_ontology_gaps(graph)
    plan = run_ontology_sop_plan(
        graph,
        sop_names=["alias-resolution", "gap-detection", "ontology-export"],
        aliases=["north star question"],
    )

    assert alias_report.by_alias()["north star question"].canonical_node_id == "north-star"
    assert alias_report.unresolved_aliases == ["unknown"]
    assert gap_report.release_blocker is True
    assert "hypothesis->missing-node:related_to" in gap_report.dangling_edges
    assert plan.final_knowledge_graph_generated is False
    assert plan.network_required is False
    assert plan.requires_human_review is True


def test_yogsoth_ontology_docs_and_contract_exist() -> None:
    expected_paths = [
        ROOT / "contracts" / "yogsoth_ontology_parity.yaml",
        ROOT / "docs" / "yogsoth-ontology-parity.md",
        ROOT / "docs" / "ontology-sop-runbook.md",
    ]

    for path in expected_paths:
        assert path.exists(), path

    contract = (ROOT / "contracts" / "yogsoth_ontology_parity.yaml").read_text(
        encoding="utf-8"
    )
    assert "final_knowledge_graph: false" in contract
    assert "network_required: false" in contract
