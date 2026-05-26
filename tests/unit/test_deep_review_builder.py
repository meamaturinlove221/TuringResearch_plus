from __future__ import annotations

from turing_research_plus.paper_digest.models import PaperDigest, PaperDigestSourceStatus
from turing_research_plus.paper_review.deep_review import build_deep_review_report


def test_deep_review_builder_blocks_fake_digest_as_real_review() -> None:
    digest = PaperDigest(
        paper_id="paper",
        title="Paper",
        source_status=PaperDigestSourceStatus.FAKE_OR_MANUAL_NOTE,
        pass1_summary="scaffold only",
        method_contribution="requires-real-paper-review",
        figures_to_inspect=["Figure 1 layout"],
        equations_to_inspect=["Equation placeholder"],
        experiment_table_notes=["Table 1 metrics"],
        collision_notes=["Sparse or voxel representation requires review."],
        related_work_positioning=["Use as related-work context only."],
        what_to_borrow=["method vocabulary after review"],
        requires_real_paper=True,
    )

    report = build_deep_review_report(digest)

    assert report.reading_status == "needs-real-paper"
    assert report.downloaded_pdf is False
    assert report.generated_final_conclusion is False
    assert any("Sparse" in item.description for item in report.claims_requiring_verification)
    assert any("advisor" in item.kind for item in report.notes_for_advisor)


def test_deep_review_builder_keeps_relation_provisional() -> None:
    digest = PaperDigest(
        paper_id="paper",
        title="Paper",
        source_status=PaperDigestSourceStatus.MANUAL_NOTE,
        pass1_summary="scaffold only",
        method_contribution="requires-real-paper-review",
        requires_real_paper=True,
    )

    report = build_deep_review_report(digest)

    assert any("provisional" in item.lower() for item in report.relation_to_our_project)
    assert "No final paper conclusion is generated." in report.limitations
