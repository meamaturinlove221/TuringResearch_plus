"""Evidence matrix construction."""

from __future__ import annotations

from turing_research_plus.survey.models import (
    EvidenceMatrix,
    EvidenceMatrixRow,
    PaperRecord,
    PaperScreeningDecision,
    PaperScreeningTable,
)


def build_evidence_matrix(
    papers: list[PaperRecord],
    screening: PaperScreeningTable,
) -> EvidenceMatrix:
    """Build a compact evidence matrix from included papers."""

    paper_by_id = {paper.paper_id: paper for paper in papers}
    rows: list[EvidenceMatrixRow] = []
    for row in screening.rows:
        if row.decision != PaperScreeningDecision.INCLUDE:
            continue
        paper = paper_by_id[row.paper_id]
        claim = paper.abstract or paper.title
        rows.append(
            EvidenceMatrixRow(
                claim=claim,
                paper_ids=[paper.paper_id],
                evidence=row.evidence,
            )
        )
    return EvidenceMatrix(rows=rows)
