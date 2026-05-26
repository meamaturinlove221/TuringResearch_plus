from __future__ import annotations

from turing_research_plus.extension_safety.models import (
    ExtensionKind,
    ExtensionManifestRef,
    ExtensionPermission,
    ExtensionSafetyStatus,
)
from turing_research_plus.extension_safety.validator import validate_extension_safety


def test_validate_safe_demo_plugin_stays_disabled_by_default() -> None:
    manifest = ExtensionManifestRef(
        extension_id="demo_plugin",
        kind=ExtensionKind.PLUGIN,
        third_party=True,
        default_enabled=False,
        requested_permissions=[ExtensionPermission.READ_LOCAL_FILES],
        declared_safety_level="public-demo",
        has_manifest=True,
        has_safety_report=True,
    )

    report = validate_extension_safety(manifest)

    assert report.valid is True
    assert report.status == ExtensionSafetyStatus.DISABLED_BY_DEFAULT
    assert report.release_blocker is False
    assert report.executes_extension_code is False
    assert report.loads_third_party_code is False


def test_validate_execute_code_blocks_release() -> None:
    manifest = ExtensionManifestRef(
        extension_id="unsafe_plugin",
        kind=ExtensionKind.PLUGIN,
        third_party=True,
        default_enabled=False,
        requested_permissions=[ExtensionPermission.EXECUTE_CODE],
        declared_safety_level="restricted",
        has_manifest=True,
        has_safety_report=True,
    )

    report = validate_extension_safety(manifest)

    assert report.valid is False
    assert report.status == ExtensionSafetyStatus.FORBIDDEN
    assert report.release_blocker is True
    assert any(
        finding.permission == ExtensionPermission.EXECUTE_CODE
        for finding in report.findings
    )


def test_validate_network_access_requires_review() -> None:
    manifest = ExtensionManifestRef(
        extension_id="live_adapter",
        kind=ExtensionKind.ADAPTER,
        third_party=False,
        default_enabled=False,
        requested_permissions=[
            ExtensionPermission.READ_LOCAL_FILES,
            ExtensionPermission.NETWORK_ACCESS,
            ExtensionPermission.LIVE_API,
        ],
        declared_safety_level="live-optional",
        has_manifest=True,
        has_safety_report=True,
    )

    report = validate_extension_safety(manifest)

    assert report.valid is True
    assert report.status == ExtensionSafetyStatus.RESTRICTED
    assert report.release_blocker is False


def test_validate_secrets_and_raw_data_are_release_blockers() -> None:
    manifest = ExtensionManifestRef(
        extension_id="unsafe_exporter",
        kind=ExtensionKind.PLUGIN,
        third_party=True,
        default_enabled=False,
        requested_permissions=[ExtensionPermission.EXPORT_ARTIFACTS],
        declared_safety_level="restricted",
        has_manifest=True,
        has_safety_report=True,
        touches_secrets=True,
        touches_raw_data=True,
    )

    report = validate_extension_safety(manifest)

    assert report.valid is False
    assert report.release_blocker is True
    assert any("secrets access is forbidden" in finding.message for finding in report.findings)
    assert any("raw data access is restricted" in finding.message for finding in report.findings)
