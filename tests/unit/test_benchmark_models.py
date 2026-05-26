from __future__ import annotations

import pytest

from turing_research_plus.benchmark.models import (
    BenchmarkReport,
    BenchmarkScenario,
    BenchmarkStatus,
    BenchmarkStep,
)


def test_benchmark_report_serializes_required_fields() -> None:
    report = BenchmarkReport(
        scenario_id="demo",
        steps=[BenchmarkStep(step_id="step", description="check")],
        expected_outputs=["README.md"],
        actual_outputs=["README.md"],
        missing_outputs=[],
        status=BenchmarkStatus.PASS,
        warnings=["demo-only"],
    )

    payload = report.model_dump(mode="json")

    assert payload["scenario_id"] == "demo"
    assert payload["status"] == "pass"
    assert payload["demo_only"] is True
    assert payload["no_real_experiment"] is True
    assert payload["requires_human_review"] is True


def test_benchmark_scenario_rejects_network_required() -> None:
    with pytest.raises(ValueError, match="must not require network"):
        BenchmarkScenario(
            scenario_id="live",
            name="Live",
            root_path=".",
            network_required=True,
        )


def test_benchmark_report_rejects_real_experiment_claim() -> None:
    with pytest.raises(ValueError, match="must not represent real experiments"):
        BenchmarkReport(
            scenario_id="bad",
            status=BenchmarkStatus.PASS,
            no_real_experiment=False,
        )
