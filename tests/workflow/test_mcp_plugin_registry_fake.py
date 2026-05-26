from __future__ import annotations

from pathlib import Path

from turing_research_plus.mcp_plugins.tools import (
    mcp_plugin_registry_check,
    mcp_plugin_registry_load,
    mcp_plugin_registry_markdown,
)

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "examples" / "plugins" / "demo_mcp_plugin" / "registry.yaml"


def test_mcp_plugin_registry_fake_is_manifest_only() -> None:
    registry = mcp_plugin_registry_load(FIXTURE)
    report = mcp_plugin_registry_check(FIXTURE)
    markdown = mcp_plugin_registry_markdown(FIXTURE)

    assert len(registry.entries) == 1
    assert registry.entries[0].namespace == "mcp"
    assert registry.entries[0].default_enabled is False
    assert registry.entries[0].live_required is False
    assert registry.entries[0].requires_api_key is False
    assert registry.entries[0].fake_mode_supported is True
    assert report.valid is True
    assert report.starts_mcp_server is False
    assert report.loads_plugin_code is False
    assert "mcp.demo_export" in markdown
    assert "Plugin code is not loaded" in markdown
