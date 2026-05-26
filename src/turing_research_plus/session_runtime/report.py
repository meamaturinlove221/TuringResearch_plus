"""Markdown rendering for session preflight reports."""

from __future__ import annotations

from turing_research_plus.session_runtime.models import SessionPreflightReport


def render_session_preflight_report(report: SessionPreflightReport) -> str:
    """Render a deterministic session preflight report."""

    lines = [
        f"# Session Preflight Report: {report.session_id}",
        "",
        f"- Context package: `{report.context_package_id}`",
        f"- Route: `{report.route_id}`",
        f"- Status: `{report.status}`",
        f"- Release blocker: `{str(report.release_blocker).lower()}`",
        f"- Remote execution enabled: `{str(report.remote_execution_enabled).lower()}`",
        f"- Live network enabled: `{str(report.live_network_enabled).lower()}`",
        f"- Proposed updates only: `{str(report.proposed_updates_only).lower()}`",
        f"- Requires human review: `{str(report.requires_human_review).lower()}`",
        "",
        "## Lookup",
        "",
        f"- Project root: `{report.lookup.project_root}`",
        f"- Context source: `{report.lookup.context_source}`",
        f"- Output dir: `{report.lookup.output_dir}`",
        "",
        "## Environment Checks",
        "",
    ]
    lines.extend(
        [
            f"- `{check.status}` `{check.check_id}`: {check.message}"
            + (f" (`{check.path}`)" if check.path else "")
            for check in report.environment_checks
        ]
        or ["- None."]
    )
    lines.extend(["", "## Findings", ""])
    lines.extend(
        [
            f"- `{finding.severity}` `{finding.finding_id}`: {finding.message}"
            + (f" (`{finding.path}`)" if finding.path else "")
            for finding in report.findings
        ]
        or ["- None."]
    )
    lines.extend(["", "## Checked Paths", ""])
    lines.extend([f"- `{path}`" for path in report.checked_paths] or ["- None."])
    lines.extend(["", "## Platform Warnings", ""])
    lines.extend([f"- `{warning}`" for warning in report.platform_warnings] or ["- None."])
    return "\n".join(lines) + "\n"
