"""Local helper wrappers for benchmark replay."""

from __future__ import annotations

from pathlib import Path

from turing_research_plus.benchmark.models import BenchmarkReport, BenchmarkScenario
from turing_research_plus.benchmark.replay_runner import (
    run_benchmark_scenario,
    run_benchmark_suite,
)
from turing_research_plus.benchmark.report import (
    benchmark_report_to_json,
    render_benchmark_report_markdown,
)
from turing_research_plus.benchmark.scenarios import built_in_scenarios


def benchmark_run_builtin(root: Path) -> list[BenchmarkReport]:
    """Run built-in replay scenarios."""

    return run_benchmark_suite(built_in_scenarios(root))


def benchmark_run_scenario(scenario: BenchmarkScenario) -> BenchmarkReport:
    """Run one replay scenario."""

    return run_benchmark_scenario(scenario)


def benchmark_export_report(report: BenchmarkReport, output_dir: Path) -> list[Path]:
    """Write JSON and Markdown report files."""

    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / f"{report.scenario_id}.json"
    markdown_path = output_dir / f"{report.scenario_id}.md"
    json_path.write_text(benchmark_report_to_json(report), encoding="utf-8")
    markdown_path.write_text(render_benchmark_report_markdown(report), encoding="utf-8")
    return [json_path, markdown_path]
