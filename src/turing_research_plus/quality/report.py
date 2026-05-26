"""Quality and regression report rendering."""

from __future__ import annotations

from turing_research_plus.quality.models import QualityReport, RegressionGateReport


def render_quality_report_markdown(report: QualityReport) -> str:
    """Render a quality report as Markdown."""

    lines = [
        f"# Quality Report: {report.report_id}",
        "",
        f"- Status: `{report.status}`",
        f"- Release ready: `{str(report.release_ready).lower()}`",
        f"- Requires human review: `{str(report.requires_human_review).lower()}`",
        "",
        "## Metrics",
        "",
        "| Metric | Score | Status | Details |",
        "| --- | ---: | --- | --- |",
    ]
    for metric in report.metrics:
        details = "<br>".join(metric.details)
        lines.append(
            f"| `{metric.metric_id}` | {metric.score:.2f} | `{metric.status}` | {details} |"
        )
    lines.extend(["", "## Warnings", "", *[f"- {item}" for item in report.warnings], ""])
    return "\n".join(lines)


def render_regression_gate_markdown(report: RegressionGateReport) -> str:
    """Render a regression gate report as Markdown."""

    lines = [
        f"# Regression Gate Report: {report.gate_id}",
        "",
        f"- Status: `{report.status}`",
        f"- Requires human review: `{str(report.requires_human_review).lower()}`",
        "",
        "## Checks",
        "",
        "| Check | Passed | Blockers | Warnings |",
        "| --- | --- | --- | --- |",
    ]
    for check in report.checks:
        blockers = "<br>".join(check.blockers)
        warnings = "<br>".join(check.warnings)
        lines.append(
            f"| `{check.check_id}` | `{str(check.passed).lower()}` | {blockers} | {warnings} |"
        )
    lines.extend(
        [
            "",
            "## Blockers",
            "",
            *[f"- `{item}`" for item in report.blockers],
            "",
            "## Boundary",
            "",
            "- This is a local quality gate.",
            "- It does not publish or tag a release.",
            "- Human review is still required.",
            "",
        ]
    )
    return "\n".join(lines)
