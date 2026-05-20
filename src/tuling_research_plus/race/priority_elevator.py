"""Race Mode Priority Elevator."""

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

from tuling_research_plus.race.models import IdeaCard, SourceHygieneStatus


class RacePriority(StrEnum):
    """Priority elevator levels."""

    P0 = "P0"
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"


class PriorityRecommendation(BaseModel):
    """Priority scoring result."""

    model_config = ConfigDict(extra="forbid")

    idea_id: str = Field(min_length=1)
    priority_score: float = Field(ge=0.0, le=1.0)
    priority: RacePriority
    strategic_fit: float = Field(ge=0.0, le=1.0)
    recommendation: str = Field(min_length=1)
    should_create_feature_capsule: bool
    blocked_by_source_hygiene: bool = False
    rationale: str = Field(min_length=1)


def priority_score(idea: IdeaCard, strategic_fit: float = 0.7) -> PriorityRecommendation:
    """Score an IdeaCard and decide whether to recommend a Feature Capsule."""

    bounded_fit = max(0.0, min(1.0, strategic_fit))
    score = round(
        0.30 * idea.value_score
        + 0.25 * idea.urgency_score
        + 0.20 * idea.feasibility_score
        + 0.15 * idea.novelty_score
        + 0.10 * bounded_fit,
        3,
    )
    blocked = idea.hygiene_gate.status != SourceHygieneStatus.PASSED
    priority = _priority_from_score(score)
    if blocked and priority in {RacePriority.P0, RacePriority.P1}:
        priority = RacePriority.P2
    should_capsule = priority == RacePriority.P1 and not blocked
    return PriorityRecommendation(
        idea_id=idea.idea_id,
        priority_score=score,
        priority=priority,
        strategic_fit=bounded_fit,
        recommendation=_recommendation(priority),
        should_create_feature_capsule=should_capsule,
        blocked_by_source_hygiene=blocked,
        rationale=_rationale(priority, score, blocked),
    )


def race_priority_score(idea: IdeaCard, strategic_fit: float = 0.7) -> dict[str, object]:
    """Thin race.priority_score wrapper."""

    return priority_score(idea, strategic_fit=strategic_fit).model_dump(mode="json")


def _priority_from_score(score: float) -> RacePriority:
    if score >= 0.85:
        return RacePriority.P0
    if score >= 0.7:
        return RacePriority.P1
    if score >= 0.45:
        return RacePriority.P2
    return RacePriority.P3


def _recommendation(priority: RacePriority) -> str:
    if priority == RacePriority.P0:
        return "prototype immediately"
    if priority == RacePriority.P1:
        return "create feature capsule this sprint"
    if priority == RacePriority.P2:
        return "document and monitor"
    return "archive"


def _rationale(priority: RacePriority, score: float, blocked: bool) -> str:
    if blocked:
        return "Source hygiene did not pass, so the idea cannot become P0/P1."
    return f"Priority {priority} assigned from weighted score {score}."

