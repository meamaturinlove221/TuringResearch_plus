from __future__ import annotations

from pathlib import Path

from turing_research_plus.docs_site.nav import (
    load_docs_site_manifest,
    load_docs_site_nav,
    validate_nav_against_manifest,
)

ROOT = Path(__file__).resolve().parents[2]


def test_load_docs_site_nav_reads_all_required_items() -> None:
    nav = load_docs_site_nav(ROOT / "docs-site" / "nav.yaml")
    manifest = load_docs_site_manifest(ROOT / "docs-site" / "site_manifest.yaml")

    assert nav.site_title == "TuringResearch Docs"
    assert len(nav.items) == len(manifest.required_sections)
    assert [item.item_id for item in nav.items] == [
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


def test_load_docs_site_manifest_matches_nav() -> None:
    nav = load_docs_site_nav(ROOT / "docs-site" / "nav.yaml")
    manifest = load_docs_site_manifest(ROOT / "docs-site" / "site_manifest.yaml")

    assert manifest.local_first is True
    assert manifest.deployment == "none"
    assert validate_nav_against_manifest(nav, manifest) == []
