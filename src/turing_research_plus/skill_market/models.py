"""Models for the local skill marketplace layout."""

from __future__ import annotations

from enum import StrEnum
from pathlib import Path
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from turing_research_plus.skills.models import SkillStatus


class SkillMarketCategory(StrEnum):
    """Marketplace skill categories."""

    ORCHESTRATION = "orchestration"
    EVIDENCE = "evidence"
    ARTIFACT = "artifact"
    VISUAL = "visual"
    ADVISOR = "advisor"
    PDF = "pdf"
    PAPER = "paper"
    WEB = "web"
    REMOTE = "remote"
    ROUTE = "route"
    FAILURE = "failure"
    DASHBOARD = "dashboard"
    WORKSPACE = "workspace"
    PLUGIN = "plugin"
    RELEASE = "release"


class SkillMarketplaceEntry(BaseModel):
    """One local skill marketplace entry."""

    model_config = ConfigDict(extra="forbid")

    skill_name: str = Field(pattern=r"^turingresearch-[a-z0-9-]+$")
    path: Path
    category: SkillMarketCategory
    status: SkillStatus
    summary: str = Field(min_length=1)
    docs: list[str] = Field(default_factory=list)
    tests: list[str] = Field(default_factory=list)
    related_contracts: list[str] = Field(default_factory=list)
    related_lanes: list[str] = Field(default_factory=list)
    related_modules: list[str] = Field(default_factory=list)
    source: str = "repo-skill"

    @model_validator(mode="after")
    def entry_has_review_metadata(self) -> Self:
        if not self.docs:
            raise ValueError("marketplace entries require docs")
        if not self.tests:
            raise ValueError("marketplace entries require tests")
        if not self.related_contracts:
            raise ValueError("marketplace entries require related contracts")
        return self


class SkillMarketplaceIndex(BaseModel):
    """Local skill marketplace index."""

    model_config = ConfigDict(extra="forbid")

    marketplace_id: str = Field(default="turingresearch_skill_marketplace", min_length=1)
    entries: list[SkillMarketplaceEntry]
    categories: list[SkillMarketCategory] = Field(default_factory=list)
    docs: list[str] = Field(default_factory=list)
    tests: list[str] = Field(default_factory=list)
    local_only: bool = True
    remote_publish: bool = False
    requires_human_review: bool = True

    @model_validator(mode="after")
    def marketplace_is_local_and_unique(self) -> Self:
        if not self.local_only or self.remote_publish:
            raise ValueError("skill marketplace layout is local-only")
        if not self.requires_human_review:
            raise ValueError("skill marketplace requires human review")
        names = [entry.skill_name for entry in self.entries]
        if len(names) != len(set(names)):
            raise ValueError("marketplace skill names must be unique")
        self.categories = sorted(
            {entry.category for entry in self.entries},
            key=lambda item: item.value,
        )
        return self


class SkillMarketplaceReviewReport(BaseModel):
    """Integrity report for the local skill marketplace."""

    model_config = ConfigDict(extra="forbid")

    marketplace_id: str = Field(min_length=1)
    valid: bool
    checked_skills: int = Field(ge=0)
    missing_skills: list[str] = Field(default_factory=list)
    invalid_names: list[str] = Field(default_factory=list)
    missing_metadata: list[str] = Field(default_factory=list)
    remote_publish: bool = False
    requires_human_review: bool = True
