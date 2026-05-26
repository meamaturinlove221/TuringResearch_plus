from __future__ import annotations

from turing_research_plus.vault_graph.edge_builder import build_edge
from turing_research_plus.vault_graph.models import VaultGraph, VaultGraphEdgeType
from turing_research_plus.vault_graph.node_builder import build_concept_node
from turing_research_plus.vault_graph.ontology_sop_runner import (
    render_ontology_sop_runbook,
    run_ontology_sop_plan,
)


def test_ontology_sop_runner_builds_review_only_plan() -> None:
    graph = VaultGraph(
        graph_id="sop-plan",
        nodes=[
            build_concept_node("concept", "Concept", aliases=["concept alias"]),
            build_concept_node("root", "Root", source_refs=["demo"]),
        ],
        edges=[build_edge("concept", "root", VaultGraphEdgeType.BELONGS_TO)],
    )

    plan = run_ontology_sop_plan(
        graph,
        sop_names=["alias-resolution", "gap-detection", "ontology-export"],
        aliases=["concept alias", "missing alias"],
    )

    assert plan.final_knowledge_graph_generated is False
    assert plan.network_required is False
    assert plan.requires_human_review is True
    assert [step.sop_name for step in plan.steps] == [
        "alias-resolution",
        "gap-detection",
        "ontology-export",
    ]
    assert plan.alias_report.by_alias()["concept alias"].canonical_node_id == "concept"
    assert plan.alias_report.unresolved_aliases == ["missing alias"]
    assert plan.proposed_outputs

    markdown = render_ontology_sop_runbook(plan)
    assert "Final knowledge graph generated: `false`" in markdown
    assert "Network required: `false`" in markdown
