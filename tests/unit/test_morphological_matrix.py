from tuling_research_plus.artifacts.models import EvidenceRef
from tuling_research_plus.hypothesis.falsifiability import build_hypothesis
from tuling_research_plus.hypothesis.models import GapPriority, Hypothesis
from tuling_research_plus.ideation.morphological_matrix import build_morphological_matrix
from tuling_research_plus.ideation.service import CreativeIdeationService
from tuling_research_plus.ideation.tools import research_idea_morphological_matrix


def evidence() -> EvidenceRef:
    return EvidenceRef(
        source_id="paper-1",
        locator="section-3",
        quote="Evidence gates reduce unsupported claims.",
    )


def hypothesis() -> Hypothesis:
    return build_hypothesis(
        GapPriority(
            gap_id="gap-1",
            description="Few studies validate workflow gates.",
            score=0.9,
            rationale="High confidence and enough evidence.",
            evidence=[evidence()],
        )
    ).model_copy(update={"score": 0.9})


def test_morphological_matrix_contains_diversity_axes() -> None:
    matrix = build_morphological_matrix(hypothesis())
    axis_names = {axis.name for axis in matrix.axes}

    assert {
        "mechanism",
        "required_data",
        "model_component",
        "evaluation_target",
        "risk_profile",
    } <= axis_names
    assert matrix.combinations()


def test_morphological_matrix_tool_returns_json_payload() -> None:
    payload = research_idea_morphological_matrix(hypothesis(), CreativeIdeationService())

    assert payload["hypothesis_link"] == "hypothesis-1"
    assert payload["axes"]

