"""Metadata-level experiment run comparison."""

from turing_research_plus.run_compare.board_index import board_ref_from_path, index_boards
from turing_research_plus.run_compare.comparator import compare_runs, input_from_dashboard
from turing_research_plus.run_compare.markdown_export import (
    render_run_comparison_markdown,
)
from turing_research_plus.run_compare.models import (
    ArtifactCompletenessEntry,
    BoardRef,
    BoardStatus,
    HardGateSummaryEntry,
    RunComparisonInput,
    RunComparisonReport,
    RunComparisonStatus,
    VisualCompletenessEntry,
)

__all__ = [
    "ArtifactCompletenessEntry",
    "BoardRef",
    "BoardStatus",
    "HardGateSummaryEntry",
    "RunComparisonInput",
    "RunComparisonReport",
    "RunComparisonStatus",
    "VisualCompletenessEntry",
    "board_ref_from_path",
    "compare_runs",
    "index_boards",
    "input_from_dashboard",
    "render_run_comparison_markdown",
]
