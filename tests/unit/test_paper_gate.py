from tuling_research_plus.artifacts.models import EvidenceRef
from tuling_research_plus.paper.figure_registry import FigureAssetRegistry
from tuling_research_plus.paper.models import ArticleBlock, ArticleBlockKind, ArticleSection
from tuling_research_plus.paper.paper_writer import (
    PaperDraftInput,
    PaperSection,
    SectionReadinessStatus,
    generate_paper_draft,
    paper_missing_evidence_for_draft,
    section_status_yaml,
)


def evidence() -> EvidenceRef:
    return EvidenceRef(source_id="brief-1", locator="section-1", quote="Evidence text.")


def article_block() -> ArticleBlock:
    return ArticleBlock(
        block_id="research_brief",
        block_kind=ArticleBlockKind.RESEARCH_BRIEF,
        section=ArticleSection.INTRODUCTION,
        text="Research brief text.",
        evidence=[evidence()],
    )


def test_draft_blocked_without_experiment_report() -> None:
    result = generate_paper_draft(
        PaperDraftInput(
            available_artifacts=["ResearchBrief", "LiteratureSurveyArtifact", "MethodDesign"],
            article_blocks=[article_block()],
            experiment_report=None,
            figure_registry=FigureAssetRegistry(),
        )
    )

    assert result.blocked is True
    assert result.draft_markdown is None
    assert "ExperimentReport" in result.missing_evidence_report.missing_artifacts


def test_section_status_generated() -> None:
    result = generate_paper_draft(PaperDraftInput(article_blocks=[article_block()]))
    yaml_text = section_status_yaml(result.section_status)

    assert "section: abstract" in yaml_text
    assert "status: blocked" in yaml_text
    assert len(result.section_status) == len(PaperSection)


def test_missing_evidence_detected() -> None:
    payload = paper_missing_evidence_for_draft(PaperDraftInput(article_blocks=[]))

    assert (
        payload["blocked_reason"]
        == "Paper draft generation blocked by missing required evidence."
    )
    assert "ArticleBlocks are required." in payload["missing_evidence"]


def test_method_section_blocked_without_architecture_figure() -> None:
    result = generate_paper_draft(
        PaperDraftInput(
            available_artifacts=[
                "ResearchBrief",
                "LiteratureSurveyArtifact",
                "MethodDesign",
                "ExperimentPlan",
            ],
            article_blocks=[article_block()],
            figure_registry=FigureAssetRegistry(),
        )
    )
    method = next(
        status for status in result.section_status if status.section == PaperSection.METHOD
    )

    assert method.status == SectionReadinessStatus.BLOCKED
    assert "method architecture figure" in method.missing_items
