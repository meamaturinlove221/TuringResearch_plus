from __future__ import annotations

import json
from pathlib import Path

from turing_research_plus.artifacts.models import EvidenceRef
from turing_research_plus.convergence import (
    CandidateKind,
    ConvergenceCandidate,
    build_convergence_decision_report,
    render_convergence_decision_report,
)
from turing_research_plus.stress_test import (
    StressStatus,
    StressTestInput,
    build_stress_scenario_library,
    render_stress_test_report,
    run_stress_test,
)

ROOT = Path(__file__).resolve().parents[2]
DEMO = ROOT / "examples" / "stress_convergence_demo" / "e2e"


def _evidence(source_id: str) -> EvidenceRef:
    return EvidenceRef(
        source_id=source_id,
        locator="fake-demo-section",
        quote="Fake/demo evidence ref for route comparison review.",
        confidence=0.7,
    )


def _stress_inputs() -> dict[str, StressTestInput]:
    return {
        "route-safe-docs-polish": StressTestInput(
            target_id="route-safe-docs-polish",
            task_summary="demo only route with documented fake/live boundary",
            evidence_refs=["fake-evidence:docs-polish"],
            artifact_refs=["artifact:parity-dashboard"],
            related_work_refs=["related:session", "related:scholar-web"],
            route_hard_gates=["no live", "do not claim experiment completion"],
            route_forbidden_actions=["claim experiment completion forbidden"],
            route_claims=["human-reviewed parity polish is ready for planning"],
            advisor_claims=["docs polish should remain review-only"],
            plugin_permissions=[],
            text_blocks=["fake/demo only; no default network; human review required"],
            data_sensitivity="demo",
            fake_demo_only=True,
            live_mode_enabled=False,
        ),
        "route-live-provider-rush": StressTestInput(
            target_id="route-live-provider-rush",
            task_summary="demo only route that tries live provider behavior",
            evidence_refs=[],
            artifact_refs=[],
            related_work_refs=["related:thin"],
            route_hard_gates=["no live", "do not claim experiment completion"],
            route_forbidden_actions=["claim experiment completion forbidden"],
            route_claims=["completed experiment with verified success"],
            advisor_claims=["camera-ready conclusion"],
            plugin_permissions=["network"],
            text_blocks=["demo only route still says observed output"],
            data_sensitivity="demo",
            fake_demo_only=True,
            live_mode_enabled=True,
        ),
        "route-heavy-refactor": StressTestInput(
            target_id="route-heavy-refactor",
            task_summary="demo only route with evidence but high resource footprint",
            evidence_refs=["fake-evidence:refactor"],
            artifact_refs=["artifact:refactor-plan"],
            related_work_refs=["related:session", "related:yogsoth"],
            route_hard_gates=["no live"],
            route_forbidden_actions=[],
            route_claims=["route remains proposed-only"],
            advisor_claims=[],
            plugin_permissions=[],
            text_blocks=["fake/demo only; no default network; human review required"],
            data_sensitivity="demo",
            fake_demo_only=True,
            live_mode_enabled=False,
        ),
    }


def _candidate(
    candidate_id: str,
    *,
    feasibility: float,
    novelty: float,
    resources: list[str],
) -> ConvergenceCandidate:
    return ConvergenceCandidate(
        candidate_id=candidate_id,
        kind=CandidateKind.RELEASE_FEATURE,
        title=candidate_id.replace("-", " ").title(),
        mechanism="stress-gated route comparison",
        expected_gain="Improve release implementation quality without executing routes.",
        feasibility=feasibility,
        novelty=novelty,
        risk="medium",
        required_resources=resources,
        evidence_refs=[_evidence(candidate_id)],
        metadata={"fake_demo_only": True},
    )


def _stress_reports() -> dict[str, object]:
    return {
        route_id: run_stress_test(request)
        for route_id, request in _stress_inputs().items()
    }


def _passed_candidates() -> list[ConvergenceCandidate]:
    reports = _stress_reports()
    candidate_specs = {
        "route-safe-docs-polish": {
            "feasibility": 0.9,
            "novelty": 0.72,
            "resources": ["docs review", "dashboard check"],
        },
        "route-live-provider-rush": {
            "feasibility": 0.82,
            "novelty": 0.9,
            "resources": ["live key", "provider review", "network gate"],
        },
        "route-heavy-refactor": {
            "feasibility": 0.5,
            "novelty": 0.86,
            "resources": [
                "runtime refactor",
                "docs migration",
                "dashboard migration",
                "new contract review",
                "release coordination",
            ],
        },
    }
    return [
        _candidate(route_id, **candidate_specs[route_id])
        for route_id, report in reports.items()
        if report.status == StressStatus.PASS
    ]


