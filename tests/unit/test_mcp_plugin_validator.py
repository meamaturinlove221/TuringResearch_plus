from __future__ import annotations

import pytest
from pydantic import ValidationError

from turing_research_plus.mcp_plugins.models import MCPPluginEntry, MCPPluginRegistry
from turing_research_plus.mcp_plugins.validator import validate_mcp_plugin_registry
from turing_research_plus.plugins.models import PluginSafetyLevel


def test_mcp_plugin_validator_accepts_demo_disabled_registry() -> None:
    entry = MCPPluginEntry(
        plugin_id="demo",
        exposed_tool_name="mcp.demo",
        namespace="mcp",
        input_schema="Input",
        output_schema="Output",
        permissions=["read_demo"],
        safety_level=PluginSafetyLevel.PUBLIC_DEMO,
        default_enabled=False,
    )
    report = validate_mcp_plugin_registry(MCPPluginRegistry(registry_id="demo", entries=[entry]))

    assert report.valid is True
    assert report.starts_mcp_server is False
    assert report.loads_plugin_code is False


def test_mcp_plugin_model_blocks_live_required_default_enabled() -> None:
    with pytest.raises(ValidationError, match="live-required"):
        MCPPluginEntry(
            plugin_id="live_demo",
            exposed_tool_name="mcp.live_demo",
            namespace="mcp",
            input_schema="Input",
            output_schema="Output",
            permissions=["network"],
            safety_level=PluginSafetyLevel.LIVE_OPTIONAL,
            default_enabled=True,
            live_required=True,
            requires_api_key=True,
            fake_mode_supported=False,
            third_party=False,
        )


def test_mcp_plugin_model_blocks_live_required_fake_mode_claim() -> None:
    with pytest.raises(ValidationError, match="fake mode"):
        MCPPluginEntry(
            plugin_id="live_demo",
            exposed_tool_name="mcp.live_demo",
            namespace="mcp",
            input_schema="Input",
            output_schema="Output",
            permissions=["network"],
            safety_level=PluginSafetyLevel.LIVE_OPTIONAL,
            live_required=True,
            requires_api_key=True,
            fake_mode_supported=True,
        )
