"""Map plugin manifests to MCP plugin entries."""

from __future__ import annotations

from turing_research_plus.mcp_plugins.models import MCPPluginEntry
from turing_research_plus.plugins.models import PluginManifest


def map_plugin_manifest_to_mcp_entries(
    manifest: PluginManifest,
    *,
    namespace: str = "mcp",
) -> list[MCPPluginEntry]:
    """Create MCP tool declarations from manifest capabilities."""

    entries: list[MCPPluginEntry] = []
    for capability in manifest.capabilities:
        tool_leaf = capability.capability_id.replace("-", "_")
        entries.append(
            MCPPluginEntry(
                plugin_id=manifest.plugin_id,
                exposed_tool_name=f"{namespace}.{tool_leaf}",
                namespace=namespace,
                input_schema=capability.inputs[0] if capability.inputs else "PluginInput",
                output_schema=capability.outputs[0] if capability.outputs else "PluginOutput",
                permissions=manifest.required_permissions,
                safety_level=manifest.safety_level,
                default_enabled=False,
                live_required=capability.live_mode,
                requires_api_key=capability.live_mode,
                fake_mode_supported=capability.fake_mode,
                third_party=manifest.third_party,
                docs=[],
                tests=[],
            )
        )
    return entries
