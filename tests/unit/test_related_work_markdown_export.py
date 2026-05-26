from __future__ import annotations

from turing_research_plus.related_work.markdown_export import (
    export_related_work_positioning_markdown,
)
from turing_research_plus.related_work.models import RelatedWorkPositioningInput
from turing_research_plus.related_work.positioning import build_related_work_positioning


def test_related_work_markdown_export_contains_review_sections() -> None:
    report = build_related_work_positioning(
        RelatedWorkPositioningInput(
            method_cards=[
                {
                    "paper_id": "humanram",
                    "title": "HumanRAM",
                    "representation": ["tri-plane"],
                }
            ]
        )
    )

    markdown = export_related_work_positioning_markdown(report)

    assert "# Related Work Positioning Report" in markdown
    assert "## Safe Claims" in markdown
    assert "## Unsafe Claims" in markdown
    assert "Requires human review" in markdown
