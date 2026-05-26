from __future__ import annotations

from pathlib import Path

from turing_research_plus.benchmark.scenarios import (
    built_in_scenarios,
    demo_workspace_scenario,
    paper_assembly_scenario,
    public_demo_scenario,
    vggt_fake_replay_scenario,
)

ROOT = Path(__file__).resolve().parents[2]


def test_built_in_scenarios_cover_required_replays() -> None:
    ids = {scenario.scenario_id for scenario in built_in_scenarios(ROOT)}

    assert ids == {
        "public_demo_replay",
        "vggt_fake_replay",
        "demo_workspace_replay",
        "paper_assembly_replay",
    }


def test_public_demo_scenario_is_demo_only() -> None:
    scenario = public_demo_scenario(ROOT)

    assert scenario.demo_only is True
    assert scenario.network_required is False
    assert "demo_evidence_ledger.json" in scenario.expected_outputs


def test_vggt_workspace_and_paper_scenarios_have_expected_outputs() -> None:
    vggt = vggt_fake_replay_scenario(ROOT)
    workspace = demo_workspace_scenario(ROOT)
    paper = paper_assembly_scenario(ROOT)

    assert "replay_manifest.yaml" in vggt.expected_outputs
    assert "workspace.yaml" in workspace.expected_outputs
    assert "paper_assembly_report.md" in paper.expected_outputs
