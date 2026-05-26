"""Benchmark replay report rendering."""

from __future__ import annotations

import json

from turing_research_plus.benchmark.models import BenchmarkReport


def benchmark_report_to_json(report: BenchmarkReport) -> str:
    """Serialize a benchmark report as stable JSON."""

    return json.dumps(report.model_dump(mode="json"), indent=2, sort_keys=True)


def render_benchmark_report_markdown(report: BenchmarkReport) -> str:
    """Render one benchmark report as Markdown."""

    lines = [
        f"# Benchmark Replay Report: {report.scenario_id}",
        "",
        f"- Status: `{report.status}`",
        f"- Demo only: `{str(report.demo_only).lower()}`",
        f"- No real experiment: `{str(report.no_real_experiment).lower()}`",
        f"- Requires human review: `{str(report.requires_human_review).lower()}`",
        "",
        "## Expected Outputs",
        "",
        *[f"- `{item}`" for item in report.expected_outputs],
        "",
        "## Actual Outputs",
        "",
        *[f"- `{item}`" for item in report.actual_outputs],
        "",
        "## Missing Outputs",
        "",
        *[f"- `{item}`" for item in report.missing_outputs],
        "",
        "## Warnings",
        "",
        *[f"- {item}" for item in report.warnings],
        "",
        "## Regression Flags",
        "",
        *[f"- `{item}`" for item in report.regression_flags],
        "",
        "## Boundary",
        "",
        "- This benchmark is a local replay check.",
        "- It does not run real experiments.",
        "- It does not create observed evidence.",
        "",
    ]
    return "\n".join(lines)
