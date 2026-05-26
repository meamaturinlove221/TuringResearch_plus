"""Models for skill registry and routing."""

from __future__ import annotations

from enum import StrEnum
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field


class SkillStatus(StrEnum):
    """Allowed skill status labels."""

    MISSING = "missing"
    STUB = "stub"
    DRAFT = "draft"
    USABLE = "usable"
    LOCKED = "locked"


class SkillRegistryEntry(BaseModel):
    """One repo-scoped skill registry entry."""

    model_config = ConfigDict(extra="forbid")

    skill_name: str = Field(pattern=r"^turingresearch-[a-z0-9-]+$")
    path: Path
    role: str = Field(min_length=1)
    when_to_use: list[str] = Field(default_factory=list)
    inputs: list[str] = Field(default_factory=list)
    outputs: list[str] = Field(default_factory=list)
    related_contracts: list[str] = Field(default_factory=list)
    related_lanes: list[str] = Field(default_factory=list)
    related_modules: list[str] = Field(default_factory=list)
    status: SkillStatus = SkillStatus.USABLE
    release_target: str = "current"


class SkillRoute(BaseModel):
    """Task category to skill recommendation mapping."""

    model_config = ConfigDict(extra="forbid")

    category: str = Field(min_length=1)
    recommended_skill: str = Field(pattern=r"^turingresearch-[a-z0-9-]+$")
    ranked_skills: list[str] = Field(default_factory=list)
    related_lane: str = Field(min_length=1)
    related_contracts: list[str] = Field(default_factory=list)
    keywords: list[str] = Field(default_factory=list)


class SkillRoutingDecision(BaseModel):
    """Routing recommendation. It never executes a skill."""

    model_config = ConfigDict(extra="forbid")

    query: str = Field(min_length=1)
    category: str = Field(min_length=1)
    recommended_skill: str = Field(pattern=r"^turingresearch-[a-z0-9-]+$")
    ranked_skills: list[str] = Field(default_factory=list)
    confidence: float = Field(ge=0, le=1)
    rationale: str = Field(min_length=1)
    related_lane: str = Field(min_length=1)
    does_not_execute: bool = True
