"""Trust policy for local plugin manifest loading."""

from __future__ import annotations

from enum import StrEnum
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from turing_research_plus.plugins.models import PluginManifest


class PluginTrustSource(StrEnum):
    """Where a plugin manifest comes from."""

    BUILT_IN_DEMO = "built-in-demo"
    WORKSPACE_LOCAL = "workspace-local"
    THIRD_PARTY = "third-party"


class PluginTrustStatus(StrEnum):
    """Trust policy decision status."""

    ALLOWED = "allowed"
    REQUIRES_LIVE_FLAG = "requires-live-flag"
    DISABLED_BY_DEFAULT = "disabled-by-default"
    BLOCKED = "blocked"


class PluginTrustDecision(BaseModel):
    """Trust policy decision for a plugin manifest."""

    model_config = ConfigDict(extra="forbid")

    plugin_id: str = Field(min_length=1)
    source: PluginTrustSource
    status: PluginTrustStatus
    trusted: bool = False
    allowed_to_load_manifest: bool = False
    expose_capabilities_disabled: bool = True
    reasons: list[str] = Field(default_factory=list)
    requires_human_review: bool = True

    @model_validator(mode="after")
    def decision_is_reviewed_and_safe(self) -> Self:
        if not self.requires_human_review:
            raise ValueError("plugin trust decisions require human review")
        if not self.expose_capabilities_disabled:
            raise ValueError("trusted local loading exposes capabilities disabled by default")
        if self.status == PluginTrustStatus.ALLOWED and not self.allowed_to_load_manifest:
            raise ValueError("allowed trust decision must allow manifest loading")
        return self


def evaluate_plugin_trust(
    manifest: PluginManifest,
    *,
    source: PluginTrustSource,
    explicit_trusted: bool = False,
    explicit_live: bool = False,
) -> PluginTrustDecision:
    """Evaluate whether a local plugin manifest may be loaded as metadata."""

    reasons: list[str] = []
    requested = set(manifest.required_permissions)

    if manifest.executes_code or "execute_code" in requested:
        return _blocked(manifest, source, "execute_code permission is blocked")
    if manifest.python_entrypoint:
        return _blocked(manifest, source, "dynamic Python entrypoints are blocked")
    if "secrets_access" in requested or "read_secrets" in requested:
        return _blocked(manifest, source, "secrets access is forbidden")
    if "remote_write" in requested:
        return _blocked(manifest, source, "remote_write permission is blocked")

    if "network_access" in requested or "live_api" in requested:
        if not explicit_live:
            return PluginTrustDecision(
                plugin_id=manifest.plugin_id,
                source=source,
                status=PluginTrustStatus.REQUIRES_LIVE_FLAG,
                trusted=False,
                allowed_to_load_manifest=False,
                reasons=["network_access or live_api requires explicit live flag"],
            )
        reasons.append("network_access allowed only because explicit live flag is set")

    if source == PluginTrustSource.BUILT_IN_DEMO:
        reasons.append("built-in demo plugin is allowed as manifest metadata")
        return PluginTrustDecision(
            plugin_id=manifest.plugin_id,
            source=source,
            status=PluginTrustStatus.ALLOWED,
            trusted=True,
            allowed_to_load_manifest=True,
            reasons=reasons,
        )

    if source == PluginTrustSource.WORKSPACE_LOCAL:
        if explicit_trusted:
            reasons.append("workspace-local plugin has explicit trusted flag")
            return PluginTrustDecision(
                plugin_id=manifest.plugin_id,
                source=source,
                status=PluginTrustStatus.ALLOWED,
                trusted=True,
                allowed_to_load_manifest=True,
                reasons=reasons,
            )
        return PluginTrustDecision(
            plugin_id=manifest.plugin_id,
            source=source,
            status=PluginTrustStatus.DISABLED_BY_DEFAULT,
            trusted=False,
            allowed_to_load_manifest=False,
            reasons=["workspace-local plugin requires explicit trusted flag"],
        )

    return PluginTrustDecision(
        plugin_id=manifest.plugin_id,
        source=source,
        status=PluginTrustStatus.DISABLED_BY_DEFAULT,
        trusted=False,
        allowed_to_load_manifest=False,
        reasons=["third-party plugin is disabled by default"],
    )


def _blocked(
    manifest: PluginManifest,
    source: PluginTrustSource,
    reason: str,
) -> PluginTrustDecision:
    return PluginTrustDecision(
        plugin_id=manifest.plugin_id,
        source=source,
        status=PluginTrustStatus.BLOCKED,
        trusted=False,
        allowed_to_load_manifest=False,
        reasons=[reason],
    )
