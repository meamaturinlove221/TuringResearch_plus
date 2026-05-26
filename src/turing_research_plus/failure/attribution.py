"""Build failure attribution reports."""

from __future__ import annotations

from turing_research_plus.failure.classifier import classify_failure_text
from turing_research_plus.failure.models import (
    FailureAnalysisInput,
    FailureAttributionReport,
    FailureInstance,
)
from turing_research_plus.failure.taxonomy import default_failure_taxonomy


def build_failure_attribution_report(
    failure: FailureInstance,
) -> FailureAttributionReport:
    """Build one conservative attribution report."""

    category = classify_failure_text(failure.text, failure.category_hint)
    entry = default_failure_taxonomy()[category]
    requires_review = not failure.evidence_refs or category.value.endswith("REQUIRED")
    return FailureAttributionReport(
        failure_id=failure.failure_id,
        related_route_id=failure.related_route_id,
        related_stage_id=failure.related_stage_id,
        related_run_id=failure.related_run_id,
        category=category,
        severity=entry.severity,
        evidence_refs=failure.evidence_refs,
        likely_causes=[entry.description],
        ruled_out_causes=["Experiment success is not inferred from this failure report."],
        next_actions=list(entry.default_next_actions),
        retry_policy=entry.default_retry_policy,
        requires_human_review=requires_review,
    )


def analyze_failures(request: FailureAnalysisInput) -> list[FailureAttributionReport]:
    """Analyze all failures in a request."""

    return [build_failure_attribution_report(failure) for failure in request.failures]
