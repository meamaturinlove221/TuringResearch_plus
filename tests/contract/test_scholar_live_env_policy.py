from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs" / "scholar-live-optional-guide.md"
EXAMPLE = ROOT / "examples" / "scholar_demo" / "live_optional"
MCP = ROOT / ".mcp.example.json"


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_scholar_live_optional_docs_lock_default_fake_mode() -> None:
    text = _text(DOC)

    assert "Scholar live mode is optional" in text
    assert "TURINGRESEARCH_MODE=fake" in text
    assert "TURINGRESEARCH_ENABLE_LIVE_TESTS=0" in text
    assert "TURINGRESEARCH_ENABLE_SEMANTIC_SCHOLAR_LIVE=0" in text
    assert "SEMANTIC_SCHOLAR_API_KEY=" in text
    assert "Fake mode requires no key" in text
    assert "no paper download by default" in text


def test_scholar_live_optional_example_contains_no_key() -> None:
    combined = "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted(EXAMPLE.rglob("*"))
        if path.is_file()
    )

    assert "SEMANTIC_SCHOLAR_API_KEY=" in combined
    assert "SEMANTIC_SCHOLAR_API_KEY=<private local value>" in combined
    assert "sk-" not in combined
    assert "ghp_" not in combined
    assert "D:/vggt" not in combined
    assert "D:\\vggt" not in combined
    assert "local_project_links.yaml" not in combined
    assert "no key in repo" in combined


def test_scholar_live_optional_mcp_env_is_disabled_by_default() -> None:
    text = _text(MCP)

    assert '"TURINGRESEARCH_ENABLE_LIVE_TESTS": "0"' in text
    assert '"TURINGRESEARCH_ENABLE_SEMANTIC_SCHOLAR_LIVE": "0"' in text
    assert '"SEMANTIC_SCHOLAR_API_KEY": ""' in text


def test_scholar_live_optional_policy_has_no_default_download_or_verified_fake() -> None:
    combined = "\n".join([_text(DOC), _text(EXAMPLE / "README.md")])

    assert "no paper download by default" in combined
    assert "no paywall bypass" in combined
    assert "no fake citation verified" in combined
    assert "live output remains review context" in combined
