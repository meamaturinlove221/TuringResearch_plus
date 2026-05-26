"""North Star workflow models."""

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator

from turing_research_plus.artifacts.models import EvidenceRef


class StartMode(StrEnum):
    """North Star start modes."""

    COLD = "cold_start"
    WARM = "warm_start"
    HOT = "hot_start"


class NorthStarInput(BaseModel):
    """Input for North Star workflow."""

    model_config = ConfigDict(extra="forbid")

    vague_user_intent: str = ""
    known_constraints: list[str] = Field(default_factory=list)
    available_resources: list[str] = Field(default_factory=list)
    current_research_context: str = ""
    advisor_comments: list[str] = Field(default_factory=list)


class NorthStarStatement(BaseModel):
    """Clear research direction statement."""

    model_config = ConfigDict(extra="forbid")

    statement: str = Field(min_length=1)
    mode: StartMode
    rationale: str = Field(min_length=1)
    evidence: list[EvidenceRef] = Field(min_length=1)


class ResearchBrief(BaseModel):
    """Research brief generated from a North Star statement."""

    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=1)
    problem: str = Field(min_length=1)
    research_goal: str = Field(min_length=1)
    scope: str = Field(min_length=1)
    constraints: list[str] = Field(default_factory=list)
    resources: list[str] = Field(default_factory=list)
    evidence: list[EvidenceRef] = Field(min_length=1)


class GoalNode(BaseModel):
    """Goal tree node."""

    model_config = ConfigDict(extra="forbid")

    goal_id: str = Field(min_length=1)
    description: str = Field(min_length=1)
    children: list["GoalNode"] = Field(default_factory=list)


class GoalTree(BaseModel):
    """Decomposed research goals."""

    model_config = ConfigDict(extra="forbid")

    root: GoalNode


class Obstacle(BaseModel):
    """Research obstacle."""

    model_config = ConfigDict(extra="forbid")

    obstacle_id: str = Field(min_length=1)
    description: str = Field(min_length=1)
    severity: str = "medium"
    rejected: bool = False
    mitigation: str | None = None


class ObstacleMap(BaseModel):
    """Obstacle map for a research direction."""

    model_config = ConfigDict(extra="forbid")

    obstacles: list[Obstacle] = Field(default_factory=list)

    @property
    def has_rejection(self) -> bool:
        return any(obstacle.rejected for obstacle in self.obstacles)


class DirectionCandidate(BaseModel):
    """Candidate research direction."""

    model_config = ConfigDict(extra="forbid")

    direction_id: str = Field(min_length=1)
    statement: str = Field(min_length=1)
    score: float = Field(ge=0.0, le=1.0)
    evidence: list[EvidenceRef] = Field(min_length=1)
    rejected: bool = False
    rejection_reason: str | None = None


class DirectionCandidates(BaseModel):
    """Ranked research direction candidates."""

    model_config = ConfigDict(extra="forbid")

    candidates: list[DirectionCandidate] = Field(min_length=1)

    @model_validator(mode="after")
    def sort_candidates(self) -> "DirectionCandidates":
        self.candidates.sort(key=lambda candidate: candidate.score, reverse=True)
        return self


class NorthStarResult(BaseModel):
    """North Star workflow output."""

    model_config = ConfigDict(extra="forbid")

    north_star: NorthStarStatement
    research_brief: ResearchBrief
    goal_tree: GoalTree
    obstacle_map: ObstacleMap
    direction_candidates: DirectionCandidates
    backtracked: bool = False
    warnings: list[str] = Field(default_factory=list)

    def model_summary(self) -> dict[str, Any]:
        """Return a compact serializable summary."""

        return {
            "statement": self.north_star.statement,
            "mode": self.north_star.mode,
            "title": self.research_brief.title,
            "top_direction": self.direction_candidates.candidates[0].statement,
            "backtracked": self.backtracked,
        }
