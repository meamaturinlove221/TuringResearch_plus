from __future__ import annotations

from pathlib import Path

from turing_research_plus.benchmark.replay_runner import run_benchmark_scenario
from turing_research_plus.benchmark.report import (
    benchmark_report_to_json,
    render_benchmark_report_markdown,
)
from turing_research_plus.benchmark.scenarios import vggt_fake_replay_scenario

ROOT = Path(__file__).resolve().parents[2]


def test_benchmark_report_json_contains_status() -> None:
    report = run_benchmark_scenario(vggt_fake_replay_scenario(ROOT))
    text = benchmark_report_to_json(report)

    assert '"scenario_id": "vggt_fake_replay"' in text
    assert '"status": "pass"' in text
    assert '"no_real_experiment": true' in text


def test_benchmark_report_markdown_keeps_replay_boundary() -> None:
    report = run_benchmark_scenario(vggt_fake_replay_scenario(ROOT))
    markdown = render_benchmark_report_markdown(report)

    assert "# Benchmark Replay Report: vggt_fake_replay" in markdown
    assert "It does not run real experiments." in markdown
    assert "It does not create observed evidence." in markdown
