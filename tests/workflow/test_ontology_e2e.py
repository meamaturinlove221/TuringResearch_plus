from __future__ import annotations

import re
from pathlib import Path

from turing_research_plus.vault_graph.alias_resolver import (
    render_alias_resolution_report,
    resolve_aliases,
)
from turing_research_plus.vault_graph.edge_builder import build_edge
from turing_research_plus.vault_graph.models import VaultGraph, VaultGraphEdgeType
from turing_research_plus.vault_graph.node_builder import build_concept_node
from turing_research_plus.vault_graph.ontology_gap_detector import (
    detect_ontology_gaps,
    render_ontology_gap_report,
)
from turing_research_plus.vault_graph.ontology_sop_runner import (
    render_ontology_sop_runbook,
    run_ontology_sop_plan,
)

ROOT = Path(__file__).resolve().parents[2]
DEMO = ROOT / "examples" / "ontology_demo" / "e2e"
CONCEPTS = DEMO / "concept_notes"
GENERATED = DEMO / "generated"

ALIAS_PATTERN = re.compile(r"^- aliases: (.+)$", re.MULTILINE)
LINK_PATTERN = re.compile(r"\[\[([^\]]+)\]\]")


def _slug(label: str) -> str:
    return label.strip().lower().replace("/", "-").replace(" ", "-")


def _aliases(text: str) -> list[str]:
    match = ALIAS_PATTERN.search(text)
    if not match:
        return []
    return [item.strip() for item in match.group(1).split(",") if item.strip()]


def _edge_config(
    source_id: str,
    target_id: str,
) -> tuple[VaultGraphEdgeType, list[str], float]:
    if source_id == "research-catalog" and target_id == "root-ontology":
        return VaultGraphEdgeType.BELONGS_TO, ["fake-demo-note"], 0.82
    if source_id == "stress-test" and target_id == "claim-review":
        return VaultGraphEdgeType.REQUIRES, ["fake-demo-note"], 0.74
    if source_id == "claim-review" and target_id == "missing-claim-evidence":
        return VaultGraphEdgeType.SUPPORTS, [], 0.32
    return VaultGraphEdgeType.RELATED_TO, ["fake-demo-note"], 0.7


def _graph_from_concept_notes() -> VaultGraph:
    nodes = []
    edges = []
    for path in sorted(CONCEPTS.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        node_id = _slug(path.stem)
        nodes.append(
            build_concept_node(
                node_id,
                path.stem,
                aliases=_aliases(text),
                source_refs=[] if node_id == "claim-review" else ["fake-demo-note"],
                confidence=0.38 if node_id == "claim-review" else 0.78,
            )
        )
        for linked_label in LINK_PATTERN.findall(text):
            target_id = _slug(linked_label)
            edge_type, source_refs, confidence = _edge_config(node_id, target_id)
            edges.append(
                build_edge(
                    node_id,
                    target_id,
                    edge_type,
                    source_refs=source_refs,
                    confidence=confidence,
                )
            )
    return VaultGraph(graph_id="ontology-e2e", nodes=nodes, edges=edges)


def test_ontology_e2e_demo_files_exist() -> None:
    expected = [
        DEMO / "README.md",
        CONCEPTS / "Root Ontology.md",
        CONCEPTS / "Research Catalog.md",
        CONCEPTS / "Stress Test.md",
        CONCEPTS / "Claim Review.md",
        GENERATED / "alias_resolution.md",
        GENERATED / "gap_report.md",
        GENERATED / "edge_suggestions.md",
        GENERATED / "ontology_report.md",
        ROOT / "docs" / "ontology-e2e.md",
    ]

    for path in expected:
        assert path.exists(), path


def test_ontology_e2e_resolves_aliases_and_reports_unresolved_terms() -> None:
    graph = _graph_from_concept_notes()
    alias_report = resolve_aliases(
        graph,
        [
            "research workflow catalog",
            "stress gate",
            "claim audit note",
            "unknown ontology term",
        ],
    )

    assert alias_report.by_alias()["research workflow catalog"].canonical_node_id == (
        "research-catalog"
    )
    assert alias_report.by_alias()["stress gate"].canonical_node_id == "stress-test"
    assert alias_report.by_alias()["claim audit note"].canonical_node_id == (
        "claim-review"
    )
    assert alias_report.unresolved_aliases == ["unknown ontology term"]
    assert alias_report.requires_human_review is True


def test_ontology_e2e_detects_gaps_and_suggests_edges() -> None:
    graph = _graph_from_concept_notes()
    gap_report = detect_ontology_gaps(graph)

    assert gap_report.release_blocker is True
    assert gap_report.missing_source_ref_nodes == ["claim-review"]
    assert gap_report.low_confidence_nodes == ["claim-review"]
    assert "stress-test" in gap_report.missing_hierarchy_edges
    assert "claim-review" in gap_report.missing_hierarchy_edges
    assert "claim-review->missing-claim-evidence:supports" in (
        gap_report.dangling_edges
    )

    edge_suggestions = (GENERATED / "edge_suggestions.md").read_text(encoding="utf-8")
    assert "`stress-test -> root-ontology` (`belongs_to`)" in edge_suggestions
    assert "`claim-review -> root-ontology` (`belongs_to`)" in edge_suggestions
    assert "`claim-review -> missing-claim-evidence` (`supports`)" in edge_suggestions
    assert "human review required" in edge_suggestions


def test_ontology_e2e_builds_sop_plan_and_report() -> None:
    graph = _graph_from_concept_notes()
    plan = run_ontology_sop_plan(
        graph,
        sop_names=[
            "alias-resolution",
            "gap-detection",
            "concept-page-creation",
            "edge-batch-creation",
            "ontology-export",
        ],
        aliases=[
            "research workflow catalog",
            "stress gate",
            "claim audit note",
            "unknown ontology term",
        ],
    )

    assert [step.sop_name for step in plan.steps] == [
        "alias-resolution",
        "gap-detection",
        "concept-page-creation",
        "edge-batch-creation",
        "ontology-export",
    ]
    assert plan.final_knowledge_graph_generated is False
    assert plan.network_required is False
    assert plan.requires_human_review is True
    assert plan.gap_report.release_blocker is True
    assert plan.alias_report.unresolved_aliases == ["unknown ontology term"]

    rendered = "\n".join(
        [
            render_alias_resolution_report(plan.alias_report),
            render_ontology_gap_report(plan.gap_report),
            render_ontology_sop_runbook(plan),
        ]
    )
    static_report = (GENERATED / "ontology_report.md").read_text(encoding="utf-8")

    for term in [
        "Alias Resolution Report: ontology-e2e",
        "Ontology Gap Report: ontology-e2e",
        "Ontology SOP Runbook: ontology-e2e",
        "Final knowledge graph generated: `false`",
        "Network required: `false`",
        "`unknown ontology term`",
    ]:
        assert term in rendered
        assert term in static_report


def test_ontology_e2e_docs_preserve_safety_boundaries() -> None:
    combined = "\n".join(
        path.read_text(encoding="utf-8")
        for path in [
            DEMO / "README.md",
            ROOT / "docs" / "ontology-e2e.md",
            GENERATED / "ontology_report.md",
        ]
    )

    required = [
        "fake/demo only",
        "no final knowledge graph",
        "no private data",
        "no default network",
        "no Evidence Ledger mutation",
        "no automatic truth inference",
        "human review required",
    ]
    for item in required:
        assert item in combined

    assert ("Tuling" + "Research") not in combined
    assert ("D:" + "/vggt") not in combined
    assert ("local_project_links" + ".yaml") not in combined
    assert ('"status": "' + 'observed"') not in combined
