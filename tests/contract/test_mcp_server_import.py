from __future__ import annotations

import importlib
import sys


def test_mcp_server_import_is_side_effect_safe(capsys) -> None:
    sys.modules.pop("tuling_research.mcp_server", None)

    module = importlib.import_module("tuling_research.mcp_server")
    captured = capsys.readouterr()

    assert module.MCP_SERVER_NAME == "tulingresearch-plus"
    assert hasattr(module, "main")
    assert captured.out == ""
    assert captured.err == ""


def test_mcp_server_health_check_dry_run() -> None:
    from tuling_research.mcp_server import core_health_check

    result = core_health_check()

    assert result["status"] == "ok"
    assert result["package"] == "tuling_research"
    assert "core.health_check" in result["tools"]
