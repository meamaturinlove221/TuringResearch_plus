"""Markdown export for run comparison reports."""

from __future__ import annotations

from turing_research_plus.run_compare.models import RunComparisonReport


def render_run_comparison_markdown(report: RunComparisonReport) -> str:
    """Render a conservative run comparison report."""

    lines = [
        "# VGGT Run Comparison",
        "",
        "This report compares metadata, boards, artifacts, hard gates, and failure labels.",
        "It does not perform image understanding and is not an experiment result.",
        "",
        "## Compared Runs",
        "",
        *[f"- `{run_id}`" for run_id in report.compared_runs],
        "",
        "## Boards",
        "",
        f"- Available boards: `{len(report.available_boards)}`",
        f"- Missing or weak boards: `{len(report.missing_boards)}`",
        "",
        *[
            f"- `{board.run_id}` missing/weak `{board.board_id}`: `{board.status}`"
            for board in report.missing_boards
        ],
        "",
        "## Artifact Completeness",
        "",
        *[
            f"- `{item.run_id}`: present `{item.present_count}`, missing `{item.missing_count}`"
            for item in report.artifact_completeness
        ],
        "",
        "## Visual Completeness",
        "",
        *[
            f"- `{item.run_id}`: available `{item.available_count}`, "
            f"missing `{item.missing_count}`, proxy-only `{item.proxy_only_count}`"
            for item in report.visual_completeness
        ],
        "",
        "## Hard Gate Summary",
        "",
        *[
            f"- `{item.run_id}`: passed `{len(item.passed)}`, failed `{len(item.failed)}`"
            for item in report.hard_gate_summary
        ],
        "",
        "## Failure Summary",
        "",
        *[
            f"- `{category}`: {', '.join(f'`{run_id}`' for run_id in runs)}"
            for category, runs in sorted(report.failure_summary.items())
        ],
        "",
        "## Claimed Improvements",
        "",
        *[f"- {claim}" for claim in report.claimed_improvements],
        "",
        "## Unsupported Claims",
        "",
        *[f"- {claim}" for claim in report.unsupported_claims],
        "",
        "## Next Actions",
        "",
        *[f"- {action}" for action in report.next_actions],
        "",
        "## Boundary",
        "",
        "- Comparison is metadata/report level only.",
        "- No Modal or VGGT execution was performed.",
        "- Planned routes are not observed results.",
        "- SparseConv3D success requires real backend evidence.",
        "- Human review is required.",
        "",
    ]
    return "\n".join(lines)
