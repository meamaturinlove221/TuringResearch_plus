"""Review-only strategy book for campaign parity."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from turing_research_plus.campaigns.catalog import CAMPAIGN_CATALOG
from turing_research_plus.campaigns.models import CampaignCatalog, CampaignDefinition

CAMPAIGN_ALIASES = {
    "hypothesis": "hypothesis_formation",
    "ideation": "creative_ideation",
    "experiment_execution": "experiment_planning",
}


class CampaignStrategyEntry(BaseModel):
    """One strategy-book entry for a campaign."""

    model_config = ConfigDict(extra="forbid")

    campaign_id: str = Field(min_length=1)
    display_id: str = Field(min_length=1)
    purpose: str = Field(min_length=1)
    when_to_use: list[str] = Field(min_length=1)
    primary_skill: str = Field(pattern=r"^turingresearch-[a-z0-9-]+$")
    expected_outputs: list[str] = Field(min_length=1)
    safety_notes: list[str] = Field(min_length=1)
    docs: list[str] = Field(min_length=1)
    tests: list[str] = Field(min_length=1)


class CampaignStrategyBook(BaseModel):
    """Static strategy book. It never executes a campaign."""

    model_config = ConfigDict(extra="forbid")

    title: str = "TuringResearch Strategy Book"
    entries: list[CampaignStrategyEntry] = Field(min_length=1)
    does_not_execute: bool = True
    does_not_call_llm: bool = True
    does_not_use_network: bool = True
    requires_human_review: bool = True

    def by_campaign_id(self) -> dict[str, CampaignStrategyEntry]:
        """Return entries keyed by campaign id and supported aliases."""

        by_id = {entry.campaign_id: entry for entry in self.entries}
        for alias, canonical in CAMPAIGN_ALIASES.items():
            if canonical in by_id:
                by_id[alias] = by_id[canonical]
        return by_id


def build_campaign_strategy_book(
    catalog: CampaignCatalog | None = None,
) -> CampaignStrategyBook:
    """Build the local strategy book from the campaign catalog."""

    active_catalog = catalog or CAMPAIGN_CATALOG
    return CampaignStrategyBook(
        entries=[_entry_from_campaign(campaign) for campaign in active_catalog.campaigns]
    )


def render_campaign_strategy_book(book: CampaignStrategyBook | None = None) -> str:
    """Render the strategy book as Markdown."""

    active_book = book or build_campaign_strategy_book()
    lines = [
        f"# {active_book.title}",
        "",
        "- Does not execute: `true`",
        "- Does not call LLM: `true`",
        "- Does not use network: `true`",
        "- Requires human review: `true`",
        "",
        "| Campaign | Purpose | Primary skill |",
        "| --- | --- | --- |",
    ]
    for entry in active_book.entries:
        lines.append(
            f"| `{entry.display_id}` | {entry.purpose} | `{entry.primary_skill}` |"
        )
    return "\n".join(lines) + "\n"


def _entry_from_campaign(campaign: CampaignDefinition) -> CampaignStrategyEntry:
    display_id = _display_id(campaign.campaign_id)
    return CampaignStrategyEntry(
        campaign_id=campaign.campaign_id,
        display_id=display_id,
        purpose=campaign.purpose,
        when_to_use=campaign.when_to_use,
        primary_skill=campaign.recommended_skills[0],
        expected_outputs=campaign.expected_outputs,
        safety_notes=campaign.safety_notes,
        docs=campaign.docs,
        tests=campaign.tests,
    )


def _display_id(campaign_id: str) -> str:
    reverse = {canonical: alias for alias, canonical in CAMPAIGN_ALIASES.items()}
    return reverse.get(campaign_id, campaign_id)
