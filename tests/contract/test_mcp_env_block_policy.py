from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

REQUIRED_ENV = {
    "TURINGRESEARCH_MODE": "fake",
    "TURINGRESEARCH_ENABLE_LIVE_TESTS": "0",
    "TURINGRESEARCH_ENABLE_SEMANTIC_SCHOLAR_LIVE": "0",
    "TURINGRESEARCH_ENABLE_APIFY_LIVE": "0",
    "TURINGRESEARCH_ENABLE_WEB_LIVE": "0",
    "TURINGRESEARCH_ENABLE_PLUGINS": "0",
    "TURINGRESEARCH_ENABLE_PLUGIN_LIVE_MODE": "0",
    "SEMANTIC_SCHOLAR_API_KEY": "",
    "APIFY_TOKEN": "",
    "OPENAI_API_KEY": "",
    "GITHUB_TOKEN": "",
}


def _env() -> dict[str, str]:
    config = json.loads((ROOT / ".mcp.example.json").read_text(encoding="utf-8"))
    return config["mcpServers"]["turingresearch-plus"]["env"]


def test_mcp_env_block_matches_policy_defaults() -> None:
    assert _env() == REQUIRED_ENV


def test_mcp_env_block_policy_docs_match_config() -> None:
    config_text = (ROOT / ".mcp.example.json").read_text(encoding="utf-8")
    policy = (ROOT / "docs" / "mcp-env-block-policy.md").read_text(encoding="utf-8")
    parity = (ROOT / "docs" / "mcp-config-parity.md").read_text(encoding="utf-8")

    for key, value in REQUIRED_ENV.items():
        assert f'"{key}": "{value}"' in config_text
        assert f'"{key}": "{value}"' in policy
        assert f'"{key}": "{value}"' in parity


def test_mcp_config_cookbook_and_troubleshooting_cover_provider_boundaries() -> None:
    text = "\n".join(
        [
            (ROOT / "docs" / "mcp-config-cookbook.md").read_text(encoding="utf-8"),
            (ROOT / "docs" / "mcp-config-troubleshooting.md").read_text(
                encoding="utf-8"
            ),
        ]
    )

    required = [
        "no API key required",
        "TURINGRESEARCH_ENABLE_LIVE_TESTS",
        "TURINGRESEARCH_ENABLE_SEMANTIC_SCHOLAR_LIVE",
        "TURINGRESEARCH_ENABLE_APIFY_LIVE",
        "TURINGRESEARCH_ENABLE_WEB_LIVE",
        "TURINGRESEARCH_ENABLE_PLUGINS",
        "TURINGRESEARCH_ENABLE_PLUGIN_LIVE_MODE",
        "missing-token",
        "must not bypass login",
        "must not fetch private or restricted content",
    ]

    for item in required:
        assert item in text
