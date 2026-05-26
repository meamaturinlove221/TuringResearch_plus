"""Thin research.insight_* tool wrappers."""

from __future__ import annotations

from typing import Any

from turing_research_plus.insight.models import GapValidationReport
from turing_research_plus.insight.service import DeepInsightService
from turing_research_plus.survey.models import LiteratureSurveyArtifact


def research_gap_analyze(
    survey_artifact: LiteratureSurveyArtifact,
    service: DeepInsightService,
) -> dict[str, Any]:
    return service.gap_analyze(survey_artifact).model_dump(mode="json")


def research_insight_generate(
    gap_report: GapValidationReport,
    service: DeepInsightService,
) -> dict[str, Any]:
    return service.insight_generate(gap_report).model_dump(mode="json")


def research_boundary_map(
    gap_report: GapValidationReport,
    service: DeepInsightService,
) -> dict[str, Any]:
    return service.boundary_map(gap_report).model_dump(mode="json")


def research_sensitivity_probe(
    gap_report: GapValidationReport,
    service: DeepInsightService,
) -> dict[str, Any]:
    return service.sensitivity_probe(gap_report).model_dump(mode="json")


def research_problem_reformulate(
    gap_report: GapValidationReport,
    service: DeepInsightService,
) -> dict[str, Any]:
    return service.problem_reformulate(gap_report).model_dump(mode="json")
