"""Markdown rendering for stress-test parity reports."""

from __future__ import annotations

from turing_research_plus.stress_test.models import StressTestReport


def render_stress_test_report(report: StressTestReport) -> str:
    """Render a stress-test report as Markdown."""

    blocker_lines = [f"- `{item}`" for item in report.blockers] or ["- none"]
    warning_lines = [f"- `{item}`" for item in report.warnings] or ["- none"]
    lines = [
        f"# Stress Test Report: {report.target_id}",
        "",
        f"- Status: `{report.status.value}`",
        f"- Requires human review: `{str(report.requires_human_review).lower()}`",
        "- Multi-agent runtime: `false`",
        "- Network required: `false`",
        f"- Convergence recommendation: {report.convergence_recommendation}",
        "",
        "## Blockers",
        "",
        *blocker_lines,
        "",
        "## Warnings",
        "",
        *warning_lines,
        "",
        "## Findings",
        "",
    ]
    for finding in report.findings:
        evidence = ", ".join(f"`{item}`" for item in finding.evidence) or "none"
        lines.extend(
            [
                f"### {finding.scenario_id.value}",
                "",
                f"- Status: `{finding.status.value}`",
                f"- Severity: `{finding.severity.value}`",
                f"- Message: {finding.message}",
                f"- Evidence: {evidence}",
                f"- Recommended action: {finding.recommended_action}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"
