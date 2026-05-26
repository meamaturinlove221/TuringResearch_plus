"""Card models and builders for refined dashboards."""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, model_validator

from turing_research_plus.ui.models import DashboardSection, DashboardSectionKind


class DashboardCardStatus(StrEnum):
    """Card status labels."""

    READY = "ready"
    PARTIAL = "partial"
    BLOCKED = "blocked"
    MISSING = "missing"
    REQUIRES_HUMAN_REVIEW = "requires-human-review"


class DashboardCard(BaseModel):
    """One dashboard summary card."""

    model_config = ConfigDict(extra="forbid")

    card_id: str = Field(pattern=r"^[a-z0-9][a-z0-9_-]*$")
    title: str = Field(min_length=1)
    category: str = Field(min_length=1)
    status: DashboardCardStatus
    summary: str = Field(min_length=1)
    source_kind: DashboardSectionKind | None = None
    requires_human_review: bool = True
    demo_safe: bool = True

    @model_validator(mode="after")
    def card_requires_review(self) -> DashboardCard:
        if not self.requires_human_review:
            raise ValueError("dashboard cards require human review")
        if not self.demo_safe:
            raise ValueError("dashboard cards must remain demo safe")
        return self


def build_dashboard_cards(sections: list[DashboardSection]) -> list[DashboardCard]:
    """Build dashboard cards from static sections."""

    cards: list[DashboardCard] = []
    for section in sections:
        cards.append(
            DashboardCard(
                card_id=section.kind.value.replace("_", "-"),
                title=section.title,
                category=section.kind.value,
                status=_status_for_markdown(section.markdown),
                summary=_summarize_markdown(section.markdown),
                source_kind=section.kind,
            )
        )
    return cards


def _status_for_markdown(markdown: str) -> DashboardCardStatus:
    text = markdown.lower()
    if "missing input:" in text or "missing" in text or "blocked" in text:
        return DashboardCardStatus.BLOCKED
    if "not-enough-evidence" in text or "requires-human-review" in text:
        return DashboardCardStatus.REQUIRES_HUMAN_REVIEW
    if "partial" in text:
        return DashboardCardStatus.PARTIAL
    return DashboardCardStatus.REQUIRES_HUMAN_REVIEW


def _summarize_markdown(markdown: str, *, limit: int = 180) -> str:
    lines = [_clean_line(line) for line in markdown.splitlines() if line.strip()]
    summary = " ".join(lines[:3]).strip()
    if not summary:
        return "No summary available; requires human review."
    if len(summary) > limit:
        return summary[: limit - 3].rstrip() + "..."
    return summary


def _clean_line(line: str) -> str:
    return line.strip().lstrip("#- ").strip("` ")
