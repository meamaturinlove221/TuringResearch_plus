from __future__ import annotations

from pathlib import Path

from turing_research_plus.mcp_plugins.tool_mapping import (
    map_plugin_manifest_to_mcp_entries,
)
from turing_research_plus.plugins.manifest import load_plugin_manifest

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "examples" / "plugins" / "demo_exporter_plugin" / "plugin.yaml"


def test_map_plugin_manifest_to_mcp_entry_is_disabled_by_default() -> None:
    manifest = load_plugin_manifest(FIXTURE)

    entries = map_plugin_manifest_to_mcp_entries(manifest)

    assert len(entries) == 1
    entry = entries[0]
    assert entry.plugin_id == "demo_exporter_plugin"
    assert entry.exposed_tool_name == "mcp.demo_markdown_export"
    assert entry.namespace == "mcp"
    assert entry.default_enabled is False
    assert entry.live_required is False
    assert entry.requires_api_key is False
    assert entry.fake_mode_supported is True
    assert entry.third_party is True


def test_map_plugin_manifest_uses_custom_namespace() -> None:
    manifest = load_plugin_manifest(FIXTURE)

    entries = map_plugin_manifest_to_mcp_entries(manifest, namespace="demo")

    assert entries[0].exposed_tool_name == "demo.demo_markdown_export"
    assert entries[0].namespace == "demo"
