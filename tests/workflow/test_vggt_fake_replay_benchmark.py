from __future__ import annotations

from pathlib import Path

from turing_research_plus.benchmark.replay_runner import run_benchmark_suite
from turing_research_plus.benchmark.scenarios import (
    paper_assembly_scenario,
    vggt_fake_replay_scenario,
)

ROOT = Path(__file__).resolve().parents[2]


def test_vggt_fake_replay_and_paper_assembly_pass_as_replay_only() -> None:
    reports = run_benchmark_suite(
        [vggt_fake_replay_scenario(ROOT), paper_assembly_scenario(ROOT)]
    )

    assert [report.scenario_id for report in reports] == [
        "vggt_fake_replay",
        "paper_assembly_replay",
    ]
    assert all(report.status == "pass" for report in reports)
    assert all(report.no_real_experiment for report in reports)
    assert all(report.demo_only for report in reports)
    assert all("benchmark replay is demo-only" in report.warnings for report in reports)
