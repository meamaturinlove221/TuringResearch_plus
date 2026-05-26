"""Evidence-backed gap extraction."""

from __future__ import annotations

from turing_research_plus.survey.models import EvidenceMatrix, GapItem, GapList


def extract_gaps(matrix: EvidenceMatrix, max_gaps: int = 3) -> GapList:
    """Extract simple evidence-backed gaps from an evidence matrix."""

    gaps: list[GapItem] = []
    for index, row in enumerate(matrix.rows[:max_gaps], start=1):
        if not row.evidence:
            raise ValueError("final gaps require EvidenceRef")
        gaps.append(
            GapItem(
                gap_id=f"gap-{index}",
                description=f"Further work is needed around: {row.claim}",
                evidence=row.evidence,
            )
        )
    return GapList(gaps=gaps)
