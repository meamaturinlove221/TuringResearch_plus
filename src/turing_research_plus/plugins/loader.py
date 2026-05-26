"""Trusted local plugin manifest loader."""

from __future__ import annotations

from pathlib import Path

from turing_research_plus.extension_safety.models import (
    ExtensionKind,
    ExtensionManifestRef,
    ExtensionPermission,
)
from turing_research_plus.extension_safety.validator import validate_extension_safety
from turing_research_plus.plugins.loading_report import PluginLoadingReport
from turing_research_plus.plugins.local_plugin import ExposedPluginCapability, LocalPlugin
from turing_research_plus.plugins.manifest import (
    load_plugin_manifest,
    load_plugin_manifest_payload,
)
from turing_research_plus.plugins.models import PluginManifest
from turing_research_plus.plugins.trust_policy import (
    PluginTrustDecision,
    PluginTrustSource,
    PluginTrustStatus,
    evaluate_plugin_trust,
)
from turing_research_plus.plugins.validator import validate_plugin_manifest

PERMISSION_MAP = {
    "read_local_files": ExtensionPermission.READ_LOCAL_FILES,
    "write_local_files": ExtensionPermission.WRITE_LOCAL_FILES,
    "network_access": ExtensionPermission.NETWORK_ACCESS,
    "live_api": ExtensionPermission.LIVE_API,
    "remote_read": ExtensionPermission.REMOTE_READ,
    "remote_write": ExtensionPermission.REMOTE_WRITE,
    "execute_code": ExtensionPermission.EXECUTE_CODE,
    "export_artifacts": ExtensionPermission.EXPORT_ARTIFACTS,
    "package_release": ExtensionPermission.PACKAGE_RELEASE,
    "read_demo_fixture": ExtensionPermission.READ_LOCAL_FILES,
    "read_demo_markdown": ExtensionPermission.READ_LOCAL_FILES,
    "write_demo_export_manifest": ExtensionPermission.EXPORT_ARTIFACTS,
}


def load_trusted_local_plugin(
    path: Path,
    *,
    source: PluginTrustSource = PluginTrustSource.WORKSPACE_LOCAL,
    explicit_trusted: bool = False,
    explicit_live: bool = False,
) -> PluginLoadingReport:
    """Load a trusted local plugin manifest as metadata only."""

    raw_payload = load_plugin_manifest_payload(path)
    validation_report = validate_plugin_manifest(raw_payload)
    if not validation_report.valid:
        return PluginLoadingReport(
            plugin_id=validation_report.plugin_id,
            manifest_path=path,
            loaded=False,
            validation_report=validation_report,
            trust_decision=PluginTrustDecision(
                plugin_id=validation_report.plugin_id,
                source=source,
                status=PluginTrustStatus.BLOCKED,
                trusted=False,
                allowed_to_load_manifest=False,
                reasons=["plugin manifest failed validation"],
            ),
            errors=[issue.message for issue in validation_report.issues],
        )

    manifest = load_plugin_manifest(path)
    validation_report = validate_plugin_manifest(manifest)
    trust_decision = evaluate_plugin_trust(
        manifest,
        source=source,
        explicit_trusted=explicit_trusted,
        explicit_live=explicit_live,
    )

    safety_report = None
    warnings: list[str] = []
    errors: list[str] = []
    exposed_capabilities: list[ExposedPluginCapability] = []

    if validation_report.valid:
        safety_report = validate_extension_safety(_manifest_to_extension_ref(manifest))
        if safety_report.findings:
            warnings.extend(finding.message for finding in safety_report.findings)
        if safety_report.release_blocker:
            errors.append("extension safety gate produced a release blocker")
    else:
        errors.extend(issue.message for issue in validation_report.issues)

    if not trust_decision.allowed_to_load_manifest:
        errors.extend(trust_decision.reasons)

    loaded = validation_report.valid and trust_decision.allowed_to_load_manifest
    loaded = loaded and safety_report is not None and not safety_report.release_blocker

    if loaded:
        exposed_capabilities = [
            ExposedPluginCapability.from_capability(capability)
            for capability in manifest.capabilities
        ]
        LocalPlugin(
            manifest=manifest,
            manifest_path=path,
            trust_decision=trust_decision,
            exposed_capabilities=exposed_capabilities,
        )

    return PluginLoadingReport(
        plugin_id=manifest.plugin_id,
        manifest_path=path,
        loaded=loaded,
        validation_report=validation_report,
        trust_decision=trust_decision,
        safety_report=safety_report,
        exposed_capabilities=exposed_capabilities,
        warnings=warnings,
        errors=errors,
    )


def _manifest_to_extension_ref(manifest: PluginManifest) -> ExtensionManifestRef:
    permissions = [_map_permission(permission) for permission in manifest.required_permissions]
    return ExtensionManifestRef(
        extension_id=manifest.plugin_id,
        kind=ExtensionKind.PLUGIN,
        third_party=manifest.third_party,
        default_enabled=False,
        requested_permissions=permissions,
        declared_safety_level=manifest.safety_level.value,
        has_manifest=True,
        has_safety_report=True,
        touches_secrets=_touches_secrets(manifest.required_permissions),
        touches_raw_data=_touches_raw_data(manifest.required_permissions),
    )


def _map_permission(permission: str) -> ExtensionPermission:
    return PERMISSION_MAP.get(permission, ExtensionPermission.READ_LOCAL_FILES)


def _touches_secrets(permissions: list[str]) -> bool:
    return any("secret" in permission for permission in permissions)


def _touches_raw_data(permissions: list[str]) -> bool:
    return any("raw_data" in permission or "raw-data" in permission for permission in permissions)
