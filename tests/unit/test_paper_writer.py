from tuling_research_plus.artifacts.models import EvidenceRef
from tuling_research_plus.paper.figure_registry import (
    FigureAsset,
    FigureAssetKind,
    FigureAssetRegistry,
)
from tuling_research_plus.paper.models import (
    ArticleBlock,
    ArticleBlockKind,
    ArticleSection,
    ExperimentReport,
)
from tuling_research_plus.paper.paper_writer import (
    PaperDraftInput,
    PaperSection,
    SectionReadinessStatus,
    generate_paper_draft,
    paper_draft_generate,
)


def evidence(source_id: str = "source-1") -> EvidenceRef:
    return EvidenceRef(source_id=source_id, locator="section-1", quote="Evidence text.")


def block(kind: ArticleBlockKind, text: str) -> ArticleBlock:
    return ArticleBlock(
        block_id=kind.value,
        block_kind=kind,
        section=ArticleSection.METHODS,
        text=text,
        evidence=[evidence(kind.value)],
    )


def experiment_report() -> ExperimentReport:
    return ExperimentReport(
        report_id="experiment-report-1",
        title="Experiment Report",
        metrics={"accuracy": 0.82, "latency_ms": 12.0},
        evidence=[evidence("experiment-report-1")],
    )


def registry() -> FigureAssetRegistry:
    return FigureAssetRegistry(
        assets=[
            FigureAsset(
                figure_id="architecture-fig-1",
                title="Architecture Figure",
                source_file="docs/architecture_16box.mmd",
                caption="Architecture figure.",
                used_in_blocks=["method_design"],
                asset_kind=FigureAssetKind.MERMAID,
            ),
            FigureAsset(
                figure_id="metrics-table-1",
                title="Metrics Table",
                source_file="paper/tables/metrics.csv",
                caption="Metrics table.",
                used_in_blocks=["experiments"],
                asset_kind=FigureAssetKind.CSV_TABLE,
            ),
        ]
    )


def complete_input() -> PaperDraftInput:
    return PaperDraftInput(
        available_artifacts=[
            "ResearchBrief",
            "LiteratureSurveyArtifact",
            "MethodDesign",
            "ExperimentPlan",
        ],
        article_blocks=[
            block(ArticleBlockKind.RESEARCH_BRIEF, "Research brief text."),
            block(ArticleBlockKind.RELATED_WORK, "Related work text."),
            block(ArticleBlockKind.METHOD_DESIGN, "Method design text."),
            block(ArticleBlockKind.EXPERIMENTS, "Experiment design text."),
        ],
        experiment_report=experiment_report(),
        figure_registry=registry(),
        stress_test_results=["Residual risk is low after mitigation."],
    )


def test_draft_generated_when_gates_pass() -> None:
    result = generate_paper_draft(complete_input())

    assert result.blocked is False
    assert result.draft_markdown is not None
    assert "## Method" in result.draft_markdown
    assert "architecture-fig-1" in result.draft_markdown


def test_figures_referenced_in_method_section() -> None:
    result = generate_paper_draft(complete_input())

    assert result.draft_markdown is not None
    assert "Architecture figures: architecture-fig-1." in result.draft_markdown


def test_no_fabricated_result_text() -> None:
    result = generate_paper_draft(complete_input())

    assert result.draft_markdown is not None
    assert "Reported metrics from ExperimentReport: accuracy=0.82, latency_ms=12.0." in (
        result.draft_markdown
    )
    assert "significant improvement" not in result.draft_markdown.lower()


def test_paper_draft_generate_tool_returns_json_payload() -> None:
    payload = paper_draft_generate(complete_input())

    assert payload["blocked"] is False
    assert payload["draft_markdown"].startswith("# TulingResearch Plus Paper Draft")


def test_section_status_ready_when_complete() -> None:
    result = generate_paper_draft(complete_input())
    statuses = {status.section: status for status in result.section_status}

    assert statuses[PaperSection.METHOD].status == SectionReadinessStatus.READY
    assert statuses[PaperSection.RESULTS].status == SectionReadinessStatus.READY
