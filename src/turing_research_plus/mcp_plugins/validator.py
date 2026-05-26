"""Validate MCP plugin registry entries without loading plugin code."""

from __future__ import annotations

from turing_research_plus.mcp_plugins.models import (
    MCPPluginRegistry,
    MCPPluginValidationIssue,
    MCPPluginValidationReport,
)

RESERVED_NAMESPACES = {"core"}


def validate_mcp_plugin_registry(registry: MCPPluginRegistry) -> MCPPluginValidationReport:
    """Validate MCP plugin exposure declarations."""

    issues: list[MCPPluginValidationIssue] = []
    seen: set[str] = set()
    for entry in registry.entries:
        if entry.exposed_tool_name in seen:
            issues.append(
                MCPPluginValidationIssue(
                    severity="high",
                    message="duplicate exposed tool name",
                    plugin_id=entry.plugin_id,
                    exposed_tool_name=entry.exposed_tool_name,
                )
            )
        seen.add(entry.exposed_tool_name)

        if entry.namespace in RESERVED_NAMESPACES:
            issues.append(
                MCPPluginValidationIssue(
                    severity="critical",
                    message="plugins cannot override core tool namespace",
                    plugin_id=entry.plugin_id,
                    exposed_tool_name=entry.exposed_tool_name,
                )
            )
        if not entry.permissions:
            issues.append(
                MCPPluginValidationIssue(
                    severity="high",
                    message="permissions are required",
                    plugin_id=entry.plugin_id,
                    exposed_tool_name=entry.exposed_tool_name,
                )
            )
        if entry.third_party and entry.default_enabled:
            issues.append(
                MCPPluginValidationIssue(
                    severity="high",
                    message="third-party plugins must be disabled by default",
                    plugin_id=entry.plugin_id,
                    exposed_tool_name=entry.exposed_tool_name,
                )
            )
        if entry.live_required and entry.default_enabled:
            issues.append(
                MCPPluginValidationIssue(
                    severity="high",
                    message="live-required plugins must be disabled by default",
                    plugin_id=entry.plugin_id,
                    exposed_tool_name=entry.exposed_tool_name,
                )
            )
        if entry.live_required and not entry.requires_api_key:
            issues.append(
                MCPPluginValidationIssue(
                    severity="medium",
                    message="live-required plugin must declare requires_api_key",
                    plugin_id=entry.plugin_id,
                    exposed_tool_name=entry.exposed_tool_name,
                )
            )

    return MCPPluginValidationReport(
        registry_id=registry.registry_id,
        valid=not issues,
        issues=issues,
        checked_tools=len(registry.entries),
        starts_mcp_server=False,
        loads_plugin_code=False,
        requires_human_review=True,
    )
