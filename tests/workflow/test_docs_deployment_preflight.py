from __future__ import annotations

from pathlib import Path

from turing_research_plus.docs_site.build_report import build_docs_site_hardening_report
from turing_research_plus.docs_site.nav import (
    load_docs_site_manifest,
    load_docs_site_nav,
    validate_nav_against_manifest,
)

ROOT = Path(__file__).resolve().parents[2]
DOCS_SITE = ROOT / "docs-site"
DIST = DOCS_SITE / "dist"
PREFLIGHT_REPORT = DOCS_SITE / "preflight_report.md"
PREFLIGHT_DOC = ROOT / "docs" / "docs-deployment-preflight.md"
BLOCKERS_DOC = ROOT / "docs" / "docs-deployment-blockers.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_docs_deployment_preflight_required_pages_exist() -> None:
    required_pages = [
        "index.md",
        "quickstart.md",
        "original-repo-parity.md",
        "public-demo.md",
        "privacy.md",
    ]
    for page in required_pages:
        assert (DOCS_SITE / "pages" / page).exists()


def test_docs_deployment_preflight_nav_validates() -> None:
    nav = load_docs_site_nav(DOCS_SITE / "nav.yaml")
    manifest = load_docs_site_manifest(DOCS_SITE / "site_manifest.yaml")

    assert validate_nav_against_manifest(nav, manifest) == []
    assert [item.item_id for item in nav.items] == manifest.required_sections


def test_docs_deployment_preflight_has_no_blockers() -> None:
    report = build_docs_site_hardening_report(ROOT, output_root=DIST)

    assert report.status == "pass_with_warnings"
    assert report.link_report.missing_pages == []
    assert report.link_report.broken_links == []
    assert report.link_report.missing_source_docs == []
    assert report.link_report.private_path_hits == []
    assert len(report.link_report.orphan_pages) == 16
    assert report.deployment_performed is False


def test_docs_deployment_preflight_reports_record_decision() -> None:
    combined = "\n".join(
        [
            _read(PREFLIGHT_DOC),
            _read(BLOCKERS_DOC),
            _read(PREFLIGHT_REPORT),
            _read(DOCS_SITE / "deployment_dry_run_report.md"),
            _read(ROOT / "docs" / "docs-deployment-strategy.md"),
            _read(ROOT / "docs" / "github-pages-deployment-plan.md"),
        ]
    )

    required = [
        "PASS WITH REVIEW WARNINGS",
        "Deployment performed: `false`",
        "Public URL: `none`",
        "nav.yaml",
        "index page exists",
        "quickstart page exists",
        "original parity page exists",
        "public demo page exists",
        "security/privacy page exists",
        "broken links",
        "orphan pages",
        "private paths",
        "secrets",
        "raw data",
        "fake deployment URL",
        "no public deployment",
    ]
    for term in required:
        assert term in combined


def test_docs_deployment_preflight_contains_no_sensitive_material() -> None:
    paths = [
        PREFLIGHT_DOC,
        BLOCKERS_DOC,
        PREFLIGHT_REPORT,
        DOCS_SITE / "nav.yaml",
        DOCS_SITE / "site_manifest.yaml",
        *[path for path in (DOCS_SITE / "pages").glob("*.md")],
        *[path for path in DIST.rglob("*") if path.is_file()],
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in paths)

    forbidden = [
        "D:" + "/vggt",
        "D:" + "\\vggt",
        "local_project_links" + ".yaml",
        "ghp_",
        "github_pat_",
        "sk-",
        "BEGIN OPENSSH PRIVATE KEY",
        "SMPL-X",
        "status" + ": observed",
        "deployed at",
        "live URL:",
    ]
    for marker in forbidden:
        assert marker not in combined

    assert "Tuling" + "Research" not in combined
