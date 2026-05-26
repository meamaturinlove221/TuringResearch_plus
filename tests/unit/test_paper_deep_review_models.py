from __future__ import annotations

import pytest

from turing_research_plus.paper_review.models import (
    DeepReviewItem,
    DeepReviewItemKind,
    DeepReviewReport,
    DeepReviewStatus,
)


def _item(item_id: str, kind: DeepReviewItemKind) -> DeepReviewItem:
    return DeepReviewItem(
        item_id=item_id,
        kind=kind,
        description="requires-real-paper-review",
    )


def test_deep_review_report_serializes_required_fields() -> None:
    report = DeepReviewReport(
        report_id="review",
        paper_id="paper",
        title="Paper",
        source_status="fake-or-manual-note",
        reading_status=DeepReviewStatus.NEEDS_REAL_PAPER,
        figures_to_inspect=[_item("fig", DeepReviewItemKind.FIGURE)],
        equations_to_inspect=[_item("eq", DeepReviewItemKind.EQUATION)],
        tables_to_inspect=[_item("table", DeepReviewItemKind.TABLE)],
        reproduction_blockers=[_item("repro", DeepReviewItemKind.REPRODUCTION)],
    )

    payload = report.model_dump(mode="json")

    assert payload["reading_status"] == "needs-real-paper"
    assert payload["requires_human_review"] is True
    assert payload["copied_long_text"] is False
    assert payload["generated_final_conclusion"] is False


def test_deep_review_report_rejects_final_conclusion() -> None:
    with pytest.raises(ValueError, match="final conclusions"):
        DeepReviewReport(
            report_id="bad",
            paper_id="paper",
            title="Paper",
            source_status="manual-note",
            reading_status=DeepReviewStatus.IN_REVIEW,
            figures_to_inspect=[_item("fig", DeepReviewItemKind.FIGURE)],
            equations_to_inspect=[_item("eq", DeepReviewItemKind.EQUATION)],
            tables_to_inspect=[_item("table", DeepReviewItemKind.TABLE)],
            reproduction_blockers=[_item("repro", DeepReviewItemKind.REPRODUCTION)],
            generated_final_conclusion=True,
        )


def test_deep_review_item_requires_human_review() -> None:
    with pytest.raises(ValueError, match="require human review"):
        DeepReviewItem(
            item_id="bad",
            kind=DeepReviewItemKind.CLAIM,
            description="claim",
            requires_human_review=False,
        )
