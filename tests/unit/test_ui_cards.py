from __future__ import annotations

import pytest

from turing_research_plus.ui.cards import (
    DashboardCard,
    DashboardCardStatus,
    build_dashboard_cards,
)
from turing_research_plus.ui.models import DashboardSection, DashboardSectionKind


def test_build_dashboard_cards_marks_blocked_content() -> None:
    sections = [
        DashboardSection(
            kind=DashboardSectionKind.VISUAL_READINESS,
            title="Visual Readiness",
            markdown="blocked: visual proof insufficient",
        )
    ]

    cards = build_dashboard_cards(sections)

    assert cards[0].status == DashboardCardStatus.BLOCKED
    assert cards[0].requires_human_review is True
    assert cards[0].demo_safe is True


def test_dashboard_card_rejects_non_demo_safe_claim() -> None:
    with pytest.raises(ValueError, match="demo safe"):
        DashboardCard(
            card_id="unsafe",
            title="Unsafe",
            category="demo",
            status=DashboardCardStatus.READY,
            summary="Unsafe fixture.",
            demo_safe=False,
        )
