"""Policy model for plugin sandbox decisions.

This module does not implement an OS-level sandbox. It defines the policy layer
that must be satisfied before future runtime sandbox work can be considered.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class SandboxPermission(StrEnum):
    """Plugin sandbox permission categories."""

    READ_PROJECT_FILES = "read_project_files"
    WRITE_PROJECT_FILES = "write_project_files"
    NETWORK_ACCESS = "network_access"
    LIVE_API_ACCESS = "live_api_access"
    REMOTE_READ = "remote_read"
    REMOTE_WRITE = "remote_write"
    EXECUTE_CODE = "execute_code"
    SHELL_ACCESS = "shell_access"
    SECRETS_ACCESS = "secrets_access"
    ARTIFACT_EXPORT = "artifact_export"


class SandboxDecisionStatus(StrEnum):
    """Decision status for one sandbox permission."""

    ALLOWED = "allowed"
    SCOPED_ONLY = "scoped-only"
    EXPLICIT_ONLY = "explicit-only"
    DENIED = "denied"


class SandboxRiskLevel(StrEnum):
    """Risk levels for plugin sandbox decisions."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class SandboxPermissionDecision(BaseModel):
    """Policy decision for one plugin sandbox permission."""

    model_config = ConfigDict(extra="forbid")

    permission: SandboxPermission
    status: SandboxDecisionStatus
    allowed: bool
    requires_explicit_enable: bool = False
    requires_human_review: bool = True
    release_blocker: bool = False
    future_sandbox_requirement: bool = False
    risk_level: SandboxRiskLevel
    reason: str = Field(min_length=1)

    @model_validator(mode="after")
    def decision_requires_review(self) -> Self:
        if not self.requires_human_review:
            raise ValueError("sandbox permission decisions require human review")
        if self.status == SandboxDecisionStatus.DENIED and self.allowed:
            raise ValueError("denied permissions cannot be allowed")
        if self.release_blocker and self.allowed:
            raise ValueError("release blockers cannot be allowed")
        return self


class PluginSandboxPolicy(BaseModel):
    """Default plugin sandbox policy."""

    model_config = ConfigDict(extra="forbid")

    policy_id: str = "default-plugin-sandbox-policy"
    allowed_permissions: list[SandboxPermission] = Field(
        default_factory=lambda: [SandboxPermission.READ_PROJECT_FILES]
    )
    denied_permissions: list[SandboxPermission] = Field(
        default_factory=lambda: [
            SandboxPermission.EXECUTE_CODE,
            SandboxPermission.SHELL_ACCESS,
            SandboxPermission.SECRETS_ACCESS,
            SandboxPermission.REMOTE_WRITE,
        ]
    )
    explicit_permissions: list[SandboxPermission] = Field(
        default_factory=lambda: [
            SandboxPermission.WRITE_PROJECT_FILES,
            SandboxPermission.NETWORK_ACCESS,
            SandboxPermission.LIVE_API_ACCESS,
            SandboxPermission.REMOTE_READ,
            SandboxPermission.ARTIFACT_EXPORT,
        ]
    )
    scoped_permissions: list[SandboxPermission] = Field(
        default_factory=lambda: [SandboxPermission.READ_PROJECT_FILES]
    )
    requires_human_review: bool = True
    implements_os_sandbox: bool = False

    @model_validator(mode="after")
    def policy_is_not_runtime_sandbox(self) -> Self:
        if not self.requires_human_review:
            raise ValueError("plugin sandbox policy requires human review")
        if self.implements_os_sandbox:
            raise ValueError("v0.7 policy layer does not implement an OS sandbox")
        return self


def default_plugin_sandbox_policy() -> PluginSandboxPolicy:
    """Return the default v0.7 plugin sandbox policy."""

    return PluginSandboxPolicy()
