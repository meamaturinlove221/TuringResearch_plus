"""Deterministic fake idea generators."""

from __future__ import annotations

from turing_research_plus.hypothesis.models import Hypothesis, HypothesisSet
from turing_research_plus.ideation.models import (
    IdeaCandidate,
    IdeaClusterKey,
    IdeaGenerationResult,
    IdeaRisk,
)
from turing_research_plus.ideation.morphological_matrix import build_morphological_matrix


def generate_ideas(
    hypothesis_set: HypothesisSet,
    result_id: str = "idea-generation-1",
) -> IdeaGenerationResult:
    """Generate deterministic idea candidates from hypotheses."""

    candidates: list[IdeaCandidate] = []
    for index, hypothesis in enumerate(hypothesis_set.hypotheses, start=1):
        candidates.extend(_ideas_for_hypothesis(hypothesis, index))
    return IdeaGenerationResult(
        result_id=result_id,
        topic=hypothesis_set.topic,
        candidates=candidates,
    )


def generate_cross_domain_ideas(
    hypothesis_set: HypothesisSet,
    domain: str = "software reliability",
) -> IdeaGenerationResult:
    """Generate deterministic cross-domain idea candidates."""

    base = generate_ideas(hypothesis_set, result_id="cross-domain-ideas")
    candidates = [
        candidate.model_copy(
            update={
                "idea_id": f"{candidate.idea_id}-cross",
                "title": f"{candidate.title} via {domain}",
                "mechanism": f"{candidate.mechanism} adapted from {domain}",
                "novelty": min(1.0, candidate.novelty + 0.08),
                "why_not_duplicate": (
                    f"Uses {domain} analogy rather than a direct workflow gate variant."
                ),
                "cluster_key": candidate.cluster_key.model_copy(
                    update={"model_component": f"{domain} analogy"}
                ),
            }
        )
        for candidate in base.candidates
    ]
    return IdeaGenerationResult(
        result_id="cross-domain-ideas",
        topic=base.topic,
        candidates=candidates,
    )


def _ideas_for_hypothesis(hypothesis: Hypothesis, index: int) -> list[IdeaCandidate]:
    matrix = build_morphological_matrix(hypothesis)
    combinations = matrix.combinations()[:2]
    ideas: list[IdeaCandidate] = []
    for variant, row in enumerate(combinations, start=1):
        mechanism = row["mechanism"]
        required_data = row["required_data"]
        model_component = row["model_component"]
        evaluation_target = row["evaluation_target"]
        risk = IdeaRisk(hypothesis.risk_level)
        ideas.append(
            IdeaCandidate(
                idea_id=f"idea-{index}-{variant}",
                title=f"Evaluate {model_component} for {evaluation_target}",
                hypothesis_link=hypothesis.hypothesis_id,
                mechanism=mechanism,
                novelty=max(0.0, min(1.0, hypothesis.score + 0.04 * variant)),
                feasibility=max(0.0, min(1.0, 0.88 - 0.06 * variant)),
                risk=risk,
                expected_gain=f"Sharper evidence for {hypothesis.statement}",
                required_resources=[required_data],
                nearest_existing_work=hypothesis.required_experiment.design,
                why_not_duplicate=(
                    "Uses a distinct mechanism/data/component/evaluation/risk cluster."
                ),
                evidence_refs=hypothesis.evidence_refs,
                cluster_key=IdeaClusterKey(
                    mechanism=mechanism,
                    required_data=required_data,
                    model_component=model_component,
                    evaluation_target=evaluation_target,
                    risk_profile=risk,
                ),
            )
        )
    return ideas
