from __future__ import annotations

from turing_research_plus.run_compare.comparator import compare_runs
from turing_research_plus.run_compare.markdown_export import (
    render_run_comparison_markdown,
)
from turing_research_plus.run_compare.models import (
    RunComparisonInput,
    RunComparisonStatus,
)


def test_run_comparison_markdown_contains_boundaries() -> None:
    report = compare_runs(
        [
            RunComparisonInput(
                run_id="V999",
                status=RunComparisonStatus.NOT_ENOUGH_EVIDENCE,
                claimed_improvements=["SparseConv3D promotion"],
            )
        ]
    )

    markdown = render_run_comparison_markdown(report)

    assert "# VGGT Run Comparison" in markdown
    assert "metadata/report level only" in markdown
    assert "No Modal or VGGT execution was performed" in markdown
    assert "SparseConv3D success requires real backend evidence" in markdown
    assert "SparseConv3D success" in markdown
    assert "promotion passed" not in markdown.lower()
