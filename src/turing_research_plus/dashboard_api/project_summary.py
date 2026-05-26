"""Project summary builder for dashboard data API."""

from __future__ import annotations

from pathlib import Path

from turing_research_plus.dashboard_api.models import DashboardProjectSummary


def build_project_summary(
    path: Path,
    *,
    project_id: str = "public_demo",
) -> DashboardProjectSummary:
    """Build a project summary from a public demo Markdown file."""

    text = path.read_text(encoding="utf-8")
    return DashboardProjectSummary(
        project_id=project_id,
        title=_first_heading(text) or "Public Demo Project",
        status=_field_after_prefix(text, "Status:") or "demo only",
        topic=_section_text(text, "Topic") or "public demo",
        north_star=_section_text(text, "North Star") or "review evidence-first workflow",
    )


def _first_heading(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def _field_after_prefix(text: str, prefix: str) -> str:
    for line in text.splitlines():
        if line.startswith(prefix):
            return line[len(prefix) :].strip()
    return ""


def _section_text(text: str, heading: str) -> str:
    capture = False
    lines: list[str] = []
    for line in text.splitlines():
        if line.strip() == f"## {heading}":
            capture = True
            continue
        if capture and line.startswith("## "):
            break
        if capture and line.strip():
            lines.append(line.strip())
    return " ".join(lines)
