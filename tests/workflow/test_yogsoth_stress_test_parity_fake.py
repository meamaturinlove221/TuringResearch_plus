from __future__ import annotations

from pathlib import Path

from turing_research_plus.stress_test.models import StressScenarioId, StressStatus, StressTestInput
from turing_research_plus.stress_test.report import render_stress_test_report
from turing_research_plus.stress_test.runner import run_stress_test
from turing_research_plus.stress_test.scenarios import list_stress_scenarios

ROOT = Path(__file__).resolve().parents[2]


def test_yogsoth_stress_test_parity_fake_workflow_covers_all_scenarios() -> None:
    scenario_ids = {scenario.scenario_id for scenario in list_stress_scenarios()}
    report = run_stress_test(
        StressTestInput(
            target_id="public-demo-stress",
            task_summary="demo only public route under review",
            evidence_refs=["evidence:ledger"],
            artifact_refs=["artifact:index"],
            related_work_refs=["paper:one", "paper:two"],
            route_hard_gates=["claim experiment completion forbidden"],
            route_forbidden_actions=["claim experiment completion forbidden"],
            route_claims=["planned review route"],
            advisor_claims=["claim is linked to evidence"],
            plugin_permissions=["read_manifest"],
        )
    )

    assert scenario_ids == set(StressScenarioId)
    assert report.status == StressStatus.PASS
    assert len(report.findings) == 9
    assert report.requires_human_review is True
    assert report.multi_agent_runtime is False
    assert report.network_required is False
    assert "automated execution" not in report.convergence_recommendation.lower()

    markdown = render_stress_test_report(report)
    assert "Stress Test Report" in markdown
    assert "missing_evidence" in markdown
    assert "advisor_pack_unsupported_claim" in markdown


def test_yogsoth_stress_test_docs_and_contract_exist() -> None:
    expected_paths = [
        ROOT / "contracts" / "yogsoth_stress_test_parity.yaml",
        ROOT / "docs" / "yogsoth-stress-test-parity.md",
        ROOT / "docs" / "research-route-stress-test.md",
    ]

    for path in expected_paths:
        assert path.exists(), path

    contract = (ROOT / "contracts" / "yogsoth_stress_test_parity.yaml").read_text(
        encoding="utf-8"
    )
    assert "multi_agent_runtime: false" in contract
    assert "network_required: false" in contract
