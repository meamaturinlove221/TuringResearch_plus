"""Thin research.idea_* tool wrappers."""

from __future__ import annotations

from typing import Any

from tuling_research_plus.hypothesis.models import Hypothesis, HypothesisSet
from tuling_research_plus.ideation.models import IdeaGenerationResult
from tuling_research_plus.ideation.service import CreativeIdeationService


def research_idea_generate(
    hypothesis_set: HypothesisSet,
    service: CreativeIdeationService,
) -> dict[str, Any]:
    return service.idea_generate(hypothesis_set).model_dump(mode="json")


def research_idea_cross_domain(
    hypothesis_set: HypothesisSet,
    service: CreativeIdeationService,
    domain: str = "software reliability",
) -> dict[str, Any]:
    return service.idea_cross_domain(hypothesis_set, domain=domain).model_dump(mode="json")


def research_idea_morphological_matrix(
    hypothesis: Hypothesis,
    service: CreativeIdeationService,
) -> dict[str, Any]:
    return service.idea_morphological_matrix(hypothesis).model_dump(mode="json")


def research_idea_quality_diversity_filter(
    generation: IdeaGenerationResult,
    service: CreativeIdeationService,
) -> dict[str, Any]:
    return service.idea_quality_diversity_filter(generation).model_dump(mode="json")

