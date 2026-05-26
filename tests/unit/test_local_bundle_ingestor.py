from __future__ import annotations

from pathlib import Path

from turing_research_plus.failure.models import FailureCategory
from turing_research_plus.run_ingest.local_bundle_ingestor import ingest_local_bundle
from turing_research_plus.run_ingest.models import RunIngestRequest, RunSourceType

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = (
    ROOT
    / "examples"
    / "vggt-human-prior-survey"
    / "run_ingest_fixtures"
    / "modal_run_fixture"
)


def test_local_bundle_ingestor_reads_fixture_without_running_modal() -> None:
    report = ingest_local_bundle(
        RunIngestRequest(source_type=RunSourceType.MODAL_FIXTURE, source_path=FIXTURE)
    )

    assert report.run_id == "modal-sparseconv-fixture-001"
    assert "predictions.npz" in report.missing_artifacts
    assert FailureCategory.SPARSE_BACKEND_UNAVAILABLE in report.failure_categories
    assert report.evidence_updates[0]["status"] == "not-enough-evidence"
