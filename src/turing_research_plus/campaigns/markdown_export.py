"""Markdown rendering for campaign catalog surfaces."""

from __future__ import annotations

from turing_research_plus.campaigns.catalog import CAMPAIGN_CATALOG
from turing_research_plus.campaigns.models import CampaignCatalog


def render_campaign_catalog_markdown(catalog: CampaignCatalog | None = None) -> str:
    """Render the campaign catalog as Markdown."""

    active_catalog = catalog or CAMPAIGN_CATALOG
    lines = [
        "# TuringResearch Campaign Catalog",
        "",
        "Status: review-only static catalog.",
        "",
        "This catalog recommends campaigns and skills. It does not execute skills,",
        "call an LLM, start an MCP server, or use the network.",
        "",
        "## Campaigns",
        "",
    ]
    for campaign in active_catalog.campaigns:
        skills = ", ".join(f"`{skill}`" for skill in campaign.recommended_skills)
        lines.extend(
            [
                f"### `{campaign.campaign_id}`",
                "",
                f"- Purpose: {campaign.purpose}",
                f"- Recommended skills: {skills}",
                f"- Fake/live boundary: {campaign.fake_live_boundary}",
                "- Preconditions: " + "; ".join(campaign.preconditions),
                "- Expected outputs: " + "; ".join(campaign.expected_outputs),
                "- Safety notes: " + "; ".join(campaign.safety_notes),
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"
