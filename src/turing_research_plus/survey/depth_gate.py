"""Depth and evidence hard gates for literature survey."""

from __future__ import annotations

from turing_research_plus.survey.models import (
    PaperScreeningTable,
    SurveyInput,
    SurveyStrategy,
)


def full_text_ratio(screening: PaperScreeningTable) -> float:
    """Return included full-text ratio."""

    if screening.included_count == 0:
        return 0.0
    return screening.full_text_count / screening.included_count


def evaluate_depth_gates(
    survey_input: SurveyInput,
    screening: PaperScreeningTable,
    conclusion_strength: str = "survey",
) -> list[str]:
    """Return blocking reasons for survey hard gates."""

    blockers: list[str] = []
    if conclusion_strength == "overview":
        blockers.append("overview cannot produce strong conclusions")
    if screening.included_count < survey_input.min_papers:
        blockers.append("not enough included papers")
    if survey_input.strategy in {SurveyStrategy.SYSTEMATIC, SurveyStrategy.DEEP}:
        if screening.full_text_count == 0:
            blockers.append("survey cannot rely only on abstracts")
    if survey_input.strategy == SurveyStrategy.DEEP:
        ratio = full_text_ratio(screening)
        if ratio < survey_input.full_text_ratio:
            blockers.append("deep survey full_text_ratio not satisfied")
    return blockers
