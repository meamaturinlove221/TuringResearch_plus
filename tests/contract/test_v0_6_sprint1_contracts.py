from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

V0_6_SPRINT1_CONTRACTS = [
    "multi_project_workspace.yaml",
    "research_project_template.yaml",
    "cross_project_evidence_graph.yaml",
    "privacy_data_policy.yaml",
]


def test_v0_6_sprint1_contracts_exist() -> None:
    missing = [
        name for name in V0_6_SPRINT1_CONTRACTS if not (ROOT / "contracts" / name).exists()
    ]

    assert missing == []


def test_v0_6_sprint1_contracts_are_no_network_and_review_first() -> None:
    offenders: list[str] = []
    for name in V0_6_SPRINT1_CONTRACTS:
        text = (ROOT / "contracts" / name).read_text(encoding="utf-8")
        lowered = text.lower()
        if "TuringResearch Plus" not in text:
            offenders.append(f"{name} missing project name")
        if "network_behavior: no_network" not in text:
            offenders.append(f"{name} missing no-network boundary")
        if "requires_human_review" not in text and "requires human review" not in lowered:
            offenders.append(f"{name} missing human review boundary")

    assert offenders == []


def test_v0_6_sprint1_docs_and_examples_exist() -> None:
    required = [
        "docs/multi-project-workspace.md",
        "docs/general-research-project-template.md",
        "docs/cross-project-evidence-graph.md",
        "docs/privacy-data-policy-layer.md",
        "examples/workspaces/demo_workspace/workspace.yaml",
        "examples/workspaces/demo_workspace/cross_project_graph.json",
        "examples/workspaces/demo_workspace/cross_project_summary.md",
    ]

    assert [path for path in required if not (ROOT / path).exists()] == []


def test_v0_6_sprint1_reports_state_boundaries() -> None:
    report = (ROOT / "docs" / "v0.6.0-sprint-1-integration-report.md").read_text(
        encoding="utf-8"
    )

    assert "GO WITH REVIEW" in report
    assert "No private project data was read" in report
    assert "No evidence transfer between projects" in report
    assert "Privacy gate is report-only" in report
