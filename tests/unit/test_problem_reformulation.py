import pytest
from pydantic import ValidationError

from turing_research_plus.artifacts.models import EvidenceRef
from turing_research_plus.insight.gap_analysis import analyze_gaps
from turing_research_plus.insight.models import ReformulatedProblem
from turing_research_plus.insight.reformulation import reformulate_problems
from turing_research_plus.insight.service import DeepInsightService
from turing_research_plus.insight.tools import research_problem_reformulate
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


def test_reformulation_states_changes_and_invariants() -> None:
    gap_report = analyze_gaps(survey_artifact())
    problem_set = reformulate_problems(gap_report)
    problem = problem_set.problems[0]

    assert problem.changes
    assert problem.invariants
    assert problem.evidence


def test_reformulation_requires_changes_and_invariants() -> None:
    with pytest.raises(ValidationError):
        ReformulatedProblem(
            problem_id="problem-1",
            original_problem="Broad problem.",
            reformulated_problem="Narrow problem.",
            changes=[],
            invariants=["Keep evidence."],
            evidence=[evidence()],
        )


def test_problem_reformulation_tool_returns_json_payload() -> None:
    gap_report = analyze_gaps(survey_artifact())
    payload = research_problem_reformulate(gap_report, DeepInsightService())

    assert payload["problems"][0]["changes"]
    assert payload["problems"][0]["invariants"]


def test_full_deep_insight_run_returns_all_outputs() -> None:
    result = DeepInsightService().run(survey_artifact())

    assert result.gap_validation_report.gaps
    assert result.insight_report.insights
    assert result.boundary_map.conditions
    assert result.sensitivity_report.assumptions
    assert result.reformulated_problem_set.problems
