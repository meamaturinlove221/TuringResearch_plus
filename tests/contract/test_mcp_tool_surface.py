from __future__ import annotations

import re
from pathlib import Path

from turing_research.tool_registry import MCP_SERVER_NAME, list_mcp_tools
from turing_research_plus.capabilities.collector import collect_capability_manifest

ROOT = Path(__file__).resolve().parents[2]
TOOL_ROW = re.compile(r"\| `(?P<tool>[a-z_]+\.[a-z0-9_]+)` \| `(?P<status>[^`]+)` \|")


def documented_mcp_tool_surface() -> dict[str, str]:
    text = (ROOT / "docs" / "mcp-tool-surface.md").read_text(encoding="utf-8")
    return {match.group("tool"): match.group("status") for match in TOOL_ROW.finditer(text)}


def test_mcp_tool_surface_matches_stdio_registry() -> None:
    registry_tools = {tool.name: tool.implementation_status for tool in list_mcp_tools()}

    assert MCP_SERVER_NAME == "turingresearch-plus"
    assert documented_mcp_tool_surface() == registry_tools


def test_mcp_tool_surface_docs_explain_capability_manifest_boundary() -> None:
    text = (ROOT / "docs" / "mcp-tool-surface.md").read_text(encoding="utf-8")
    capability_manifest = collect_capability_manifest()
    capability_tool_names = {
        capability.tool_name
        for capability in capability_manifest.capabilities
        if capability.tool_name
    }

    assert capability_tool_names
    assert set(documented_mcp_tool_surface()) != capability_tool_names
    assert "broader" in text
    assert "capability manifest" in text
    assert "local capability catalog" in text
    assert "Only the tools listed above" in text
    assert "Plugin tools are disabled by default" in text


def test_mcp_tool_surface_has_no_prior_naming() -> None:
    text = "\n".join(
        [
            (ROOT / "docs" / "mcp-tool-surface.md").read_text(encoding="utf-8"),
            (ROOT / "docs" / "mcp-distribution-guide.md").read_text(encoding="utf-8"),
            (ROOT / "docs" / "mcp-config-examples.md").read_text(encoding="utf-8"),
        ]
    )

    assert "Tuling" + "Research" not in text
