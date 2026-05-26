"""Models for the TuringResearch capability manifest."""

from __future__ import annotations

from enum import StrEnum
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class CapabilityCategory(StrEnum):
    """Capability categories exposed in the public index."""

    EVIDENCE = "evidence"
    ARTIFACT = "artifact"
    VISUAL = "visual"
    ADVISOR = "advisor"
    PDF = "pdf"
    PAPER = "paper"
    CITATION = "citation"
    COLLISION = "collision"
    RELATED_WORK = "related work"
    ROUTE = "route"
    FAILURE = "failure"
    DASHBOARD = "dashboard"
    REMOTE_ARTIFACT = "remote artifact"
    HANDOFF = "handoff"
    PLUGIN = "plugin"
    WORKSPACE = "workspace"


class CapabilitySafetyLevel(StrEnum):
    """Safety labels for capability exposure."""

    PUBLIC_DEMO = "public-demo"
    LOCAL_REVIEW = "local-review"
    LIVE_OPTIONAL = "live-optional"
    RESTRICTED = "restricted"


class CapabilityStatus(StrEnum):
    """Implementation status labels for capability entries."""

    IMPLEMENTED_MINIMAL = "implemented_minimal"
    IMPLEMENTED_DRY_RUN = "implemented_dry_run"
    CONTRACT_ONLY = "contract_only"
    PLANNED = "planned"
    DESIGN_DRAFT = "design_draft"


class CapabilityEntry(BaseModel):
    """One tool, adapter, exporter, or workflow capability."""

    model_config = ConfigDict(extra="forbid")

    capability_id: str = Field(pattern=r"^[a-z0-9][a-z0-9_.-]*$")
    name: str = Field(min_length=1)
    category: CapabilityCategory
    tool_name: str | None = Field(default=None, pattern=r"^[a-z_][a-z0-9_]*\.[a-z0-9_]+$")
    command: str | None = None
    module: str = Field(min_length=1)
    input_model: str = Field(min_length=1)
    output_model: str = Field(min_length=1)
    live_mode: bool = False
    fake_mode: bool = True
    required_env: list[str] = Field(default_factory=list)
    safety_level: CapabilitySafetyLevel = CapabilitySafetyLevel.LOCAL_REVIEW
    status: CapabilityStatus = CapabilityStatus.IMPLEMENTED_MINIMAL
    docs: list[str] = Field(default_factory=list)
    tests: list[str] = Field(default_factory=list)
    related_skills: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def capability_is_explicit_about_surface(self) -> Self:
        if self.live_mode and not self.required_env:
            raise ValueError("live capabilities must declare required_env")
        if not self.fake_mode and self.safety_level == CapabilitySafetyLevel.PUBLIC_DEMO:
            raise ValueError("public demo capabilities must support fake mode")
        if not self.docs:
            raise ValueError("capability entries require docs")
        if not self.tests:
            raise ValueError("capability entries require tests")
        return self


class CapabilityManifest(BaseModel):
    """Unified capability manifest for tools, adapters, exporters, and workflows."""

    model_config = ConfigDict(extra="forbid")

    manifest_id: str = Field(min_length=1)
    project: str = Field(default="TuringResearch Plus", min_length=1)
    version: str = Field(default="0.1.0", min_length=1)
    capabilities: list[CapabilityEntry] = Field(default_factory=list)
    categories: list[CapabilityCategory] = Field(default_factory=list)
    docs: list[str] = Field(default_factory=list)
    tests: list[str] = Field(default_factory=list)
    requires_human_review: bool = True
    generated_from_static_catalog: bool = True
    starts_mcp_server: bool = False
    executes_tools: bool = False

    @model_validator(mode="after")
    def manifest_is_review_only_and_complete(self) -> Self:
        if not self.requires_human_review:
            raise ValueError("capability manifests require human review")
        if self.starts_mcp_server or self.executes_tools:
            raise ValueError("capability manifest generation must not execute runtime tools")
        capability_ids = [entry.capability_id for entry in self.capabilities]
        if len(capability_ids) != len(set(capability_ids)):
            raise ValueError("capability ids must be unique")
        self.categories = sorted(
            {entry.category for entry in self.capabilities},
            key=lambda item: item.value,
        )
        return self
