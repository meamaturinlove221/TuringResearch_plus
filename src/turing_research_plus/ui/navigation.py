"""Navigation helpers for refined static dashboards."""

from __future__ import annotations

import re

from pydantic import BaseModel, ConfigDict, Field

from turing_research_plus.ui.models import DashboardSection


class DashboardNavItem(BaseModel):
    """One static dashboard navigation item."""

    model_config = ConfigDict(extra="forbid")

    item_id: str = Field(pattern=r"^[a-z0-9][a-z0-9_-]*$")
    title: str = Field(min_length=1)
    kind: str = Field(min_length=1)
    href: str = Field(min_length=1)


def section_slug(title: str) -> str:
    """Return a stable ASCII slug for a dashboard section title."""

    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return slug or "section"


def build_dashboard_navigation(sections: list[DashboardSection]) -> list[DashboardNavItem]:
    """Build static anchor navigation for dashboard sections."""

    seen: dict[str, int] = {}
    items: list[DashboardNavItem] = []
    for section in sections:
        base = section_slug(section.title)
        count = seen.get(base, 0)
        seen[base] = count + 1
        item_id = base if count == 0 else f"{base}-{count + 1}"
        items.append(
            DashboardNavItem(
                item_id=item_id,
                title=section.title,
                kind=section.kind.value,
                href=f"#{item_id}",
            )
        )
    return items
