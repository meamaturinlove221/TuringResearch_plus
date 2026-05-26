"""Public API facade for plugin and extension modules."""

from turing_research_plus.capabilities import CapabilityManifest
from turing_research_plus.extension_safety import ExtensionSafetyReport
from turing_research_plus.mcp_plugins import MCPPluginRegistry
from turing_research_plus.plugins import (
    PluginManifest,
    PluginRegistry,
    load_plugin_manifest,
    validate_plugin_manifest,
)

NAMESPACE = "turing_research_plugins"
COMPATIBILITY_NAMESPACE = "turing_research_plus"
STABILITY = "experimental"
PUBLIC_MODULE_ALIASES = {
    "plugins": "turing_research_plus.plugins",
    "mcp_plugins": "turing_research_plus.mcp_plugins",
    "capabilities": "turing_research_plus.capabilities",
    "extension_safety": "turing_research_plus.extension_safety",
    "skill_market": "turing_research_plus.skill_market",
}

__all__ = [
    "COMPATIBILITY_NAMESPACE",
    "NAMESPACE",
    "PUBLIC_MODULE_ALIASES",
    "STABILITY",
    "CapabilityManifest",
    "ExtensionSafetyReport",
    "MCPPluginRegistry",
    "PluginManifest",
    "PluginRegistry",
    "load_plugin_manifest",
    "validate_plugin_manifest",
]
