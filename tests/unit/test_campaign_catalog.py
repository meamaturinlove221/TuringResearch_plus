from __future__ import annotations

from turing_research_plus.campaigns.catalog import (
    CAMPAIGN_CATALOG,
    get_campaign,
    list_campaigns,
)
from turing_research_plus.campaigns.markdown_export import render_campaign_catalog_markdown

EXPECTED_CAMPAIGNS = {
    "north_star",
    "knowledge_acquisition",
    "deep_insight",
    "hypothesis_formation",
    "creative_ideation",
    "convergence",
    "stress_test",
    "experiment_planning",
    "artifact_audit",
    "advisor_pack",
    "public_release",
}


def test_campaign_catalog_contains_required_campaigns() -> None:
    assert {campaign.campaign_id for campaign in CAMPAIGN_CATALOG.campaigns} == EXPECTED_CAMPAIGNS


def test_each_campaign_has_required_review_fields() -> None:
    for campaign in list_campaigns():
        assert campaign.purpose
        assert campaign.when_to_use
        assert campaign.preconditions
        assert campaign.recommended_skills
        assert campaign.required_inputs
        assert campaign.expected_outputs
        assert campaign.safety_notes
        assert campaign.fake_live_boundary
        assert campaign.docs
        assert campaign.tests


def test_get_campaign_returns_definition() -> None:
    campaign = get_campaign("public_release")

    assert campaign.campaign_id == "public_release"
    assert campaign.recommended_skills[0] == "turingresearch-qa-release"


def test_campaign_markdown_export_is_review_only() -> None:
    markdown = render_campaign_catalog_markdown()

    assert "# TuringResearch Campaign Catalog" in markdown
    assert "does not execute skills" in markdown
    assert "`public_release`" in markdown
