from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def test_scholar_web_parity_gate_required_docs_exist() -> None:
    required = [
        "docs/scholar-full-tool-surface.md",
        "docs/scholar-fake-live-walkthrough.md",
        "docs/web-full-tool-surface.md",
        "docs/apify-workflow-templates.md",
        "docs/mcp-tool-parity-v1.3.md",
        "docs/mcp-tool-surface-v1.3.md",
        "docs/scholar-web-parity-gate-report.md",
        "docs/scholar-web-parity-go-no-go.md",
    ]

    for path in required:
        assert (ROOT / path).exists(), path


def test_scholar_web_parity_gate_covers_required_tool_surfaces() -> None:
    combined = "\n".join(
        [
            _read("docs/scholar-full-tool-surface.md"),
            _read("docs/web-full-tool-surface.md"),
            _read("docs/mcp-tool-surface-v1.3.md"),
        ]
    )

    required_tools = [
        "scholar.paper_searching",
        "scholar.paper_content",
        "scholar.paper_reference",
        "scholar.paper_reading",
        "web.web_fetching",
        "web.web_content",
        "web.cache",
        "web.source_metadata",
        "web.apify_optional",
    ]

    for tool in required_tools:
        assert tool in combined


def test_scholar_web_parity_gate_keeps_live_optional() -> None:
    config = json.loads((ROOT / ".mcp.example.json").read_text(encoding="utf-8"))
    server = config["mcpServers"]["turingresearch-plus"]
    env = server["env"]
    surface = server["tool_surface_v1_3"]

    assert env["TURINGRESEARCH_MODE"] == "fake"
    assert env["TURINGRESEARCH_ENABLE_LIVE_TESTS"] == "0"
    assert env["TURINGRESEARCH_ENABLE_SEMANTIC_SCHOLAR_LIVE"] == "0"
    assert env["TURINGRESEARCH_ENABLE_WEB_LIVE"] == "0"
    assert env["TURINGRESEARCH_ENABLE_APIFY_LIVE"] == "0"
    assert surface["status"] == "documentation-contract-only"
    assert surface["starts_mcp_server"] is False
    assert all(tool["mcp_enabled_by_default"] is False for tool in surface["tools"])


def test_scholar_web_parity_gate_apify_templates_are_disabled_by_default() -> None:
    templates = [
        ROOT / "examples" / "apify_workflows" / "project_page_fetch.yaml",
        ROOT / "examples" / "apify_workflows" / "search_result_fetch.yaml",
        ROOT / "examples" / "apify_workflows" / "content_extract.yaml",
    ]

    for template in templates:
        text = template.read_text(encoding="utf-8")
        assert "live_enabled: false" in text
        assert "requires_token: false" in text
        assert "login_bypass: false" in text
        assert "private_content_scraping: false" in text
        assert "automatic_evidence_promotion: false" in text


def test_scholar_web_parity_gate_has_no_secrets_or_private_paths() -> None:
    combined = "\n".join(
        [
            _read("docs/scholar-full-tool-surface.md"),
            _read("docs/scholar-fake-live-walkthrough.md"),
            _read("docs/web-full-tool-surface.md"),
            _read("docs/apify-workflow-templates.md"),
            _read("docs/mcp-tool-parity-v1.3.md"),
            _read("docs/scholar-web-parity-gate-report.md"),
            _read("docs/scholar-web-parity-go-no-go.md"),
            (ROOT / ".mcp.example.json").read_text(encoding="utf-8"),
        ]
    )

    token_like = re.compile(
        r"(sk-[A-Za-z0-9_-]{8,}|ghp_[A-Za-z0-9_]{8,}|xox[baprs]-[A-Za-z0-9-]+)"
    )
    assert not token_like.search(combined)
    assert "Tuling" + "Research" not in combined
    assert "D:" + "/vggt" not in combined
    assert "local_project_links.yaml" not in combined


def test_scholar_web_parity_gate_blocks_unsupported_paper_claims() -> None:
    combined = "\n".join(
        [
            _read("docs/scholar-full-tool-surface.md"),
            _read("docs/scholar-fake-live-walkthrough.md"),
            _read("docs/web-full-tool-surface.md"),
            _read("docs/scholar-web-parity-gate-report.md"),
            _read("docs/scholar-web-parity-go-no-go.md"),
        ]
    ).lower()

    required_boundaries = [
        "no automatic full paper download",
        "no paywall bypass",
        "no final paper conclusion",
        "no fake citation is marked as verified",
        "review-only",
    ]

    for boundary in required_boundaries:
        assert boundary in combined
    assert "fake citation is verified" not in combined
    assert "camera-ready paper text" in combined
