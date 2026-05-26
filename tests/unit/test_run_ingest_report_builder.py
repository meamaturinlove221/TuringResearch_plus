from __future__ import annotations

from pathlib import Path

from turing_research_plus.failure.models import FailureCategory
from turing_research_plus.run_ingest.models import BackendStatus, RunSourceType
from turing_research_plus.run_ingest.report_builder import build_run_ingest_report


def test_report_builder_flags_report_only_and_missing_visuals() -> None:
    report = build_run_ingest_report(
        source_type=RunSourceType.THIN_REVIEW_BUNDLE,
        source_path=Path("thin"),
        payload={
            "run_id": "thin",
            "status": "PARTIAL",
            "backend_status": "fallback backend used",
            "artifacts": ["failure_report.md"],
        },
    )

    assert report.backend_status == BackendStatus.FALLBACK_USED
    assert FailureCategory.REPORT_ONLY in report.failure_categories
    assert FailureCategory.FALLBACK_ONLY in report.failure_categories
    assert FailureCategory.VISUAL_PROOF_INSUFFICIENT in report.failure_categories
    assert "board_inventory.md" in report.missing_artifacts


def test_report_builder_selects_best_candidate() -> None:
    report = build_run_ingest_report(
        source_type=RunSourceType.MANUAL_SUMMARY,
        source_path=Path("manual.json"),
        payload={
            "run_id": "manual",
            "status": "PARTIAL",
            "candidates": [
                {"candidate_id": "a", "score": 0.1},
                {"candidate_id": "b", "score": 0.9},
            ],
        },
    )

    assert report.best_candidate is not None
    assert report.best_candidate.candidate_id == "b"
