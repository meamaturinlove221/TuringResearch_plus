from __future__ import annotations

import json
from pathlib import Path

from turing_research.mcp_server import build_stdio_manifest, core_health_check

ROOT = Path(__file__).resolve().parents[2]


def test_mcp_manifest_exposes_stdio_server_without_live_requirements() -> None:
    manifest = build_stdio_manifest()

    assert manifest["server_name"] == "turingresearch-plus"
    assert manifest["package"] == "turing_research"
    assert manifest["transport"] == "stdio"
    assert "core.health_check" in {tool["name"] for tool in manifest["tools"]}


def test_mcp_health_check_is_fake_default_safe() -> None:
    health = core_health_check()

    assert health["status"] == "ok"
    assert health["package"] == "turing_research"
    assert "core.health_check" in health["tools"]


def test_mcp_example_json_has_no_real_key_and_disables_live_tests() -> None:
    config = json.loads((ROOT / ".mcp.example.json").read_text(encoding="utf-8"))
    server = config["mcpServers"]["turingresearch-plus"]

    assert server["command"] == "turingresearch-plus-mcp"
    assert server["args"] == ["--manifest"]
    assert server["env"]["TURINGRESEARCH_ENABLE_LIVE_TESTS"] == "0"
    assert server["env"]["SEMANTIC_SCHOLAR_API_KEY"] == ""
    assert server["env"]["APIFY_TOKEN"] == ""
    assert server["env"]["OPENAI_API_KEY"] == ""
    assert server["env"]["GITHUB_TOKEN"] == ""


def test_mcp_server_reference_documents_stdio_boundary() -> None:
    text = (ROOT / "docs" / "mcp-server-reference.md").read_text(encoding="utf-8")

    assert "server name: `turingresearch-plus`" in text
    assert "transport target: STDIO" in text
    assert "Live adapters are opt-in" in text
    assert "not automatically promoted to public MCP APIs" in text
