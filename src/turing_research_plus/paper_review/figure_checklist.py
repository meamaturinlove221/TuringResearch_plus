"""Figure and table checklist builders for deep review."""

from __future__ import annotations

from turing_research_plus.paper_digest.models import PaperDigest
from turing_research_plus.paper_review.models import (
    DeepReviewItem,
    DeepReviewItemKind,
    DeepReviewStatus,
)


def build_figure_checklist(digest: PaperDigest) -> list[DeepReviewItem]:
    """Build figure inspection checklist items from a digest."""

    figures = digest.figures_to_inspect or ["requires-real-paper-review figure list"]
    return [
        DeepReviewItem(
            item_id=f"{digest.paper_id}-figure-{index}",
            kind=DeepReviewItemKind.FIGURE,
            description=figure,
            source_status=digest.source_status,
            status=DeepReviewStatus.NEEDS_REAL_PAPER
            if digest.requires_real_paper
            else DeepReviewStatus.IN_REVIEW,
        )
        for index, figure in enumerate(figures, start=1)
    ]


def build_table_checklist(digest: PaperDigest) -> list[DeepReviewItem]:
    """Build table inspection checklist items from a digest."""

    tables = digest.experiment_table_notes or ["requires-real-paper-review table list"]
    return [
        DeepReviewItem(
            item_id=f"{digest.paper_id}-table-{index}",
            kind=DeepReviewItemKind.TABLE,
            description=table,
            source_status=digest.source_status,
            status=DeepReviewStatus.NEEDS_REAL_PAPER
            if digest.requires_real_paper
            else DeepReviewStatus.IN_REVIEW,
        )
        for index, table in enumerate(tables, start=1)
    ]
