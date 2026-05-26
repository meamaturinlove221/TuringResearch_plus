"""Models for the static campaign catalog."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, model_validator


class CampaignDefinition(BaseModel):
    """One review-only campaign definition."""

    model_config = ConfigDict(extra="forbid")

    campaign_id: str = Field(pattern=r"^[a-z][a-z0-9_]*$")
    purpose: str = Field(min_length=1)
    when_to_use: list[str] = Field(min_length=1)
    preconditions: list[str] = Field(min_length=1)
    recommended_skills: list[str] = Field(min_length=1)
    required_inputs: list[str] = Field(min_length=1)
    expected_outputs: list[str] = Field(min_length=1)
    safety_notes: list[str] = Field(min_length=1)
    fake_live_boundary: str = Field(min_length=1)
    docs: list[str] = Field(min_length=1)
    tests: list[str] = Field(min_length=1)
    keywords: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def require_turingresearch_skills(self) -> CampaignDefinition:
        invalid = [
            skill
            for skill in self.recommended_skills
            if not skill.startswith("turingresearch-")
        ]
        if invalid:
            msg = f"recommended skills must be turingresearch-* names: {invalid}"
            raise ValueError(msg)
        return self


class CampaignCatalog(BaseModel):
    """Static catalog of review-only campaigns."""

    model_config = ConfigDict(extra="forbid")

    campaigns: list[CampaignDefinition] = Field(min_length=1)

    @model_validator(mode="after")
    def require_unique_campaign_ids(self) -> CampaignCatalog:
        ids = [campaign.campaign_id for campaign in self.campaigns]
        if len(ids) != len(set(ids)):
            raise ValueError("campaign ids must be unique")
        return self

    def by_id(self) -> dict[str, CampaignDefinition]:
        """Return campaign definitions keyed by id."""

        return {campaign.campaign_id: campaign for campaign in self.campaigns}


class CampaignRouteDecision(BaseModel):
    """Campaign routing recommendation. It never executes anything."""

    model_config = ConfigDict(extra="forbid")

    task_description: str = Field(min_length=1)
    recommended_campaign: str = Field(min_length=1)
    recommended_skill: str = Field(pattern=r"^turingresearch-[a-z0-9-]+$")
    ranked_campaigns: list[str] = Field(default_factory=list)
    ranked_skills: list[str] = Field(default_factory=list)
    confidence: float = Field(ge=0, le=1)
    rationale: str = Field(min_length=1)
    does_not_execute: bool = True
    does_not_call_llm: bool = True
    does_not_use_network: bool = True
