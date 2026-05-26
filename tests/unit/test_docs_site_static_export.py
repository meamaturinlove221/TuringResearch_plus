from __future__ import annotations

from pathlib import Path

from turing_research_plus.docs_site.static_export import (
    export_static_docs_site,
    render_static_export_manifest_markdown,
)

ROOT = Path(__file__).resolve().parents[2]


def test_docs_site_static_export_writes_manifest(tmp_path: Path) -> None:
    manifest = export_static_docs_site(ROOT, output_root=tmp_path)

    names = {item.path for item in manifest.files}
    assert "index.html" in names
    assert "quickstart.html" in names
    assert "site.css" in names
    assert manifest.deployment_performed is False
    assert manifest.requires_human_review is True
    assert (tmp_path / "static_export_manifest.json").exists()
    assert all(len(item.sha256) == 64 for item in manifest.files)


def test_static_export_manifest_markdown_records_no_deployment(tmp_path: Path) -> None:
    manifest = export_static_docs_site(ROOT, output_root=tmp_path, write_manifest=False)
    markdown = render_static_export_manifest_markdown(manifest)

    assert "Deployment performed: `false`" in markdown
    assert "Requires human review: `true`" in markdown
    assert "index.html" in markdown
