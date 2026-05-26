from __future__ import annotations

import json
from pathlib import Path

from turing_research_plus.citation_graph.expander import CitationGraphExpander
from turing_research_plus.collision.models import PaperComparisonInput
from turing_research_plus.collision.tools import collision_risk_detect
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


def test_scholar_flow_cache_to_collision_risk() -> None:
    cached = EXAMPLE / "paper_method_cards" / "humanram.fixture.md"
    search = run_scholar_search_pipeline(
        ScholarPipelineRequest(
            query="HumanRAM",
            paper_id="humanram",
            cached_markdown_path=cached,
        )
    )
    refs = resolve_references(
        ReferencePipelineRequest(cached_markdown=search.cached_content.markdown)
    )
    plan = build_three_pass_reading_plan("humanram", "HumanRAM fixture")
    card = extract_paper_method_card(
        PaperMethodCardInput(
            paper_id="humanram",
            title="HumanRAM fixture",
            source_type=PaperSourceType.FAKE_OR_MANUAL_NOTE,
            source_path=cached,
        )
    )
    graph = CitationGraphExpander().fake_vggt_related_work_graph()
    report = collision_risk_detect(
        PaperComparisonInput(
            compared_papers=[card.model_dump(mode="json")],
            citation_graph=json.loads(graph.model_dump_json()),
        )
    )

    assert search.selected_source == ScholarSourcePriority.CACHED_MARKDOWN
    assert refs.requires_human_review is True
    assert plan.human_verified is False
    assert card.requires_human_review is True
    assert graph.requires_human_review is True
    assert report.requires_human_review is True
    assert report.safe_claims
    assert report.missing_evidence


def test_scholar_flow_fake_arxiv_default_no_live_network() -> None:
    result = run_scholar_search_pipeline(ScholarPipelineRequest(query="VGGT human prior"))

    assert result.selected_source == ScholarSourcePriority.ARXIV
    assert result.source_metadata[0].human_verified is False
    assert any("Fake arXiv adapter" in item for item in result.limitations)
