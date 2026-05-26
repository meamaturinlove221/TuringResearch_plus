import pytest
from pydantic import ValidationError

from turing_research_plus.artifacts.models import EvidenceRef
from turing_research_plus.survey.gap_extractor import extract_gaps
from turing_research_plus.survey.models import EvidenceMatrix, EvidenceMatrixRow


def test_gap_extraction_requires_evidence() -> None:
    with pytest.raises(ValidationError):
        EvidenceMatrixRow(claim="Unsupported claim", paper_ids=["p1"], evidence=[])


def test_gap_extraction_returns_evidence_backed_gaps() -> None:
    matrix = EvidenceMatrix(
        rows=[
            EvidenceMatrixRow(
                claim="Few studies compare runtime gates.",
                paper_ids=["p1"],
                evidence=[
                    EvidenceRef(
                        source_id="p1",
                        locator="section-2",
                        quote="Runtime gates remain underexplored.",
                    )
                ],
            )
        ]
    )

    gaps = extract_gaps(matrix)

    assert gaps.gaps[0].gap_id == "gap-1"
    assert gaps.gaps[0].evidence[0].source_id == "p1"
