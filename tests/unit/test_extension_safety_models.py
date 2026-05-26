from __future__ import annotations

import pytest

from turing_research_plus.extension_safety.models import (
    ExtensionKind,
    ExtensionManifestRef,
    ExtensionPermission,
    ExtensionSafetyReport,
    ExtensionSafetyStatus,
)


def test_extension_manifest_ref_records_required_fields() -> None:
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

    assert manifest.extension_id == "demo_plugin"
    assert manifest.kind == ExtensionKind.PLUGIN
    assert manifest.third_party is True
    assert manifest.default_enabled is False


def test_extension_manifest_requires_permissions() -> None:
    with pytest.raises(ValueError, match="requested permissions"):
        ExtensionManifestRef(
            extension_id="demo_plugin",
            kind=ExtensionKind.PLUGIN,
            requested_permissions=[],
            declared_safety_level="public-demo",
        )


def test_third_party_extension_cannot_default_enable() -> None:
    with pytest.raises(ValueError, match="disabled by default"):
        ExtensionManifestRef(
            extension_id="demo_plugin",
            kind=ExtensionKind.PLUGIN,
            third_party=True,
            default_enabled=True,
            requested_permissions=[ExtensionPermission.READ_LOCAL_FILES],
            declared_safety_level="public-demo",
        )


def test_extension_safety_report_is_validation_only() -> None:
    with pytest.raises(ValueError, match="must not execute"):
        ExtensionSafetyReport(
            extension_id="demo_plugin",
            kind=ExtensionKind.PLUGIN,
            valid=True,
            status=ExtensionSafetyStatus.ALLOW_WITH_REVIEW,
            executes_extension_code=True,
        )
