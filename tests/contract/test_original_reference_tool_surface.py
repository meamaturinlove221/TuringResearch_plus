from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "contracts" / "original_reference_tool_surface.yaml"

REQUIRED_DOCS = [
    "docs/original-reference-tool-surface-audit.md",
    "docs/" + "neo" + "cortica-tool-surface-matrix.md",
    "docs/yogsoth-tool-surface-matrix.md",
    "docs/missing-tool-surface-actions.md",
]

SESSION_SURFACES = [
    "preflight",
    "context pack",
    "transfer",
    "launch",
    "return manifest",
    "memory policy",
]

SCHOLAR_SURFACES = [
    "paper search",
    "paper content",
    "paper reference",
    "paper reading",
    "cached markdown",
    "fallback policy",
]

WEB_SURFACES = [
    "web_fetching",
    "web_content",
    "Apify optional",
    "cache",
    "source metadata",
]

YOGSOTH_SURFACES = [
    "campaign routing",
    "research catalog",
    "vault",
    "ontology",
    "convergence",
    "stress test",
    "experiment execution",
]


def _read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def test_original_reference_tool_surface_docs_exist() -> None:
    missing = [path for path in REQUIRED_DOCS if not (ROOT / path).exists()]

    assert missing == []


def test_original_reference_tool_surface_contract_covers_required_surfaces() -> None:
    text = CONTRACT.read_text(encoding="utf-8").lower()

    required_terms = [
        "mcp-stdio",
        "local-python",
        "config-docs",
        "policy-only",
        "preflight",
        "context_pack",
        "return_manifest",
        "memory_policy",
        "paper_search",
        "paper_content",
        "paper_reference",
        "paper_reading",
        "cached_markdown",
        "fallback_policy",
        "web_fetching",
        "web_content",
        "apify_optional",
        "source_metadata",
        "campaign_routing",
        "research_catalog",
        "vault",
        "ontology",
        "convergence",
        "stress_test",
        "experiment_execution",
    ]
    for term in required_terms:
        assert term in text


def test_neocortica_tool_surface_matrix_covers_required_entries() -> None:
    matrix = _read("docs/" + "neo" + "cortica-tool-surface-matrix.md")

    for term in [*SESSION_SURFACES, *SCHOLAR_SURFACES, *WEB_SURFACES]:
        assert term in matrix

    assert "run_pod_context_preflight" in matrix
    assert "build_session_context_pack_manifest" in matrix
    assert "build_structured_return_manifest" in matrix
    assert "run_web_fetching_tool" in matrix
    assert "web_content_from_fetch_result" in matrix


def test_yogsoth_tool_surface_matrix_covers_required_entries() -> None:
    matrix = _read("docs/yogsoth-tool-surface-matrix.md")

    for term in YOGSOTH_SURFACES:
        assert term in matrix

    assert "build_campaign_execution_plan" in matrix
    assert "build_wiki_vault_export" in matrix
    assert "run_stress_test" in matrix
    assert "build_experiment_execution_plan" in matrix


def test_tool_surface_audit_preserves_mcp_boundary_and_safety() -> None:
    audit = _read("docs/original-reference-tool-surface-audit.md")
    actions = _read("docs/missing-tool-surface-actions.md")
    combined = f"{audit}\n{actions}"

    required_boundaries = [
        "MCP stdio remains deliberately narrow",
        "broader capability manifest",
        "no default networking",
        "no remote command execution",
        "no automatic experiment execution",
        "no fake/demo result promotion",
    ]
    for boundary in required_boundaries:
        assert boundary in combined

    token_like = re.compile(
        r"(sk-[A-Za-z0-9_-]{8,}|ghp_[A-Za-z0-9_]{8,}|xox[baprs]-[A-Za-z0-9-]+)"
    )
    assert "Tuling" + "Research" not in combined
    assert "D:" + "/vggt" not in combined
    assert "D:\\vggt" not in combined
    assert not token_like.search(combined)
