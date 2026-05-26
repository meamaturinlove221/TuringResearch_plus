from __future__ import annotations

from pathlib import Path

from turing_research_plus.benchmark.models import BenchmarkScenario
from turing_research_plus.benchmark.replay_runner import run_benchmark_scenario
from turing_research_plus.benchmark.scenarios import public_demo_scenario

ROOT = Path(__file__).resolve().parents[2]


def test_replay_runner_passes_public_demo_outputs() -> None:
    report = run_benchmark_scenario(public_demo_scenario(ROOT))

    assert report.status == "pass"
    assert not report.missing_outputs
    assert "demo_dashboard.html" in report.actual_outputs
    assert report.demo_only is True
    assert report.no_real_experiment is True


def test_replay_runner_flags_missing_outputs(tmp_path: Path) -> None:
    (tmp_path / "present.md").write_text("ok", encoding="utf-8")
    scenario = BenchmarkScenario(
        scenario_id="missing-demo",
        name="Missing Demo",
        root_path=tmp_path.as_posix(),
        expected_outputs=["present.md", "missing.md"],
    )

    report = run_benchmark_scenario(scenario)

    assert report.status == "partial"
    assert report.actual_outputs == ["present.md"]
    assert report.missing_outputs == ["missing.md"]
    assert report.regression_flags == ["missing-output:missing.md"]
