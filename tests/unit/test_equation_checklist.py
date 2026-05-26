from __future__ import annotations

from turing_research_plus.paper_digest.models import PaperDigest, PaperDigestSourceStatus
from turing_research_plus.paper_review.equation_checklist import build_equation_checklist


def test_equation_checklist_does_not_fabricate_equations() -> None:
    digest = PaperDigest(
        paper_id="paper",
        title="Paper",
        source_status=PaperDigestSourceStatus.FAKE_OR_MANUAL_NOTE,
        pass1_summary="scaffold",
        method_contribution="requires-real-paper-review",
        equations_to_inspect=[],
    )

    equations = build_equation_checklist(digest)

    assert equations[0].description == "requires-real-paper-review equation list"
    assert equations[0].source_status == "fake-or-manual-note"
    assert equations[0].requires_human_review is True
