from __future__ import annotations

from turing_research_plus.paper_digest.models import PaperDigest, PaperDigestSourceStatus
from turing_research_plus.paper_review.reproduction_questions import (
    build_implementation_questions,
    build_reproduction_questions,
)


def test_reproduction_questions_capture_sparse_and_smpl_blockers() -> None:
    digest = PaperDigest(
        paper_id="paper",
        title="Paper",
        source_status=PaperDigestSourceStatus.FAKE_OR_MANUAL_NOTE,
        pass1_summary="scaffold",
        pass2_notes=["Extract method mechanics from real paper."],
        method_contribution="requires-real-paper-review",
        collision_notes=[
            "SMPL / SMPL-X overlap requires paper-level verification.",
            "Sparse or voxel representation may overlap with route.",
        ],
    )

    questions = build_reproduction_questions(digest)
    implementation = build_implementation_questions(digest)

    descriptions = "\n".join(item.description for item in questions)
    assert "backend evidence" in descriptions
    assert "SMPL / SMPL-X assumptions" in descriptions
    assert implementation[0].description == "Extract method mechanics from real paper."
