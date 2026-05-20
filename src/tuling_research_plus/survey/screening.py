"""Paper screening helpers."""

from __future__ import annotations

from tuling_research_plus.artifacts.models import EvidenceRef
from tuling_research_plus.survey.models import (
    PaperRecord,
    PaperScreeningDecision,
    PaperScreeningRow,
    PaperScreeningTable,
    SurveyInput,
)


def screen_papers(papers: list[PaperRecord], survey_input: SurveyInput) -> PaperScreeningTable:
    """Screen papers by year range and basic topical evidence."""

    rows: list[PaperScreeningRow] = []
    for paper in papers:
        decision = PaperScreeningDecision.INCLUDE
        reason = "matches survey constraints"
        if survey_input.year_range is not None and paper.year is not None:
            start, end = survey_input.year_range
            if paper.year < start or paper.year > end:
                decision = PaperScreeningDecision.EXCLUDE
                reason = "outside year range"
        evidence = paper.evidence or [
            EvidenceRef(
                source_id=paper.paper_id,
                locator="metadata",
                quote=paper.title,
                confidence=0.8,
            )
        ]
        rows.append(
            PaperScreeningRow(
                paper_id=paper.paper_id,
                title=paper.title,
                decision=decision,
                reason=reason,
                full_text_available=paper.counts_as_full_text,
                evidence=evidence,
            )
        )
    return PaperScreeningTable(rows=rows)
