"""Models for MCP plugin registry entries."""

from __future__ import annotations

from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from turing_research_plus.plugins.models import PluginSafetyLevel


class MCPPluginEntry(BaseModel):
    """One plugin tool exposure declaration."""

    model_config = ConfigDict(extra="forbid")

    plugin_id: str = Field(min_length=1)
    exposed_tool_name: str = Field(pattern=r"^[a-z_][a-z0-9_]*\.[a-z0-9_]+$")
    namespace: str = Field(min_length=1)
    input_schema: str = Field(min_length=1)
    output_schema: str = Field(min_length=1)
    permissions: list[str] = Field(default_factory=list)
    safety_level: PluginSafetyLevel
    default_enabled: bool = False
    live_required: bool = False
    requires_api_key: bool = False
    fake_mode_supported: bool = True
    third_party: bool = True
    docs: list[str] = Field(default_factory=list)
    tests: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def mcp_plugin_entry_is_safe_by_default(self) -> Self:
        if not self.namespace:
            raise ValueError("MCP plugin tools require a namespace")
        if self.exposed_tool_name.split(".", 1)[0] != self.namespace:
            raise ValueError("tool namespace must match exposed_tool_name")
        if self.namespace == "core":
            raise ValueError("plugins cannot override core tools")
        if not self.permissions:
            raise ValueError("MCP plugin tools must declare permissions")
        if self.third_party and self.default_enabled:
            raise ValueError("third-party MCP plugins default_enabled must be false")
        if self.live_required and self.default_enabled:
            raise ValueError("live-required MCP plugins default_enabled must be false")
        if self.live_required and self.fake_mode_supported:
            raise ValueError("live-required plugins cannot claim fake mode support")
        return self


class MCPPluginRegistry(BaseModel):
    """Registry of plugin-exposed MCP tool declarations."""

    model_config = ConfigDict(extra="forbid")

    registry_id: str = Field(min_length=1)
    entries: list[MCPPluginEntry] = Field(default_factory=list)
    disabled_tools: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    requires_human_review: bool = True

    @model_validator(mode="after")
    def registry_requires_review_and_unique_tools(self) -> Self:
        if not self.requires_human_review:
            raise ValueError("MCP plugin registries require human review")
        names = [entry.exposed_tool_name for entry in self.entries]
        if len(names) != len(set(names)):
            raise ValueError("MCP plugin exposed tool names must be unique")
        self.disabled_tools = sorted(
            {entry.exposed_tool_name for entry in self.entries if not entry.default_enabled}
        )
        return self


class MCPPluginValidationIssue(BaseModel):
    """One MCP plugin registry validation issue."""

    model_config = ConfigDict(extra="forbid")

    severity: str = Field(min_length=1)
    message: str = Field(min_length=1)
    plugin_id: str | None = None
    exposed_tool_name: str | None = None


class MCPPluginValidationReport(BaseModel):
    """Validation report for MCP plugin registry exposure."""

    model_config = ConfigDict(extra="forbid")

    registry_id: str = Field(min_length=1)
    valid: bool
    issues: list[MCPPluginValidationIssue] = Field(default_factory=list)
    checked_tools: int = Field(ge=0)
    requires_human_review: bool = True
    starts_mcp_server: bool = False
    loads_plugin_code: bool = False

    @model_validator(mode="after")
    def report_is_validation_only(self) -> Self:
        if not self.requires_human_review:
            raise ValueError("MCP plugin validation reports require human review")
        if self.starts_mcp_server:
            raise ValueError("MCP plugin validation must not start MCP server")
        if self.loads_plugin_code:
            raise ValueError("MCP plugin validation must not load plugin code")
        return self
