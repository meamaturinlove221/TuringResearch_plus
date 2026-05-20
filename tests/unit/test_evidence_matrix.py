from tuling_research_plus.artifacts.models import EvidenceRef
from tuling_research_plus.survey.evidence_matrix import build_evidence_matrix
from tuling_research_plus.survey.models import PaperRecord, SurveyInput, SurveyStrategy
from tuling_research_plus.survey.screening import screen_papers


def test_paper_screening_and_evidence_matrix() -> None:
    papers = [
        PaperRecord(
            paper_id="p1",
            title="Paper One",
            year=2022,
            abstract="Method A works.",
            evidence=[EvidenceRef(source_id="p1", locator="abstract", quote="Method A works.")],
        ),
        PaperRecord(paper_id="p2", title="Paper Two", year=2010),
    ]
    survey_input = SurveyInput(
        topic="methods",
        strategy=SurveyStrategy.SCOPING,
        year_range=(2020, 2026),
        min_papers=1,
        research_goal="Map methods.",
    )

    screening = screen_papers(papers, survey_input)
    matrix = build_evidence_matrix(papers, screening)

    assert screening.included_count == 1
    assert screening.rows[1].decision == "exclude"
    assert matrix.rows[0].claim == "Method A works."
    assert matrix.rows[0].paper_ids == ["p1"]
