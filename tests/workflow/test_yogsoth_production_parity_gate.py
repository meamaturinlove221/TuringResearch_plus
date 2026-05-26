from __future__ import annotations

import json
from pathlib import Path

from turing_research_plus.campaigns import build_campaign_execution_trace
from turing_research_plus.experiment_execution.plan_builder import (
    build_experiment_execution_plan,
)
from turing_research_plus.experiment_route.models import ExperimentRouteSpec
from turing_research_plus.stress_test.models import StressStatus, StressTestInput
from turing_research_plus.stress_test.runner import run_stress_test
from turing_research_plus.vault_graph.alias_resolver import resolve_aliases
from turing_research_plus.vault_graph.backlink_index import build_backlink_index
from turing_research_plus.vault_graph.dangling_link_report import (
    build_dangling_link_report,
)
from turing_research_plus.vault_graph.edge_builder import build_edge
from turing_research_plus.vault_graph.edge_quality import evaluate_edge_quality
from turing_research_plus.vault_graph.models import VaultGraph, VaultGraphEdgeType
from turing_research_plus.vault_graph.node_builder import build_concept_node
from turing_research_plus.vault_graph.ontology_gap_detector import (
    detect_ontology_gaps,
)
from turing_research_plus.vault_graph.wiki_export import build_wiki_vault_export

ROOT = Path(__file__).resolve().parents[2]


def _vault_graph() -> VaultGraph:
    return VaultGraph(
        graph_id="yogsoth-production-vault-gate",
        nodes=[
            build_concept_node("research-catalog", "Research Catalog"),
            build_concept_node("stress-test", "Stress Test"),
            build_concept_node("artifact-audit", "Artifact Audit", confidence=0.4),
        ],
        edges=[
            build_edge(
                "research-catalog",
                "stress-test",
                VaultGraphEdgeType.MAPS_TO,
                source_refs=["fake-gate"],
            ),
            build_edge("stress-test", "artifact-audit", VaultGraphEdgeType.SUPPORTS),
            build_edge(
                "artifact-audit",
                "missing-evidence",
                VaultGraphEdgeType.SUPPORTS,
                confidence=0.3,
            ),
        ],
    )


def _ontology_graph() -> VaultGraph:
    return VaultGraph(
        graph_id="yogsoth-production-ontology-gate",
        nodes=[
            build_concept_node(
                "research-catalog",
                "Research Catalog",
                aliases=["research workflow catalog"],
                source_refs=["fake-gate"],
            ),
            build_concept_node(
                "claim-review",
                "Claim Review",
                aliases=["claim audit note"],
                confidence=0.35,
            ),
        ],
        edges=[
            build_edge(
                "research-catalog",
                "claim-review",
                VaultGraphEdgeType.REQUIRES,
                source_refs=["fake-gate"],
            ),
            build_edge("claim-review", "missing-claim", VaultGraphEdgeType.SUPPORTS),
        ],
    )


def test_yogsoth_production_gate_e2e_docs_and_examples_exist() -> None:
    required_paths = [
        ROOT / "tests" / "workflow" / "test_campaign_trace_e2e.py",
        ROOT / "tests" / "workflow" / "test_research_catalog_e2e.py",
        ROOT / "tests" / "workflow" / "test_vault_wiki_e2e.py",
        ROOT / "tests" / "workflow" / "test_ontology_e2e.py",
        ROOT / "tests" / "workflow" / "test_stress_convergence_e2e.py",
        ROOT / "tests" / "workflow" / "test_experiment_runbook_e2e.py",
        ROOT / "docs" / "campaign-trace-e2e.md",
        ROOT / "docs" / "research-catalog-e2e.md",
        ROOT / "docs" / "vault-wiki-e2e.md",
        ROOT / "docs" / "ontology-e2e.md",
        ROOT / "docs" / "stress-convergence-e2e.md",
        ROOT / "docs" / "experiment-runbook-e2e.md",
        ROOT / "docs" / "yogsoth-production-parity-gate-report.md",
        ROOT / "docs" / "yogsoth-production-parity-go-no-go.md",
        ROOT / "examples" / "campaigns" / "e2e_trace_demo",
        ROOT / "examples" / "research_catalog" / "e2e_demo",
        ROOT / "examples" / "vault_wiki_demo" / "e2e",
        ROOT / "examples" / "ontology_demo" / "e2e",
        ROOT / "examples" / "stress_convergence_demo" / "e2e",
        ROOT / "examples" / "experiment_execution" / "e2e_runbook_demo",
    ]

    for path in required_paths:
        assert path.exists(), path


def test_yogsoth_production_gate_campaign_and_catalog_e2e_pass() -> None:
    trace = build_campaign_execution_trace(
        "stress test unsafe claim review before public release",
        provided_inputs=["candidate claim or release surface"],
    )
    catalog_report = json.loads(
        (
            ROOT / "examples" / "research_catalog" / "e2e_demo" / "catalog_report.json"
        ).read_text(encoding="utf-8")
    )

    assert trace.fake_trace is True
    assert trace.does_not_execute is True
    assert trace.does_not_use_network is True
    assert trace.does_not_mutate_evidence_ledger is True
    assert trace.ready_for_execution is False
    assert trace.requires_human_review is True
    assert catalog_report["status"] == "pass-with-review"
    assert catalog_report["campaign_id"] == "stress_test"
    assert catalog_report["recommended_skill"] == "turingresearch-fusion-stress-test"


