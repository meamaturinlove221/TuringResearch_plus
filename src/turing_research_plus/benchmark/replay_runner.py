"""Local replay runner for benchmark scenarios."""

from __future__ import annotations

import time
from pathlib import Path

from turing_research_plus.benchmark.models import (
    BenchmarkReport,
    BenchmarkScenario,
    BenchmarkStatus,
)


def run_benchmark_scenario(scenario: BenchmarkScenario) -> BenchmarkReport:
    """Check expected local outputs for one replay scenario."""

    started = time.perf_counter()
    root = Path(scenario.root_path)
    actual: list[str] = []
    missing: list[str] = []
    for output in scenario.expected_outputs:
        path = root / output
        if path.exists():
            actual.append(output)
        else:
            missing.append(output)
    warnings = [
        "benchmark replay is demo-only",
        "benchmark replay does not run real experiments",
    ]
    regression_flags = [f"missing-output:{item}" for item in missing]
    status = BenchmarkStatus.PASS
    if missing and actual:
        status = BenchmarkStatus.PARTIAL
    elif missing and not actual:
        status = BenchmarkStatus.FAIL
    return BenchmarkReport(
        scenario_id=scenario.scenario_id,
        steps=scenario.steps,
        expected_outputs=scenario.expected_outputs,
        actual_outputs=actual,
        missing_outputs=missing,
        status=status,
        duration=round(time.perf_counter() - started, 6),
        warnings=warnings,
        regression_flags=regression_flags,
        demo_only=True,
        no_real_experiment=True,
        requires_human_review=True,
    )


def run_benchmark_suite(scenarios: list[BenchmarkScenario]) -> list[BenchmarkReport]:
    """Run a list of local replay scenarios."""

    return [run_benchmark_scenario(scenario) for scenario in scenarios]
