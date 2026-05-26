from __future__ import annotations

from pathlib import Path

from turing_research_plus.capabilities.collector import collect_capability_manifest
from turing_research_plus.extension_safety.models import (
    ExtensionKind,
    ExtensionManifestRef,
    ExtensionPermission,
    ExtensionSafetyStatus,
)
from turing_research_plus.extension_safety.validator import validate_extension_safety
from turing_research_plus.mcp_plugins.registry import load_mcp_plugin_registry
from turing_research_plus.mcp_plugins.validator import validate_mcp_plugin_registry
from turing_research_plus.plugins.registry import load_plugin_registry
from turing_research_plus.skill_market.catalog import (
    build_skill_marketplace_index,
    review_skill_marketplace,
)

ROOT = Path(__file__).resolve().parents[2]


def test_v0_6_plugin_system_fake_end_to_end_chain() -> None:
    plugin_registry = load_plugin_registry(ROOT / "examples" / "plugins")
    mcp_registry = load_mcp_plugin_registry(
        ROOT / "examples" / "plugins" / "demo_mcp_plugin" / "registry.yaml"
    )
    mcp_report = validate_mcp_plugin_registry(mcp_registry)
    capability_manifest = collect_capability_manifest()
    skill_market = build_skill_marketplace_index(ROOT / ".agents" / "skills")
    skill_report = review_skill_marketplace(skill_market, ROOT / ".agents" / "skills")
    extension_manifest = ExtensionManifestRef(
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
    extension_report = validate_extension_safety(extension_manifest)

    assert len(plugin_registry.plugins) >= 2
    assert plugin_registry.requires_human_review is True
    assert all(plugin.status == "disabled" for plugin in plugin_registry.plugins)
    assert mcp_report.valid is True
    assert mcp_report.starts_mcp_server is False
    assert mcp_report.loads_plugin_code is False
    assert mcp_registry.disabled_tools == ["mcp.demo_export"]
    assert "plugin" in {category.value for category in capability_manifest.categories}
    assert "workspace" in {category.value for category in capability_manifest.categories}
    assert capability_manifest.starts_mcp_server is False
    assert capability_manifest.executes_tools is False
    assert skill_report.valid is True
    assert skill_market.remote_publish is False
    assert extension_report.valid is True
    assert extension_report.status == ExtensionSafetyStatus.RESTRICTED
    assert extension_report.executes_extension_code is False
    assert extension_report.loads_third_party_code is False


def test_v0_6_plugin_system_blocks_core_tool_override() -> None:
    mcp_registry = load_mcp_plugin_registry(
        ROOT / "examples" / "plugins" / "demo_mcp_plugin" / "registry.yaml"
    )

    assert all(not entry.exposed_tool_name.startswith("core.") for entry in mcp_registry.entries)
    assert all(entry.namespace != "core" for entry in mcp_registry.entries)
