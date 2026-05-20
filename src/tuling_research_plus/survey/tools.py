"""Thin research.survey_* tool wrappers."""

from __future__ import annotations

from typing import Any

from tuling_research_plus.survey.models import SurveyInput, SurveyResult
from tuling_research_plus.survey.service import LiteratureSurveyService


def research_survey_plan(
    survey_input: SurveyInput,
    service: LiteratureSurveyService,
) -> dict[str, Any]:
    return service.plan(survey_input).model_dump(mode="json")


def research_survey_run(
    survey_input: SurveyInput,
    service: LiteratureSurveyService,
    dry_run: bool = True,
) -> dict[str, Any]:
    return service.run(survey_input, dry_run=dry_run).model_dump(mode="json")


def research_survey_status(result: SurveyResult) -> dict[str, Any]:
    return {"status": result.status, "blocked_reason": result.blocked_reason}


def research_survey_export(result: SurveyResult) -> str:
    return result.to_markdown()
