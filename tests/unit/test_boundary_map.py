import pytest

from tuling_research_plus.artifacts.models import EvidenceRef
from tuling_research_plus.insight.boundary import build_boundary_map
from tuling_research_plus.insight.gap_analysis import analyze_gaps
from tuling_research_plus.insight.models import (
    BoundaryCondition,
    BoundaryConditionType,
    BoundaryMap,
)
from tuling_research_plus.insight.service import DeepInsightService
from tuling_research_plus.insight.tools import research_boundary_map
from tuling_research_plus.survey.models import (
    EvidenceMatrix,
    GapItem,
    GapList,
    LiteratureSurveyArtifact,
    MethodTaxonomy,
    PaperScreeningTable,
    SurveyStatus,
    SurveyStrategy,
)


def evidence(source_id: str = "paper-1") -> EvidenceRef:
    return EvidenceRef(
        source_id=source_id,
        locator="section-2",
        quote="Runtime gates are underexplored.",
    )


def survey_artifact() -> LiteratureSurveyArtifact:
    return LiteratureSurveyArtifact(
        survey_id="survey-1",
        topic="research workflow quality gates",
        strategy=SurveyStrategy.SCOPING,
        status=SurveyStatus.COMPLETED,
        screening_table=PaperScreeningTable(),
        method_taxonomy=MethodTaxonomy(),
        evidence_matrix=EvidenceMatrix(),
        gap_list=GapList(
            gaps=[
                GapItem(
                    gap_id="gap-1",
                    description="Few studies validate workflow gates.",
                    evidence=[evidence()],
                )
            ]
        ),
    )


def test_boundary_map_has_valid_and_invalid_conditions() -> None:
    gap_report = analyze_gaps(survey_artifact())
    boundary_map = build_boundary_map(gap_report)

    condition_types = {condition.condition_type for condition in boundary_map.conditions}
    assert BoundaryConditionType.VALID in condition_types
    assert BoundaryConditionType.INVALID in condition_types
    assert all(condition.evidence for condition in boundary_map.conditions)


def test_boundary_map_requires_valid_condition() -> None:
    with pytest.raises(ValueError, match="valid condition"):
        BoundaryMap(
            map_id="map-1",
            topic="quality gates",
            conditions=[
                BoundaryCondition(
                    condition_id="invalid-1",
                    condition_type=BoundaryConditionType.INVALID,
                    description="Outside surveyed evidence.",
                    evidence=[evidence()],
                ),
                BoundaryCondition(
                    condition_id="invalid-2",
                    condition_type=BoundaryConditionType.INVALID,
                    description="Without comparable data.",
                    evidence=[evidence("paper-2")],
                ),
            ],
        )


def test_boundary_tool_returns_json_payload() -> None:
    gap_report = analyze_gaps(survey_artifact())
    payload = research_boundary_map(gap_report, DeepInsightService())

    assert payload["conditions"][0]["condition_type"] == "valid"
    assert payload["conditions"][1]["condition_type"] == "invalid"
