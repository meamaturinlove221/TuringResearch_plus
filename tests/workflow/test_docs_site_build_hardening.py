from __future__ import annotations

from pathlib import Path

from turing_research_plus.docs_site.build_report import (
    build_docs_site_hardening_report,
    render_build_hardening_markdown,
)
from turing_research_plus.docs_site.link_checker import check_docs_site_links
from turing_research_plus.docs_site.static_export import export_static_docs_site

ROOT = Path(__file__).resolve().parents[2]


def test_docs_site_build_hardening_workflow(tmp_path: Path) -> None:
    link_report = check_docs_site_links(ROOT)
    export_manifest = export_static_docs_site(ROOT, output_root=tmp_path)
    report = build_docs_site_hardening_report(ROOT, output_root=tmp_path)

    assert link_report.has_blockers is False
    assert export_manifest.deployment_performed is False
    assert report.status in {"pass", "pass_with_warnings"}
    assert report.export_manifest.files
    assert "static_export_manifest.json" not in {item.path for item in report.export_manifest.files}

    markdown = render_build_hardening_markdown(report)
    assert "Private path hits" in markdown
    assert "- no deployment" in markdown
    assert "Requires human review: `true`" in markdown
