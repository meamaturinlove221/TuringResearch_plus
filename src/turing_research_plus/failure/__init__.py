"""Failure Taxonomy Engine for TuringResearch Plus."""

from turing_research_plus.failure.attribution import build_failure_attribution_report
from turing_research_plus.failure.classifier import classify_failure_text
from turing_research_plus.failure.models import (
    FailureAnalysisInput,
    FailureAttributionReport,
    FailureCategory,
    FailureInstance,
    FailureSeverity,
    RetryPolicy,
)
from turing_research_plus.failure.next_action import next_actions_for_category
from turing_research_plus.failure.taxonomy import default_failure_taxonomy

__all__ = [
    "FailureAnalysisInput",
    "FailureAttributionReport",
    "FailureCategory",
    "FailureInstance",
    "FailureSeverity",
    "RetryPolicy",
    "build_failure_attribution_report",
    "classify_failure_text",
    "default_failure_taxonomy",
    "next_actions_for_category",
]
