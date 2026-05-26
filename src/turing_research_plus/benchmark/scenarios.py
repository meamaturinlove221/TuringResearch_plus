"""Built-in local benchmark replay scenarios."""

from __future__ import annotations

from pathlib import Path

from turing_research_plus.benchmark.models import BenchmarkScenario, BenchmarkStep


def public_demo_scenario(root: Path) -> BenchmarkScenario:
    """Build the public demo replay scenario."""

    demo_root = root / "examples" / "public_demo"
    expected = [
        "README.md",
        "demo_research_intent.md",
        "demo_evidence_ledger.json",
        "demo_artifact_index.md",
        "demo_visual_inventory.md",
        "demo_related_work.md",
        "demo_advisor_pack.md",
        "demo_dashboard.html",
    ]
    return BenchmarkScenario(
        scenario_id="public_demo_replay",
        name="Public Demo Replay",
        root_path=demo_root.as_posix(),
        steps=[
            BenchmarkStep(
                step_id="public-demo-files",
                description="Check public demo fixture files.",
                expected_outputs=expected,
            )
        ],
        expected_outputs=expected,
    )


def vggt_fake_replay_scenario(root: Path) -> BenchmarkScenario:
    """Build the VGGT fake replay scenario."""

    replay_root = root / "examples" / "vggt-human-prior-survey" / "dogfooding_replay"
    expected = [
        "replay_report.md",
        "replay_manifest.yaml",
        "replay_missing_items.md",
        "replay_next_actions.md",
    ]
    return BenchmarkScenario(
        scenario_id="vggt_fake_replay",
        name="VGGT Fake Replay",
        root_path=replay_root.as_posix(),
        steps=[
            BenchmarkStep(
                step_id="vggt-replay-files",
                description="Check VGGT fake replay artifacts.",
                expected_outputs=expected,
            )
        ],
        expected_outputs=expected,
    )


def demo_workspace_scenario(root: Path) -> BenchmarkScenario:
    """Build the demo workspace replay scenario."""

    workspace_root = root / "examples" / "workspaces" / "demo_workspace"
    expected = [
        "workspace.yaml",
        "cross_project_graph.json",
        "cross_project_summary.md",
    ]
    return BenchmarkScenario(
        scenario_id="demo_workspace_replay",
        name="Demo Workspace Replay",
        root_path=workspace_root.as_posix(),
        steps=[
            BenchmarkStep(
                step_id="workspace-files",
                description="Check demo workspace outputs.",
                expected_outputs=expected,
            )
        ],
        expected_outputs=expected,
    )


def paper_assembly_scenario(root: Path) -> BenchmarkScenario:
    """Build the paper assembly replay scenario."""

    paper_root = root / "examples" / "vggt-human-prior-survey" / "paper_scaffold"
    expected = [
        "paper_assembly_report.md",
        "ready_sections.md",
        "blocked_sections.md",
        "paper_outline.md",
        "method_section_skeleton.md",
        "related_work_skeleton.md",
        "experiment_section_skeleton.md",
    ]
    return BenchmarkScenario(
        scenario_id="paper_assembly_replay",
        name="Paper Assembly Replay",
        root_path=paper_root.as_posix(),
        steps=[
            BenchmarkStep(
                step_id="paper-assembly-files",
                description="Check paper assembly gate outputs.",
                expected_outputs=expected,
            )
        ],
        expected_outputs=expected,
    )


def built_in_scenarios(root: Path) -> list[BenchmarkScenario]:
    """Return built-in replay scenarios."""

    return [
        public_demo_scenario(root),
        vggt_fake_replay_scenario(root),
        demo_workspace_scenario(root),
        paper_assembly_scenario(root),
    ]
