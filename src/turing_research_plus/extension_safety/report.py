"""Markdown report rendering for extension safety."""

from __future__ import annotations

from turing_research_plus.extension_safety.models import ExtensionSafetyReport


def render_extension_safety_report_markdown(report: ExtensionSafetyReport) -> str:
    """Render an extension safety report as Markdown."""

    lines = [
        f"# Extension Safety Report: {report.extension_id}",
        "",
        f"- Kind: `{report.kind}`",
        f"- Valid: `{str(report.valid).lower()}`",
        f"- Status: `{report.status}`",
        f"- Release blocker: `{str(report.release_blocker).lower()}`",
        f"- Requires human review: `{str(report.requires_human_review).lower()}`",
        f"- Executes extension code: `{str(report.executes_extension_code).lower()}`",
        f"- Loads third-party code: `{str(report.loads_third_party_code).lower()}`",
        "",
        "## Permission Decisions",
        "",
    ]
    if report.decisions:
        for decision in report.decisions:
            lines.append(
                f"- `{decision.permission}`: `{decision.status}` "
                f"risk=`{decision.risk_level}` - {decision.reason}"
            )
    else:
        lines.append("- none")

    lines.extend(["", "## Findings", ""])
    if report.findings:
        for finding in report.findings:
            permission = f" `{finding.permission}`" if finding.permission else ""
            lines.append(
                f"- `{finding.severity}`{permission}: {finding.message}; "
                f"release_blocker=`{str(finding.release_blocker).lower()}`"
            )
    else:
        lines.append("- none")

    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- The safety gate validates declarations only.",
            "- It does not execute extension code.",
            "- It does not load third-party entrypoints.",
            "- It does not grant runtime permissions.",
            "",
        ]
    )
    return "\n".join(lines)
