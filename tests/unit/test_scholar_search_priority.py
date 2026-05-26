from __future__ import annotations

from pathlib import Path

from turing_research_plus.scholar_pipeline.models import (
    ScholarPipelineRequest,
    ScholarPipelineStatus,
    ScholarSourcePriority,
)
from turing_research_plus.scholar_pipeline.search_pipeline import run_scholar_search_pipeline


def test_cached_markdown_has_highest_priority(tmp_path: Path) -> None:
    cached = tmp_path / "paper.md"
    cached.write_text("# Cached Paper\n\n## References\n- Ref A\n", encoding="utf-8")

    result = run_scholar_search_pipeline(
        ScholarPipelineRequest(query="Cached Paper", paper_id="cached", cached_markdown_path=cached)
    )

    assert result.selected_source == ScholarSourcePriority.CACHED_MARKDOWN
    assert result.status == ScholarPipelineStatus.CACHE_HIT
    assert result.cached_content is not None
    assert result.requires_human_review is True


def test_arxiv_fake_precedes_semantic_scholar_in_dry_run() -> None:
    result = run_scholar_search_pipeline(ScholarPipelineRequest(query="SparseConv3D"))

    assert result.selected_source == ScholarSourcePriority.ARXIV
    assert result.status == ScholarPipelineStatus.FAKE_RESULT
    assert result.source_priority[:3] == [
        ScholarSourcePriority.CACHED_MARKDOWN,
        ScholarSourcePriority.ARXIV,
        ScholarSourcePriority.SEMANTIC_SCHOLAR,
    ]
    assert result.source_metadata[0].human_verified is False


def test_known_arxiv_url_does_not_download_full_text() -> None:
    result = run_scholar_search_pipeline(
        ScholarPipelineRequest(
            query="Known arXiv paper",
            known_arxiv_url="https://arxiv.org/abs/0000.00000",
        )
    )

    assert result.selected_source == ScholarSourcePriority.ARXIV
    assert "no full text was downloaded" in result.limitations[0]
