"""Paper and advisor summary builder for dashboard data API."""

from __future__ import annotations

from pathlib import Path

from turing_research_plus.dashboard_api.models import DashboardPaperSummary


def build_paper_summary(related_work_path: Path, advisor_path: Path) -> DashboardPaperSummary:
    """Build a paper/advisor summary from public demo Markdown files."""

    related = related_work_path.read_text(encoding="utf-8")
    advisor = advisor_path.read_text(encoding="utf-8")
    return DashboardPaperSummary(
        method_notes=_section_bullets(related, "Method Card Sketch"),
        related_work_groups=[
            item.replace("Group: ", "")
            for item in _section_bullets(related, "Related Work Positioning")
        ],
        safe_claims=_section_bullets(related, "Safe Claims"),
        unsafe_claims=_section_bullets(related, "Unsafe Claims"),
        advisor_next_actions=_section_bullets(advisor, "Next Actions"),
    )


def _section_bullets(text: str, heading: str) -> list[str]:
    capture = False
    bullets: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped == f"## {heading}":
            capture = True
            continue
        if capture and stripped.startswith("## "):
            break
        if capture and stripped.startswith("- "):
            bullets.append(stripped[2:].strip())
    return bullets
