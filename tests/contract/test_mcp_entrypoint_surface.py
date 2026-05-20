from __future__ import annotations

import importlib
import json
import socket
import sys

import pytest

MINIMAL_TOOLS = {
    "core.health_check",
    "core.paper_content",
    "core.web_content",
    "core.session_list",
    "pdf.inspect",
    "pdf.to_markdown",
    "pdf.markdown_content",
}


def test_mcp_server_import_does_not_start_network_or_write_stdio(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    def blocked_socket(*args: object, **kwargs: object) -> socket.socket:
        raise AssertionError("mcp_server import attempted network access")

    monkeypatch.setattr(socket, "socket", blocked_socket)
    sys.modules.pop("tuling_research.mcp_server", None)

    module = importlib.import_module("tuling_research.mcp_server")
    captured = capsys.readouterr()

    assert module.MCP_SERVER_NAME == "tulingresearch-plus"
    assert callable(module.main)
    assert captured.out == ""
    assert captured.err == ""


def test_tool_registry_surface_is_testable() -> None:
    registry = importlib.import_module("tuling_research.tool_registry")

    tools = registry.list_mcp_tools()
    tool_names = {tool.name for tool in tools}

    assert registry.MCP_SERVER_NAME == "tulingresearch-plus"
    assert MINIMAL_TOOLS <= tool_names
    assert registry.get_tool_descriptor("core.health_check") is not None


def test_health_check_can_dry_run_through_mcp_entrypoint() -> None:
    mcp_server = importlib.import_module("tuling_research.mcp_server")

    direct = mcp_server.core_health_check()
    dispatched = mcp_server.dry_run_tool("core.health_check")

    assert direct["status"] == "ok"
    assert dispatched["status"] == "ok"
    assert "core.health_check" in dispatched["tools"]


def test_manifest_and_health_check_cli_payloads_are_explicit(
    capsys: pytest.CaptureFixture[str],
) -> None:
    mcp_server = importlib.import_module("tuling_research.mcp_server")

    manifest_result = mcp_server.main(["--manifest"])
    manifest_capture = capsys.readouterr()
    health_result = mcp_server.main(["--health-check"])
    health_capture = capsys.readouterr()

    manifest = json.loads(manifest_capture.out)
    health = json.loads(health_capture.out)

    assert manifest_result == 0
    assert health_result == 0
    assert manifest_capture.err == ""
    assert health_capture.err == ""
    assert manifest["server_name"] == "tulingresearch-plus"
    assert manifest["transport"] == "stdio"
    assert MINIMAL_TOOLS <= {tool["name"] for tool in manifest["tools"]}
    assert health["status"] == "ok"
    assert health["package"] == "tuling_research"
