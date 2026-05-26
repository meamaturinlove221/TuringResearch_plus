"""North Star workflow service."""

from __future__ import annotations

from typing import Protocol

from turing_research_plus.artifacts.models import EvidenceRef
from turing_research_plus.north_star.models import (
    DirectionCandidate,
    DirectionCandidates,
    GoalNode,
    GoalTree,
    NorthStarInput,
    NorthStarResult,
    NorthStarStatement,
    Obstacle,
    ObstacleMap,
    ResearchBrief,
    StartMode,
)


class PaperService(Protocol):
    """Protocol for paper evidence services."""

    def evidence_for_topic(self, topic: str) -> list[EvidenceRef]: ...


class WebService(Protocol):
    """Protocol for web evidence services."""

    def evidence_for_topic(self, topic: str) -> list[EvidenceRef]: ...


class NorthStarService:
    """Convert vague intent into a research brief and direction."""

    def __init__(
        self,
        paper_service: PaperService | None = None,
        web_service: WebService | None = None,
    ) -> None:
        self.paper_service = paper_service
        self.web_service = web_service

    def init(self, workflow_input: NorthStarInput) -> NorthStarResult:
        """Run the North Star workflow."""

        mode = self._start_mode(workflow_input)
        evidence = self._collect_evidence(workflow_input)
        candidates = self.direction_rank(workflow_input, evidence)
        obstacle_map = self.obstacle_analyze(workflow_input, candidates)
        backtracked = False
        warnings: list[str] = []
        if obstacle_map.has_rejection:
            candidates = self._backtrack_candidates(candidates, obstacle_map)
            backtracked = True
            warnings.append("Obstacle rejection triggered direction backtrack.")

        north_star = NorthStarStatement(
            statement=candidates.candidates[0].statement,
            mode=mode,
            rationale=f"Selected from {mode} intent with available evidence.",
            evidence=candidates.candidates[0].evidence,
        )
        brief = self.research_brief_generate(workflow_input, north_star)
        return NorthStarResult(
            north_star=north_star,
            research_brief=brief,
            goal_tree=self.goal_decompose(brief),
            obstacle_map=obstacle_map,
            direction_candidates=candidates,
            backtracked=backtracked,
            warnings=warnings,
        )

    def research_brief_generate(
        self,
        workflow_input: NorthStarInput,
        north_star: NorthStarStatement,
    ) -> ResearchBrief:
        """Generate a ResearchBrief."""

        title = self._title_from_statement(north_star.statement)
        return ResearchBrief(
            title=title,
            problem=self._problem_from_input(workflow_input),
            research_goal=north_star.statement,
            scope=workflow_input.current_research_context or "Initial scope to be refined.",
            constraints=workflow_input.known_constraints,
            resources=workflow_input.available_resources,
            evidence=north_star.evidence,
        )

    def goal_decompose(self, brief: ResearchBrief) -> GoalTree:
        """Decompose a research brief into a goal tree."""

        return GoalTree(
            root=GoalNode(
                goal_id="goal-root",
                description=brief.research_goal,
                children=[
                    GoalNode(goal_id="goal-1", description="Map existing evidence."),
                    GoalNode(goal_id="goal-2", description="Identify unresolved obstacles."),
                    GoalNode(goal_id="goal-3", description="Define evaluation criteria."),
                ],
            )
        )

    def obstacle_analyze(
        self,
        workflow_input: NorthStarInput,
        candidates: DirectionCandidates,
    ) -> ObstacleMap:
        """Analyze obstacles and mark rejected directions."""

        obstacles: list[Obstacle] = []
        constraint_text = " ".join(workflow_input.known_constraints).lower()
        if "impossible" in constraint_text or "no data" in constraint_text:
            obstacles.append(
                Obstacle(
                    obstacle_id="obstacle-1",
                    description="Constraint rejects the top direction.",
                    severity="high",
                    rejected=True,
                    mitigation="Backtrack to a narrower evidence-first direction.",
                )
            )
        if not obstacles:
            obstacles.append(
                Obstacle(
                    obstacle_id="obstacle-1",
                    description="Scope drift risk.",
                    severity="medium",
                    mitigation="Keep a narrow research brief.",
                )
            )
        return ObstacleMap(obstacles=obstacles)

    def direction_rank(
        self,
        workflow_input: NorthStarInput,
        evidence: list[EvidenceRef],
    ) -> DirectionCandidates:
        """Rank candidate research directions deterministically."""

        topic = self._topic(workflow_input)
        base_evidence = evidence or [self._fallback_evidence(topic)]
        candidates = [
            DirectionCandidate(
                direction_id="direction-1",
                statement=f"Study {topic} through evidence-backed workflow design.",
                score=0.9,
                evidence=base_evidence,
            ),
            DirectionCandidate(
                direction_id="direction-2",
                statement=f"Map constraints and evaluation criteria for {topic}.",
                score=0.7,
                evidence=base_evidence,
            ),
        ]
        return DirectionCandidates(candidates=candidates)

    def collect_evidence(self, workflow_input: NorthStarInput) -> list[EvidenceRef]:
        """Collect evidence through fake paper/web service protocols."""

        return self._collect_evidence(workflow_input)

    def _backtrack_candidates(
        self,
        candidates: DirectionCandidates,
        obstacle_map: ObstacleMap,
    ) -> DirectionCandidates:
        reason = "; ".join(obstacle.description for obstacle in obstacle_map.obstacles)
        updated = []
        for index, candidate in enumerate(candidates.candidates):
            if index == 0:
                updated.append(
                    candidate.model_copy(
                        update={
                            "rejected": True,
                            "rejection_reason": reason,
                            "score": 0.1,
                        }
                    )
                )
            else:
                updated.append(candidate.model_copy(update={"score": 0.95}))
        return DirectionCandidates(candidates=updated)

    def _start_mode(self, workflow_input: NorthStarInput) -> StartMode:
        intent = workflow_input.vague_user_intent.strip()
        if not intent and not workflow_input.current_research_context:
            return StartMode.COLD
        if len(intent.split()) >= 5 and workflow_input.current_research_context:
            return StartMode.HOT
        return StartMode.WARM

    def _collect_evidence(self, workflow_input: NorthStarInput) -> list[EvidenceRef]:
        topic = self._topic(workflow_input)
        evidence: list[EvidenceRef] = []
        if self.paper_service is not None:
            evidence.extend(self.paper_service.evidence_for_topic(topic))
        if self.web_service is not None:
            evidence.extend(self.web_service.evidence_for_topic(topic))
        return evidence

    def _fallback_evidence(self, topic: str) -> EvidenceRef:
        return EvidenceRef(
            source_id="north-star:input",
            locator="user-intent",
            quote=topic,
            confidence=0.5,
        )

    def _topic(self, workflow_input: NorthStarInput) -> str:
        if workflow_input.vague_user_intent.strip():
            return workflow_input.vague_user_intent.strip()
        if workflow_input.current_research_context.strip():
            return workflow_input.current_research_context.strip()
        return "an under-specified research direction"

    def _problem_from_input(self, workflow_input: NorthStarInput) -> str:
        if workflow_input.advisor_comments:
            return workflow_input.advisor_comments[0]
        return f"Clarify research direction for {self._topic(workflow_input)}."

    def _title_from_statement(self, statement: str) -> str:
        words = statement.rstrip(".").split()
        return " ".join(words[:8])
