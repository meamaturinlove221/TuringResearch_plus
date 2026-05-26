"""Markdown export for MCP plugin registries."""

from __future__ import annotations

from turing_research_plus.mcp_plugins.models import MCPPluginRegistry
from turing_research_plus.mcp_plugins.validator import validate_mcp_plugin_registry


def render_mcp_plugin_registry_markdown(registry: MCPPluginRegistry) -> str:
    """Render a registry as Markdown."""

    report = validate_mcp_plugin_registry(registry)
    lines = [
        f"# MCP Plugin Registry: {registry.registry_id}",
        "",
        f"- Tools: `{len(registry.entries)}`",
        f"- Validation valid: `{str(report.valid).lower()}`",
        f"- Requires human review: `{str(registry.requires_human_review).lower()}`",
        "",
        "| Tool | Plugin | Namespace | Enabled | Live | API key | Fake mode |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for entry in registry.entries:
        lines.append(
            f"| `{entry.exposed_tool_name}` | `{entry.plugin_id}` | `{entry.namespace}` | "
            f"`{str(entry.default_enabled).lower()}` | "
            f"`{str(entry.live_required).lower()}` | "
            f"`{str(entry.requires_api_key).lower()}` | "
            f"`{str(entry.fake_mode_supported).lower()}` |"
        )

    lines.extend(["", "## Disabled Tools", ""])
    lines.extend([f"- `{tool}`" for tool in registry.disabled_tools] or ["- none"])
    lines.extend(["", "## Validation Issues", ""])
    if report.issues:
        for issue in report.issues:
            lines.append(
                f"- `{issue.severity}` `{issue.exposed_tool_name}`: {issue.message}"
            )
    else:
        lines.append("- none")

    lines.extend(
        [
            "",
            "## Safety Boundary",
            "",
            "- Registry validation does not start the MCP server.",
            "- Plugin code is not loaded.",
            "- Third-party tools default to disabled.",
            "- Live-required tools default to disabled.",
            "",
        ]
    )
    return "\n".join(lines)
