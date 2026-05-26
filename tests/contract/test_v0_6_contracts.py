from __future__ import annotations

from pathlib import Path

from turing_research_plus.benchmark.scenarios import built_in_scenarios
from turing_research_plus.quality.regression_gate import run_regression_gate

ROOT = Path(__file__).resolve().parents[2]

V0_6_CONTRACTS = [
    "multi_project_workspace.yaml",
    "research_project_template.yaml",
    "cross_project_evidence_graph.yaml",
    "privacy_data_policy.yaml",
    "plugin_architecture.yaml",
    "mcp_plugin_registry.yaml",
    "tool_capability_manifest.yaml",
    "skill_marketplace.yaml",
    "extension_safety.yaml",
    "paper_writing_scaffold.yaml",
    "method_section_builder.yaml",
    "related_work_draft.yaml",
    "experiment_section_builder.yaml",
    "benchmark_replay.yaml",
    "quality_regression_gate.yaml",
]


def test_v0_6_contract_files_exist() -> None:
    missing = [
        name for name in V0_6_CONTRACTS if not (ROOT / "contracts" / name).exists()
    ]

    assert missing == []


def test_v0_6_contracts_preserve_no_network_and_review_boundaries() -> None:
    offenders: list[str] = []
    for name in V0_6_CONTRACTS:
        text = (ROOT / "contracts" / name).read_text(encoding="utf-8")
        lowered = text.lower()
        if "TuringResearch Plus" not in text:
            offenders.append(f"{name}: missing project name")
        if "network_behavior: no_network" not in text:
            offenders.append(f"{name}: missing no-network boundary")
        if "requires_human_review" not in text and "requires human review" not in lowered:
            offenders.append(f"{name}: missing human review boundary")

    assert offenders == []


def test_v0_6_docs_and_examples_exist() -> None:
    required = [
        "docs/v0.6.0-sprint-1-integration-report.md",
        "docs/v0.6.0-sprint-2-plugin-integration-report.md",
        "docs/paper-assembly-gate.md",
        "docs/benchmark-replay-suite.md",
        "docs/quality-metrics.md",
        "docs/regression-gate.md",
        "examples/public_demo/README.md",
        "examples/workspaces/demo_workspace/workspace.yaml",
        "examples/vggt-human-prior-survey/dogfooding_replay/replay_report.md",
        "examples/vggt-human-prior-survey/paper_scaffold/paper_assembly_report.md",
    ]

    assert [path for path in required if not (ROOT / path).exists()] == []


def test_v0_6_builtin_replay_scenarios_cover_required_surface() -> None:
    scenario_ids = {scenario.scenario_id for scenario in built_in_scenarios(ROOT)}

    assert scenario_ids == {
        "public_demo_replay",
        "vggt_fake_replay",
        "demo_workspace_replay",
        "paper_assembly_replay",
    }


def test_v0_6_regression_gate_passes_without_live_requirements() -> None:
    report = run_regression_gate(ROOT)

    assert report.status == "pass"
    assert report.blockers == []
    assert any(check.check_id == "live-tests-default-skip" for check in report.checks)
