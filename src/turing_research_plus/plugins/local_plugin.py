"""Local plugin metadata wrappers."""

from __future__ import annotations

from pathlib import Path
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from turing_research_plus.plugins.models import PluginCapability, PluginManifest
from turing_research_plus.plugins.trust_policy import PluginTrustDecision


class ExposedPluginCapability(BaseModel):
    """Capability exposed as disabled metadata only."""

    model_config = ConfigDict(extra="forbid")

    capability_id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    category: str = Field(min_length=1)
    disabled_by_default: bool = True
    live_mode: bool = False
    fake_mode: bool = True

    @classmethod
    def from_capability(cls, capability: PluginCapability) -> ExposedPluginCapability:
        return cls(
            capability_id=capability.capability_id,
            name=capability.name,
            category=capability.category,
            disabled_by_default=True,
            live_mode=capability.live_mode,
            fake_mode=capability.fake_mode,
        )


class LocalPlugin(BaseModel):
    """A safely loaded local plugin manifest.

    This object contains metadata only. It never imports or executes plugin code.
    """

    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True)

    manifest: PluginManifest
    manifest_path: Path
    trust_decision: PluginTrustDecision
    exposed_capabilities: list[ExposedPluginCapability] = Field(default_factory=list)
    executes_code: bool = False
    loads_entrypoint: bool = False
    requires_human_review: bool = True

    @model_validator(mode="after")
    def local_plugin_is_metadata_only(self) -> Self:
        if not self.requires_human_review:
            raise ValueError("local plugin loading requires human review")
        if self.executes_code or self.loads_entrypoint:
            raise ValueError("local plugin loader must not execute code or load entrypoints")
        if not self.trust_decision.allowed_to_load_manifest:
            raise ValueError("local plugin requires an allowed trust decision")
        if any(not capability.disabled_by_default for capability in self.exposed_capabilities):
            raise ValueError("plugin capabilities must be disabled by default")
        return self
