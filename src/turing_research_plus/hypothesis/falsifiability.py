"""Falsifiability checks and hypothesis generation."""

from __future__ import annotations

from turing_research_plus.hypothesis.models import (
    ExperimentRequirement,
    FalsifiabilityCriteria,
    GapPriority,
    Hypothesis,
    RiskLevel,
)


def build_hypothesis(priority: GapPriority, index: int = 1) -> Hypothesis:
    """Build a falsifiable hypothesis from one prioritized gap."""

    risk_level = RiskLevel.HIGH if priority.score < 0.65 else RiskLevel.MEDIUM
    if priority.score >= 0.82:
        risk_level = RiskLevel.LOW
    return Hypothesis(
        hypothesis_id=f"hypothesis-{index}",
        statement=(
            "If explicit evidence gates are introduced, then uncertainty around "
            f"{priority.description} will decrease."
        ),
        mechanism=(
            "Evidence gates force each workflow claim to cite source-backed validation "
            "before downstream synthesis."
        ),
        independent_variables=["evidence gate strictness", "minimum evidence count"],
        dependent_variables=["unsupported claim rate", "validated gap confidence"],
        control_variables=["topic scope", "survey strategy", "available corpus size"],
        falsifiability_criteria=FalsifiabilityCriteria(
            observable_prediction=(
                "Unsupported claim rate decreases after evidence gates are applied."
            ),
            falsifying_observation=(
                "Unsupported claim rate stays the same or increases under the gate."
            ),
            measurement_window="one dry-run campaign",
            minimum_test="compare baseline workflow output against gated workflow output",
        ),
        success_criteria=[
            "unsupported claim rate decreases",
            "validated gap confidence does not decrease",
        ],
        failure_interpretation=(
            "The gate may be too weak, evidence quality may be insufficient, or the "
            "gap may need reformulation."
        ),
        required_experiment=ExperimentRequirement(
            design="controlled dry-run comparison",
            required_data=["baseline output", "gated output", "evidence audit table"],
            measurement="difference in unsupported claim rate",
        ),
        boundary_conditions=[
            "Applies to evidence-backed research workflow artifacts.",
            "Does not apply when no authorized evidence is available.",
        ],
        evidence_refs=priority.evidence,
        risk_level=risk_level,
    )


def is_falsifiable(hypothesis: Hypothesis) -> bool:
    """Return whether a hypothesis has all falsifiability fields populated."""

    criteria = hypothesis.falsifiability_criteria
    return all(
        [
            bool(criteria.observable_prediction.strip()),
            bool(criteria.falsifying_observation.strip()),
            bool(criteria.measurement_window.strip()),
            bool(criteria.minimum_test.strip()),
            bool(hypothesis.required_experiment.required_data),
            bool(hypothesis.success_criteria),
            bool(hypothesis.failure_interpretation.strip()),
        ]
    )
