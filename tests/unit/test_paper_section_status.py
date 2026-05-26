from __future__ import annotations

from turing_research_plus.paper_write.models import PaperSectionPlan, PaperSectionStatus
from turing_research_plus.paper_write.section_status import (
    infer_section_status,
    summarize_section_status,
)


def test_infer_section_status_blocks_unsafe_claims_first() -> None:
    assert (
        infer_section_status(
            evidence_refs=["artifact.md"],
            missing_evidence=["real run"],
            unsafe_claims=["success without evidence"],
        )
        == PaperSectionStatus.BLOCKED_UNSAFE_CLAIMS
    )


def test_infer_section_status_requires_missing_evidence() -> None:
    assert (
        infer_section_status(missing_evidence=["real experiment"])
        == PaperSectionStatus.NEEDS_EVIDENCE
    )


def test_infer_section_status_marks_evidence_refs_for_review() -> None:
    assert (
        infer_section_status(evidence_refs=["evidence_summary.md"])
        == PaperSectionStatus.NEEDS_HUMAN_REVIEW
    )


def test_infer_section_status_defaults_to_outline_only() -> None:
    assert infer_section_status() == PaperSectionStatus.OUTLINE_ONLY


def test_summarize_section_status_exports_stable_lines() -> None:
    lines = summarize_section_status(
        [
            PaperSectionPlan(
                section_id="method",
                title="Method",
                status=PaperSectionStatus.OUTLINE_ONLY,
            )
        ]
    )

    assert lines == ["- `method` `outline-only`: Method"]
