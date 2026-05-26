"""Equation checklist builders for deep review."""

from __future__ import annotations

from turing_research_plus.paper_digest.models import PaperDigest
from turing_research_plus.paper_review.models import (
    DeepReviewItem,
    DeepReviewItemKind,
    DeepReviewStatus,
)


def build_equation_checklist(digest: PaperDigest) -> list[DeepReviewItem]:
    """Build equation inspection checklist items without fabricating equations."""

    equations = digest.equations_to_inspect or [
        "requires-real-paper-review equation list"
    ]
    return [
        DeepReviewItem(
            item_id=f"{digest.paper_id}-equation-{index}",
            kind=DeepReviewItemKind.EQUATION,
            description=equation,
            source_status=digest.source_status,
            status=DeepReviewStatus.NEEDS_REAL_PAPER
            if digest.requires_real_paper
            else DeepReviewStatus.IN_REVIEW,
        )
        for index, equation in enumerate(equations, start=1)
    ]
