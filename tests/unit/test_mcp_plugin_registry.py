from __future__ import annotations

from pathlib import Path

from turing_research_plus.mcp_plugins.markdown_export import (
    render_mcp_plugin_registry_markdown,
)
from turing_research_plus.mcp_plugins.registry import load_mcp_plugin_registry

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "examples" / "plugins" / "demo_mcp_plugin" / "registry.yaml"


def test_load_mcp_plugin_registry_fixture() -> None:
    registry = load_mcp_plugin_registry(FIXTURE)

    assert registry.registry_id == "demo_mcp_plugin_registry"
    assert len(registry.entries) == 1
    assert registry.entries[0].exposed_tool_name == "mcp.demo_export"
    assert registry.entries[0].default_enabled is False
    assert registry.entries[0].requires_api_key is False
    assert registry.disabled_tools == ["mcp.demo_export"]


def test_mcp_plugin_registry_markdown_states_no_runtime_loading() -> None:
    registry = load_mcp_plugin_registry(FIXTURE)
    markdown = render_mcp_plugin_registry_markdown(registry)

    assert "Registry validation does not start the MCP server" in markdown
    assert "Plugin code is not loaded" in markdown
    assert "mcp.demo_export" in markdown
