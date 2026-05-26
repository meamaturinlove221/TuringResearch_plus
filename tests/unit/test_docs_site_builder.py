from __future__ import annotations

from pathlib import Path

from turing_research_plus.docs_site.builder import build_docs_site
from turing_research_plus.docs_site.markdown_render import render_markdown_to_html
from turing_research_plus.docs_site.models import DocsSiteBuildRequest

ROOT = Path(__file__).resolve().parents[2]


def test_markdown_render_supports_headings_links_and_lists() -> None:
    html = render_markdown_to_html("# Title\n\n- [Quick](quickstart.md)\n- `code`\n")

    assert "<h1>Title</h1>" in html
    assert '<a href="quickstart.md">Quick</a>' in html
    assert "<code>code</code>" in html


def test_docs_site_builder_writes_static_html(tmp_path: Path) -> None:
    result = build_docs_site(
        DocsSiteBuildRequest(
            repo_root=ROOT,
            docs_site_root=ROOT / "docs-site",
            output_root=tmp_path,
            nav_path=ROOT / "docs-site" / "nav.yaml",
            manifest_path=ROOT / "docs-site" / "site_manifest.yaml",
        )
    )

    assert result.site_id == "turingresearch-docs-site"
    assert not result.warnings
    assert (tmp_path / "index.html").exists()
    assert (tmp_path / "quickstart.html").exists()
    assert (tmp_path / "site.css").exists()
    assert "TuringResearch Docs" in (tmp_path / "index.html").read_text(encoding="utf-8")
