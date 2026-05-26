"""Thin research.hypothesis_* tool wrappers."""

from __future__ import annotations

from typing import Any

from turing_research_plus.hypothesis.models import GapPriorityReport, Hypothesis, HypothesisSet
from turing_research_plus.hypothesis.service import HypothesisFormationService
from turing_research_plus.insight.models import GapValidationReport, InsightReport


def research_gap_prioritize(
    gap_report: GapValidationReport,
    service: HypothesisFormationService,
) -> dict[str, Any]:
    return service.gap_prioritize(gap_report).model_dump(mode="json")


def research_hypothesis_generate(
    gap_priorities: GapPriorityReport,
    service: HypothesisFormationService,
    insight_report: InsightReport | None = None,
) -> dict[str, Any]:
    return service.hypothesis_generate(gap_priorities, insight_report).model_dump(mode="json")


def research_hypothesis_operationalize(
    hypothesis: Hypothesis,
    service: HypothesisFormationService,
) -> dict[str, Any]:
    return service.hypothesis_operationalize(hypothesis).model_dump(mode="json")


def research_research_question_formulate(
    hypothesis: Hypothesis,
    service: HypothesisFormationService,
) -> dict[str, Any]:
    return service.research_question_formulate(hypothesis).model_dump(mode="json")


def research_hypothesis_portfolio_build(
    hypothesis_set: HypothesisSet,
    service: HypothesisFormationService,
    max_items: int = 3,
) -> dict[str, Any]:
    return service.hypothesis_portfolio_build(hypothesis_set, max_items=max_items).model_dump(
        mode="json"
    )
