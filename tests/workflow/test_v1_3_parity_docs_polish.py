from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def test_v1_3_parity_docs_polish_files_exist() -> None:
    required = [
        "README.md",
        "docs/reference-parity-dashboard.md",
        "docs/original-reference-parity-summary.md",
        "docs/aris-still-deferred-v1.3.md",
        "docs/v1.3.0-docs-polish-report.md",
    ]

    for path in required:
        assert (ROOT / path).exists(), path


def test_readme_explains_v1_3_original_reference_parity() -> None:
    readme = _read("README.md")
    lower = readme.lower()

    required = [
        "v1.3 Original Reference Parity",
        "Neocortica Session parity",
        "Neocortica Scholar parity",
        "Neocortica Web parity",
        "yogsoth parity",
        "ARIS",
        "no automatic remote execution",
        "Fake / Live Boundary",
        "Privacy-first",
    ]
    for term in required:
        assert term in readme

    assert "aris | deferred and reference-only" in lower
    assert "no cross-model review" in lower
    assert "no default network" in lower


def test_reference_parity_dashboard_is_updated_for_v1_3() -> None:
    dashboard = _read("docs/reference-parity-dashboard.md")

    required = [
        "Status: v1.3 public review dashboard.",
        "Neocortica Session parity",
        "Neocortica Scholar parity",
        "Neocortica Web parity",
        "MCP / Skill parity",
        "Campaign trace",
        "Research Catalog dashboard",
        "Convergence decision report",
        "ARIS remains deferred from v1.3 implementation",
        "examples/public_demo/v1_3_original_parity_demo/",
    ]
    for term in required:
        assert term in dashboard


def test_original_reference_summary_and_aris_page_preserve_boundaries() -> None:
    summary = _read("docs/original-reference-parity-summary.md")
    aris = _read("docs/aris-still-deferred-v1.3.md")
    combined = summary + "\n" + aris

    required = [
        "fake/default runtime parity",
        "fake/default tool surface parity",
        "documentation-contract parity",
        "review surface parity",
        "ARIS cross-model review",
        "ARIS proof-checker",
        "ARIS meta-optimize",
        "ARIS paper-claim-audit",
        "not v1.3 implementation",
        "requires design and safety review",
    ]
    for term in required:
        assert term in combined

    forbidden_claims = [
        "ARIS is implemented",
        "cross-model review is enabled",
        "proof-checker is available",
        "meta-optimize is available",
        "paper-claim audit is available",
    ]
    for claim in forbidden_claims:
        assert claim not in combined


def test_v1_3_parity_docs_polish_public_safety() -> None:
    paths = [
        "README.md",
        "docs/reference-parity-dashboard.md",
        "docs/original-reference-parity-summary.md",
        "docs/aris-still-deferred-v1.3.md",
        "docs/v1.3.0-docs-polish-report.md",
    ]
    combined = "\n".join(_read(path) for path in paths)

    forbidden = ["D:/vggt", "D:\\vggt", "local_project_links.yaml", "ghp_", "sk-"]
    for marker in forbidden:
        assert marker not in combined

    assert "Tuling" + "Research" not in combined
    assert "does not claim VGGT experiment success or SparseConv3D success" in combined
    assert "observed " + "success" not in combined.lower()
