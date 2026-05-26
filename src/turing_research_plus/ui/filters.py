"""Static filter helpers for refined dashboards."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from turing_research_plus.ui.cards import DashboardCard, DashboardCardStatus


class DashboardFilterOption(BaseModel):
    """One static filter option."""

    model_config = ConfigDict(extra="forbid")

    filter_id: str = Field(pattern=r"^[a-z0-9][a-z0-9_-]*$")
    label: str = Field(min_length=1)
    count: int = Field(ge=0)


def build_status_filters(cards: list[DashboardCard]) -> list[DashboardFilterOption]:
    """Build card status filters."""

    options: list[DashboardFilterOption] = []
    for status in DashboardCardStatus:
        count = sum(1 for card in cards if card.status == status)
        if count:
            options.append(
                DashboardFilterOption(
                    filter_id=f"status-{status.value.replace('_', '-')}",
                    label=status.value,
                    count=count,
                )
            )
    return options


def filter_cards_by_status(
    cards: list[DashboardCard],
    status: DashboardCardStatus,
) -> list[DashboardCard]:
    """Return cards with a matching status."""

    return [card for card in cards if card.status == status]
