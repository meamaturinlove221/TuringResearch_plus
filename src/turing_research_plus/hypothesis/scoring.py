"""Gap and hypothesis scoring helpers."""

from __future__ import annotations

from turing_research_plus.hypothesis.models import GapPriority, GapPriorityReport, Hypothesis
from turing_research_plus.insight.models import GapValidationReport


def prioritize_gaps(
    gap_report: GapValidationReport,
    report_id: str = "gap-priority-1",
) -> GapPriorityReport:
    """Rank validated gaps with deterministic local scoring."""

    priorities = [
        GapPriority(
            gap_id=gap.gap_id,
            description=gap.description,
            score=_gap_score(gap.confidence, len(gap.evidence), index),
            rationale="Prioritized by validation confidence and available evidence.",
            evidence=gap.evidence,
        )
        for index, gap in enumerate(gap_report.gaps)
    ]
    return GapPriorityReport(
        report_id=report_id,
        topic=gap_report.topic,
        priorities=priorities,
    )


def score_hypothesis(hypothesis: Hypothesis, priority: GapPriority) -> Hypothesis:
    """Return a scored copy of a hypothesis."""

    risk_penalty = {"low": 0.0, "medium": 0.08, "high": 0.16}[hypothesis.risk_level]
    variable_bonus = min(
        0.1,
        0.02
        * (
            len(hypothesis.independent_variables)
            + len(hypothesis.dependent_variables)
            + len(hypothesis.control_variables)
        ),
    )
    score = min(1.0, max(0.0, priority.score + variable_bonus - risk_penalty))
    return hypothesis.model_copy(update={"score": round(score, 3)})


def _gap_score(confidence: float, evidence_count: int, index: int) -> float:
    evidence_bonus = min(0.2, evidence_count * 0.05)
    rank_penalty = min(0.2, index * 0.03)
    return round(min(1.0, max(0.0, confidence + evidence_bonus - rank_penalty)), 3)
