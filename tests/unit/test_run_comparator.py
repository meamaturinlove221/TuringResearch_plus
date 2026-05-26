from __future__ import annotations

from pathlib import Path

from turing_research_plus.dashboard.run_dashboard import build_run_dashboard
from turing_research_plus.run_compare.board_index import board_ref_from_path
from turing_research_plus.run_compare.comparator import compare_runs, input_from_dashboard
from turing_research_plus.run_compare.models import (
    RunComparisonInput,
    RunComparisonStatus,
)
from turing_research_plus.run_ingest.modal_ingestor import ingest_modal_run
from turing_research_plus.run_ingest.models import RunIngestRequest, RunSourceType

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = (
    ROOT
    / "examples"
    / "vggt-human-prior-survey"
    / "run_ingest_fixtures"
    / "modal_run_fixture"
)


def test_compare_runs_flags_vggt_unsupported_claims() -> None:
    report = compare_runs(
        [
            RunComparisonInput(
                run_id="V770",
                status=RunComparisonStatus.LOCAL_OBSERVED,
                boards=[board_ref_from_path("V770", "boards/source_view.png")],
                claimed_improvements=["full human completion"],
            ),
            RunComparisonInput(
                run_id="V129",
                status=RunComparisonStatus.LOCAL_OBSERVED,
                boards=[board_ref_from_path("V129", "boards/hairline_delta.png")],
                claimed_improvements=["local positive"],
            ),
            RunComparisonInput(
                run_id="V260",
                status=RunComparisonStatus.HARD_BLOCKED,
                claimed_improvements=["successful adjacent prediction route"],
            ),
            RunComparisonInput(
                run_id="V999",
                status=RunComparisonStatus.NOT_ENOUGH_EVIDENCE,
                claimed_improvements=["SparseConv3D promotion"],
            ),
        ]
    )

    joined = "\n".join(report.unsupported_claims)

    assert "V770 cannot be claimed as full human completion" in joined
    assert "V129 local positive comparison must retain regression warning" in joined
    assert "V260 is hard-blocked" in joined
    assert "V999 long-run does not equal promotion" in joined
    assert "SparseConv3D success requires real backend evidence" in joined


def test_input_from_dashboard_keeps_modal_route_not_enough_evidence() -> None:
    run_report = ingest_modal_run(
        RunIngestRequest(source_type=RunSourceType.MODAL_FIXTURE, source_path=FIXTURE)
    )
    dashboard = build_run_dashboard(run_report)
    comparison_input = input_from_dashboard(dashboard)

    assert comparison_input.status == RunComparisonStatus.NOT_ENOUGH_EVIDENCE
    assert comparison_input.artifacts_missing == [
        "predictions.npz",
        "board_inventory.md",
        "sha256_manifest.txt",
        "cleanup_report.md",
    ]


def test_compare_dashboard_input_flags_sparse_backend_evidence() -> None:
    run_report = ingest_modal_run(
        RunIngestRequest(source_type=RunSourceType.MODAL_FIXTURE, source_path=FIXTURE)
    )
    dashboard = build_run_dashboard(run_report)
    comparison_input = input_from_dashboard(dashboard)

    report = compare_runs([comparison_input])

    assert "modal-sparseconv-fixture-001" in report.compared_runs
    assert any("real sparse backend evidence" in action for action in report.next_actions)
