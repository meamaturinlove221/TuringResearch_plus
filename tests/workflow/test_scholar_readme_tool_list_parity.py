from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def test_scholar_readme_tool_list_docs_cover_full_tool_surface() -> None:
    combined = "\n".join(
        [
            _read("docs/scholar-production-tool-list.md"),
            _read("docs/scholar-pipeline-public-readme-section.md"),
            _read("examples/scholar_demo/TOOL_LIST.md"),
        ]
    )

    for tool in [
        "scholar.paper_searching",
        "scholar.paper_content",
        "scholar.paper_reference",
        "scholar.paper_reading",
    ]:
        assert tool in combined

    for term in [
        "cache-first",
        "cached Markdown",
        "manual fallback",
        "three-pass reading",
        "review-only",
    ]:
        assert term in combined


def test_scholar_mcp_fake_results_match_config_boundary() -> None:
    config = json.loads((ROOT / ".mcp.example.json").read_text(encoding="utf-8"))
    server = config["mcpServers"]["turingresearch-plus"]
    env = server["env"]
    text = _read("docs/scholar-mcp-test-results-fake.md")

    assert env["TURINGRESEARCH_MODE"] == "fake"
    assert env["TURINGRESEARCH_ENABLE_LIVE_TESTS"] == "0"
    assert env["TURINGRESEARCH_ENABLE_SEMANTIC_SCHOLAR_LIVE"] == "0"
    assert "MCP server started | `false`" in text
    assert "API key required | `false`" in text
    assert "6 passed" in text


def test_scholar_readme_tool_list_keeps_safety_boundaries() -> None:
    combined = "\n".join(
        [
            _read("docs/scholar-production-tool-list.md"),
            _read("docs/scholar-pipeline-public-readme-section.md"),
            _read("docs/scholar-mcp-test-results-fake.md"),
            _read("examples/scholar_demo/TOOL_LIST.md"),
        ]
    )

    required = [
        "no automatic full paper download",
        "no paywall bypass",
        "no fake citation is marked as verified",
        "no final paper conclusion",
        "human review required",
    ]
    for item in required:
        assert item in combined

    forbidden = ["D:/vggt", "D:\\vggt", "local_project_links.yaml", "ghp_"]
    for marker in forbidden:
        assert marker not in combined
    assert "sk-" not in combined
    assert "fake citation is verified" not in combined