def test_stress_convergence_e2e_demo_files_exist() -> None:
    expected = [
        DEMO / "README.md",
        DEMO / "route_candidates.json",
        DEMO / "stress_report.md",
        DEMO / "convergence_decision.md",
        DEMO / "e2e_summary.md",
        ROOT / "docs" / "stress-convergence-e2e.md",
    ]

    for path in expected:
        assert path.exists(), path


def test_stress_convergence_e2e_runs_stress_before_convergence() -> None:
    reports = _stress_reports()

    assert reports["route-safe-docs-polish"].status == StressStatus.PASS
    assert reports["route-safe-docs-polish"].blockers == []
    assert reports["route-live-provider-rush"].status == StressStatus.FAIL
    assert "missing_evidence" in reports["route-live-provider-rush"].blockers
    assert "fake_result_risk" in reports["route-live-provider-rush"].blockers
    assert "unsafe_plugin" in reports["route-live-provider-rush"].blockers
    assert reports["route-heavy-refactor"].status == StressStatus.PASS


def test_stress_convergence_e2e_decision_uses_stress_passed_candidates() -> None:
    report = build_convergence_decision_report(
        _passed_candidates(),
        report_id="stress-convergence-e2e",
    )
    rendered = render_convergence_decision_report(report)

    ranked_ids = {score.candidate_id for score in report.ranked_candidates}
    rejected_ids = {score.candidate_id for score in report.rejected_candidates}

    assert report.final_recommendation == "route-safe-docs-polish"
    assert "route-live-provider-rush" not in ranked_ids
    assert "route-safe-docs-polish" in ranked_ids
    assert "route-heavy-refactor" in rejected_ids
    assert "resource footprint too large for current phase" in rendered
    assert "Does not execute route: `true`" in rendered
    assert report.to_research_artifact().artifact_id == (
        "decision-stress-convergence-e2e"
    )


def test_stress_convergence_e2e_static_outputs_match_runtime() -> None:
    reports = _stress_reports()
    stress_markdown = "\n".join(
        render_stress_test_report(report) for report in reports.values()
    )
    decision = build_convergence_decision_report(
        _passed_candidates(),
        report_id="stress-convergence-e2e",
    )
    decision_markdown = render_convergence_decision_report(decision)
    static_stress = (DEMO / "stress_report.md").read_text(encoding="utf-8")
    static_decision = (DEMO / "convergence_decision.md").read_text(encoding="utf-8")
    static_candidates = json.loads(
        (DEMO / "route_candidates.json").read_text(encoding="utf-8")
    )

    for term in [
        "route-safe-docs-polish",
        "route-live-provider-rush",
        "missing_evidence",
        "fake_result_risk",
        "unsafe_plugin",
    ]:
        assert term in stress_markdown
        assert term in static_stress

    for term in [
        "Final recommendation: `route-safe-docs-polish`",
        "route-heavy-refactor",
        "Does not execute route: `true`",
        "Run stress-test review before implementation.",
    ]:
        assert term in decision_markdown
        assert term in static_decision

    assert static_candidates["fake_demo_only"] is True
    assert static_candidates["does_not_execute_routes"] is True
    assert len(static_candidates["candidates"]) == 3


def test_stress_convergence_e2e_docs_preserve_safety_boundaries() -> None:
    combined = "\n".join(
        path.read_text(encoding="utf-8")
        for path in [
            DEMO / "README.md",
            DEMO / "e2e_summary.md",
            ROOT / "docs" / "stress-convergence-e2e.md",
        ]
    )
    library = build_stress_scenario_library()

    required = [
        "fake/demo only",
        "no multi-agent runtime",
        "no route execution",
        "no default network",
        "no Evidence Ledger mutation",
        "human review required",
    ]
    for item in required:
        assert item in combined

    assert library.multi_agent_runtime is False
    assert library.network_required is False
    assert ("Tuling" + "Research") not in combined
    assert ("D:" + "/vggt") not in combined
    assert ("local_project_links" + ".yaml") not in combined
    assert ('"status": "' + 'observed"') not in combined
