from __future__ import annotations

from turing_research_plus.ui.html_render import (
    render_dashboard_html,
    render_dashboard_markdown,
)
from turing_research_plus.ui.models import (
    DashboardSection,
    DashboardSectionKind,
    StaticDashboardSpec,
)


def test_render_dashboard_html_escapes_markdown() -> None:
    spec = StaticDashboardSpec(
        dashboard_id="dash-1",
        title="Dashboard",
        project_name="Project",
        output_dir="out",
        sections=[
            DashboardSection(
                kind=DashboardSectionKind.RUN_DASHBOARD,
                title="Run Dashboard",
                markdown="<script>alert('x')</script>\nSparseConv3D success is not claimed.",
            )
        ],
    )

    html = render_dashboard_html(spec)

    assert "&lt;script&gt;" in html
    assert "<script>alert" not in html
    assert "No Modal execution" in html
    assert "Not an experiment result" in html


def test_render_dashboard_markdown_preserves_boundaries() -> None:
    spec = StaticDashboardSpec(
        dashboard_id="dash-1",
        title="Dashboard",
        project_name="Project",
        output_dir="out",
        sections=[
            DashboardSection(
                kind=DashboardSectionKind.PROJECT_OVERVIEW,
                title="Overview",
                markdown="Review only.",
            )
        ],
    )

    markdown = render_dashboard_markdown(spec)

    assert "No Modal execution" in markdown
    assert "No VGGT execution" in markdown
    assert "Not an experiment result" in markdown
