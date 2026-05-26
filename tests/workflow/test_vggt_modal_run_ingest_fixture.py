from __future__ import annotations

from pathlib import Path

from turing_research_plus.failure.models import FailureCategory
from turing_research_plus.run_ingest.models import RunIngestRequest, RunSourceType
from turing_research_plus.run_ingest.tools import ingest_experiment_run

ROOT = Path(__file__).resolve().parents[2]
EXAMPLE = ROOT / "examples" / "vggt-human-prior-survey"
FIXTURE = EXAMPLE / "run_ingest_fixtures" / "modal_run_fixture"


def test_vggt_modal_run_ingest_fixture_is_not_success_claim() -> None:
    report = ingest_experiment_run(
        RunIngestRequest(source_type=RunSourceType.MODAL_FIXTURE, source_path=FIXTURE)
    )

    assert report.status == "ROUTE_EXHAUSTED_WITH_FAILURE_ANALYSIS"
    assert report.backend_status == "real_backend_missing"
    assert "predictions.npz" in report.missing_artifacts
    assert "board_inventory.md" in report.missing_artifacts
    assert "cleanup_report.md" in report.missing_artifacts
    assert FailureCategory.REAL_BACKEND_UNAVAILABLE in report.failure_categories
    assert FailureCategory.MISSING_ASSETS in report.failure_categories
    assert FailureCategory.VISUAL_PROOF_INSUFFICIENT in report.failure_categories
    assert report.evidence_updates[0]["status"] == "not-enough-evidence"
    assert report.requires_human_review is True


def test_run_ingest_report_example_exists() -> None:
    text = (EXAMPLE / "run_ingest_report.md").read_text(encoding="utf-8")

    assert "not-enough-evidence" in text
    assert "SparseConv3D" not in text or "success" not in text
