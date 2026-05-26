"""Campaign precondition checks for review-only routing."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from turing_research_plus.campaigns.catalog import get_campaign
from turing_research_plus.campaigns.strategy_book import CAMPAIGN_ALIASES


class CampaignPreconditionReport(BaseModel):
    """Precondition status for one recommended campaign."""

    model_config = ConfigDict(extra="forbid")

    campaign_id: str = Field(min_length=1)
    provided_inputs: list[str] = Field(default_factory=list)
    required_preconditions: list[str] = Field(default_factory=list)
    missing_preconditions: list[str] = Field(default_factory=list)
    ready_for_planning: bool = False
    does_not_fabricate_missing_inputs: bool = True
    requires_human_review: bool = True


def evaluate_campaign_preconditions(
    campaign_id: str,
    provided_inputs: list[str] | None = None,
) -> CampaignPreconditionReport:
    """Evaluate campaign preconditions without inventing missing inputs."""

    canonical_id = CAMPAIGN_ALIASES.get(campaign_id, campaign_id)
    campaign = get_campaign(canonical_id)
    provided = [item.strip().lower() for item in provided_inputs or [] if item.strip()]
    missing = [
        precondition
        for precondition in campaign.preconditions
        if not _is_precondition_satisfied(precondition, provided)
    ]
    return CampaignPreconditionReport(
        campaign_id=canonical_id,
        provided_inputs=provided_inputs or [],
        required_preconditions=list(campaign.preconditions),
        missing_preconditions=missing,
        ready_for_planning=not missing,
    )


def render_campaign_precondition_report(report: CampaignPreconditionReport) -> str:
    """Render a precondition report as Markdown."""

    lines = [
        f"# Campaign Preconditions: {report.campaign_id}",
        "",
        f"- Ready for planning: `{str(report.ready_for_planning).lower()}`",
        "- Does not fabricate missing inputs: "
        f"`{str(report.does_not_fabricate_missing_inputs).lower()}`",
        f"- Requires human review: `{str(report.requires_human_review).lower()}`",
        "",
        "## Missing Preconditions",
        "",
    ]
    lines.extend([f"- {item}" for item in report.missing_preconditions] or ["- none"])
    return "\n".join(lines) + "\n"


def _is_precondition_satisfied(precondition: str, provided: list[str]) -> bool:
    normalized = precondition.lower()
    return any(item in normalized or normalized in item for item in provided)
