import pytest
from pydantic import ValidationError

from turing_research_plus.artifacts.models import EvidenceRef
from turing_research_plus.insight.gap_analysis import analyze_gaps
from turing_research_plus.insight.models import GapValidation
from turing_research_plus.insight.service import DeepInsightService
from turing_research_plus.insight.tools import research_gap_analyze, research_insight_generate
from turing_research_plus.survey.models import (
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


def test_no_gap_without_evidence() -> None:
    with pytest.raises(ValidationError):
        GapValidation(
            gap_id="gap-1",
            description="Unsupported gap.",
            evidence=[],
        )


def test_gap_analysis_returns_research_artifact() -> None:
    report = analyze_gaps(survey_artifact())
    artifact = report.to_research_artifact()

    assert report.gaps[0].gap_id == "gap-1"
    assert artifact.evidence[0].source_id == "paper-1"
    assert "gap_validation" in artifact.tags


def test_no_insight_without_supporting_and_contradicting_evidence() -> None:
    report = analyze_gaps(survey_artifact())
    insight_report = DeepInsightService().insight_generate(report)

    insight = insight_report.insights[0]
    assert insight.supporting_evidence
    assert insight.contradicting_evidence
    assert insight_report.to_research_artifact().evidence


def test_gap_and_insight_tools_return_json_payloads() -> None:
    service = DeepInsightService()
    gap_payload = research_gap_analyze(survey_artifact(), service)
    gap_report = analyze_gaps(survey_artifact())
    insight_payload = research_insight_generate(gap_report, service)

    assert gap_payload["topic"] == "research workflow quality gates"
    assert insight_payload["insights"][0]["supporting_evidence"]
    assert insight_payload["insights"][0]["contradicting_evidence"]

