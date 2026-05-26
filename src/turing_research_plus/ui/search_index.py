"""Simple static search index for dashboards."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from turing_research_plus.ui.cards import DashboardCard
from turing_research_plus.ui.models import DashboardSection
from turing_research_plus.ui.navigation import section_slug


class DashboardSearchEntry(BaseModel):
    """One static search entry."""

    model_config = ConfigDict(extra="forbid")

    entry_id: str = Field(pattern=r"^[a-z0-9][a-z0-9_-]*$")
    title: str = Field(min_length=1)
    category: str = Field(min_length=1)
    text: str = Field(min_length=1)
    href: str = Field(min_length=1)


def build_search_index(
    sections: list[DashboardSection],
    cards: list[DashboardCard],
) -> list[DashboardSearchEntry]:
    """Build a static local search index from sections and cards."""

    entries: list[DashboardSearchEntry] = []
    for section in sections:
        slug = section_slug(section.title)
        text = " ".join([section.title, section.kind.value, section.markdown])
        entries.append(
            DashboardSearchEntry(
                entry_id=f"section-{slug}",
                title=section.title,
                category=section.kind.value,
                text=_compact_text(text),
                href=f"#{slug}",
            )
        )
    for card in cards:
        entries.append(
            DashboardSearchEntry(
                entry_id=f"card-{card.card_id}",
                title=card.title,
                category=card.category,
                text=_compact_text(f"{card.title} {card.status.value} {card.summary}"),
                href=f"#card-{card.card_id}",
            )
        )
    return entries


def search_entries(entries: list[DashboardSearchEntry], query: str) -> list[DashboardSearchEntry]:
    """Search entries with a case-insensitive substring match."""

    needle = query.casefold().strip()
    if not needle:
        return entries
    return [entry for entry in entries if needle in entry.text.casefold()]


def _compact_text(text: str) -> str:
    return " ".join(text.split())
