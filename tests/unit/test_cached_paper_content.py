from __future__ import annotations

from pathlib import Path

from turing_research_plus.scholar_pipeline.cached_content import read_cached_paper_content


def test_cached_paper_content_reads_markdown_and_references(tmp_path: Path) -> None:
    path = tmp_path / "paper.md"
    path.write_text("# Paper\n\nBody\n\n## References\n- Ref A\n", encoding="utf-8")

    content = read_cached_paper_content(paper_id="p1", title="Paper", markdown_path=path)

    assert content.cache_hit is True
    assert content.references_section() is not None
    assert content.source_metadata[0].provider == "cached_markdown"
    assert content.source_metadata[0].human_verified is False
