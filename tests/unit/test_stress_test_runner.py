from __future__ import annotations

from turing_research_plus.stress_test.models import StressStatus, StressTestInput
from turing_research_plus.stress_test.report import render_stress_test_report
from turing_research_plus.stress_test.runner import run_stress_test


def test_stress_test_runner_passes_clean_review_context() -> None:
    report = run_stress_test(
        StressTestInput(
            target_id="clean-route",
            task_summary="demo only route with review boundary",
            evidence_refs=["evidence:demo"],
            artifact_refs=["artifact:index"],
            related_work_refs=["paper:a", "paper:b"],
            route_hard_gates=["claim experiment completion forbidden"],
            route_forbidden_actions=["claim experiment completion forbidden"],
            route_claims=["planned route only"],
            advisor_claims=["advisor note linked to evidence"],
            plugin_permissions=["read_manifest"],
        )
    )

    assert report.status == StressStatus.PASS
    assert report.blockers == []
    assert report.network_required is False
    assert report.multi_agent_runtime is False


def test_stress_test_runner_blocks_common_release_risks() -> None:
    report = run_stress_test(
        StressTestInput(
            target_id="risky-route",
            task_summary="observed final paper proves experiment succeeded with D:/private path",
            route_hard_gates=["claim experiment completion forbidden", "no live"],
            route_forbidden_actions=["claim experiment completion forbidden"],
            route_claims=["experiment completed"],
            advisor_claims=["advisor says claim is supported"],
            plugin_permissions=["execute_code", "secrets"],
            data_sensitivity="private",
            live_mode_enabled=True,
        )
    )

    assert report.status == StressStatus.FAIL
    assert "missing_evidence" in report.blockers
    assert "fake_result_risk" in report.blockers
    assert "overclaim" in report.blockers
    assert "artifact_missing" in report.blockers
    assert "unsafe_plugin" in report.blockers
    assert "privacy_leak" in report.blockers
    assert "route_contradiction" in report.blockers
    assert "advisor_pack_unsupported_claim" in report.blockers

    markdown = render_stress_test_report(report)
    assert "Multi-agent runtime: `false`" in markdown
    assert "Network required: `false`" in markdown
