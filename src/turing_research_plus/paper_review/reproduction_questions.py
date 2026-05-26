"""Reproduction question builders for paper deep review."""

from __future__ import annotations

from turing_research_plus.paper_digest.models import PaperDigest
from turing_research_plus.paper_review.models import (
    DeepReviewItem,
    DeepReviewItemKind,
    DeepReviewStatus,
)


def build_reproduction_questions(digest: PaperDigest) -> list[DeepReviewItem]:
    """Build implementation and reproduction questions from digest notes."""

    questions = [
        "What exact inputs, preprocessing, and camera/body assumptions are required?",
        "Which training objective and losses are needed for reproduction?",
        "Which artifacts, metrics, and tables are required to compare fairly?",
    ]
    if any("voxel" in note.lower() or "sparse" in note.lower() for note in digest.collision_notes):
        questions.append("Does the sparse or voxel component require backend evidence?")
    if any("smpl" in note.lower() for note in digest.collision_notes):
        questions.append("Which SMPL / SMPL-X assumptions affect transfer to our route?")
    return [
        DeepReviewItem(
            item_id=f"{digest.paper_id}-repro-{index}",
            kind=DeepReviewItemKind.REPRODUCTION,
            description=question,
            source_status=digest.source_status,
            status=DeepReviewStatus.BLOCKED
            if digest.requires_real_paper
            else DeepReviewStatus.IN_REVIEW,
        )
        for index, question in enumerate(questions, start=1)
    ]


def build_implementation_questions(digest: PaperDigest) -> list[DeepReviewItem]:
    """Build implementation questions from method notes."""

    notes = digest.pass2_notes or ["requires-real-paper-review implementation notes"]
    return [
        DeepReviewItem(
            item_id=f"{digest.paper_id}-implementation-{index}",
            kind=DeepReviewItemKind.IMPLEMENTATION,
            description=note,
            source_status=digest.source_status,
            status=DeepReviewStatus.NEEDS_REAL_PAPER
            if digest.requires_real_paper
            else DeepReviewStatus.IN_REVIEW,
        )
        for index, note in enumerate(notes, start=1)
    ]
