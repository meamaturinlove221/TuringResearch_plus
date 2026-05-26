from __future__ import annotations

import hashlib
import re
from pathlib import Path

from turing_research_plus.docs_site.build_report import build_docs_site_hardening_report
from turing_research_plus.docs_site.nav import (
    load_docs_site_manifest,
    load_docs_site_nav,
    validate_nav_against_manifest,
)

ROOT = Path(__file__).resolve().parents[2]
DIST = ROOT / "docs-site" / "dist"
DIST_MANIFEST = ROOT / "docs-site" / "dist_manifest.yaml"
DRY_RUN_REPORT = ROOT / "docs-site" / "deployment_dry_run_report.md"


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def test_v1_5_docs_sprint_gate_required_artifacts_exist() -> None:
    required = [
        "docs/docs-deployment-strategy.md",
        "docs/github-pages-deployment-plan.md",
        "docs/static-hosting-deployment-plan.md",
        "docs/local-only-docs-plan.md",
        "docs/docs-site-build-hardening.md",
        "docs/public-docs-navigation-polish.md",
        "docs/docs-deployment-dry-run.md",
        "docs-site/build_report.md",
        "docs-site/dist_manifest.yaml",
        "docs-site/deployment_dry_run_report.md",
        "docs/v1.5.0-docs-sprint-gate-report.md",
        "docs/v1.5.0-docs-go-no-go.md",
    ]
    for path in required:
        assert (ROOT / path).exists()


def test_v1_5_docs_sprint_gate_nav_is_polished() -> None:
    nav = load_docs_site_nav(ROOT / "docs-site" / "nav.yaml")
    manifest = load_docs_site_manifest(ROOT / "docs-site" / "site_manifest.yaml")

    expected = [
        "overview",
        "quickstart",
        "concepts",
        "original_repo_parity",
        "public_demo",
        "docs_dashboard",
        "plugin_mcp",
        "split_repos",
        "security_privacy",
        "faq",
        "roadmap",
    ]
    assert [item.item_id for item in nav.items] == expected
    assert manifest.required_sections == expected
    assert validate_nav_against_manifest(nav, manifest) == []


def test_v1_5_docs_sprint_gate_build_hardening_has_no_blockers() -> None:
    report = build_docs_site_hardening_report(ROOT, output_root=DIST)

    assert report.status in {"pass", "pass_with_warnings"}
    assert report.link_report.has_blockers is False
    assert report.link_report.missing_pages == []
    assert report.link_report.broken_links == []
    assert report.link_report.missing_source_docs == []
    assert report.link_report.private_path_hits == []
    assert report.deployment_performed is False


def test_v1_5_docs_sprint_gate_dry_run_manifest_matches_dist() -> None:
    manifest = DIST_MANIFEST.read_text(encoding="utf-8")
    paths = re.findall(r"^\s+- path:\s+(.+)$", manifest, re.M)

    assert "deployment_performed: false" in manifest
    assert "public_url: none" in manifest
    assert paths
    for relative in paths:
        path = DIST / relative
        assert path.exists()
        assert f"    sha256: {_sha256(path)}" in manifest


def test_v1_5_docs_sprint_gate_go_no_go_boundaries() -> None:
    combined = "\n".join(
        [
            _read("docs/v1.5.0-docs-sprint-gate-report.md"),
            _read("docs/v1.5.0-docs-go-no-go.md"),
            _read("docs/docs-deployment-dry-run.md"),
            DRY_RUN_REPORT.read_text(encoding="utf-8"),
        ]
    )

    required = [
        "GO for docs deployment prep",
        "NO-GO for automatic public deployment",
        "no public deployment",
        "no real public URL",
        "no analytics",
        "no secrets",
        "no private paths",
        "no raw data",
        "human review required",
    ]
    for term in required:
        assert term in combined


def test_v1_5_docs_sprint_gate_contains_no_sensitive_material() -> None:
    paths = [
        *[path for path in DIST.rglob("*") if path.is_file()],
        DIST_MANIFEST,
        DRY_RUN_REPORT,
        ROOT / "docs" / "v1.5.0-docs-sprint-gate-report.md",
        ROOT / "docs" / "v1.5.0-docs-go-no-go.md",
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in paths)

    forbidden = [
        "D:" + "/vggt",
        "D:" + "\\vggt",
        "local_project_links" + ".yaml",
        "ghp_",
        "sk-",
        "SMPL-X",
        "deployed at",
        "live URL:",
        "status" + ": observed",
    ]
    for marker in forbidden:
        assert marker not in combined
    assert "Tuling" + "Research" not in combined
