from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def test_v1_4_docs_polish_files_exist() -> None:
    required = [
        "README.md",
        "docs/original-repo-production-parity-summary.md",
        "docs/aris-still-deferred-v1.4.md",
        "docs/v1.4.0-docs-polish-report.md",
        "docs/original-repo-parity-dashboard-v2.md",
    ]

    for path in required:
        assert (ROOT / path).exists(), path


def test_readme_explains_v1_4_original_repo_production_parity() -> None:
    readme = _read("README.md")

    required = [
        "v1.4 Original Repo Production Parity",
        "Neocortica Session",
        "Neocortica Scholar",
        "Neocortica Web",
        "yogsoth-ai",
        "ARIS",
        "no default network",
        "no remote command execution",
        "Fake / Live Boundary",
        "Privacy-first",
        "docs/original-repo-production-parity-summary.md",
        "docs/original-repo-parity-dashboard-v2.md",
    ]
    for term in required:
        assert term in readme

    lower = readme.lower()
    assert "production parity" in lower
    assert "fake/default" in lower
    assert "future reference only" in lower


def test_v1_4_summary_and_aris_page_preserve_deferred_boundaries() -> None:
    summary = _read("docs/original-repo-production-parity-summary.md")
    aris = _read("docs/aris-still-deferred-v1.4.md")
    combined = summary + "\n" + aris

    required = [
        "Neocortica Session",
        "Neocortica Scholar",
        "Neocortica Web",
        "yogsoth-ai",
        "ARIS runtime",
        "Cross-model review",
        "Proof-checker",
        "Meta-optimize",
        "Paper-claim-audit",
        "no automatic experiment execution",
        "no automatic Evidence Ledger mutation",
        "no fake/demo result promotion",
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


def test_v1_4_docs_polish_public_safety() -> None:
    paths = [
        "README.md",
        "docs/original-repo-production-parity-summary.md",
        "docs/aris-still-deferred-v1.4.md",
        "docs/v1.4.0-docs-polish-report.md",
    ]
    combined = "\n".join(_read(path) for path in paths)

    forbidden = [
        "D:" + "/vggt",
        "D:" + "\\vggt",
        "local_project_links" + ".yaml",
        "ghp_",
        "sk-",
        '"status": "' + 'observed"',
    ]
    for marker in forbidden:
        assert marker not in combined

    assert "Tuling" + "Research" not in combined
    assert "not proof that any VGGT experiment succeeded" in combined
    assert "does not claim VGGT or SparseConv3D experiment success" in combined
