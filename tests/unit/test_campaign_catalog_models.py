from __future__ import annotations

import pytest

from turing_research_plus.campaigns.models import (
    CampaignCatalog,
    CampaignDefinition,
    CampaignRouteDecision,
)


def campaign_definition(**overrides: object) -> CampaignDefinition:
    data = {
        "campaign_id": "north_star",
        "purpose": "Clarify scope.",
        "when_to_use": ["project start"],
        "preconditions": ["intent"],
        "recommended_skills": ["turingresearch-fusion-north-star"],
        "required_inputs": ["intent"],
        "expected_outputs": ["north star"],
        "safety_notes": ["do not promote plans"],
        "fake_live_boundary": "Local planning only.",
        "docs": ["docs/north-star.md"],
        "tests": ["tests/unit/test_template_registry.py"],
    }
    data.update(overrides)
    return CampaignDefinition(**data)


def test_campaign_definition_requires_turingresearch_skill_names() -> None:
    with pytest.raises(ValueError, match="recommended skills"):
        campaign_definition(recommended_skills=["other-skill"])


def test_campaign_catalog_requires_unique_ids() -> None:
    with pytest.raises(ValueError, match="unique"):
        CampaignCatalog(campaigns=[campaign_definition(), campaign_definition()])


def test_route_decision_is_non_executing_by_default() -> None:
    decision = CampaignRouteDecision(
        task_description="prepare public launch",
        recommended_campaign="public_release",
        recommended_skill="turingresearch-qa-release",
        confidence=0.8,
        rationale="matched release",
    )

    assert decision.does_not_execute is True
    assert decision.does_not_call_llm is True
    assert decision.does_not_use_network is True
