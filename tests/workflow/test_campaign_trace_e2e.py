from __future__ import annotations

import json
from pathlib import Path

from turing_research_plus.campaigns import (
    build_campaign_execution_trace,
    get_campaign,
    render_campaign_execution_trace,
    route_campaign,
)

ROOT = Path(__file__).resolve().parents[2]
DEMO = ROOT / "examples" / "campaigns" / "e2e_trace_demo"
TASK_DESCRIPTION = "stress test unsafe claim review before public release"
PROVIDED_INPUTS = ["candidate claim or release surface"]


def test_campaign_trace_e2e_routes_task_intent_to_campaign() -> None:
    route = route_campaign(TASK_DESCRIPTION)
    summary = json.loads((DEMO / "route_summary.json").read_text(encoding="utf-8"))

    assert route.recommended_campaign == "stress_test"
    assert route.recommended_skill == "turingresearch-fusion-stress-test"
    assert route.confidence == summary["confidence"]
    assert summary["task_description"] == TASK_DESCRIPTION
    assert summary["campaign_id"] == route.recommended_campaign
    assert summary["recommended_skill"] == route.recommended_skill


def test_campaign_trace_e2e_records_required_inputs_and_skill_map() -> None:
    campaign = get_campaign("stress_test")
    required_inputs = (DEMO / "required_inputs.md").read_text(encoding="utf-8")
    skill_map = (DEMO / "skill_map.md").read_text(encoding="utf-8")

    for precondition in campaign.preconditions:
        assert precondition in required_inputs
    for required in campaign.required_inputs:
        assert required in required_inputs
    for expected in campaign.expected_outputs:
        assert expected in (DEMO / "expected_outputs.md").read_text(encoding="utf-8")

    assert campaign.recommended_skills[0] in skill_map
    assert "turingresearch-master-orchestrator" in skill_map
    assert "does not execute the skill" in skill_map


def test_campaign_trace_e2e_generates_expected_trace_report() -> None:
    trace = build_campaign_execution_trace(
        TASK_DESCRIPTION,
        provided_inputs=PROVIDED_INPUTS,
    )
    rendered = render_campaign_execution_trace(trace)
    fixture = (DEMO / "trace_report.md").read_text(encoding="utf-8")
    summary = json.loads((DEMO / "route_summary.json").read_text(encoding="utf-8"))

    assert trace.trace_id == "campaign-trace-stress-test"
    assert trace.campaign_id == "stress_test"
    assert trace.recommended_skill == "turingresearch-fusion-stress-test"
    assert trace.missing_preconditions == []
    assert trace.fake_trace is True
    assert trace.ready_for_execution is False
    assert trace.does_not_execute is True
    assert trace.does_not_call_llm is True
    assert trace.does_not_use_network is True
    assert trace.does_not_mutate_evidence_ledger is True
    assert trace.requires_human_review is True
    assert all(step.executed is False for step in trace.steps)
    assert all(step.called_tool is False for step in trace.steps)
    assert all(step.called_llm is False for step in trace.steps)
    assert all(step.used_network is False for step in trace.steps)
    assert all(step.wrote_evidence_ledger is False for step in trace.steps)

    assert summary["missing_preconditions"] == trace.missing_preconditions
    assert summary["ready_for_planning"] is True
    assert "# Campaign Execution Trace: stress_test" in fixture
    assert "Trace id: `campaign-trace-stress-test`" in fixture
    assert "proposed outputs are not observed evidence" in rendered
    assert "master orchestrator remains in control" in rendered


def test_campaign_trace_e2e_demo_docs_are_public_safe() -> None:
    combined = "\n".join(path.read_text(encoding="utf-8") for path in DEMO.rglob("*"))

    assert "fake trace only" in combined
    assert "no agent runtime" in combined
    assert "no network" in combined
    assert "does not mutate evidence ledger" in combined.lower()
    assert "human review required" in combined
    assert "Tuling" + "Research" not in combined
    assert ("D:" + "/vggt") not in combined
    assert ("local_project_links" + ".yaml") not in combined
    assert ('"status": "' + 'observed"') not in combined
