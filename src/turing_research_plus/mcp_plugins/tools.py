"""Local helper wrappers for MCP plugin registries."""

from __future__ import annotations

from pathlib import Path

from turing_research_plus.mcp_plugins.markdown_export import (
    render_mcp_plugin_registry_markdown,
)
from turing_research_plus.mcp_plugins.models import (
    MCPPluginRegistry,
    MCPPluginValidationReport,
)
from turing_research_plus.mcp_plugins.registry import load_mcp_plugin_registry
from turing_research_plus.mcp_plugins.validator import validate_mcp_plugin_registry


def mcp_plugin_registry_load(path: Path) -> MCPPluginRegistry:
    """Load an MCP plugin registry manifest without starting MCP."""

    return load_mcp_plugin_registry(path)


def mcp_plugin_registry_check(path: Path) -> MCPPluginValidationReport:
    """Validate an MCP plugin registry manifest."""

    return validate_mcp_plugin_registry(mcp_plugin_registry_load(path))


def mcp_plugin_registry_markdown(path: Path) -> str:
    """Render an MCP plugin registry manifest as Markdown."""

    return render_mcp_plugin_registry_markdown(mcp_plugin_registry_load(path))
