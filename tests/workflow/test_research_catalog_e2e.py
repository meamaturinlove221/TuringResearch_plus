from __future__ import annotations

import json
from pathlib import Path

from turing_research_plus.campaigns import (
    build_campaign_execution_trace,
    get_campaign,
    route_campaign,
)
from turing_research_plus.experiment_execution import (
    build_experiment_execution_plan,
    render_experiment_execution_runbook,
)
from turing_research_plus.experiment_route.models import ExperimentRouteSpec
from turing_research_plus.stress_test import StressTestInput, run_stress_test
from turing_research_plus.stress_test.models import StressStatus

ROOT = Path(__file__).resolve().parents[2]
DEMO = ROOT / "examples" / "research_catalog" / "e2e_demo"
DASHBOARD = ROOT / "examples" / "research_catalog" / "dashboard.json"


def _load_workspace() -> dict[str, object]:
    return json.loads((DEMO / "workspace_manifest.json").read_text(encoding="utf-8"))


def _string_list(data: dict[str, object], key: str) -> list[str]:
    values = data[key]
    assert isinstance(values, list)
    return [str(item) for item in values]


def test_research_catalog_e2e_routes_workspace_intent() -> None:
    workspace = _load_workspace()
    route = route_campaign(str(workspace["task_intent"]))
    trace = build_campaign_execution_trace(
        str(workspace["task_intent"]),
        provided_inputs=_string_list(workspace, "provided_inputs"),
    )

    assert route.recommended_campaign == "stress_test"
    assert route.recommended_skill == "turingresearch-fusion-stress-test"
    assert trace.campaign_id == route.recommended_campaign
    assert trace.recommended_skill == route.recommended_skill
    assert trace.missing_preconditions == []
    assert trace.fake_trace is True
    assert trace.does_not_execute is True


def test_research_catalog_e2e_dashboard_groups_and_skill_map() -> None:
    dashboard = json.loads(DASHBOARD.read_text(encoding="utf-8"))
    report = json.loads((DEMO / "catalog_report.json").read_text(encoding="utf-8"))
    campaign = get_campaign("stress_test")

    dashboard_groups = {group["id"] for group in dashboard["groups"]}
    assert set(report["dashboard_groups"]) == dashboard_groups
    assert "stress_test" in dashboard["groups"][0]["items"]
    assert campaign.recommended_skills[0] == report["recommended_skill"]
    assert "turingresearch-fusion-stress-test" in (
        DEMO / "catalog_report.md"
    ).read_text(encoding="utf-8")


def test_research_catalog_e2e_runs_stress_review_from_workspace() -> None:
    workspace = _load_workspace()
    report = run_stress_test(
        StressTestInput(
            target_id=str(workspace["workspace_id"]),
            task_summary=str(workspace["task_intent"]),
            evidence_refs=_string_list(workspace, "evidence_refs"),
            artifact_refs=_string_list(workspace, "artifact_refs"),
            related_work_refs=_string_list(workspace, "related_work_refs"),
            route_hard_gates=["claim experiment completion forbidden", "no live"],
            route_forbidden_actions=["claim experiment completion forbidden"],
            route_claims=_string_list(workspace, "route_claims"),
            advisor_claims=_string_list(workspace, "advisor_claims"),
            plugin_permissions=_string_list(workspace, "plugin_permissions"),
            text_blocks=_string_list(workspace, "text_blocks"),
            data_sensitivity=str(workspace["data_sensitivity"]),
            fake_demo_only=bool(workspace["fake_demo_only"]),
            live_mode_enabled=bool(workspace["live_mode_enabled"]),
        )
    )

    assert report.status == StressStatus.PASS
    assert report.blockers == []
    assert report.multi_agent_runtime is False
    assert report.network_required is False
    assert report.requires_human_review is True


def test_research_catalog_e2e_builds_experiment_runbook_summary() -> None:
    route_spec = ExperimentRouteSpec.model_validate_json(
        (DEMO / "route_spec.json").read_text(encoding="utf-8")
    )
    plan = build_experiment_execution_plan(route_spec)
    runbook = render_experiment_execution_runbook(plan)
    report = json.loads((DEMO / "catalog_report.json").read_text(encoding="utf-8"))

    assert plan.status.value == report["experiment_plan_status"]
    assert plan.automatically_executes is False
    assert plan.remote_execution is False
    assert plan.writes_observed_result is False
    assert plan.ingest_contract.proposed_evidence_only is True
    assert "catalog report" in {item.description for item in plan.artifact_requirements}
    assert "Writes observed result: `false`" in runbook


def test_research_catalog_e2e_static_report_matches_generated_surfaces() -> None:
    workspace = _load_workspace()
    route = route_campaign(str(workspace["task_intent"]))
    report_json = json.loads((DEMO / "catalog_report.json").read_text(encoding="utf-8"))
    report_md = (DEMO / "catalog_report.md").read_text(encoding="utf-8")
    vault_context = (DEMO / "vault_context.md").read_text(encoding="utf-8")

    assert report_json["workspace_id"] == workspace["workspace_id"]
    assert report_json["campaign_id"] == route.recommended_campaign
    assert report_json["recommended_skill"] == route.recommended_skill
    assert report_json["status"] == "pass-with-review"
    assert "Catalog Flow" in report_md
    assert "vault context" in report_md
    assert "[[Research Catalog]]" in vault_context
    assert "[[Stress Test]]" in vault_context
    assert "[[Experiment Runbook]]" in vault_context


def test_research_catalog_e2e_docs_preserve_safety_boundaries() -> None:
    combined = "\n".join(path.read_text(encoding="utf-8") for path in DEMO.rglob("*"))
    docs = (ROOT / "docs" / "research-catalog-e2e.md").read_text(encoding="utf-8")
    combined = f"{combined}\n{docs}"

    required = [
        "no agent runtime",
        "no automatic tool execution",
        "no default network",
        "no experiment execution",
        "no Evidence Ledger mutation",
        "no fake/demo result promotion",
        "human review required",
    ]
    for item in required:
        assert item in combined

    assert "Tuling" + "Research" not in combined
    assert ("D:" + "/vggt") not in combined
    assert ("local_project_links" + ".yaml") not in combined
    assert ('"status": "' + 'observed"') not in combined
