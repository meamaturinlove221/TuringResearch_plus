from __future__ import annotations

from pathlib import Path

from turing_research_plus.vault_graph.alias_resolver import resolve_aliases
from turing_research_plus.vault_graph.edge_builder import build_edge
from turing_research_plus.vault_graph.models import VaultGraph, VaultGraphEdgeType
from turing_research_plus.vault_graph.node_builder import build_concept_node
from turing_research_plus.vault_graph.ontology_gap_detector import detect_ontology_gaps
from turing_research_plus.vault_graph.ontology_sop_runner import (
    run_ontology_sop_plan,
)

ROOT = Path(__file__).resolve().parents[2]
DEMO = ROOT / "examples" / "ontology_demo"


def _demo_graph() -> VaultGraph:
    return VaultGraph(
        graph_id="ontology-demo",
        nodes=[
            build_concept_node(
                "north-star",
                "North Star",
                aliases=["north star question", "research target"],
                source_refs=["fake-demo"],
                confidence=0.8,
            ),
            build_concept_node(
                "hypothesis",
                "Hypothesis",
                aliases=["research claim"],
                confidence=0.4,
            ),
            build_concept_node(
                "research-catalog",
                "Research Catalog",
                aliases=["research workflow catalog"],
                source_refs=["fake-demo"],
                confidence=0.75,
            ),
        ],
        edges=[
            build_edge(
                "north-star",
                "research-catalog",
                VaultGraphEdgeType.BELONGS_TO,
                source_refs=["fake-demo"],
            ),
            build_edge("hypothesis", "missing-node", VaultGraphEdgeType.RELATED_TO),
        ],
    )


def test_ontology_runbook_demo_files_exist() -> None:
    expected = [
        DEMO / "README.md",
        DEMO / "concepts" / "North Star.md",
        DEMO / "concepts" / "Hypothesis.md",
        DEMO / "concepts" / "Research Catalog.md",
        DEMO / "ontology_runbook.md",
        DEMO / "gap_report.md",
        ROOT / "docs" / "ontology-runbook-demo.md",
    ]

    for path in expected:
        assert path.exists(), path


def test_ontology_runbook_demo_matches_runtime_reports() -> None:
    graph = _demo_graph()
    aliases = ["north star question", "research workflow catalog", "unknown term"]
    alias_report = resolve_aliases(graph, aliases)
    gap_report = detect_ontology_gaps(graph)
    plan = run_ontology_sop_plan(
        graph,
        sop_names=[
            "alias-resolution",
            "gap-detection",
            "concept-page-creation",
            "edge-batch-creation",
            "ontology-export",
        ],
        aliases=aliases,
    )

    assert alias_report.by_alias()["north star question"].canonical_node_id == (
        "north-star"
    )
    assert alias_report.by_alias()["research workflow catalog"].canonical_node_id == (
        "research-catalog"
    )
    assert alias_report.unresolved_aliases == ["unknown term"]
    assert "hypothesis" in gap_report.missing_source_ref_nodes
    assert "hypothesis" in gap_report.low_confidence_nodes
    assert "hypothesis" in gap_report.missing_hierarchy_edges
    assert "hypothesis->missing-node:related_to" in gap_report.dangling_edges
    assert plan.final_knowledge_graph_generated is False
    assert plan.network_required is False
    assert plan.requires_human_review is True


def test_ontology_runbook_demo_markdown_covers_required_surfaces() -> None:
    combined = "\n".join(
        [
            (DEMO / "README.md").read_text(encoding="utf-8"),
            (DEMO / "ontology_runbook.md").read_text(encoding="utf-8"),
            (DEMO / "gap_report.md").read_text(encoding="utf-8"),
            (ROOT / "docs" / "ontology-runbook-demo.md").read_text(encoding="utf-8"),
        ]
    )

    required = [
        "alias resolution",
        "gap detection",
        "concept pages",
        "edge suggestions",
        "unresolved",
        "missing source references",
        "low-confidence",
        "dangling edge",
        "Final knowledge graph generated: `false`",
    ]
    for term in required:
        assert term in combined


def test_ontology_runbook_demo_is_public_safe() -> None:
    paths = [
        DEMO / "README.md",
        DEMO / "concepts" / "North Star.md",
        DEMO / "concepts" / "Hypothesis.md",
        DEMO / "concepts" / "Research Catalog.md",
        DEMO / "ontology_runbook.md",
        DEMO / "gap_report.md",
        ROOT / "docs" / "ontology-runbook-demo.md",
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in paths)

    assert "fake/demo only" in combined
    assert "no network" in combined
    assert "no private data" in combined
    assert "no Evidence Ledger mutation" in combined
    assert "no final knowledge graph" in combined

    forbidden = ["D:/vggt", "D:\\vggt", "local_project_links.yaml", "ghp_", "sk-"]
    for marker in forbidden:
        assert marker not in combined
