"""Candidate scoring for convergence."""

from __future__ import annotations

from tuling_research_plus.convergence.models import (
    CandidateKind,
    CandidateScore,
    ConvergenceCandidate,
)
from tuling_research_plus.hypothesis.models import Hypothesis, RiskLevel
from tuling_research_plus.ideation.models import IdeaCandidate, IdeaRisk


def from_idea(candidate: IdeaCandidate) -> ConvergenceCandidate:
    """Normalize an IdeaCandidate for convergence."""

    return ConvergenceCandidate(
        candidate_id=candidate.idea_id,
        kind=CandidateKind.IDEA,
        title=candidate.title,
        mechanism=candidate.mechanism,
        expected_gain=candidate.expected_gain,
        feasibility=candidate.feasibility,
        novelty=candidate.novelty,
        risk=candidate.risk,
        required_resources=candidate.required_resources,
        evidence_refs=candidate.evidence_refs,
        metadata={"hypothesis_link": candidate.hypothesis_link},
    )


def from_hypothesis(candidate: Hypothesis) -> ConvergenceCandidate:
    """Normalize a Hypothesis for convergence."""

    return ConvergenceCandidate(
        candidate_id=candidate.hypothesis_id,
        kind=CandidateKind.HYPOTHESIS,
        title=candidate.statement,
        mechanism=candidate.mechanism,
        expected_gain="Testable knowledge gain from falsifiable hypothesis.",
        feasibility=_feasibility_from_risk(candidate.risk_level),
        novelty=candidate.score,
        risk=candidate.risk_level,
        required_resources=candidate.required_experiment.required_data,
        evidence_refs=candidate.evidence_refs,
        metadata={"required_experiment": candidate.required_experiment.model_dump(mode="json")},
    )


def score_candidate(candidate: ConvergenceCandidate) -> CandidateScore:
    """Score one candidate with explicit deterministic criteria."""

    evidence_strength = min(1.0, len(candidate.evidence_refs) * 0.2 + 0.6)
    feasibility = candidate.feasibility
    novelty = candidate.novelty
    expected_gain = _expected_gain_score(candidate.expected_gain)
    risk_adjustment = _risk_adjustment(candidate.risk)
    total = round(
        max(
            0.0,
            min(
                1.0,
                0.3 * evidence_strength
                + 0.25 * feasibility
                + 0.2 * novelty
                + 0.15 * expected_gain
                + 0.1 * risk_adjustment,
            ),
        ),
        3,
    )
    return CandidateScore(
        candidate_id=candidate.candidate_id,
        total_score=total,
        criteria={
            "evidence_strength": round(evidence_strength, 3),
            "feasibility": round(feasibility, 3),
            "novelty": round(novelty, 3),
            "expected_gain": round(expected_gain, 3),
            "risk_adjustment": round(risk_adjustment, 3),
        },
        rationale="Weighted deterministic convergence score.",
        evidence_refs=candidate.evidence_refs,
    )


def score_candidates(candidates: list[ConvergenceCandidate]) -> list[CandidateScore]:
    """Score and rank candidates."""

    return sorted(
        [score_candidate(candidate) for candidate in candidates],
        key=lambda score: score.total_score,
        reverse=True,
    )


def scoring_matrix(scores: list[CandidateScore]) -> dict[str, dict[str, float]]:
    """Return scoring matrix keyed by candidate id."""

    return {score.candidate_id: score.criteria for score in scores}


def _feasibility_from_risk(risk: RiskLevel) -> float:
    if risk == RiskLevel.LOW:
        return 0.85
    if risk == RiskLevel.MEDIUM:
        return 0.7
    return 0.55


def _expected_gain_score(expected_gain: str) -> float:
    lowered = expected_gain.lower()
    if "release" in lowered or "implementation" in lowered:
        return 0.85
    if "lower" in lowered or "reduce" in lowered or "sharper" in lowered:
        return 0.8
    return 0.7


def _risk_adjustment(risk: str) -> float:
    if risk == IdeaRisk.LOW or risk == RiskLevel.LOW:
        return 0.9
    if risk == IdeaRisk.MEDIUM or risk == RiskLevel.MEDIUM:
        return 0.7
    return 0.45

