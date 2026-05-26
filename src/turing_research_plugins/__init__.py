"""Plugin system public namespace facade."""

from turing_research_plugins.public_api import (
    COMPATIBILITY_NAMESPACE,
    NAMESPACE,
    PUBLIC_MODULE_ALIASES,
    STABILITY,
    CapabilityManifest,
    ExtensionSafetyReport,
    MCPPluginRegistry,
    PluginManifest,
    PluginRegistry,
    load_plugin_manifest,
    validate_plugin_manifest,
)

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
