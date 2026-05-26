from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / ".mcp.example.json"


def _config() -> dict[str, object]:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def _server() -> dict[str, object]:
    return _config()["mcpServers"]["turingresearch-plus"]  # type: ignore[index]


def test_mcp_config_parity_keeps_stable_server_shape() -> None:
    config = _config()
    server = _server()

    assert config["schema_version"] == "1.2-mcp-config-parity"
    assert config["status"] == "public-safe-template"
    assert server["command"] == "turingresearch-plus-mcp"
    assert server["args"] == ["--manifest"]
    assert isinstance(server["env"], dict)
    assert isinstance(server["notes"], list)
    assert isinstance(server["capabilities"], dict)


def test_mcp_config_parity_keeps_fake_mode_default_and_live_opt_in() -> None:
    env = _server()["env"]

    assert env["TURINGRESEARCH_MODE"] == "fake"
    assert env["TURINGRESEARCH_ENABLE_LIVE_TESTS"] == "0"
    assert env["TURINGRESEARCH_ENABLE_SEMANTIC_SCHOLAR_LIVE"] == "0"
    assert env["TURINGRESEARCH_ENABLE_APIFY_LIVE"] == "0"
    assert env["TURINGRESEARCH_ENABLE_WEB_LIVE"] == "0"
    assert env["TURINGRESEARCH_ENABLE_SFTP_LIVE"] == "0"


def test_mcp_config_parity_keeps_optional_providers_and_plugins_disabled() -> None:
    server = _server()
    env = server["env"]
    capabilities = server["capabilities"]

    assert capabilities["semantic_scholar"] == "optional-live-disabled-by-default"
    assert capabilities["apify"] == "optional-live-disabled-by-default"
    assert capabilities["web_fetch"] == "optional-live-disabled-by-default"
    assert capabilities["sftp"] == "optional-live-disabled-by-default"
    assert capabilities["plugins"] == "disabled-by-default"
    assert env["TURINGRESEARCH_ENABLE_PLUGINS"] == "0"
    assert env["TURINGRESEARCH_ENABLE_PLUGIN_LIVE_MODE"] == "0"


def test_mcp_config_parity_has_no_real_key_or_old_name() -> None:
    text = CONFIG_PATH.read_text(encoding="utf-8")
    env = _server()["env"]

    for key in [
        "SEMANTIC_SCHOLAR_API_KEY",
        "APIFY_TOKEN",
        "OPENAI_API_KEY",
        "GITHUB_TOKEN",
        "TURINGRESEARCH_SFTP_CREDENTIAL",
        "TURINGRESEARCH_SFTP_KEY_PATH",
        "TURINGRESEARCH_SFTP_TARGET",
    ]:
        assert env[key] == ""

    token_like = re.compile(
        r"(sk-[A-Za-z0-9_-]{8,}|ghp_[A-Za-z0-9_]{8,}|xox[baprs]-[A-Za-z0-9-]+)"
    )
    assert not token_like.search(text)
    assert "Tuling" + "Research" not in text
    assert "D:" + "/vggt" not in text
