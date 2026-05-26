from __future__ import annotations

import re
from pathlib import Path

from turing_research.mcp_server import build_stdio_manifest, dry_run_tool, list_registered_tools
from turing_research.tool_registry import MCP_SERVER_NAME, get_tool_descriptor, list_mcp_tools

ROOT = Path(__file__).resolve().parents[2]
MINIMAL_TOOLS = {
    "core.health_check",
    "core.paper_content",
    "core.web_content",
    "core.session_list",
    "pdf.inspect",
    "pdf.to_markdown",
    "pdf.markdown_content",
}


def test_mcp_server_name_and_minimal_tools_are_registered() -> None:
    tools = {tool.name: tool for tool in list_mcp_tools()}

    assert MCP_SERVER_NAME == "turingresearch-plus"
    assert MINIMAL_TOOLS <= set(tools)
    for tool_name in MINIMAL_TOOLS:
        descriptor = tools[tool_name]
        assert descriptor.implementation_status == "implemented_minimal"
        assert descriptor.dry_run_supported is True


def test_registry_lookup_and_manifest_are_serializable() -> None:
    descriptor = get_tool_descriptor("core.health_check")
    manifest = build_stdio_manifest()

    assert descriptor is not None
    assert descriptor.name == "core.health_check"
    assert manifest["server_name"] == "turingresearch-plus"
    assert {tool["name"] for tool in manifest["tools"]} == {
        tool["name"] for tool in list_registered_tools()
    }


def test_core_health_check_can_dry_run_through_registry_dispatch() -> None:
    result = dry_run_tool("core.health_check")

    assert result["status"] == "ok"
    assert {
        "core.health_check",
        "core.paper_content",
        "core.web_content",
        "core.session_list",
    } <= set(result["tools"])


def test_mcp_docs_mark_all_tools_with_status() -> None:
    content = (ROOT / "docs" / "mcp-tools.md").read_text(encoding="utf-8")
    tool_rows = re.findall(
        r"\| `([a-z_]+\.[a-z0-9_]+)` \| `[^`]+` \| `[^`]+` \| `([^`]+)` \|",
        content,
    )

    assert tool_rows
    for _tool_name, status in tool_rows:
        assert status in {"implemented_minimal", "implemented_dry_run", "contract_only", "blocked"}
