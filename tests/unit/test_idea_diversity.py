from tuling_research_plus.artifacts.models import EvidenceRef
from tuling_research_plus.ideation.diversity import quality_diversity_filter
from tuling_research_plus.ideation.models import (
    IdeaCandidate,
    IdeaClusterKey,
    IdeaGenerationResult,
    IdeaRisk,
)
from tuling_research_plus.ideation.service import CreativeIdeationService
from tuling_research_plus.ideation.tools import research_idea_quality_diversity_filter


def evidence(source_id: str = "paper-1") -> EvidenceRef:
    return EvidenceRef(
        source_id=source_id,
        locator="section-3",
        quote="Evidence gates reduce unsupported claims.",
    )


def cluster_key(component: str = "gate threshold") -> IdeaClusterKey:
    return IdeaClusterKey(
        mechanism="evidence gate",
        required_data="audit table",
        model_component=component,
        evaluation_target="unsupported claim rate",
        risk_profile=IdeaRisk.MEDIUM,
    )


def idea(idea_id: str, novelty: float, component: str = "gate threshold") -> IdeaCandidate:
    return IdeaCandidate(
        idea_id=idea_id,
        title=f"Evaluate {component}",
        hypothesis_link="hypothesis-1",
        mechanism="evidence gate",
        novelty=novelty,
        feasibility=0.8,
        risk=IdeaRisk.MEDIUM,
        expected_gain="Lower unsupported claim rate.",
        required_resources=["audit table"],
        nearest_existing_work="controlled dry-run comparison",
        why_not_duplicate="Uses a diversity cluster.",
        evidence_refs=[evidence(idea_id)],
        cluster_key=cluster_key(component),
    )


def generation() -> IdeaGenerationResult:
    return IdeaGenerationResult(
        result_id="ideas-1",
        topic="quality gates",
        candidates=[
            idea("idea-low", 0.6),
            idea("idea-high", 0.9),
            idea("idea-other", 0.7, component="audit sampler"),
        ],
    )


def test_diversity_gate_removes_near_duplicates() -> None:
    report = quality_diversity_filter(generation())

    retained_ids = {candidate.idea_id for candidate in report.retained}
    rejected_ids = {candidate.idea_id for candidate in report.rejected_duplicates}
    assert "idea-high" in retained_ids
    assert "idea-low" in rejected_ids
    assert report.cluster_count == 2


def test_diversity_gate_clusters_by_required_dimensions() -> None:
    report = quality_diversity_filter(generation())
    signatures = [candidate.cluster_key.signature() for candidate in report.retained]

    assert len(signatures) == len(set(signatures))


def test_diversity_tool_returns_json_payload() -> None:
    payload = research_idea_quality_diversity_filter(generation(), CreativeIdeationService())

    assert payload["cluster_count"] == 2
    assert payload["rejected_duplicates"][0]["idea_id"] == "idea-low"

