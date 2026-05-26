import pytest

from turing_research_plus.failure.models import (
    FailureAttributionReport,
    FailureCategory,
    FailureSeverity,
    RetryPolicy,
)


def test_failure_report_requires_evidence_or_human_review() -> None:
    with pytest.raises(ValueError, match="requires evidence_refs"):
        FailureAttributionReport(
            failure_id="f1",
            category=FailureCategory.NOT_ENOUGH_EVIDENCE,
            severity=FailureSeverity.HIGH,
            likely_causes=["missing"],
            next_actions=["collect evidence"],
            retry_policy=RetryPolicy.REQUIRES_HUMAN_REVIEW,
        )


def test_failure_report_markdown_contains_category() -> None:
    report = FailureAttributionReport(
        failure_id="f1",
        category=FailureCategory.HUMAN_REVIEW_REQUIRED,
        severity=FailureSeverity.MEDIUM,
        likely_causes=["ambiguous"],
        next_actions=["review"],
        retry_policy=RetryPolicy.REQUIRES_HUMAN_REVIEW,
        requires_human_review=True,
    )

    assert "HUMAN_REVIEW_REQUIRED" in report.to_markdown()
