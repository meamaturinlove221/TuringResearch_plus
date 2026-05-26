from __future__ import annotations

from pathlib import Path

from turing_research_plus.benchmark.replay_runner import run_benchmark_scenario
from turing_research_plus.benchmark.scenarios import public_demo_scenario

ROOT = Path(__file__).resolve().parents[2]


def test_public_demo_replay_passes_without_network_or_real_experiment() -> None:
    report = run_benchmark_scenario(public_demo_scenario(ROOT))

    assert report.scenario_id == "public_demo_replay"
    assert report.status == "pass"
    assert report.missing_outputs == []
    assert "benchmark replay does not run real experiments" in report.warnings
    assert report.demo_only is True
    assert report.no_real_experiment is True
