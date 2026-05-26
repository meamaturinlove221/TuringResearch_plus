from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GATE = ROOT / "docs" / "optional-live-safety-gate.md"
PYPROJECT = ROOT / "pyproject.toml"
MCP = ROOT / ".mcp.example.json"
DOCS = [
    ROOT / "docs" / "optional-live-polish-scope.md",
    ROOT / "docs" / "optional-live-safety-policy.md",
    ROOT / "docs" / "optional-live-test-policy-v1.5.md",
    ROOT / "docs" / "scholar-live-optional-guide.md",
    ROOT / "docs" / "web-apify-live-optional-guide.md",
    ROOT / "docs" / "sftp-live-optional-guide.md",
    GATE,
]


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _mcp_env() -> dict[str, str]:
    config = json.loads(MCP.read_text(encoding="utf-8"))
    return config["mcpServers"]["turingresearch-plus"]["env"]


def test_optional_live_safety_gate_doc_records_required_checks() -> None:
    text = _text(GATE)

    assert "PASS FOR OPTIONAL LIVE POLISH / NO-GO FOR DEFAULT LIVE" in text
    assert "live disabled by default" in text
    assert "env explicit" in text
    assert "no secrets" in text
    assert "no live tests in default suite" in text
    assert "no remote command" in text
    assert "no private scraping" in text
    assert "no old naming" in text


def test_optional_live_mcp_env_defaults_are_disabled() -> None:
    env = _mcp_env()

    assert env["TURINGRESEARCH_MODE"] == "fake"
    assert env["TURINGRESEARCH_ENABLE_LIVE_TESTS"] == "0"
    assert env["TURINGRESEARCH_ENABLE_SEMANTIC_SCHOLAR_LIVE"] == "0"
    assert env["TURINGRESEARCH_ENABLE_WEB_LIVE"] == "0"
    assert env["TURINGRESEARCH_ENABLE_APIFY_LIVE"] == "0"
    assert env["SEMANTIC_SCHOLAR_API_KEY"] == ""
    assert env["APIFY_TOKEN"] == ""


def test_optional_live_default_suite_excludes_live_tests() -> None:
    text = _text(PYPROJECT)

    assert "-m 'not live and not manual'" in text
    assert '"live: tests requiring live network/API credentials; skipped by default"' in text


def test_optional_live_docs_require_explicit_env_and_no_secret_storage() -> None:
    combined = "\n".join(_text(path) for path in DOCS)

    assert "TURINGRESEARCH_ENABLE_LIVE_TESTS=1" in combined
    assert "TURINGRESEARCH_ENABLE_SEMANTIC_SCHOLAR_LIVE=1" in combined
    assert "TURINGRESEARCH_ENABLE_WEB_LIVE=1" in combined
    assert "TURINGRESEARCH_ENABLE_APIFY_LIVE=1" in combined
    assert "TURINGRESEARCH_ENABLE_SFTP_LIVE=1" in combined
    assert "Credentials must never be committed." in combined
    assert "Reports must not log secrets." in combined
    assert "no private scraping" in combined
    assert "no remote command" in combined


def test_optional_live_docs_have_no_secret_or_old_name() -> None:
    combined = "\n".join(_text(path) for path in DOCS)
    old_name = "Tuling" + "Research"

    assert old_name not in combined
    assert "D:/vggt" not in combined
    assert "D:\\vggt" not in combined
    assert "local_project_links.yaml" not in combined
    assert "ghp_" not in combined
    assert "github_pat_" not in combined
    assert "sk-" not in combined
    assert "https://github.com/" not in combined
