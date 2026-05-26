from __future__ import annotations

from turing_research_plus.paper_digest.models import PaperDigest, PaperDigestSourceStatus
from turing_research_plus.paper_review.figure_checklist import (
    build_figure_checklist,
    build_table_checklist,
)


def test_figure_checklist_uses_digest_figures() -> None:
    digest = PaperDigest(
        paper_id="paper",
        title="Paper",
        source_status=PaperDigestSourceStatus.FAKE_OR_MANUAL_NOTE,
        pass1_summary="scaffold",
        method_contribution="requires-real-paper-review",
        figures_to_inspect=["Figure 1 architecture"],
        experiment_table_notes=["Table 1 experiments"],
    )

    figures = build_figure_checklist(digest)
    tables = build_table_checklist(digest)

    assert figures[0].kind == "figure"
    assert figures[0].status == "needs-real-paper"
    assert tables[0].kind == "table"
    assert tables[0].description == "Table 1 experiments"
