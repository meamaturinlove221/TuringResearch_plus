"""Thin research.north_star_* tool wrappers."""

from __future__ import annotations

from typing import Any

from turing_research_plus.north_star.models import NorthStarInput, NorthStarStatement, ResearchBrief
from turing_research_plus.north_star.service import NorthStarService


def research_north_star_init(
    workflow_input: NorthStarInput,
    service: NorthStarService,
) -> dict[str, Any]:
    return service.init(workflow_input).model_dump(mode="json")


def research_research_brief_generate(
    workflow_input: NorthStarInput,
    north_star: NorthStarStatement,
    service: NorthStarService,
) -> dict[str, Any]:
    return service.research_brief_generate(workflow_input, north_star).model_dump(mode="json")


def research_goal_decompose(brief: ResearchBrief, service: NorthStarService) -> dict[str, Any]:
    return service.goal_decompose(brief).model_dump(mode="json")


def research_obstacle_analyze(
    workflow_input: NorthStarInput,
    service: NorthStarService,
) -> dict[str, Any]:
    result = service.init(workflow_input)
    return result.obstacle_map.model_dump(mode="json")


def research_direction_rank(
    workflow_input: NorthStarInput,
    service: NorthStarService,
) -> dict[str, Any]:
    evidence = service.collect_evidence(workflow_input)
    return service.direction_rank(workflow_input, evidence).model_dump(mode="json")
