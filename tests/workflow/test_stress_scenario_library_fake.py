from __future__ import annotations

from pathlib import Path

from turing_research_plus.stress_test import (
    build_stress_scenario_library,
    render_stress_scenario_library,
)
from turing_research_plus.stress_test.models import StressStatus, StressTestInput
from turing_research_plus.stress_test.runner import run_stress_test

ROOT = Path(__file__).resolve().parents[2]


def test_stress_scenario_library_fake_workflow_is_review_only() -> None:
    library = build_stress_scenario_library()
    rendered = render_stress_scenario_library(library)
    report = run_stress_test(
        StressTestInput(
            target_id="stress-library-demo",
            task_summary="demo only route with unsupported advisor claim",
            advisor_claims=["camera-ready conclusion"],
            plugin_permissions=["network"],
            route_hard_gates=["no live", "do not claim experiment completion"],
            route_claims=["completed experiment"],
            fake_demo_only=True,
        )
    )

    assert library.by_id()["missing_evidence"].category == "evidence"
    assert library.by_id()["plugin_permission_risk"].category == "plugin_safety"
    assert "Multi-agent runtime: `false`" in rendered
    assert report.status == StressStatus.FAIL
    assert "missing_evidence" in report.blockers
    assert "unsafe_plugin" in report.blockers
    assert report.multi_agent_runtime is False
    assert report.network_required is False


def test_stress_scenario_library_docs_and_example_cover_required_scenarios() -> None:
    docs = (ROOT / "docs" / "stress-scenario-library.md").read_text(encoding="utf-8")
    example = (ROOT / "examples" / "stress_scenarios" / "README.md").read_text(
        encoding="utf-8"
    )
    combined = docs + "\n" + example

    required = [
        "missing_evidence",
        "unsupported_claim",
        "fake_result_risk",
        "artifact_omission",
        "citation_weakness",
        "privacy_leak",
        "unsafe_remote_action",
        "plugin_permission_risk",
        "route_contradiction",
        "advisor_report_overclaim",
    ]
    for scenario in required:
        assert scenario in combined

    assert "no multi-agent runtime" in combined
    assert "no network" in combined
    assert "human review required" in combined


def test_stress_scenario_library_docs_are_public_safe() -> None:
    combined = "\n".join(
        [
            (ROOT / "docs" / "stress-scenario-library.md").read_text(encoding="utf-8"),
            (ROOT / "examples" / "stress_scenarios" / "README.md").read_text(
                encoding="utf-8"
            ),
        ]
    )

    forbidden = ["D:/vggt", "D:\\vggt", "local_project_links.yaml", "ghp_", "sk-"]
    for marker in forbidden:
        assert marker not in combined
