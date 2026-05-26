"""Markdown export for plugin registries."""

from __future__ import annotations

from turing_research_plus.plugins.models import PluginRegistry


def render_plugin_registry_markdown(registry: PluginRegistry) -> str:
    """Render a plugin registry as Markdown."""

    lines = [
        f"# Plugin Registry: {registry.registry_id}",
        "",
        f"- Plugin count: `{len(registry.plugins)}`",
        f"- Requires human review: `{str(registry.requires_human_review).lower()}`",
        "",
        "| Plugin | Type | Status | Safety | Permissions |",
        "| --- | --- | --- | --- | --- |",
    ]
    for plugin in registry.plugins:
        permissions = ", ".join(plugin.required_permissions) or "none"
        lines.append(
            f"| `{plugin.plugin_id}` | `{plugin.type}` | `{plugin.status}` | "
            f"`{plugin.safety_level}` | {permissions} |"
        )

    lines.extend(["", "## Disabled Plugins", ""])
    lines.extend([f"- `{plugin_id}`" for plugin_id in registry.disabled_plugins] or ["- none"])
    lines.extend(["", "## Warnings", ""])
    lines.extend([f"- {warning}" for warning in registry.warnings] or ["- none"])
    lines.extend(
        [
            "",
            "## Safety Boundary",
            "",
            "- Registry loading validates manifests only.",
            "- Plugin code is not executed.",
            "- Unknown Python entrypoints are not loaded.",
            "- Third-party plugins remain disabled by default.",
            "",
        ]
    )
    return "\n".join(lines)
