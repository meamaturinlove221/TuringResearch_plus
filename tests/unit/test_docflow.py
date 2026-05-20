from tuling_research_plus.artifacts.models import EvidenceRef
from tuling_research_plus.paper.docflow import (
    article_block_update,
    build_docflow_graph,
    docflow_status,
    missing_evidence,
    paper_docflow_status,
)
from tuling_research_plus.paper.models import (
    ArticleBlockKind,
    ArticleBlockUpdateInput,
    DocflowStatusInput,
    ExperimentReport,
)


def evidence(source_id: str = "brief-1") -> EvidenceRef:
    return EvidenceRef(source_id=source_id, locator="section-1", quote="Evidence text.")


def experiment_report() -> ExperimentReport:
    return ExperimentReport(
        report_id="experiment-report-1",
        title="Experiment Report",
        evidence=[evidence("experiment-report-1")],
    )


def complete_input() -> DocflowStatusInput:
    return DocflowStatusInput(
        available_artifacts=[
            "ResearchBrief",
            "LiteratureSurveyArtifact",
            "PDFMarkdownOutput",
            "GapReport",
            "HypothesisPortfolio",
            "IdeaPortfolio",
            "DecisionReport",
            "ExperimentPlan",
            "StressTestReport",
        ],
        evidence_by_block={
            "research_brief": [evidence("brief-1")],
            "related_work": [evidence("survey-1")],
            "method_design": [evidence("decision-1")],
            "experiments": [evidence("plan-1")],
        },
        required_figures={"paper_draft": ["fig-1"]},
        available_figures=["fig-1"],
        experiment_report=experiment_report(),
    )


def test_missing_upstream_artifact_detected() -> None:
    result = docflow_status(
        DocflowStatusInput(
            available_artifacts=[],
            evidence_by_block={"research_brief": [evidence()]},
        )
    )

    research_brief = result.registry.get_block(ArticleBlockKind.RESEARCH_BRIEF)

    assert research_brief.ready is False
    assert research_brief.missing_artifacts == ["ResearchBrief"]
    assert result.missing_item_report.missing_artifacts["research_brief"] == ["ResearchBrief"]


def test_article_block_readiness_calculated() -> None:
    result = docflow_status(complete_input())

    assert result.registry.get_block(ArticleBlockKind.RESEARCH_BRIEF).ready is True
    assert result.registry.get_block(ArticleBlockKind.PAPER_DRAFT).ready is True
    assert result.readiness_report.ready is True
    assert result.readiness_report.blocked_blocks == []


def test_docflow_graph_generated() -> None:
    graph = build_docflow_graph()

    assert graph.startswith("flowchart TD")
    assert "research_brief --> related_work" in graph
    assert "ExperimentReport{{ExperimentReport Gate}} --> paper_draft" in graph


def test_paper_draft_blocked_until_experiment_report_exists() -> None:
    input_data = complete_input()
    input_data = input_data.model_copy(update={"experiment_report": None})

    result = docflow_status(input_data)
    paper_draft = result.registry.get_block(ArticleBlockKind.PAPER_DRAFT)

    assert paper_draft.ready is False
    assert paper_draft.blocked_reason is not None
    assert "ExperimentReport is required" in paper_draft.blocked_reason
    assert result.readiness_report.draft_blocked is True


def test_missing_evidence_report_generated() -> None:
    result = missing_evidence(DocflowStatusInput(available_artifacts=["ResearchBrief"]))

    assert result.missing_evidence
    assert result.missing_evidence[0].requirement == "EvidenceRef"


def test_required_figures_block_article_block_update() -> None:
    result = article_block_update(
        ArticleBlockUpdateInput(
            block_kind=ArticleBlockKind.PAPER_DRAFT,
            text="Draft text.",
            available_artifacts=["ExperimentReport"],
            evidence_refs=[evidence("draft-1")],
            required_figures=["fig-1"],
            available_figures=[],
            experiment_report=experiment_report(),
        )
    )

    assert result.accepted is False
    assert result.block.missing_figures == ["fig-1"]


def test_paper_docflow_status_tool_returns_json_payload() -> None:
    payload = paper_docflow_status(complete_input())

    assert payload["readiness_report"]["ready"] is True
    assert len(payload["registry"]["blocks"]) == 5
