from __future__ import annotations

from tests.workflow.example_helpers import (
    assert_example_contract,
    example_evidence,
    read_json,
    to_pretty_json,
)

from tuling_research_plus.experiment.design import design_experiment
from tuling_research_plus.hypothesis.service import HypothesisFormationService
from tuling_research_plus.insight.models import GapValidation, GapValidationReport
from tuling_research_plus.north_star.models import ResearchBrief
from tuling_research_plus.survey.models import PaperRecord, SurveyInput, SurveyStrategy
from tuling_research_plus.survey.service import LiteratureSurveyService


class FakePaperService:
    def search(self, survey_input: SurveyInput, limit: int) -> list[PaperRecord]:
        return [
            PaperRecord(
                paper_id=f"vggt-paper-{index}",
                title=f"VGGT human prior fixture {index}",
                year=2024,
                abstract="Human priors improve reconstruction quality under occlusion.",
                has_full_text=index < 3,
                evidence=[example_evidence(f"vggt-paper-{index}")],
                tags=["human_prior", "reconstruction"],
            )
            for index in range(1, min(limit, 3) + 1)
        ]


class FakePDFService:
    def to_markdown(self, paper: PaperRecord) -> PaperRecord:
        return paper.model_copy(update={"pdf_markdown_path": f"cache/{paper.paper_id}.md"})


def test_vggt_human_prior_example_dry_run_outputs_required_artifacts() -> None:
    required = {
        "ResearchBrief",
        "LiteratureSurveyArtifact",
        "GapReport",
        "HypothesisPortfolio",
        "ExperimentPlan",
    }
    assert_example_contract("vggt-human-prior-survey", required)
    request = read_json("vggt-human-prior-survey/input/request.json")
    evidence = example_evidence("vggt-request")

    brief = ResearchBrief(
        title="VGGT Human Prior Survey",
        problem="Human priors are not consistently evaluated in VGGT-style reconstruction.",
        research_goal=request["research_goal"],
        scope=request["topic"],
        constraints=["fake-service dry run", "no real network"],
        resources=["local fixtures"],
        evidence=[evidence],
    )
    survey_input = SurveyInput(
        topic=request["topic"],
        strategy=SurveyStrategy(request["strategy"]),
        year_range=tuple(request["year_range"]),
        min_papers=request["min_papers"],
        full_text_ratio=request["full_text_ratio"],
        seed_papers=request["seed_papers"],
        research_goal=request["research_goal"],
    )
    survey_result = LiteratureSurveyService(
        paper_service=FakePaperService(),
        pdf_service=FakePDFService(),
    ).run(survey_input, survey_id="vggt-human-prior", dry_run=True)
    assert survey_result.artifact is not None
    gap_report = GapValidationReport(
        report_id="vggt-gap-report",
        topic=request["topic"],
        gaps=[
            GapValidation(
                gap_id=gap.gap_id,
                description=gap.description,
                evidence=gap.evidence,
                confidence=0.84,
            )
            for gap in survey_result.artifact.gap_list.gaps
        ],
    )
    hypothesis_service = HypothesisFormationService()
    priorities = hypothesis_service.gap_prioritize(gap_report)
    hypotheses = hypothesis_service.hypothesis_generate(priorities)
    portfolio = hypothesis_service.hypothesis_portfolio_build(hypotheses, max_items=1)
    experiment_plan = design_experiment(portfolio.selected[0])

    outputs = {
        "ResearchBrief": brief.model_dump(mode="json"),
        "LiteratureSurveyArtifact": survey_result.artifact.model_dump(mode="json"),
        "GapReport": gap_report.model_dump(mode="json"),
        "HypothesisPortfolio": portfolio.model_dump(mode="json"),
        "ExperimentPlan": experiment_plan.model_dump(mode="json"),
    }
    markdown = "\n".join(
        [
            "# VGGT Human Prior Survey Dry Run",
            survey_result.to_markdown(),
            f"- ExperimentPlan: `{experiment_plan.plan_id}`",
        ]
    )

    assert set(outputs) == required
    assert survey_result.status.value == "completed"
    assert experiment_plan.controls
    assert experiment_plan.metrics
    assert "Literature Survey" in markdown
    assert "ExperimentPlan" in markdown
    assert "HypothesisPortfolio" in to_pretty_json(outputs)
