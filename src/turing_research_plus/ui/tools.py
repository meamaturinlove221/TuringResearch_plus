"""Local helper wrappers for lightweight dashboard UI."""

from __future__ import annotations

from pathlib import Path

from turing_research_plus.ui.models import StaticDashboardRequest, StaticDashboardSpec
from turing_research_plus.ui.project_dashboard import (
    RefinedDashboardBundle,
    build_refined_project_dashboard,
    write_public_demo_refined_dashboard,
)
from turing_research_plus.ui.static_dashboard import build_static_dashboard


def ui_dashboard_local(request: StaticDashboardRequest) -> StaticDashboardSpec:
    """Build a static local dashboard."""

    return build_static_dashboard(request)


def ui_refined_dashboard_local(request: StaticDashboardRequest) -> RefinedDashboardBundle:
    """Build a refined static local dashboard."""

    return build_refined_project_dashboard(request)


def ui_public_demo_refined_dashboard(output_path: Path) -> Path:
    """Write the safe public demo refined dashboard."""

    return write_public_demo_refined_dashboard(output_path)
