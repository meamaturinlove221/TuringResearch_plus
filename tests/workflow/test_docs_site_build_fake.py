from __future__ import annotations

from pathlib import Path

from turing_research_plus.docs_site.builder import build_docs_site_from_repo

ROOT = Path(__file__).resolve().parents[2]


def test_docs_site_fake_build_outputs_static_html(tmp_path: Path) -> None:
    result = build_docs_site_from_repo(ROOT, output_root=tmp_path)

    generated = {path.name for path in result.generated_files}
    assert "index.html" in generated
    assert "original-repo-parity.html" in generated
    assert "public-demo.html" in generated
    assert "roadmap.html" in generated
    assert "faq.html" in generated
    assert "site.css" in generated
    assert result.requires_human_review is True

    index = (tmp_path / "index.html").read_text(encoding="utf-8")
    assert "Overview" in index
    assert "not deployed by default" in index

    quickstart = (tmp_path / "quickstart.html").read_text(encoding="utf-8")
    assert "no API key required" in quickstart
    assert "Source Docs" in quickstart
    assert "https://github.com/" not in quickstart
