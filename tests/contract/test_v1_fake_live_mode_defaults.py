from __future__ import annotations

import json
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_v1_default_pytest_excludes_live_and_manual_tests() -> None:
    metadata = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    addopts = metadata["tool"]["pytest"]["ini_options"]["addopts"]

    assert "not live" in addopts
    assert "not manual" in addopts


def test_v1_mcp_example_is_fake_default() -> None:
    config = json.loads((ROOT / ".mcp.example.json").read_text(encoding="utf-8"))
    env = config["mcpServers"]["turingresearch-plus"]["env"]

    assert env["TURINGRESEARCH_MODE"] == "fake"
    assert env["TURINGRESEARCH_ENABLE_LIVE_TESTS"] == "0"
    assert env["TURINGRESEARCH_ENABLE_PLUGINS"] == "0"
    assert env["TURINGRESEARCH_ENABLE_PLUGIN_LIVE_MODE"] == "0"


def test_v1_install_and_quickstart_do_not_require_live_keys() -> None:
    text = "\n".join(
        [
            (ROOT / "docs" / "install.md").read_text(encoding="utf-8"),
            (ROOT / "docs" / "quickstart.md").read_text(encoding="utf-8"),
            (ROOT / "docs" / "v1.0.0-fake-live-mode-guide.md").read_text(
                encoding="utf-8"
            ),
        ]
    )

    assert "No real API key is required" in text
    assert "live adapters are optional" in text.lower()
    assert "unknown plugin execution" in text.lower()
