"""Lightweight static dashboard UI."""

from turing_research_plus.ui.cards import DashboardCard, DashboardCardStatus, build_dashboard_cards
from turing_research_plus.ui.filters import (
    DashboardFilterOption,
    build_status_filters,
    filter_cards_by_status,
)
from turing_research_plus.ui.html_render import (
    render_dashboard_html,
    render_dashboard_markdown,
)
from turing_research_plus.ui.interview_demo_view import (
    InterviewDemoSection,
    InterviewDemoView,
    build_interview_demo_view,
    render_interview_demo_html,
    write_interview_demo_view,
)
from turing_research_plus.ui.models import (
    DashboardSection,
    DashboardSectionKind,
    StaticDashboardRequest,
    StaticDashboardSpec,
)
from turing_research_plus.ui.navigation import DashboardNavItem, build_dashboard_navigation
from turing_research_plus.ui.parity_showcase import (
    ParityShowcasePage,
    ParityShowcaseRow,
    build_parity_showcase_page,
    render_parity_showcase_html,
    write_parity_showcase,
)
from turing_research_plus.ui.project_dashboard import (
    RefinedDashboardBundle,
    build_refined_project_dashboard,
    render_refined_dashboard_html,
    write_public_demo_refined_dashboard,
)
from turing_research_plus.ui.search_index import (
    DashboardSearchEntry,
    build_search_index,
    search_entries,
)
from turing_research_plus.ui.showcase_landing import (
    ShowcaseLandingPage,
    ShowcaseLandingSection,
    build_showcase_landing_page,
    render_showcase_landing_html,
    write_showcase_landing,
)
from turing_research_plus.ui.static_dashboard import build_static_dashboard

__all__ = [
    "DashboardCard",
    "DashboardCardStatus",
    "DashboardFilterOption",
    "DashboardNavItem",
    "DashboardSection",
    "DashboardSectionKind",
    "DashboardSearchEntry",
    "InterviewDemoSection",
    "InterviewDemoView",
    "ParityShowcasePage",
    "ParityShowcaseRow",
    "RefinedDashboardBundle",
    "ShowcaseLandingPage",
    "ShowcaseLandingSection",
    "StaticDashboardRequest",
    "StaticDashboardSpec",
    "build_dashboard_cards",
    "build_dashboard_navigation",
    "build_interview_demo_view",
    "build_parity_showcase_page",
    "build_refined_project_dashboard",
    "build_search_index",
    "build_showcase_landing_page",
    "build_status_filters",
    "build_static_dashboard",
    "filter_cards_by_status",
    "render_dashboard_html",
    "render_dashboard_markdown",
    "render_interview_demo_html",
    "render_parity_showcase_html",
    "render_refined_dashboard_html",
    "render_showcase_landing_html",
    "search_entries",
    "write_showcase_landing",
    "write_public_demo_refined_dashboard",
    "write_interview_demo_view",
    "write_parity_showcase",
]
