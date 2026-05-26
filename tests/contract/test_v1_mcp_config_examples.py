from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _mcp_config() -> dict[str, object]:
    return json.loads((ROOT / ".mcp.example.json").read_text(encoding="utf-8"))


def test_v1_mcp_example_names_server_and_command() -> None:
    config = _mcp_config()
    servers = config["mcpServers"]
    assert isinstance(servers, dict)
    server = servers["turingresearch-plus"]

    assert server["command"] == "turingresearch-plus-mcp"
    assert server["args"] == ["--manifest"]


def test_v1_mcp_example_config_has_no_real_secret_values() -> None:
    text = (ROOT / ".mcp.example.json").read_text(encoding="utf-8")
    server = _mcp_config()["mcpServers"]["turingresearch-plus"]
    env = server["env"]

    assert env["SEMANTIC_SCHOLAR_API_KEY"] == ""
    assert env["APIFY_TOKEN"] == ""
    assert env["OPENAI_API_KEY"] == ""
    assert env["GITHUB_TOKEN"] == ""
    assert not re.search(r"(sk-[A-Za-z0-9_-]{8,}|ghp_[A-Za-z0-9_]{8,})", text)
    assert "Tuling" + "Research" not in text


def test_v1_mcp_docs_explain_fake_live_and_plugin_boundaries() -> None:
    docs = [
        ROOT / "docs" / "mcp-server-reference.md",
        ROOT / "docs" / "mcp-distribution-guide.md",
        ROOT / "docs" / "mcp-config-examples.md",
        ROOT / "docs" / "v1.0.0-install-sanity-report.md",
        ROOT / "docs" / "v1.0.0-fake-live-mode-guide.md",
    ]
    text = "\n".join(path.read_text(encoding="utf-8") for path in docs)

    assert "server name: `turingresearch-plus`" in text
    assert "TURINGRESEARCH_ENABLE_PLUGINS=0" in text
    assert "TURINGRESEARCH_ENABLE_PLUGIN_LIVE_MODE=0" in text
    assert "live mode is opt-in" in text.lower() or "live mode is optional" in text.lower()
    assert "no real API key" in text or "No real API key" in text
