"""Markdown report rendering for privacy scans."""

from __future__ import annotations

from turing_research_plus.privacy.models import PrivacyScanReport


def render_privacy_scan_report_markdown(report: PrivacyScanReport) -> str:
    """Render a privacy scan report as Markdown."""

    lines = [
        "# Privacy Scan Report",
        "",
        f"- Scanned paths: `{len(report.scanned_paths)}`",
        f"- Findings: `{len(report.findings)}`",
        f"- Severity: `{report.severity}`",
        f"- Release blocker: `{str(report.release_blocker).lower()}`",
        f"- Redaction possible: `{str(report.redaction_possible).lower()}`",
        f"- Requires human review: `{str(report.requires_human_review).lower()}`",
        "",
        "## Findings",
        "",
    ]
    if report.findings:
        for finding in report.findings:
            location = (
                f"{finding.path}:{finding.line_number}"
                if finding.line_number is not None
                else finding.path
            )
            lines.append(
                f"- `{finding.severity}` `{finding.finding_type}` at `{location}`: "
                f"{finding.recommended_action}"
            )
    else:
        lines.append("- none")

    lines.extend(["", "## Proposed Redactions", ""])
    if report.proposed_redactions:
        for proposal in report.proposed_redactions:
            lines.append(f"- `{proposal.path}`: replace with `{proposal.replacement}`")
    else:
        lines.append("- none")

    lines.extend(["", "## Limitations", ""])
    lines.extend([f"- {item}" for item in report.limitations] or ["- none"])
    lines.append("")
    return "\n".join(lines)
