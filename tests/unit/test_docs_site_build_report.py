from __future__ import annotations

from pathlib import Path

from turing_research_plus.docs_site.build_report import (
    build_docs_site_hardening_report,
    render_build_hardening_markdown,
)

ROOT = Path(__file__).resolve().parents[2]


def test_docs_site_build_report_combines_checks_and_export(tmp_path: Path) -> None:
    report = build_docs_site_hardening_report(ROOT, output_root=tmp_path)

    assert report.status in {"pass", "pass_with_warnings"}
    assert report.deployment_performed is False
    assert report.requires_human_review is True
    assert report.link_report.has_blockers is False
    assert report.export_manifest.files
    assert report.link_report.orphan_pages


def test_docs_site_build_report_markdown_has_required_sections(tmp_path: Path) -> None:
    report = build_docs_site_hardening_report(ROOT, output_root=tmp_path)
    markdown = render_build_hardening_markdown(report)

    assert "# Docs Site Build Report" in markdown
    assert "Status: pass_with_warnings." in markdown
    assert "- no deployment" in markdown
    assert "- no analytics" in markdown
    assert "## Findings" in markdown
