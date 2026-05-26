"""Build static dashboards from existing local review artifacts."""

from __future__ import annotations

from pathlib import Path

from turing_research_plus.ui.html_render import (
    render_dashboard_html,
    render_dashboard_markdown,
)
from turing_research_plus.ui.models import (
    DashboardSection,
    DashboardSectionKind,
    StaticDashboardRequest,
    StaticDashboardSpec,
)

SECTION_SOURCES: list[tuple[DashboardSectionKind, str, str, str]] = [
    (
        DashboardSectionKind.PROJECT_OVERVIEW,
        "Project Overview",
        "knowledge",
        "README.md",
    ),
    (
        DashboardSectionKind.EVIDENCE_STATUS,
        "Evidence Status",
        "knowledge",
        "evidence_summary.md",
    ),
    (
        DashboardSectionKind.ARTIFACT_COMPLETENESS,
        "Artifact Completeness",
        "knowledge",
        "artifact_summary.md",
    ),
    (
        DashboardSectionKind.VISUAL_READINESS,
        "Visual Readiness",
        "knowledge",
        "visual_readiness.md",
    ),
    (
        DashboardSectionKind.RUN_DASHBOARD,
        "Run Dashboard",
        "run_dashboard",
        "run_dashboard.md",
    ),
    (
        DashboardSectionKind.RELATED_WORK,
        "Related Work",
        "knowledge",
        "related_work_positioning.md",
    ),
    (
        DashboardSectionKind.FAILURE_TAXONOMY,
        "Failure Taxonomy",
        "knowledge",
        "failure_taxonomy.md",
    ),
    (
        DashboardSectionKind.ADVISOR_NEXT_ACTIONS,
        "Advisor Next Actions",
        "advisor",
        "next_actions.md",
    ),
]


def build_static_dashboard(
    request: StaticDashboardRequest,
    *,
    write_files: bool = True,
) -> StaticDashboardSpec:
    """Build a static dashboard spec and optionally write HTML/Markdown files."""

    sections = [_load_section(request, item) for item in SECTION_SOURCES]
    spec = StaticDashboardSpec(
        dashboard_id=request.dashboard_id,
        title=request.title,
        project_name=request.project_name,
        output_dir=str(request.output_dir),
        sections=sections,
        generated_files=[
            str(request.output_dir / "index.html"),
            str(request.output_dir / "dashboard.md"),
        ],
        limitations=[
            "Static dashboard only; no login, server, or cloud deployment.",
            "UI displays existing review artifacts only.",
            "UI is not an experiment result.",
            "SparseConv3D success is not claimed without evidence.",
        ],
        requires_human_review=True,
        ui_executed_experiment=False,
        server_required=False,
        login_required=False,
        cloud_deployed=False,
    )
    if write_files:
        request.output_dir.mkdir(parents=True, exist_ok=True)
        (request.output_dir / "index.html").write_text(
            render_dashboard_html(spec),
            encoding="utf-8",
        )
        (request.output_dir / "dashboard.md").write_text(
            render_dashboard_markdown(spec),
            encoding="utf-8",
        )
    return spec


def _load_section(
    request: StaticDashboardRequest,
    source: tuple[DashboardSectionKind, str, str, str],
) -> DashboardSection:
    kind, title, source_group, filename = source
    root = _root_for(request, source_group)
    path = root / filename
    markdown = _read_optional(path)
    return DashboardSection(
        kind=kind,
        title=title,
        markdown=markdown,
        source_path=str(path),
        status="requires-human-review",
        requires_human_review=True,
    )


def _root_for(request: StaticDashboardRequest, source_group: str) -> Path:
    if source_group == "advisor":
        return request.advisor_pack_dir
    if source_group == "run_dashboard":
        return request.run_dashboard_dir
    return request.knowledge_pack_dir


def _read_optional(path: Path) -> str:
    if path.exists():
        return path.read_text(encoding="utf-8")
    return f"Missing input: {path}"
