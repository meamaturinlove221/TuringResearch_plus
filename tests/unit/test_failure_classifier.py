from turing_research_plus.failure.classifier import classify_failure_text
from turing_research_plus.failure.models import FailureCategory


def test_classifier_detects_missing_assets() -> None:
    assert (
        classify_failure_text("V260 missing adjacent predictions and semantic assets")
        == FailureCategory.MISSING_ASSETS
    )


def test_classifier_detects_sparse_backend_unavailable() -> None:
    assert (
        classify_failure_text("SparseConv3D backend unavailable")
        == FailureCategory.SPARSE_BACKEND_UNAVAILABLE
    )


def test_classifier_detects_report_only() -> None:
    assert classify_failure_text("report-only output") == FailureCategory.REPORT_ONLY


def test_classifier_falls_back_to_human_review() -> None:
    assert classify_failure_text("unclear failure") == FailureCategory.HUMAN_REVIEW_REQUIRED
