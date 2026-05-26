from __future__ import annotations

from pathlib import Path

from turing_research_plus.case_study.gallery import (
    load_case_gallery_manifest,
    render_case_gallery_markdown,
)
from turing_research_plus.privacy.scanner import scan_privacy_paths

ROOT = Path(__file__).resolve().parents[2]
GALLERY = ROOT / "examples" / "public_demo" / "case_gallery"
MANIFEST = GALLERY / "gallery_manifest.yaml"
DOCS_SITE_PAGE = ROOT / "docs-site" / "pages" / "case-study-gallery.md"


def test_case_gallery_public_demo_manifest_is_safe() -> None:
    manifest = load_case_gallery_manifest(MANIFEST)

    assert manifest.requires_human_review is True
    assert manifest.published is False
    for item in manifest.cases:
        assert item.demo_status == "demo-only"
        assert item.privacy_level in {"public-demo", "public-safe-case"}
        assert item.requires_human_review is True
        assert not item.dashboard_link.startswith(("http://", "https://"))
        assert not item.advisor_pack_link.startswith(("http://", "https://"))
        assert item.available_artifacts
        assert item.limitations


def test_case_gallery_public_demo_privacy_gate_is_clean() -> None:
    report = scan_privacy_paths([GALLERY, ROOT / "docs" / "case-study-gallery.md"])

    assert report.release_blocker is False
    assert report.findings == []
    assert report.requires_human_review is True


def test_case_gallery_docs_site_page_exists() -> None:
    page = DOCS_SITE_PAGE.read_text(encoding="utf-8")

    assert "Case Study Gallery" in page
    assert "../../docs/case-study-gallery.md" in page
    assert "../../examples/public_demo/case_gallery/gallery_manifest.yaml" in page


def test_case_gallery_markdown_has_no_private_or_external_url_payloads() -> None:
    markdown = render_case_gallery_markdown(load_case_gallery_manifest(MANIFEST))

    assert "D:/vggt" not in markdown
    assert "D:\\\\vggt" not in markdown
    assert "https://github.com/" not in markdown
    assert "sk-" not in markdown
    assert "ghp_" not in markdown
    assert "local_project_links.yaml" not in markdown
