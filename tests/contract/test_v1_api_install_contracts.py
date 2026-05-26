from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

ROUND_181_DOCS = [
    ROOT / "docs" / "v1.0.0-api-install-integration-report.md",
    ROOT / "docs" / "v1.0.0-api-install-known-limitations.md",
    ROOT / "lanes" / "162_v1_api_install_integration.md",
]

REQUIRED_UPSTREAM_REPORTS = [
    ROOT / "docs" / "v1.0.0-final-scope.md",
    ROOT / "docs" / "v1.0.0-public-api.md",
    ROOT / "docs" / "v1.0.0-namespace-compatibility-report.md",
    ROOT / "docs" / "v1.0.0-cli-mcp-sanity.md",
    ROOT / "docs" / "v1.0.0-quickstart.md",
    ROOT / "docs" / "v1.0.0-demo-refresh-report.md",
    ROOT / "docs" / "v1.0.0-benchmark-refresh-report.md",
]


def _combined_round_text() -> str:
    return "\n".join(path.read_text(encoding="utf-8") for path in ROUND_181_DOCS)


def test_v1_api_install_gate_docs_exist() -> None:
    missing = [
        str(path.relative_to(ROOT))
        for path in [*ROUND_181_DOCS, *REQUIRED_UPSTREAM_REPORTS]
        if not path.exists()
    ]

    assert missing == []


def test_v1_api_install_report_covers_round_175_to_180_surfaces() -> None:
    text = (ROOT / "docs" / "v1.0.0-api-install-integration-report.md").read_text(
        encoding="utf-8"
    )
    required_terms = [
        "v1.0 scope",
        "public API freeze",
        "namespace compatibility",
        "CLI/MCP sanity",
        "public quickstart",
        "demo/benchmark refresh",
        "turing_research_plus",
        "turing_research_core",
        "turingresearch-plus",
        "v1_public_demo_replay",
    ]

    for term in required_terms:
        assert term in text


def test_v1_api_install_known_limitations_preserve_honest_boundaries() -> None:
    text = (
        ROOT / "docs" / "v1.0.0-api-install-known-limitations.md"
    ).read_text(encoding="utf-8")
    lowered = text.lower()
    required_terms = [
        "no saas",
        "no automatic experiment execution",
        "no automatic final paper",
        "live adapters",
        "unknown plugin",
        "human review",
        "fake/demo",
    ]

    for term in required_terms:
        assert term in lowered


def test_v1_api_install_docs_and_config_have_no_real_secrets_or_private_paths() -> None:
    text = _combined_round_text()
    text += "\n" + (ROOT / ".mcp.example.json").read_text(encoding="utf-8")
    config = json.loads((ROOT / ".mcp.example.json").read_text(encoding="utf-8"))
    env = config["mcpServers"]["turingresearch-plus"]["env"]

    forbidden = [
        "D:" + "/vggt",
        "D:\\vggt",
        "local_project_links" + ".yaml",
        "SMPLX" + "_",
        "Tuling" + "Research",
    ]
    token_like = re.compile(
        r"(sk-[A-Za-z0-9_-]{8,}|ghp_[A-Za-z0-9_]{8,}|xox[baprs]-[A-Za-z0-9-]+)"
    )

    for item in forbidden:
        assert item not in text
    assert not token_like.search(text)
    assert env["SEMANTIC_SCHOLAR_API_KEY"] == ""
    assert env["APIFY_TOKEN"] == ""
    assert env["OPENAI_API_KEY"] == ""
    assert env["GITHUB_TOKEN"] == ""


def test_v1_api_install_gate_keeps_fake_and_live_boundaries_explicit() -> None:
    text = _combined_round_text()
    lowered = text.lower()

    assert "fake" in lowered
    assert "live mode" in lowered or "live adapters" in lowered
    assert "explicit opt-in" in lowered or "opt-in" in lowered
    assert "plugin tools disabled by default" in lowered
    assert "no observed fake result" in lowered
