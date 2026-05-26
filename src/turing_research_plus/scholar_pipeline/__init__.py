"""Scholar and paper pipeline refinement helpers."""

from turing_research_plus.scholar_pipeline.cached_content import read_cached_paper_content
from turing_research_plus.scholar_pipeline.fallback_policy import (
    ScholarFallbackPolicy,
    ScholarFallbackRule,
    ScholarFallbackStatus,
    build_scholar_fallback_policy,
    render_scholar_fallback_policy,
)
from turing_research_plus.scholar_pipeline.heavy_pdf_backend_slot import (
    HeavyPdfBackendKind,
    HeavyPdfBackendRequest,
    HeavyPdfBackendSlot,
    HeavyPdfBackendStatus,
    build_heavy_pdf_backend_slot,
    render_heavy_pdf_backend_slot,
)
from turing_research_plus.scholar_pipeline.mcp_usage_export import (
    ScholarMcpUsageGuide,
    build_scholar_mcp_usage_guide,
    render_scholar_mcp_usage_guide,
)
from turing_research_plus.scholar_pipeline.models import (
    CachedPaperContent,
    PaperReference,
    ReferencePipelineRequest,
    ReferencePipelineResult,
    ScholarPipelineRequest,
    ScholarPipelineResult,
    ScholarSourcePriority,
    ThreePassReadingPlan,
)
from turing_research_plus.scholar_pipeline.reading_plan import build_three_pass_reading_plan
from turing_research_plus.scholar_pipeline.reference_pipeline import resolve_references
from turing_research_plus.scholar_pipeline.search_pipeline import run_scholar_search_pipeline
from turing_research_plus.scholar_pipeline.source_priority import (
    DEFAULT_SOURCE_PRIORITY,
    ScholarSourcePriorityPlan,
    build_scholar_source_priority_plan,
    render_scholar_source_priority_plan,
)
from turing_research_plus.scholar_pipeline.tool_list_export import (
    ScholarToolEntry,
    ScholarToolList,
    build_scholar_tool_list,
    render_scholar_tool_list,
)

__all__ = [
    "CachedPaperContent",
    "DEFAULT_SOURCE_PRIORITY",
    "HeavyPdfBackendKind",
    "HeavyPdfBackendRequest",
    "HeavyPdfBackendSlot",
    "HeavyPdfBackendStatus",
    "PaperReference",
    "ReferencePipelineRequest",
    "ReferencePipelineResult",
    "ScholarFallbackPolicy",
    "ScholarFallbackRule",
    "ScholarFallbackStatus",
    "ScholarMcpUsageGuide",
    "ScholarPipelineRequest",
    "ScholarPipelineResult",
    "ScholarSourcePriorityPlan",
    "ScholarSourcePriority",
    "ScholarToolEntry",
    "ScholarToolList",
    "ThreePassReadingPlan",
    "build_scholar_fallback_policy",
    "build_heavy_pdf_backend_slot",
    "build_scholar_mcp_usage_guide",
    "build_scholar_source_priority_plan",
    "build_scholar_tool_list",
    "build_three_pass_reading_plan",
    "read_cached_paper_content",
    "render_scholar_fallback_policy",
    "render_heavy_pdf_backend_slot",
    "render_scholar_mcp_usage_guide",
    "render_scholar_source_priority_plan",
    "render_scholar_tool_list",
    "resolve_references",
    "run_scholar_search_pipeline",
]
