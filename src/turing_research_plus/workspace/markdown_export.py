"""Markdown exporters for workspace overviews."""

from __future__ import annotations

from turing_research_plus.workspace.models import WorkspaceOverview


def render_workspace_overview_markdown(overview: WorkspaceOverview) -> str:
    """Render a workspace overview as Markdown."""

    lines = [
        f"# Workspace Overview: {overview.workspace_name}",
        "",
        f"- Workspace ID: `{overview.workspace_id}`",
        f"- Project count: `{overview.project_count}`",
        f"- Requires human review: `{str(overview.requires_human_review).lower()}`",
        f"- Evidence source: `{str(overview.evidence_source).lower()}`",
        "",
        "## Projects",
        "",
        "| Project | Type | Status | Privacy | Missing paths | Fake/demo |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for project in overview.projects:
        missing = ", ".join(project.missing_paths) if project.missing_paths else "none"
        lines.append(
            "| "
            f"`{project.project_id}` / {project.project_name} | "
            f"`{project.project_type}` | `{project.status}` | "
            f"`{project.privacy_level}` | {missing} | "
            f"`{str(project.fake_demo).lower()}` |"
        )

    lines.extend(["", "## Safety Warnings", ""])
    lines.extend([f"- {warning}" for warning in overview.safety_warnings] or ["- none"])
    lines.extend(["", "## Limitations", ""])
    lines.extend([f"- {limitation}" for limitation in overview.limitations] or ["- none"])
    lines.append("")
    return "\n".join(lines)
