from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs" / "web-apify-live-optional-guide.md"
EXAMPLE = ROOT / "examples" / "apify_workflows" / "live_optional"
MCP = ROOT / ".mcp.example.json"


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_apify_live_optional_docs_lock_default_fake_mode() -> None:
    text = _text(DOC)

    assert "Web and Apify live mode is optional" in text
    assert "TURINGRESEARCH_MODE=fake" in text
    assert "TURINGRESEARCH_ENABLE_LIVE_TESTS=0" in text
    assert "TURINGRESEARCH_ENABLE_WEB_LIVE=0" in text
    assert "TURINGRESEARCH_ENABLE_APIFY_LIVE=0" in text
    assert "APIFY_TOKEN=" in text
    assert "`APIFY_TOKEN` is optional" in text


def test_apify_live_optional_example_contains_no_token() -> None:
    combined = "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted(EXAMPLE.rglob("*"))
        if path.is_file()
    )

    assert "APIFY_TOKEN=" in combined
    assert "APIFY_TOKEN=<private local value>" in combined
    assert "sk-" not in combined
    assert "ghp_" not in combined
    assert "D:/vggt" not in combined
    assert "D:\\vggt" not in combined
    assert "local_project_links.yaml" not in combined
    assert "no token in repo" in combined


def test_apify_live_optional_mcp_env_is_disabled_by_default() -> None:
    text = _text(MCP)

    assert '"TURINGRESEARCH_ENABLE_LIVE_TESTS": "0"' in text
    assert '"TURINGRESEARCH_ENABLE_WEB_LIVE": "0"' in text
    assert '"TURINGRESEARCH_ENABLE_APIFY_LIVE": "0"' in text
    assert '"APIFY_TOKEN": ""' in text


def test_apify_live_optional_policy_blocks_private_scraping_and_login_bypass() -> None:
    combined = "\n".join([_text(DOC), _text(EXAMPLE / "README.md")])

    assert "no private scraping" in combined
    assert "no login bypass" in combined
    assert "no paywall bypass" in combined
    assert "no cookie storage" in combined
    assert "live output remains review context" in combined
