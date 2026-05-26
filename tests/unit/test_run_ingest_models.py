from __future__ import annotations

from turing_research_plus.failure.models import FailureCategory
from turing_research_plus.run_ingest.models import (
    BackendStatus,
    RunIngestReport,
    RunSourceType,
    RunStatus,
)


def test_run_ingest_report_prevents_success_without_real_backend() -> None:
    report = RunIngestReport(
        run_id="r1",
        route_id="modal_sparseconv_v0",
        source_type=RunSourceType.MODAL_FIXTURE,
        source_path="fixture",
        status=RunStatus.REVIEW_READY_NOT_PROMOTED,
        backend_status=BackendStatus.REAL_BACKEND_MISSING,
    )

    assert FailureCategory.NOT_ENOUGH_EVIDENCE in report.failure_categories
    assert report.requires_human_review is True


def test_run_ingest_report_exports_markdown() -> None:
    report = RunIngestReport(
        run_id="r1",
        route_id="route",
        source_type=RunSourceType.MANUAL_SUMMARY,
        source_path="manual.json",
        status=RunStatus.UNKNOWN,
    )

    assert "# Run Ingest Report" in report.to_markdown()
