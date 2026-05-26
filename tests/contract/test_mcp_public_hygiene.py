from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MCP = ROOT / ".mcp.example.json"
README = ROOT / "README.md"
DOCS = [
    ROOT / "docs" / "mcp-public-config-guide.md",
    ROOT / "docs" / "env-block-public-hygiene.md",
    ROOT / "docs" / "no-dotenv-public-policy.md",
    ROOT / "docs" / "mcp-config-parity.md",
    ROOT / "docs" / "mcp-env-block-policy.md",
    ROOT / "docs" / "optional-live-safety-policy.md",
]


def _config() -> dict[str, object]:
    return json.loads(MCP.read_text(encoding="utf-8"))


def _env() -> dict[str, str]:
    return _config()["mcpServers"]["turingresearch-plus"]["env"]  # type: ignore[index]


def test_mcp_public_template_is_fake_default_and_disabled_live() -> None:
    env = _env()

    assert env["TURINGRESEARCH_MODE"] == "fake"
    assert env["TURINGRESEARCH_ENABLE_LIVE_TESTS"] == "0"
    assert env["TURINGRESEARCH_ENABLE_SEMANTIC_SCHOLAR_LIVE"] == "0"
    assert env["TURINGRESEARCH_ENABLE_WEB_LIVE"] == "0"
    assert env["TURINGRESEARCH_ENABLE_APIFY_LIVE"] == "0"
    assert env["TURINGRESEARCH_ENABLE_SFTP_LIVE"] == "0"
    assert env["TURINGRESEARCH_ENABLE_PLUGINS"] == "0"
    assert env["TURINGRESEARCH_ENABLE_PLUGIN_LIVE_MODE"] == "0"


def test_mcp_public_template_uses_blank_credential_placeholders() -> None:
    env = _env()
    credential_keys = [
        "SEMANTIC_SCHOLAR_API_KEY",
        "APIFY_TOKEN",
        "OPENAI_API_KEY",
        "GITHUB_TOKEN",
        "TURINGRESEARCH_SFTP_CREDENTIAL",
        "TURINGRESEARCH_SFTP_KEY_PATH",
        "TURINGRESEARCH_SFTP_TARGET",
    ]

    for key in credential_keys:
        assert key in env
        assert env[key] == ""


def test_mcp_public_template_documents_disabled_capabilities() -> None:
    server = _config()["mcpServers"]["turingresearch-plus"]  # type: ignore[index]
    capabilities = server["capabilities"]
    notes = "\n".join(server["notes"])

    assert capabilities["semantic_scholar"] == "optional-live-disabled-by-default"
    assert capabilities["web_fetch"] == "optional-live-disabled-by-default"
    assert capabilities["apify"] == "optional-live-disabled-by-default"
    assert capabilities["sftp"] == "optional-live-disabled-by-default"
    assert capabilities["plugins"] == "disabled-by-default"
    assert "never in this example file" in notes


def test_readme_explains_fake_default_and_explicit_live_env() -> None:
    text = README.read_text(encoding="utf-8")

    assert "TuringResearch is fake/demo-first by default" in text
    assert "Live adapters are optional and disabled by default" in text
    assert "TURINGRESEARCH_ENABLE_LIVE_TESTS=0" in text
    assert "TURINGRESEARCH_ENABLE_SFTP_LIVE=0" in text
    assert "explicit private" in text


def test_mcp_public_hygiene_docs_exist_and_align_with_config() -> None:
    combined = "\n".join(path.read_text(encoding="utf-8") for path in DOCS)

    for key, value in _env().items():
        if value == "":
            assert f"{key}" in combined
        else:
            assert f"{key}" in combined

    assert "Do not commit `.env`" in combined
    assert "Live mode requires explicit private env" in combined
