from turing_research_plus.artifacts.models import EvidenceRef
from turing_research_plus.survey.models import (
    PaperRecord,
    SurveyInput,
    SurveyStatus,
    SurveyStrategy,
)
from turing_research_plus.survey.service import LiteratureSurveyService
from turing_research_plus.survey.tools import (
    research_survey_export,
    research_survey_plan,
    research_survey_run,
    research_survey_status,
)


class FakePaperService:
    def search(self, survey_input: SurveyInput, limit: int) -> list[PaperRecord]:
        return [
            PaperRecord(
                paper_id="p1",
                title="Paper One",
                year=2023,
                abstract="Depth gates improve survey reliability.",
                has_full_text=True,
                evidence=[
                    EvidenceRef(
                        source_id="p1",
                        locator="full-text",
                        quote="Depth gates improve survey reliability.",
                    )
                ],
                tags=["workflow"],
            ),
            PaperRecord(
                paper_id="p2",
                title="Paper Two",
                year=2024,
                abstract="PDF conversion can count as full text.",
                has_full_text=False,
                evidence=[
                    EvidenceRef(
                        source_id="p2",
                        locator="abstract",
                        quote="PDF conversion can count as full text.",
                    )
                ],
                tags=["pdf"],
            ),
        ]


class FakePDFMarkdownService:
    def to_markdown(self, paper: PaperRecord) -> PaperRecord:
        if paper.paper_id == "p2":
            return paper.model_copy(update={"pdf_markdown_path": "cache/p2.md"})
        return paper


class FakeSemanticGraphService:
    def expand_seed_papers(self, seed_papers: list[str], budget: int) -> list[PaperRecord]:
        return [
            PaperRecord(
                paper_id="p3",
                title="Snowball Paper",
                year=2025,
                abstract="Snowball expansion reaches saturation.",
                has_full_text=True,
                evidence=[
                    EvidenceRef(
                        source_id="p3",
                        locator="full-text",
                        quote="Snowball expansion reaches saturation.",
                    )
                ],
            )
        ]


def test_literature_survey_dry_run_and_markdown_export() -> None:
    service = LiteratureSurveyService(
        paper_service=FakePaperService(),
        pdf_service=FakePDFMarkdownService(),
    )
    survey_input = SurveyInput(
        topic="workflow gates",
        strategy=SurveyStrategy.DEEP,
        min_papers=2,
        full_text_ratio=1.0,
        research_goal="Assess hard gates.",
    )

    result = service.run(survey_input, dry_run=True)

    assert result.status == SurveyStatus.COMPLETED
    assert result.artifact is not None
    assert result.artifact.screening_table.full_text_count == 2
    assert result.artifact.gap_list.gaps[0].evidence
    markdown = service.export_markdown(result)
    assert "# Literature Survey: workflow gates" in markdown
    assert "## Gaps" in markdown


def test_snowball_survey_expands_citation_lineage() -> None:
    service = LiteratureSurveyService(
        paper_service=FakePaperService(),
        pdf_service=FakePDFMarkdownService(),
        graph_service=FakeSemanticGraphService(),
    )
    survey_input = SurveyInput(
        topic="snowball",
        strategy=SurveyStrategy.SNOWBALL,
        min_papers=2,
        seed_papers=["p1"],
        research_goal="Trace citation lineage.",
    )

    result = service.run(survey_input, dry_run=True)

    assert result.status == SurveyStatus.COMPLETED
    assert result.artifact is not None
    assert result.artifact.citation_lineage is not None
    assert "p3" in result.artifact.citation_lineage.expanded_papers


def test_survey_tool_wrappers() -> None:
    service = LiteratureSurveyService(
        paper_service=FakePaperService(),
        pdf_service=FakePDFMarkdownService(),
    )
    survey_input = SurveyInput(
        topic="tool wrappers",
        strategy=SurveyStrategy.SCOPING,
        min_papers=1,
        research_goal="Check wrappers.",
    )

    plan = research_survey_plan(survey_input, service)
    run = research_survey_run(survey_input, service)
    status = research_survey_status(service.run(survey_input))
    export = research_survey_export(service.run(survey_input))

    assert plan["survey_input"]["topic"] == "tool wrappers"
    assert run["status"] == SurveyStatus.COMPLETED
    assert status["status"] == SurveyStatus.COMPLETED
    assert export.startswith("# Literature Survey")
