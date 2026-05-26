from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def load_config() -> dict[str, object]:
    return json.loads((ROOT / ".mcp.example.json").read_text(encoding="utf-8"))


def test_mcp_example_uses_turingresearch_plus_server_and_env_block() -> None:
    config = load_config()
    servers = config["mcpServers"]
    server = servers["turingresearch-plus"]

    assert server["command"] == "turingresearch-plus-mcp"
    assert server["args"] == ["--manifest"]
    assert isinstance(server["env"], dict)


def test_mcp_example_has_no_real_credentials() -> None:
    server = load_config()["mcpServers"]["turingresearch-plus"]
    env = server["env"]

    for key in ["SEMANTIC_SCHOLAR_API_KEY", "APIFY_TOKEN", "OPENAI_API_KEY", "GITHUB_TOKEN"]:
        assert env[key] == ""


def test_mcp_example_disables_live_adapters_and_plugins_by_default() -> None:
    server = load_config()["mcpServers"]["turingresearch-plus"]
    env = server["env"]

    assert env["TURINGRESEARCH_MODE"] == "fake"
    assert env["TURINGRESEARCH_ENABLE_LIVE_TESTS"] == "0"
    assert env["TURINGRESEARCH_ENABLE_SEMANTIC_SCHOLAR_LIVE"] == "0"
    assert env["TURINGRESEARCH_ENABLE_APIFY_LIVE"] == "0"
    assert env["TURINGRESEARCH_ENABLE_WEB_LIVE"] == "0"
    assert env["TURINGRESEARCH_ENABLE_PLUGINS"] == "0"
    assert env["TURINGRESEARCH_ENABLE_PLUGIN_LIVE_MODE"] == "0"
