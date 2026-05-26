from __future__ import annotations

from turing_research_plus.ui.cards import DashboardCard, DashboardCardStatus
from turing_research_plus.ui.filters import build_status_filters, filter_cards_by_status


def test_build_status_filters_counts_cards() -> None:
    cards = [
        DashboardCard(
            card_id="a",
            title="A",
            category="evidence",
            status=DashboardCardStatus.BLOCKED,
            summary="Blocked.",
        ),
        DashboardCard(
            card_id="b",
            title="B",
            category="advisor",
            status=DashboardCardStatus.BLOCKED,
            summary="Blocked.",
        ),
        DashboardCard(
            card_id="c",
            title="C",
            category="paper",
            status=DashboardCardStatus.REQUIRES_HUMAN_REVIEW,
            summary="Review.",
        ),
    ]

    filters = build_status_filters(cards)

    assert {item.label: item.count for item in filters} == {
        "blocked": 2,
        "requires-human-review": 1,
    }
    assert len(filter_cards_by_status(cards, DashboardCardStatus.BLOCKED)) == 2
