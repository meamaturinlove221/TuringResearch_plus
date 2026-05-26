"""Reports for trusted local plugin loading."""

from __future__ import annotations

from pathlib import Path
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from turing_research_plus.extension_safety.models import ExtensionSafetyReport
from turing_research_plus.plugins.local_plugin import ExposedPluginCapability
from turing_research_plus.plugins.models import PluginValidationReport
from turing_research_plus.plugins.trust_policy import PluginTrustDecision


class PluginLoadingReport(BaseModel):
    """Review report for one attempted local plugin manifest load."""

    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True)

    plugin_id: str = Field(min_length=1)
    manifest_path: Path
    loaded: bool
    validation_report: PluginValidationReport
    trust_decision: PluginTrustDecision
    safety_report: ExtensionSafetyReport | None = None
    exposed_capabilities: list[ExposedPluginCapability] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)
    requires_human_review: bool = True
    executes_code: bool = False
    loads_entrypoint: bool = False

    @model_validator(mode="after")
    def loading_report_is_metadata_only(self) -> Self:
        if not self.requires_human_review:
            raise ValueError("plugin loading reports require human review")
        if self.executes_code or self.loads_entrypoint:
            raise ValueError("plugin loading report cannot execute code or load entrypoints")
        if self.loaded and not self.trust_decision.allowed_to_load_manifest:
            raise ValueError("loaded report requires allowed trust decision")
        if self.loaded and not self.validation_report.valid:
            raise ValueError("loaded report requires valid manifest")
        if self.loaded and self.safety_report is not None and self.safety_report.release_blocker:
            raise ValueError("loaded report cannot have release-blocking safety findings")
        return self
