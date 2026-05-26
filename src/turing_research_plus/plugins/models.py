"""Models for manifest-only plugin architecture."""

from __future__ import annotations

from enum import StrEnum
from pathlib import Path
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class PluginType(StrEnum):
    """Allowed plugin types."""

    ADAPTER = "adapter"
    EXPORTER = "exporter"
    WORKFLOW = "workflow"
    SKILL = "skill"
    VALIDATOR = "validator"
    RENDERER = "renderer"


class PluginEntryKind(StrEnum):
    """Allowed plugin entry kinds."""

    MANIFEST_ONLY = "manifest-only"
    LOCAL_HELPER_DECLARATION = "local-helper-declaration"
    MCP_TOOL_DECLARATION = "mcp-tool-declaration"
    SKILL_DECLARATION = "skill-declaration"


class PluginSafetyLevel(StrEnum):
    """Plugin safety levels."""

    PUBLIC_DEMO = "public-demo"
    LOCAL_REVIEW = "local-review"
    LIVE_OPTIONAL = "live-optional"
    RESTRICTED = "restricted"
    DISABLED = "disabled"


class PluginStatus(StrEnum):
    """Plugin registry status values."""

    DISABLED = "disabled"
    DRAFT = "draft"
    REVIEW = "requires-review"
    ENABLED = "enabled"


class PluginCapability(BaseModel):
    """One capability declared by a plugin."""

    model_config = ConfigDict(extra="forbid")

    capability_id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    category: str = Field(min_length=1)
    description: str = Field(min_length=1)
    inputs: list[str] = Field(default_factory=list)
    outputs: list[str] = Field(default_factory=list)
    live_mode: bool = False
    fake_mode: bool = True


class PluginManifest(BaseModel):
    """Manifest-only plugin declaration.

    The manifest does not authorize dynamic imports or code execution.
    """

    model_config = ConfigDict(extra="forbid")

    plugin_id: str = Field(pattern=r"^[a-z0-9][a-z0-9_-]*$")
    name: str = Field(min_length=1)
    version: str = Field(min_length=1)
    type: PluginType
    entry_kind: PluginEntryKind = PluginEntryKind.MANIFEST_ONLY
    capabilities: list[PluginCapability] = Field(default_factory=list)
    required_permissions: list[str] = Field(default_factory=list)
    config_schema: dict[str, object] = Field(default_factory=dict)
    inputs: list[str] = Field(default_factory=list)
    outputs: list[str] = Field(default_factory=list)
    safety_level: PluginSafetyLevel
    status: PluginStatus = PluginStatus.DISABLED
    author: str | None = None
    license: str | None = None
    third_party: bool = True
    executes_code: bool = False
    python_entrypoint: str | None = None
    manifest_path: Path | None = None

    @model_validator(mode="after")
    def manifest_is_safe_by_default(self) -> Self:
        if not self.required_permissions:
            raise ValueError("plugin manifest must declare required permissions")
        if self.executes_code:
            raise ValueError("plugin architecture does not execute plugin code")
        if self.python_entrypoint:
            raise ValueError("plugin architecture does not load Python entrypoints")
        if self.third_party and self.status != PluginStatus.DISABLED:
            raise ValueError("third-party plugins must be disabled by default")
        if self.safety_level == PluginSafetyLevel.DISABLED and self.status != PluginStatus.DISABLED:
            raise ValueError("disabled safety level requires disabled status")
        return self


class PluginRegistry(BaseModel):
    """A registry of validated plugin manifests."""

    model_config = ConfigDict(extra="forbid")

    registry_id: str = Field(min_length=1)
    plugins: list[PluginManifest] = Field(default_factory=list)
    disabled_plugins: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    requires_human_review: bool = True

    @model_validator(mode="after")
    def registry_requires_review_and_unique_ids(self) -> Self:
        if not self.requires_human_review:
            raise ValueError("plugin registry requires human review")
        plugin_ids = [plugin.plugin_id for plugin in self.plugins]
        if len(plugin_ids) != len(set(plugin_ids)):
            raise ValueError("plugin ids must be unique")
        self.disabled_plugins = sorted(
            {plugin.plugin_id for plugin in self.plugins if plugin.status == PluginStatus.DISABLED}
        )
        return self


class PluginValidationIssue(BaseModel):
    """One plugin validation issue."""

    model_config = ConfigDict(extra="forbid")

    severity: str = Field(min_length=1)
    message: str = Field(min_length=1)
    field: str | None = None


class PluginValidationReport(BaseModel):
    """Validation report for one plugin manifest."""

    model_config = ConfigDict(extra="forbid")

    plugin_id: str = Field(min_length=1)
    valid: bool
    issues: list[PluginValidationIssue] = Field(default_factory=list)
    safety_level: PluginSafetyLevel
    status: PluginStatus
    executes_code: bool = False
    loads_entrypoint: bool = False
    requires_human_review: bool = True

    @model_validator(mode="after")
    def validation_report_requires_review(self) -> Self:
        if not self.requires_human_review:
            raise ValueError("plugin validation reports require human review")
        if self.executes_code or self.loads_entrypoint:
            raise ValueError("plugin validation cannot execute code or load entrypoints")
        return self
