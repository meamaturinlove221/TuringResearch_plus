"""Capsule-local tool wrappers for failure taxonomy."""

from __future__ import annotations

from typing import Any

from turing_research_plus.failure.attribution import analyze_failures
from turing_research_plus.failure.models import FailureAnalysisInput


def experiment_failure_analyze(request: FailureAnalysisInput) -> dict[str, Any]:
    """Analyze failure instances and return JSON-safe reports."""

    return {"reports": [report.model_dump(mode="json") for report in analyze_failures(request)]}
