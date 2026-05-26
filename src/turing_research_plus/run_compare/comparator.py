"""Metadata-level run comparison logic."""

from __future__ import annotations

from collections import defaultdict

from turing_research_plus.dashboard.models import RunDashboardReport
from turing_research_plus.run_compare.board_index import index_boards
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


def input_from_dashboard(report: RunDashboardReport) -> RunComparisonInput:
    """Convert a run dashboard into comparison metadata."""

    status = _status_from_dashboard(report)
    boards = [
        BoardRef(
            run_id=report.run_id,
            board_id="board_inventory",
            status=BoardStatus.MISSING,
            warnings=["board inventory missing"],
        )
    ]
    return RunComparisonInput(
        run_id=report.run_id,
        route_id=report.route_id,
        status=status,
        boards=boards,
        artifacts_present=[
            f"present-artifact-{index + 1}"
            for index in range(report.artifact_completeness.present_count)
        ],
        artifacts_missing=report.artifact_completeness.missing_artifacts,
        hard_gates_passed=[gate.gate_id for gate in report.hard_gates if gate.passed],
        hard_gates_failed=[gate.gate_id for gate in report.hard_gates if not gate.passed],
        failure_categories=report.failure_categories,
        claimed_improvements=[],
        notes=[
            "created from RunDashboardReport",
            "dashboard is review-only and does not execute experiments",
        ],
    )


def compare_runs(runs: list[RunComparisonInput]) -> RunComparisonReport:
    """Build a conservative comparison report from run metadata."""

    available_boards, missing_boards = index_boards(runs)
    failure_summary: dict[str, list[str]] = defaultdict(list)
    claimed_improvements: list[str] = []
    unsupported_claims: list[str] = []
    next_actions: list[str] = []

    for run in runs:
        for category in run.failure_categories:
            failure_summary[category].append(run.run_id)
        claimed_improvements.extend(run.claimed_improvements)
        unsupported_claims.extend(_unsupported_claims(run))
        next_actions.extend(_next_actions(run))

    return RunComparisonReport(
        compared_runs=[run.run_id for run in runs],
        available_boards=available_boards,
        missing_boards=missing_boards,
        artifact_completeness=[
            ArtifactCompletenessEntry(
                run_id=run.run_id,
                present_count=len(run.artifacts_present),
                missing_count=len(run.artifacts_missing),
                missing_artifacts=run.artifacts_missing,
            )
            for run in runs
        ],
        visual_completeness=[_visual_completeness(run) for run in runs],
        hard_gate_summary=[
            HardGateSummaryEntry(
                run_id=run.run_id,
                passed=run.hard_gates_passed,
                failed=run.hard_gates_failed,
            )
            for run in runs
        ],
        failure_summary=dict(sorted(failure_summary.items())),
        claimed_improvements=claimed_improvements,
        unsupported_claims=list(dict.fromkeys(unsupported_claims)),
        next_actions=list(dict.fromkeys(next_actions)),
        requires_human_review=True,
        image_understanding_performed=False,
    )


def _status_from_dashboard(report: RunDashboardReport) -> RunComparisonStatus:
    status = report.run_status.lower()
    if "hard_blocked" in status:
        return RunComparisonStatus.HARD_BLOCKED
    if "review_ready" in status and report.backend_status == "real_backend_confirmed":
        return RunComparisonStatus.REQUIRES_HUMAN_REVIEW
    if "not_enough" in status or report.artifact_completeness.missing_count:
        return RunComparisonStatus.NOT_ENOUGH_EVIDENCE
    return RunComparisonStatus.REQUIRES_HUMAN_REVIEW


def _visual_completeness(run: RunComparisonInput) -> VisualCompletenessEntry:
    available = [board for board in run.boards if board.status == BoardStatus.AVAILABLE]
    missing = [board for board in run.boards if board.status == BoardStatus.MISSING]
    proxy = [board for board in run.boards if board.status == BoardStatus.PROXY_ONLY]
    warnings = [warning for board in run.boards for warning in board.warnings]
    if not run.boards:
        warnings.append("board inventory missing")
    return VisualCompletenessEntry(
        run_id=run.run_id,
        available_count=len(available),
        missing_count=len(missing) if run.boards else 1,
        proxy_only_count=len(proxy),
        warnings=list(dict.fromkeys(warnings)),
    )


def _unsupported_claims(run: RunComparisonInput) -> list[str]:
    unsupported: list[str] = []
    lowered_claims = " ".join(run.claimed_improvements).lower()
    lowered_notes = " ".join(run.notes).lower()
    run_id_lower = run.run_id.lower()

    if "v770" in run_id_lower and "full human completion" in lowered_claims:
        unsupported.append("V770 cannot be claimed as full human completion.")
    if "v129" in run_id_lower and "regression" not in lowered_notes:
        unsupported.append("V129 local positive comparison must retain regression warning.")
    if "v260" in run_id_lower:
        unsupported.append("V260 is hard-blocked and should not be compared as success.")
    if "v999" in run_id_lower and "promotion" in lowered_claims:
        unsupported.append("V999 long-run does not equal promotion.")
    if (
        "sparseconv3d" in lowered_claims
        or "sparseconv" in lowered_claims
        or "modal" in run_id_lower
    ) and "real_backend_confirmed" not in lowered_notes:
        unsupported.append("SparseConv3D success requires real backend evidence.")
    if run.status in {
        RunComparisonStatus.PLANNED,
        RunComparisonStatus.NOT_ENOUGH_EVIDENCE,
        RunComparisonStatus.HARD_BLOCKED,
    } and run.claimed_improvements:
        unsupported.append(f"{run.run_id} has claims but status is {run.status.value}.")
    return unsupported


def _next_actions(run: RunComparisonInput) -> list[str]:
    actions: list[str] = []
    if run.status == RunComparisonStatus.HARD_BLOCKED:
        actions.append(f"{run.run_id}: resolve hard blocker before comparison.")
    if run.artifacts_missing:
        actions.append(f"{run.run_id}: collect missing artifact metadata.")
    if not run.boards or any(board.status != BoardStatus.AVAILABLE for board in run.boards):
        actions.append(f"{run.run_id}: add advisor-ready board inventory.")
    if any("SPARSE" in item or "REAL_BACKEND" in item for item in run.failure_categories):
        actions.append(f"{run.run_id}: collect real sparse backend evidence.")
    return actions
