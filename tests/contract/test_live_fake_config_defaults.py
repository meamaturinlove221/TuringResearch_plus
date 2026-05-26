from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_live_fake_docs_explain_fake_default_and_live_opt_in() -> None:
    docs = "\n".join(
        [
            (ROOT / "docs" / "mcp-config-polish-v1.0.md").read_text(encoding="utf-8"),
            (ROOT / "docs" / "mcp-env-block-policy.md").read_text(encoding="utf-8"),
            (ROOT / "docs" / "live-fake-config-examples.md").read_text(encoding="utf-8"),
        ]
    ).lower()

    assert "fake/default" in docs
    assert "live mode is opt-in" in docs
    assert "turingresearch_enable_live_tests=1" in docs
    assert "plugin tools disabled by default" in docs


def test_config_examples_do_not_contain_real_keys() -> None:
    text = "\n".join(
        [
            (ROOT / ".mcp.example.json").read_text(encoding="utf-8"),
            (ROOT / "docs" / "live-fake-config-examples.md").read_text(encoding="utf-8"),
        ]
    )
    config = json.loads((ROOT / ".mcp.example.json").read_text(encoding="utf-8"))
    env = config["mcpServers"]["turingresearch-plus"]["env"]

    assert "sk-" not in text
    assert "ghp_" not in text
    assert all(value == "0" or value == "fake" or value == "" for value in env.values())
