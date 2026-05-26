"""Future plugin sandbox roadmap helpers."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class FutureSandboxMilestone(BaseModel):
    """One future sandbox milestone."""

    model_config = ConfigDict(extra="forbid")

    milestone_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    status: str = Field(min_length=1)
    required_before_runtime_execution: bool = True
    notes: list[str] = Field(default_factory=list)


class FutureSandboxRoadmap(BaseModel):
    """Roadmap for future OS/runtime sandbox work."""

    model_config = ConfigDict(extra="forbid")

    roadmap_id: str = "future-plugin-sandbox-roadmap"
    milestones: list[FutureSandboxMilestone] = Field(default_factory=list)
    implements_os_sandbox_now: bool = False
    requires_human_review: bool = True


def build_future_sandbox_roadmap() -> FutureSandboxRoadmap:
    """Return the v0.7 future sandbox roadmap."""

    return FutureSandboxRoadmap(
        milestones=[
            FutureSandboxMilestone(
                milestone_id="threat-model",
                title="Plugin threat model",
                status="planned",
                notes=["Define trust boundaries and attacker model."],
            ),
            FutureSandboxMilestone(
                milestone_id="dependency-isolation",
                title="Dependency isolation",
                status="planned",
                notes=["Separate plugin dependencies from core runtime."],
            ),
            FutureSandboxMilestone(
                milestone_id="filesystem-scope",
                title="Filesystem scope enforcement",
                status="planned",
                notes=["Restrict plugin reads/writes to reviewed project paths."],
            ),
            FutureSandboxMilestone(
                milestone_id="network-policy",
                title="Network policy enforcement",
                status="planned",
                notes=["Keep network disabled unless explicit live mode is reviewed."],
            ),
            FutureSandboxMilestone(
                milestone_id="provenance",
                title="Plugin provenance and disable flow",
                status="planned",
                notes=["Track plugin source, version, review state, and disable path."],
            ),
        ]
    )
