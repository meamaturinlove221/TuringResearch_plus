import pytest
from pydantic import ValidationError

from tuling_research_plus.artifacts.models import EvidenceRef
from tuling_research_plus.hypothesis.falsifiability import build_hypothesis
from tuling_research_plus.hypothesis.models import GapPriority, Hypothesis


def evidence() -> EvidenceRef:
    return EvidenceRef(
        source_id="paper-1",
        locator="section-3",
        quote="Evidence gates reduce unsupported claims.",
    )


def priority() -> GapPriority:
    return GapPriority(
        gap_id="gap-1",
        description="Few studies validate workflow gates.",
        score=0.9,
        rationale="High confidence and enough evidence.",
        evidence=[evidence()],
    )


def test_hypothesis_contains_required_fields() -> None:
    hypothesis = build_hypothesis(priority())

    assert hypothesis.statement
    assert hypothesis.mechanism
    assert hypothesis.independent_variables
    assert hypothesis.dependent_variables
    assert hypothesis.control_variables
    assert hypothesis.falsifiability_criteria.falsifying_observation
    assert hypothesis.success_criteria
    assert hypothesis.failure_interpretation
    assert hypothesis.required_experiment.required_data
    assert hypothesis.boundary_conditions
    assert hypothesis.evidence_refs
    assert hypothesis.risk_level == "low"


def test_hypothesis_requires_evidence_refs() -> None:
    hypothesis = build_hypothesis(priority()).model_dump()
    hypothesis["evidence_refs"] = []

    with pytest.raises(ValidationError):
        Hypothesis(**hypothesis)
