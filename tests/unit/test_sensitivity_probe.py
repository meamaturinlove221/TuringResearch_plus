import pytest

from tuling_research_plus.artifacts.models import EvidenceRef
from tuling_research_plus.insight.gap_analysis import analyze_gaps
from tuling_research_plus.insight.models import AssumptionSensitivity, SensitivityReport
from tuling_research_plus.insight.sensitivity import probe_sensitivity
from tuling_research_plus.insight.service import DeepInsightService
from tuling_research_plus.insight.tools import research_sensitivity_probe
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


def evidence() -> EvidenceRef:
    return EvidenceRef(
        source_id="paper-1",
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


def test_sensitivity_report_identifies_load_bearing_assumptions() -> None:
    gap_report = analyze_gaps(survey_artifact())
    report = probe_sensitivity(gap_report)

    assert any(assumption.load_bearing for assumption in report.assumptions)
    assert report.assumptions[0].evidence


def test_sensitivity_report_requires_load_bearing_assumption() -> None:
    with pytest.raises(ValueError, match="load-bearing"):
        SensitivityReport(
            report_id="sensitivity-1",
            topic="quality gates",
            assumptions=[
                AssumptionSensitivity(
                    assumption_id="assumption-1",
                    statement="Terminology is comparable.",
                    load_bearing=False,
                    sensitivity="Normalization may be needed.",
                    evidence=[evidence()],
                )
            ],
        )


def test_sensitivity_tool_returns_json_payload() -> None:
    gap_report = analyze_gaps(survey_artifact())
    payload = research_sensitivity_probe(gap_report, DeepInsightService())

    assert payload["assumptions"][0]["load_bearing"] is True

