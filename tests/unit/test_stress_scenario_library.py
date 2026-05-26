from __future__ import annotations

from turing_research_plus.stress_test.scenario_library import (
    build_stress_scenario_library,
    render_stress_scenario_library,
)


def test_stress_scenario_library_contains_required_scenarios() -> None:
    library = build_stress_scenario_library()
    by_id = library.by_id()

    required = {
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
    }

    assert required <= set(by_id)
    assert library.multi_agent_runtime is False
    assert library.network_required is False
    assert library.requires_human_review is True


def test_stress_scenario_library_entries_are_review_only() -> None:
    library = build_stress_scenario_library()

    assert all(item.requires_human_review is True for item in library.scenarios)
    assert all(item.fake_runnable is True for item in library.scenarios)
    assert all(item.multi_agent_runtime is False for item in library.scenarios)
    assert all(item.network_required is False for item in library.scenarios)
    assert library.by_id()["unsafe_remote_action"].default_severity == "critical"
    assert library.by_id()["citation_weakness"].default_severity == "medium"


def test_render_stress_scenario_library_mentions_required_boundaries() -> None:
    rendered = render_stress_scenario_library()

    assert "# Stress Scenario Library" in rendered
    assert "Multi-agent runtime: `false`" in rendered
    assert "Network required: `false`" in rendered
    assert "Requires human review: `true`" in rendered
    assert "`advisor_report_overclaim`" in rendered
