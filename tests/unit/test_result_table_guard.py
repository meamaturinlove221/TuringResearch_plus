from __future__ import annotations

import pytest

from turing_research_plus.paper_write.result_table_guard import (
    ResultTableGuardReport,
    build_missing_result_table_guard,
    render_result_table_guard,
)


def test_missing_result_table_guard_blocks_result_values() -> None:
    report = build_missing_result_table_guard(
        missing_artifacts=["predictions.npz", "board_inventory.md"],
        run_status="ROUTE_EXHAUSTED_WITH_FAILURE_ANALYSIS",
        route_status="requires-real-experiment",
    )

    assert report.result_tables_allowed is False
    assert "main_quantitative_results" in report.missing_result_tables
    assert "predictions.npz" in report.missing_artifacts
    assert any("SparseConv3D success" in claim for claim in report.blocked_claims)
    assert report.dashboard_is_not_result is True


def test_result_table_guard_rejects_allowed_with_missing_evidence() -> None:
    with pytest.raises(ValueError, match="missing evidence"):
        ResultTableGuardReport(
            result_tables_allowed=True,
            missing_result_tables=["main_quantitative_results"],
            missing_artifacts=[],
        )


def test_render_result_table_guard_keeps_missing_boundary() -> None:
    report = build_missing_result_table_guard(
        missing_artifacts=["sha256_manifest.txt"],
        run_status="ROUTE_EXHAUSTED_WITH_FAILURE_ANALYSIS",
        route_status="requires-real-experiment",
    )
    markdown = render_result_table_guard(report)

    assert "Result tables allowed: `false`" in markdown
    assert "`sha256_manifest.txt`" in markdown
    assert "No result value is generated." in markdown
    assert "No figure or table is fabricated." in markdown
