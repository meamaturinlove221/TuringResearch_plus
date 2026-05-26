"""Thin local wrappers for scholar pipeline refinement."""

from __future__ import annotations

from typing import Any

from turing_research_plus.scholar_pipeline.models import (
    ReferencePipelineRequest,
    ScholarPipelineRequest,
)
from turing_research_plus.scholar_pipeline.reading_plan import build_three_pass_reading_plan
from turing_research_plus.scholar_pipeline.reference_pipeline import resolve_references
from turing_research_plus.scholar_pipeline.search_pipeline import run_scholar_search_pipeline


def paper_search_pipeline_tool(request: ScholarPipelineRequest) -> dict[str, Any]:
    """Run cache-first scholar search in fake/default mode."""

    return run_scholar_search_pipeline(request).model_dump(mode="json")


def paper_reference_pipeline_tool(request: ReferencePipelineRequest) -> dict[str, Any]:
    """Resolve references with fallback order."""

    return resolve_references(request).model_dump(mode="json")


def paper_three_pass_plan_tool(paper_id: str, title: str) -> dict[str, Any]:
    """Build a three-pass reading plan."""

    return build_three_pass_reading_plan(paper_id, title).model_dump(mode="json")
