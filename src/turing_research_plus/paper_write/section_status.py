"""Section status helpers for paper scaffolds."""

from __future__ import annotations

from turing_research_plus.paper_write.models import PaperSectionPlan, PaperSectionStatus


def infer_section_status(
    *,
    evidence_refs: list[str] | None = None,
    missing_evidence: list[str] | None = None,
    unsafe_claims: list[str] | None = None,
) -> PaperSectionStatus:
    """Infer a conservative section status."""

    if unsafe_claims:
        return PaperSectionStatus.BLOCKED_UNSAFE_CLAIMS
    if missing_evidence:
        return PaperSectionStatus.NEEDS_EVIDENCE
    if evidence_refs:
        return PaperSectionStatus.NEEDS_HUMAN_REVIEW
    return PaperSectionStatus.OUTLINE_ONLY


def summarize_section_status(sections: list[PaperSectionPlan]) -> list[str]:
    """Create short status lines for section_status.md."""

    return [
        f"- `{section.section_id}` `{section.status}`: {section.title}"
        for section in sections
    ]
