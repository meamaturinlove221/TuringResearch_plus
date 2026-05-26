"""Operator-facing Scholar tool surfaces for v1.3 parity."""

from turing_research_plus.scholar_tools.paper_content import (
    PaperContentToolRequest,
    PaperContentToolResult,
    run_paper_content_tool,
)
from turing_research_plus.scholar_tools.paper_reading import (
    PaperReadingToolRequest,
    PaperReadingToolResult,
    run_paper_reading_tool,
)
from turing_research_plus.scholar_tools.paper_reference import (
    PaperReferenceToolRequest,
    PaperReferenceToolResult,
    run_paper_reference_tool,
)
from turing_research_plus.scholar_tools.paper_searching import (
    PaperSearchingToolRequest,
    PaperSearchingToolResult,
    run_paper_searching_tool,
)
from turing_research_plus.scholar_tools.tool_surface import (
    ScholarFullToolSurface,
    ScholarToolSurfaceEntry,
    build_scholar_full_tool_surface,
    render_scholar_full_tool_surface,
)

__all__ = [
    "PaperContentToolRequest",
    "PaperContentToolResult",
    "PaperReadingToolRequest",
    "PaperReadingToolResult",
    "PaperReferenceToolRequest",
    "PaperReferenceToolResult",
    "PaperSearchingToolRequest",
    "PaperSearchingToolResult",
    "ScholarFullToolSurface",
    "ScholarToolSurfaceEntry",
    "build_scholar_full_tool_surface",
    "render_scholar_full_tool_surface",
    "run_paper_content_tool",
    "run_paper_reading_tool",
    "run_paper_reference_tool",
    "run_paper_searching_tool",
]
