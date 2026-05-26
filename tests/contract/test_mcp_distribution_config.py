from __future__ import annotations

import json
import re
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_mcp_distribution_package_and_server_names_are_stable() -> None:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    project = pyproject["project"]
    scripts = project["scripts"]
    config = json.loads((ROOT / ".mcp.example.json").read_text(encoding="utf-8"))

    assert project["name"] == "turingresearch-plus"
    assert scripts["turingresearch-plus-mcp"] == "turing_research.mcp_server:main"
    assert "turingresearch-plus" in config["mcpServers"]


def test_mcp_example_config_is_fake_default_and_no_secret() -> None:
    config = json.loads((ROOT / ".mcp.example.json").read_text(encoding="utf-8"))
    server = config["mcpServers"]["turingresearch-plus"]
    env = server["env"]
    text = (ROOT / ".mcp.example.json").read_text(encoding="utf-8")

    assert server["command"] == "turingresearch-plus-mcp"
    assert server["args"] == ["--manifest"]
    assert env["TURINGRESEARCH_MODE"] == "fake"
    assert env["TURINGRESEARCH_ENABLE_LIVE_TESTS"] == "0"
    assert env["TURINGRESEARCH_ENABLE_PLUGINS"] == "0"
    assert env["TURINGRESEARCH_ENABLE_PLUGIN_LIVE_MODE"] == "0"
    assert env["SEMANTIC_SCHOLAR_API_KEY"] == ""
    assert env["APIFY_TOKEN"] == ""
    assert env["OPENAI_API_KEY"] == ""
    assert env["GITHUB_TOKEN"] == ""
    assert not re.search(r"(sk-[A-Za-z0-9_-]{8,}|ghp_[A-Za-z0-9_]{8,})", text)
    assert "Tuling" + "Research" not in text


def test_mcp_distribution_docs_cover_fake_live_and_plugin_boundaries() -> None:
    guide = (ROOT / "docs" / "mcp-distribution-guide.md").read_text(encoding="utf-8")
    examples = (ROOT / "docs" / "mcp-config-examples.md").read_text(encoding="utf-8")
    troubleshooting = (ROOT / "docs" / "mcp-troubleshooting.md").read_text(encoding="utf-8")

    assert "package name: `turingresearch-plus`" in guide
    assert "server name: `turingresearch-plus`" in guide
    assert "Fake/default mode" in guide
    assert "Live mode is optional" in guide
    assert "plugin tools disabled by default" in guide
    assert "TURINGRESEARCH_ENABLE_PLUGINS=0" in examples
    assert "TURINGRESEARCH_ENABLE_PLUGIN_LIVE_MODE=0" in troubleshooting
    assert "does not require API keys" in troubleshooting
