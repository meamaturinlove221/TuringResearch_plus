"""Compatibility report models for plugin manifests.

The report is a static review artifact. It does not enable plugins, start MCP,
or execute extension code.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class PluginCompatibilityStatus(StrEnum):
    """Overall plugin compatibility status."""

    COMPATIBLE_WITH_REVIEW = "compatible-with-review"
    NEEDS_REVIEW = "needs-review"
    BLOCKED = "blocked"


class PluginCompatibilitySeverity(StrEnum):
    """Finding severities."""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    BLOCKER = "blocker"


class PluginCompatibilityFinding(BaseModel):
    """One compatibility finding."""

    model_config = ConfigDict(extra="forbid")

    check_id: str = Field(pattern=r"^[a-z0-9][a-z0-9_.-]*$")
    passed: bool
    severity: PluginCompatibilitySeverity
    message: str = Field(min_length=1)
    release_blocker: bool = False


class PluginCompatibilityMatrix(BaseModel):
    """Boolean compatibility matrix for one plugin."""

    model_config = ConfigDict(extra="forbid")

    manifest_schema_valid: bool = False
    capability_ids_valid: bool = False
    required_permissions_declared: bool = False
    safety_policy_satisfied: bool = False
    mcp_mapping_valid: bool = False
    docs_present: bool = False
    tests_declared: bool = False
    no_core_tool_override: bool = False
    no_old_project_naming: bool = False
    no_forbidden_permission: bool = False

    @property
    def all_passed(self) -> bool:
        """Return true when every compatibility check passes."""

        return all(
            [
                self.manifest_schema_valid,
                self.capability_ids_valid,
                self.required_permissions_declared,
                self.safety_policy_satisfied,
                self.mcp_mapping_valid,
                self.docs_present,
                self.tests_declared,
                self.no_core_tool_override,
                self.no_old_project_naming,
                self.no_forbidden_permission,
            ]
        )


class PluginCompatibilityReport(BaseModel):
    """Static compatibility report for one plugin."""

    model_config = ConfigDict(extra="forbid")

    plugin_id: str = Field(min_length=1)
    status: PluginCompatibilityStatus
    matrix: PluginCompatibilityMatrix
    findings: list[PluginCompatibilityFinding] = Field(default_factory=list)
    capability_ids: list[str] = Field(default_factory=list)
    mcp_tools: list[str] = Field(default_factory=list)
    docs: list[str] = Field(default_factory=list)
    tests: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    requires_human_review: bool = True
    executes_plugin_code: bool = False
    loads_entrypoint: bool = False
    starts_mcp_server: bool = False
    enables_plugin: bool = False

    @model_validator(mode="after")
    def report_is_review_only(self) -> Self:
        if not self.requires_human_review:
            raise ValueError("plugin compatibility reports require human review")
        if self.executes_plugin_code or self.loads_entrypoint:
            raise ValueError("plugin compatibility must not execute or load plugin code")
        if self.starts_mcp_server:
            raise ValueError("plugin compatibility must not start MCP server")
        if self.enables_plugin:
            raise ValueError("plugin compatibility must not enable plugins")
        return self
