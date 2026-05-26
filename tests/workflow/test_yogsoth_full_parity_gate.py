from __future__ import annotations

import json
from pathlib import Path

from turing_research_plus.artifacts.models import EvidenceRef
from turing_research_plus.campaigns import build_campaign_execution_trace
from turing_research_plus.convergence import (
    CandidateKind,
    ConvergenceCandidate,
    build_convergence_decision_report,
)
from turing_research_plus.stress_test import build_stress_scenario_library

ROOT = Path(__file__).resolve().parents[2]


def evidence(source_id: str) -> EvidenceRef:
    return EvidenceRef(
        source_id=source_id,
        locator="section-1",
        quote="Fake evidence for yogsoth full parity gate.",
    )


def candidate(candidate_id: str, feasibility: float, novelty: float) -> ConvergenceCandidate:
    return ConvergenceCandidate(
        candidate_id=candidate_id,
        kind=CandidateKind.IMPLEMENTATION_VARIANT,
        title=f"Route {candidate_id}",
        mechanism="local route comparison",
        expected_gain="Improve v1.3 implementation quality.",
        feasibility=feasibility,
        novelty=novelty,
        risk="medium",
        required_resources=["review table"],
        evidence_refs=[evidence(candidate_id)],
    )


def test_yogsoth_full_parity_surfaces_are_fake_runnable() -> None:
    trace = build_campaign_execution_trace(
        "stress test unsupported route",
        provided_inputs=["candidate claim or release surface"],
    )
    stress_library = build_stress_scenario_library()
    convergence = build_convergence_decision_report(
        [
            candidate("campaign-trace-first", 0.9, 0.75),
            candidate("dashboard-first", 0.72, 0.78),
        ],
        report_id="yogsoth-full-parity-gate",
    )

    assert trace.fake_trace is True
    assert trace.ready_for_execution is False
    assert all(step.executed is False for step in trace.steps)
    assert "missing_evidence" in stress_library.by_id()
    assert "advisor_report_overclaim" in stress_library.by_id()
    assert convergence.final_recommendation == "campaign-trace-first"
    assert "Run stress-test review before implementation." in convergence.next_actions


def test_yogsoth_full_parity_docs_and_demos_exist() -> None:
    required_paths = [
        ROOT / "docs" / "campaign-execution-trace.md",
        ROOT / "docs" / "research-catalog-dashboard.md",
        ROOT / "docs" / "vault-wiki-export-demo.md",
        ROOT / "docs" / "ontology-runbook-demo.md",
        ROOT / "docs" / "stress-scenario-library.md",
        ROOT / "docs" / "convergence-decision-report.md",
        ROOT / "docs" / "yogsoth-full-parity-gate-report.md",
        ROOT / "docs" / "yogsoth-full-parity-go-no-go.md",
        ROOT / "examples" / "research_catalog" / "dashboard.json",
        ROOT / "examples" / "vault_wiki_demo" / "edge_audit_report.md",
        ROOT / "examples" / "ontology_demo" / "ontology_runbook.md",
        ROOT / "examples" / "stress_scenarios" / "README.md",
        ROOT / "examples" / "convergence_demo" / "decision_report.md",
    ]

    for path in required_paths:
        assert path.exists(), path


def test_yogsoth_full_parity_dashboard_is_review_only() -> None:
    dashboard = json.loads(
        (ROOT / "examples" / "research_catalog" / "dashboard.json").read_text(
            encoding="utf-8"
        )
    )

    assert dashboard["dashboard_only"] is True
    assert dashboard["requires_human_review"] is True
    assert dashboard["no_agent_runtime"] is True
    assert dashboard["no_tool_execution"] is True
    assert dashboard["no_default_network"] is True
    assert dashboard["no_experiment_execution"] is True


def test_yogsoth_full_parity_gate_docs_record_go_no_go() -> None:
    report = (ROOT / "docs" / "yogsoth-full-parity-gate-report.md").read_text(
        encoding="utf-8"
    )
    go_no_go = (ROOT / "docs" / "yogsoth-full-parity-go-no-go.md").read_text(
        encoding="utf-8"
    )
    combined = report + "\n" + go_no_go

    required = [
        "GO WITH REVIEW",
        "Campaign trace",
        "Research Catalog dashboard",
        "Vault wiki demo",
        "Ontology demo",
        "Stress scenario library",
        "Convergence decision report",
        "No agent runtime",
        "No fake result observed",
        "human review required",
    ]
    for term in required:
        assert term in combined


def test_yogsoth_full_parity_gate_is_public_safe() -> None:
    paths = [
        ROOT / "docs" / "yogsoth-full-parity-gate-report.md",
        ROOT / "docs" / "yogsoth-full-parity-go-no-go.md",
        ROOT / "docs" / "campaign-execution-trace.md",
        ROOT / "docs" / "research-catalog-dashboard.md",
        ROOT / "docs" / "vault-wiki-export-demo.md",
        ROOT / "docs" / "ontology-runbook-demo.md",
        ROOT / "docs" / "stress-scenario-library.md",
        ROOT / "docs" / "convergence-decision-report.md",
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in paths)

    forbidden = ["D:/vggt", "D:\\vggt", "local_project_links.yaml", "ghp_", "sk-"]
    for marker in forbidden:
        assert marker not in combined

    assert "Tuling" + "Research" not in combined
    assert "automatic Evidence Ledger mutation" in combined
    assert "fake/demo result promotion" in combined