def test_yogsoth_production_gate_vault_and_ontology_e2e_pass() -> None:
    vault_graph = _vault_graph()
    backlinks = build_backlink_index(vault_graph)
    dangling = build_dangling_link_report(vault_graph)
    edge_quality = evaluate_edge_quality(vault_graph)
    wiki_export = build_wiki_vault_export(vault_graph)

    assert backlinks.by_node_id()["stress-test"].backlinks == ["research-catalog"]
    assert dangling.release_blocker is True
    assert "stress-test->artifact-audit:supports" in edge_quality.missing_edges
    assert "artifact-audit->missing-evidence:supports" in edge_quality.weak_edges
    assert wiki_export.requires_human_review is True
    assert "Research Catalog" in wiki_export.pages

    ontology_graph = _ontology_graph()
    alias_report = resolve_aliases(
        ontology_graph,
        ["research workflow catalog", "claim audit note", "unknown term"],
    )
    gap_report = detect_ontology_gaps(ontology_graph)

    assert alias_report.by_alias()["research workflow catalog"].canonical_node_id == (
        "research-catalog"
    )
    assert alias_report.by_alias()["claim audit note"].canonical_node_id == (
        "claim-review"
    )
    assert alias_report.unresolved_aliases == ["unknown term"]
    assert "claim-review" in gap_report.missing_source_ref_nodes
    assert "claim-review" in gap_report.low_confidence_nodes
    assert "claim-review->missing-claim:supports" in gap_report.dangling_edges


def test_yogsoth_production_gate_stress_convergence_and_experiment_e2e_pass() -> None:
    stress_report = run_stress_test(
        StressTestInput(
            target_id="yogsoth-production-gate",
            task_summary="fake/demo only route with safe review boundaries",
            evidence_refs=["fake-evidence:gate"],
            artifact_refs=["artifact:gate-report"],
            related_work_refs=["related:campaign", "related:convergence"],
            route_hard_gates=["no live", "claim experiment completion forbidden"],
            route_forbidden_actions=["claim experiment completion forbidden"],
            route_claims=["route remains proposed-only"],
            advisor_claims=["gate remains review-only"],
            plugin_permissions=[],
            text_blocks=["fake/demo only; no default network; human review required"],
            data_sensitivity="demo",
            fake_demo_only=True,
            live_mode_enabled=False,
        )
    )
    route = ExperimentRouteSpec.model_validate_json(
        (
            ROOT
            / "examples"
            / "experiment_execution"
            / "e2e_runbook_demo"
            / "route_dsl.json"
        ).read_text(encoding="utf-8")
    )
    execution_plan = build_experiment_execution_plan(route)

    assert stress_report.status == StressStatus.PASS
    assert stress_report.blockers == []
    assert stress_report.multi_agent_runtime is False
    assert stress_report.network_required is False
    assert execution_plan.automatically_executes is False
    assert execution_plan.remote_execution is False
    assert execution_plan.modal_call is False
    assert execution_plan.gpu_call is False
    assert execution_plan.writes_observed_result is False
    assert execution_plan.ingest_contract.proposed_evidence_only is True
    assert execution_plan.ingest_contract.writes_observed_result is False


def test_yogsoth_production_gate_docs_record_go_no_go() -> None:
    report = (ROOT / "docs" / "yogsoth-production-parity-gate-report.md").read_text(
        encoding="utf-8"
    )
    go_no_go = (ROOT / "docs" / "yogsoth-production-parity-go-no-go.md").read_text(
        encoding="utf-8"
    )
    combined = report + "\n" + go_no_go

    required = [
        "GO WITH REVIEW",
        "campaign trace E2E",
        "research catalog E2E",
        "vault wiki E2E",
        "ontology E2E",
        "stress/convergence E2E",
        "experiment runbook E2E",
        "No automatic experiment execution",
        "No fake result observed",
        "human review required",
    ]
    for term in required:
        assert term in combined


def test_yogsoth_production_gate_public_safety_boundaries() -> None:
    paths = [
        ROOT / "docs" / "yogsoth-production-parity-gate-report.md",
        ROOT / "docs" / "yogsoth-production-parity-go-no-go.md",
        ROOT / "docs" / "campaign-trace-e2e.md",
        ROOT / "docs" / "research-catalog-e2e.md",
        ROOT / "docs" / "vault-wiki-e2e.md",
        ROOT / "docs" / "ontology-e2e.md",
        ROOT / "docs" / "stress-convergence-e2e.md",
        ROOT / "docs" / "experiment-runbook-e2e.md",
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in paths)

    required = [
        "no default network",
        "no Evidence Ledger mutation",
        "human review required",
    ]
    for term in required:
        assert term in combined

    forbidden = [
        "D:" + "/vggt",
        "D:" + "\\vggt",
        "local_project_links" + ".yaml",
        "ghp_",
        "sk-",
        '"status": "' + 'observed"',
    ]
    for marker in forbidden:
        assert marker not in combined

    assert "Tuling" + "Research" not in combined
    assert "automatic experiment execution enabled" not in combined.lower()
