from __future__ import annotations

from turing_research_plus.scholar_pipeline.models import ReferencePipelineRequest, ReferenceSource
from turing_research_plus.scholar_pipeline.reference_pipeline import resolve_references


def test_semantic_scholar_references_primary_with_pagination_flag() -> None:
    result = resolve_references(ReferencePipelineRequest(paper_id="S2-1", limit=2))

    assert result.source == ReferenceSource.SEMANTIC_SCHOLAR
    assert len(result.references) == 2
    assert result.pagination_used is True
    assert result.references[0].requires_human_review is True


def test_cached_markdown_reference_fallback() -> None:
    markdown = "# Paper\n\n## References\n- NeuralBody paper\n- HumanRAM paper\n"

    result = resolve_references(ReferencePipelineRequest(cached_markdown=markdown))

    assert result.source == ReferenceSource.CACHED_MARKDOWN
    assert result.fallback_used is True
    assert [ref.title for ref in result.references] == ["NeuralBody paper", "HumanRAM paper"]


def test_manual_reference_fallback_when_no_provider_or_cache() -> None:
    result = resolve_references(
        ReferencePipelineRequest(manual_references=["Manual paper A", "Manual paper B"])
    )

    assert result.source == ReferenceSource.MANUAL
    assert len(result.references) == 2
