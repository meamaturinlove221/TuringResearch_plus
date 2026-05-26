"""Build conservative paper deep review reports."""

from __future__ import annotations

from pathlib import Path

from turing_research_plus.paper_digest.digest_builder import build_paper_digest
from turing_research_plus.paper_digest.models import (
    PaperDigest,
    PaperDigestInput,
    PaperDigestSourceStatus,
)
from turing_research_plus.paper_review.equation_checklist import build_equation_checklist
from turing_research_plus.paper_review.figure_checklist import (
    build_figure_checklist,
    build_table_checklist,
)
from turing_research_plus.paper_review.models import (
    DeepReviewItem,
    DeepReviewItemKind,
    DeepReviewReport,
    DeepReviewStatus,
)
from turing_research_plus.paper_review.reproduction_questions import (
    build_implementation_questions,
    build_reproduction_questions,
)


def build_deep_review_report(
    digest: PaperDigest,
    *,
    report_id: str | None = None,
    relation_to_our_project: list[str] | None = None,
) -> DeepReviewReport:
    """Build a deep review checklist report from a PaperDigest."""

    reading_status = (
        DeepReviewStatus.NEEDS_REAL_PAPER
        if digest.requires_real_paper
        else DeepReviewStatus.IN_REVIEW
    )
    claims = _claim_verification_items(digest)
    advisor_notes = _advisor_notes(digest)
    return DeepReviewReport(
        report_id=report_id or f"{digest.paper_id}_deep_review",
        paper_id=digest.paper_id,
        title=digest.title,
        source_status=digest.source_status,
        reading_status=reading_status,
        figures_to_inspect=build_figure_checklist(digest),
        equations_to_inspect=build_equation_checklist(digest),
        tables_to_inspect=build_table_checklist(digest),
        implementation_questions=build_implementation_questions(digest),
        reproduction_blockers=build_reproduction_questions(digest),
        relation_to_our_project=relation_to_our_project
        or _relation_to_project(digest),
        claims_requiring_verification=claims,
        notes_for_advisor=advisor_notes,
        limitations=[
            "Deep review report is a checklist, not proof of full paper reading.",
            "No final paper conclusion is generated.",
            "No formulas, figures, or citations are fabricated.",
            *digest.limitations,
        ],
    )


def build_neuralbody_deep_review_fixture(root: Path) -> DeepReviewReport:
    """Build the VGGT NeuralBody deep-review fixture from local notes."""

    source = (
        root
        / "examples"
        / "vggt-human-prior-survey"
        / "paper_method_cards"
        / "neuralbody.fixture.md"
    )
    digest = build_paper_digest(
        PaperDigestInput(
            paper_id="neuralbody-fixture",
            title="NeuralBody Fixture",
            source_status=PaperDigestSourceStatus.FAKE_OR_MANUAL_NOTE,
            source_text=source.read_text(encoding="utf-8"),
        )
    )
    return build_deep_review_report(
        digest,
        report_id="neuralbody_deep_review_fixture",
        relation_to_our_project=[
            "Use as sparse voxel / body-prior related-work candidate only.",
            "Do not treat fixture as citation-grade source.",
            "Verify method mechanics, figures, equations, and tables from the real paper.",
        ],
    )


def _claim_verification_items(digest: PaperDigest) -> list[DeepReviewItem]:
    claims = [
        *digest.related_work_positioning,
        *digest.collision_notes,
        *digest.what_to_borrow,
    ] or ["requires-real-paper-review claim list"]
    return [
        DeepReviewItem(
            item_id=f"{digest.paper_id}-claim-{index}",
            kind=DeepReviewItemKind.CLAIM,
            description=claim,
            source_status=digest.source_status,
            status=DeepReviewStatus.BLOCKED
            if digest.requires_real_paper
            else DeepReviewStatus.IN_REVIEW,
        )
        for index, claim in enumerate(claims, start=1)
    ]


def _advisor_notes(digest: PaperDigest) -> list[DeepReviewItem]:
    notes = [
        "Ask advisor whether this paper is central enough for full manual review.",
        "Confirm whether figures/tables can be cited or must be redrawn from scratch.",
        "Keep fixture status visible in related-work planning.",
    ]
    return [
        DeepReviewItem(
            item_id=f"{digest.paper_id}-advisor-{index}",
            kind=DeepReviewItemKind.ADVISOR_NOTE,
            description=note,
            source_status=digest.source_status,
            status=DeepReviewStatus.NEEDS_REAL_PAPER,
        )
        for index, note in enumerate(notes, start=1)
    ]


def _relation_to_project(digest: PaperDigest) -> list[str]:
    return [
        *digest.related_work_positioning,
        *digest.collision_notes,
        "Relation to our project remains provisional until real paper review.",
    ]
