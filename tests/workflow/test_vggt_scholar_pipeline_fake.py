from __future__ import annotations

from pathlib import Path

from turing_research_plus.paper_method.extractor import extract_paper_method_card
from turing_research_plus.paper_method.models import PaperMethodCardInput, PaperSourceType
from turing_research_plus.scholar_pipeline.models import (
    ReferencePipelineRequest,
    ScholarPipelineRequest,
    ScholarSourcePriority,
)
from turing_research_plus.scholar_pipeline.reading_plan import build_three_pass_reading_plan
from turing_research_plus.scholar_pipeline.reference_pipeline import resolve_references
from turing_research_plus.scholar_pipeline.search_pipeline import run_scholar_search_pipeline

EXAMPLE = Path("examples") / "vggt-human-prior-survey"


def test_vggt_scholar_pipeline_fake_cache_to_method_card() -> None:
    cached = EXAMPLE / "paper_method_cards" / "neuralbody.fixture.md"

    search = run_scholar_search_pipeline(
        ScholarPipelineRequest(
            query="NeuralBody",
            paper_id="neuralbody",
            cached_markdown_path=cached,
        )
    )
    refs = resolve_references(
        ReferencePipelineRequest(cached_markdown=search.cached_content.markdown)
    )
    plan = build_three_pass_reading_plan("neuralbody", "NeuralBody fixture")
    card = extract_paper_method_card(
        PaperMethodCardInput(
            paper_id="neuralbody",
            title="NeuralBody fixture",
            source_type=PaperSourceType.FAKE_OR_MANUAL_NOTE,
            source_path=cached,
        )
    )

    assert search.selected_source == ScholarSourcePriority.CACHED_MARKDOWN
    assert refs.requires_human_review is True
    assert plan.requires_real_paper_review is True
    assert card.requires_human_review is True
    assert "method card" in plan.outputs
