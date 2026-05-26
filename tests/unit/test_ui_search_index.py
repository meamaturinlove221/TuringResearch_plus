from __future__ import annotations

from turing_research_plus.ui.cards import build_dashboard_cards
from turing_research_plus.ui.models import DashboardSection, DashboardSectionKind
from turing_research_plus.ui.search_index import build_search_index, search_entries


def test_build_search_index_includes_sections_and_cards() -> None:
    sections = [
        DashboardSection(
            kind=DashboardSectionKind.FAILURE_TAXONOMY,
            title="Failure Board",
            markdown="NOT_ENOUGH_EVIDENCE and visual proof insufficient.",
        )
    ]
    cards = build_dashboard_cards(sections)

    entries = build_search_index(sections, cards)

    assert len(entries) == 2
    assert search_entries(entries, "visual")
    assert search_entries(entries, "missing-term") == []
    assert search_entries(entries, "") == entries
