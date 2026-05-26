"""Hypothesis portfolio construction."""

from __future__ import annotations

from turing_research_plus.hypothesis.finer import formulate_research_question
from turing_research_plus.hypothesis.models import (
    HypothesisPortfolio,
    HypothesisSet,
    ResearchQuestion,
)


def build_portfolio(
    hypothesis_set: HypothesisSet,
    max_items: int = 3,
    portfolio_id: str = "portfolio-1",
) -> HypothesisPortfolio:
    """Select a compact portfolio from ranked hypotheses."""

    selected = hypothesis_set.hypotheses[:max_items]
    questions: list[ResearchQuestion] = [
        formulate_research_question(hypothesis)
        for hypothesis in selected
    ]
    return HypothesisPortfolio(
        portfolio_id=portfolio_id,
        topic=hypothesis_set.topic,
        selected=selected,
        research_questions=questions,
        rationale="Selected highest-scoring falsifiable hypotheses with evidence refs.",
    )
