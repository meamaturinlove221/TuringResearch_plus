"""Models for extension safety gates."""

from __future__ import annotations

from enum import StrEnum
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ExtensionKind(StrEnum):
    """Extension surfaces covered by the safety gate."""

    PLUGIN = "plugin"
    MCP_PLUGIN = "mcp_plugin"
    SKILL = "skill"
    ADAPTER = "adapter"


class ExtensionPermission(StrEnum):
    """Permission types an extension may request."""

    READ_LOCAL_FILES = "read_local_files"
    WRITE_LOCAL_FILES = "write_local_files"
    NETWORK_ACCESS = "network_access"
    LIVE_API = "live_api"
    REMOTE_READ = "remote_read"
    REMOTE_WRITE = "remote_write"
    EXECUTE_CODE = "execute_code"
    EXPORT_ARTIFACTS = "export_artifacts"
    PACKAGE_RELEASE = "package_release"


class ExtensionRiskLevel(StrEnum):
    """Safety risk levels."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ExtensionSafetyStatus(StrEnum):
    """Validation status values."""

    ALLOW_WITH_REVIEW = "allow-with-review"
    DISABLED_BY_DEFAULT = "disabled-by-default"
    RESTRICTED = "restricted"
    FORBIDDEN = "forbidden"


class ExtensionManifestRef(BaseModel):
    """Minimal extension manifest reference used by the safety gate."""

    model_config = ConfigDict(extra="forbid")

    extension_id: str = Field(pattern=r"^[a-z0-9][a-z0-9_.-]*$")
    kind: ExtensionKind
    third_party: bool = True
    default_enabled: bool = False
    requested_permissions: list[ExtensionPermission] = Field(default_factory=list)
    declared_safety_level: str = Field(min_length=1)
    has_manifest: bool = True
    has_safety_report: bool = False
    touches_secrets: bool = False
    touches_raw_data: bool = False
    notes: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def manifest_ref_is_explicit(self) -> Self:
        if not self.requested_permissions:
            raise ValueError("extensions must declare requested permissions")
        if self.third_party and self.default_enabled:
            raise ValueError("third-party extensions must be disabled by default")
        return self


class PermissionDecision(BaseModel):
    """Policy decision for one requested permission."""

    model_config = ConfigDict(extra="forbid")

    permission: ExtensionPermission
    allowed: bool
    status: ExtensionSafetyStatus
    risk_level: ExtensionRiskLevel
    reason: str = Field(min_length=1)


class ExtensionSafetyFinding(BaseModel):
    """One validation finding."""

    model_config = ConfigDict(extra="forbid")

    severity: ExtensionRiskLevel
    message: str = Field(min_length=1)
    permission: ExtensionPermission | None = None
    release_blocker: bool = False


class ExtensionSafetyReport(BaseModel):
    """Safety report for one extension manifest."""

    model_config = ConfigDict(extra="forbid")

    extension_id: str = Field(min_length=1)
    kind: ExtensionKind
    valid: bool
    status: ExtensionSafetyStatus
    decisions: list[PermissionDecision] = Field(default_factory=list)
    findings: list[ExtensionSafetyFinding] = Field(default_factory=list)
    release_blocker: bool = False
    requires_human_review: bool = True
    executes_extension_code: bool = False
    loads_third_party_code: bool = False

    @model_validator(mode="after")
    def report_is_validation_only(self) -> Self:
        if not self.requires_human_review:
            raise ValueError("extension safety reports require human review")
        if self.executes_extension_code or self.loads_third_party_code:
            raise ValueError("extension safety gate must not execute or load extension code")
        return self
