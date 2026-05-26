"""FINER research question formulation."""

from __future__ import annotations

from turing_research_plus.hypothesis.models import FINERAssessment, Hypothesis, ResearchQuestion


def assess_finer(hypothesis: Hypothesis) -> FINERAssessment:
    """Score a hypothesis with deterministic FINER criteria."""

    feasible = 0.85 if hypothesis.risk_level != "high" else 0.65
    interesting = 0.8
    novel = 0.75 if hypothesis.score >= 0.75 else 0.65
    ethical = 0.95
    relevant = min(0.95, 0.7 + hypothesis.score * 0.2)
    overall = round((feasible + interesting + novel + ethical + relevant) / 5, 3)
    return FINERAssessment(
        feasible=feasible,
        interesting=interesting,
        novel=novel,
        ethical=ethical,
        relevant=round(relevant, 3),
        overall=overall,
    )


def formulate_research_question(
    hypothesis: Hypothesis,
    question_id: str | None = None,
) -> ResearchQuestion:
    """Formulate a precise research question from a hypothesis."""

    finer = assess_finer(hypothesis)
    independent = hypothesis.independent_variables[0]
    dependent = hypothesis.dependent_variables[0]
    return ResearchQuestion(
        question_id=question_id or f"rq-{hypothesis.hypothesis_id}",
        question=(
            f"To what extent does {independent} change {dependent} under "
            f"{hypothesis.boundary_conditions[0]}?"
        ),
        hypothesis_id=hypothesis.hypothesis_id,
        finer_score=finer.overall,
        evidence_refs=hypothesis.evidence_refs,
    )

