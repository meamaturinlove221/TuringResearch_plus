from __future__ import annotations

from pathlib import Path

from turing_research_plus.docs_site.link_checker import (
    check_docs_site_links,
    render_link_check_markdown,
)

ROOT = Path(__file__).resolve().parents[2]


def test_docs_site_link_checker_passes_current_nav() -> None:
    report = check_docs_site_links(ROOT)

    assert report.has_blockers is False
    assert report.missing_pages == []
    assert report.missing_source_docs == []
    assert report.broken_links == []
    assert report.private_path_hits == []
    assert len(report.checked_pages) >= 10


def test_docs_site_link_checker_reports_missing_orphan_and_private_path(
    tmp_path: Path,
) -> None:
    site = tmp_path / "docs-site"
    pages = site / "pages"
    pages.mkdir(parents=True)
    (tmp_path / "README.md").write_text("# Demo\n", encoding="utf-8")
    (pages / "intro.md").write_text(
        "# Intro\n\n[Missing](missing.md)\n\nDo not publish `.env`.\n",
        encoding="utf-8",
    )
    (pages / "orphan.md").write_text("# Orphan\n", encoding="utf-8")
    (site / "nav.yaml").write_text(
        "\n".join(
            [
                "site_title: Demo Docs",
                "status: test",
                "items:",
                "  - id: intro",
                "    title: Intro",
                "    page: pages/intro.md",
                "    source_docs:",
                "      - ../README.md",
                "  - id: missing",
                "    title: Missing",
                "    page: pages/missing-page.md",
                "    source_docs:",
                "      - ../missing-source.md",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    (site / "site_manifest.yaml").write_text(
        "\n".join(
            [
                "site_id: demo-docs",
                "status: test",
                "source_of_truth: repository_markdown",
                "local_first: true",
                "deployment: none",
                "cloud_dependency: false",
                "large_frontend_framework: false",
                "private_data_required: false",
                "fake_links_allowed: false",
                "required_sections:",
                "  - intro",
                "  - missing",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    report = check_docs_site_links(tmp_path)
    markdown = render_link_check_markdown(report)

    assert report.has_blockers is True
    assert [item.kind for item in report.broken_links] == ["broken_link"]
    assert [item.kind for item in report.missing_pages] == ["missing_page"]
    assert [item.kind for item in report.missing_source_docs] == ["missing_source_doc"]
    assert [item.kind for item in report.orphan_pages] == ["orphan_page"]
    assert [item.kind for item in report.private_path_hits] == ["private_path"]
    assert "Status: blocked." in markdown
