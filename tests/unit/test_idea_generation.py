from turing_research_plus.artifacts.models import EvidenceRef
from turing_research_plus.hypothesis.falsifiability import build_hypothesis
from turing_research_plus.hypothesis.models import GapPriority, HypothesisSet
from turing_research_plus.ideation.generators import generate_cross_domain_ideas, generate_ideas
from turing_research_plus.ideation.service import CreativeIdeationService
from turing_research_plus.ideation.tools import research_idea_cross_domain, research_idea_generate


def evidence() -> EvidenceRef:
    return EvidenceRef(
        source_id="paper-1",
        locator="section-3",
        quote="Evidence gates reduce unsupported claims.",
    )


def hypothesis_set() -> HypothesisSet:
    hypothesis = build_hypothesis(
        GapPriority(
            gap_id="gap-1",
            description="Few studies validate workflow gates.",
            score=0.9,
            rationale="High confidence and enough evidence.",
            evidence=[evidence()],
        )
    ).model_copy(update={"score": 0.9})
    return HypothesisSet(
        set_id="hypothesis-set-1",
        topic="research workflow quality gates",
        hypotheses=[hypothesis],
    )


def test_idea_generation_is_deterministic_and_evidence_backed() -> None:
    first = generate_ideas(hypothesis_set())
    second = generate_ideas(hypothesis_set())

    assert first.model_dump(mode="json") == second.model_dump(mode="json")
    assert first.candidates[0].evidence_refs
    assert first.candidates[0].hypothesis_link == "hypothesis-1"


def test_cross_domain_generation_changes_cluster_component() -> None:
    result = generate_cross_domain_ideas(hypothesis_set(), domain="clinical triage")

    assert "clinical triage" in result.candidates[0].title
    assert result.candidates[0].cluster_key.model_component == "clinical triage analogy"


def test_idea_service_builds_artifact_shaped_portfolio() -> None:
    portfolio = CreativeIdeationService().build_portfolio(hypothesis_set())
    artifact = portfolio.to_research_artifact()

    assert portfolio.ideas
    assert portfolio.diversity_report.cluster_count == len(portfolio.ideas)
    assert artifact.evidence
    assert "creative_ideation" in artifact.tags


def test_idea_tools_return_json_payloads() -> None:
    service = CreativeIdeationService()
    idea_payload = research_idea_generate(hypothesis_set(), service)
    cross_payload = research_idea_cross_domain(
        hypothesis_set(),
        service,
        domain="clinical triage",
    )

    assert idea_payload["candidates"][0]["title"]
    assert "clinical triage" in cross_payload["candidates"][0]["title"]
