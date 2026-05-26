from __future__ import annotations

import pytest

from turing_research_plus.mcp_plugins.models import MCPPluginEntry, MCPPluginRegistry
from turing_research_plus.plugins.models import PluginSafetyLevel


def test_mcp_plugin_entry_records_required_registry_fields() -> None:
    entry = MCPPluginEntry(
        plugin_id="demo",
        exposed_tool_name="mcp.demo",
        namespace="mcp",
        input_schema="Input",
        output_schema="Output",
        permissions=["read_demo"],
        safety_level=PluginSafetyLevel.PUBLIC_DEMO,
        default_enabled=False,
        live_required=False,
        requires_api_key=False,
        fake_mode_supported=True,
    )

    assert entry.plugin_id == "demo"
    assert entry.exposed_tool_name == "mcp.demo"
    assert entry.namespace == "mcp"
    assert entry.permissions == ["read_demo"]
    assert entry.safety_level == PluginSafetyLevel.PUBLIC_DEMO
    assert entry.default_enabled is False
    assert entry.live_required is False
    assert entry.requires_api_key is False
    assert entry.fake_mode_supported is True


def test_mcp_plugin_entry_requires_matching_namespace() -> None:
    with pytest.raises(ValueError, match="namespace must match"):
        MCPPluginEntry(
            plugin_id="demo",
            exposed_tool_name="mcp.demo",
            namespace="wrong",
            input_schema="Input",
            output_schema="Output",
            permissions=["read_demo"],
            safety_level=PluginSafetyLevel.PUBLIC_DEMO,
        )


def test_mcp_plugin_entry_blocks_core_override() -> None:
    with pytest.raises(ValueError, match="cannot override core"):
        MCPPluginEntry(
            plugin_id="demo",
            exposed_tool_name="core.health_check",
            namespace="core",
            input_schema="Input",
            output_schema="Output",
            permissions=["read_demo"],
            safety_level=PluginSafetyLevel.PUBLIC_DEMO,
        )


def test_mcp_plugin_entry_requires_permissions() -> None:
    with pytest.raises(ValueError, match="declare permissions"):
        MCPPluginEntry(
            plugin_id="demo",
            exposed_tool_name="mcp.demo",
            namespace="mcp",
            input_schema="Input",
            output_schema="Output",
            permissions=[],
            safety_level=PluginSafetyLevel.PUBLIC_DEMO,
        )


def test_mcp_plugin_registry_requires_unique_tools() -> None:
    entry = MCPPluginEntry(
        plugin_id="demo",
        exposed_tool_name="mcp.demo",
        namespace="mcp",
        input_schema="Input",
        output_schema="Output",
        permissions=["read_demo"],
        safety_level=PluginSafetyLevel.PUBLIC_DEMO,
    )

    with pytest.raises(ValueError, match="unique"):
        MCPPluginRegistry(registry_id="demo", entries=[entry, entry])
