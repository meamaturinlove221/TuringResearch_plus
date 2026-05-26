from __future__ import annotations

from turing_research_plus.extension_safety.models import (
    ExtensionKind,
    ExtensionManifestRef,
    ExtensionPermission,
    ExtensionSafetyStatus,
)
from turing_research_plus.extension_safety.tools import (
    extension_safety_check,
    extension_safety_markdown,
)


def test_extension_safety_fake_plugin_and_mcp_plugin_flow() -> None:
    plugin = ExtensionManifestRef(
        extension_id="demo_exporter_plugin",
        kind=ExtensionKind.PLUGIN,
        third_party=True,
        default_enabled=False,
        requested_permissions=[
            ExtensionPermission.READ_LOCAL_FILES,
            ExtensionPermission.EXPORT_ARTIFACTS,
        ],
        declared_safety_level="public-demo",
        has_manifest=True,
        has_safety_report=True,
    )
    mcp_plugin = ExtensionManifestRef(
        extension_id="demo_mcp_plugin",
        kind=ExtensionKind.MCP_PLUGIN,
        third_party=True,
        default_enabled=False,
        requested_permissions=[ExtensionPermission.READ_LOCAL_FILES],
        declared_safety_level="public-demo",
        has_manifest=True,
        has_safety_report=True,
    )

    plugin_report = extension_safety_check(plugin)
    mcp_report = extension_safety_check(mcp_plugin)
    markdown = extension_safety_markdown(mcp_plugin)

    assert plugin_report.valid is True
    assert plugin_report.status == ExtensionSafetyStatus.RESTRICTED
    assert mcp_report.valid is True
    assert mcp_report.status == ExtensionSafetyStatus.DISABLED_BY_DEFAULT
    assert plugin_report.executes_extension_code is False
    assert mcp_report.loads_third_party_code is False
    assert "does not execute extension code" in markdown


def test_extension_safety_blocks_fake_unsafe_adapter() -> None:
    adapter = ExtensionManifestRef(
        extension_id="unsafe_live_adapter",
        kind=ExtensionKind.ADAPTER,
        third_party=True,
        default_enabled=False,
        requested_permissions=[
            ExtensionPermission.NETWORK_ACCESS,
            ExtensionPermission.REMOTE_WRITE,
        ],
        declared_safety_level="restricted",
        has_manifest=True,
        has_safety_report=True,
    )

    report = extension_safety_check(adapter)

    assert report.valid is False
    assert report.status == ExtensionSafetyStatus.FORBIDDEN
    assert report.release_blocker is True
    assert any(
        finding.permission == ExtensionPermission.REMOTE_WRITE
        for finding in report.findings
    )
