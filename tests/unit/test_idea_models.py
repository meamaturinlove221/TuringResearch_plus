import pytest
from pydantic import ValidationError

from tuling_research_plus.artifacts.models import EvidenceRef
from tuling_research_plus.ideation.models import IdeaCandidate, IdeaClusterKey, IdeaRisk


def evidence() -> EvidenceRef:
    return EvidenceRef(
        source_id="paper-1",
        locator="section-3",
        quote="Evidence gates reduce unsupported claims.",
    )


def cluster_key() -> IdeaClusterKey:
    return IdeaClusterKey(
        mechanism="evidence gate",
        required_data="audit table",
        model_component="gate threshold",
        evaluation_target="unsupported claim rate",
        risk_profile=IdeaRisk.MEDIUM,
    )


def idea_candidate() -> IdeaCandidate:
    return IdeaCandidate(
        idea_id="idea-1",
        title="Evaluate gate thresholds",
        hypothesis_link="hypothesis-1",
        mechanism="evidence gate",
        novelty=0.8,
        feasibility=0.7,
        risk=IdeaRisk.MEDIUM,
        expected_gain="Lower unsupported claim rate.",
        required_resources=["audit table"],
        nearest_existing_work="controlled dry-run comparison",
        why_not_duplicate="Uses a distinct threshold cluster.",
        evidence_refs=[evidence()],
        cluster_key=cluster_key(),
    )


def test_idea_candidate_contains_required_fields() -> None:
    idea = idea_candidate()

    assert idea.title
    assert idea.hypothesis_link == "hypothesis-1"
    assert idea.mechanism
    assert idea.novelty > 0
    assert idea.feasibility > 0
    assert idea.risk == IdeaRisk.MEDIUM
    assert idea.expected_gain
    assert idea.required_resources
    assert idea.nearest_existing_work
    assert idea.why_not_duplicate
    assert idea.evidence_refs
    assert idea.quality_score > 0


def test_idea_candidate_requires_evidence_refs() -> None:
    payload = idea_candidate().model_dump()
    payload["evidence_refs"] = []

    with pytest.raises(ValidationError):
        IdeaCandidate(**payload)


def test_cluster_signature_normalizes_text() -> None:
    key = cluster_key().model_copy(update={"mechanism": "Evidence Gate"})

    assert key.signature()[0] == "evidence gate"

