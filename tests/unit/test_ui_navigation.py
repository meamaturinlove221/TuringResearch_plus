from __future__ import annotations

from turing_research_plus.ui.models import DashboardSection, DashboardSectionKind
from turing_research_plus.ui.navigation import build_dashboard_navigation, section_slug


def test_section_slug_is_stable_ascii() -> None:
    assert section_slug("Project Overview Cards") == "project-overview-cards"
    assert section_slug("!!!") == "section"


def test_build_dashboard_navigation_creates_unique_anchors() -> None:
    sections = [
        DashboardSection(
            kind=DashboardSectionKind.PROJECT_OVERVIEW,
            title="Overview",
            markdown="Review only.",
        ),
        DashboardSection(
            kind=DashboardSectionKind.EVIDENCE_STATUS,
            title="Overview",
            markdown="Requires review.",
        ),
    ]

    nav = build_dashboard_navigation(sections)

    assert [item.item_id for item in nav] == ["overview", "overview-2"]
    assert nav[0].href == "#overview"
    assert nav[1].kind == "evidence_status"
