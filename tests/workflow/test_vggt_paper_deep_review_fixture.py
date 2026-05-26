from __future__ import annotations

from pathlib import Path

from turing_research_plus.paper_review.deep_review import (
    build_neuralbody_deep_review_fixture,
)
from turing_research_plus.paper_review.markdown_export import (
    render_deep_review_report_markdown,
)

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = (
    ROOT
    / "examples"
    / "vggt-human-prior-survey"
    / "paper_deep_review"
    / "neuralbody_review_checklist.md"
)


def test_vggt_neuralbody_deep_review_fixture_is_review_only() -> None:
    report = build_neuralbody_deep_review_fixture(ROOT)
    markdown = render_deep_review_report_markdown(report)

    assert report.paper_id == "neuralbody-fixture"
    assert report.reading_status == "needs-real-paper"
    assert report.requires_human_review is True
    assert report.downloaded_pdf is False
    assert report.generated_final_conclusion is False
    assert "not a claim of completed real deep reading" in markdown
    assert "No PDF is downloaded" in markdown


def test_committed_neuralbody_deep_review_fixture_keeps_boundaries() -> None:
    text = FIXTURE.read_text(encoding="utf-8")

    assert "Paper Deep Review: NeuralBody Fixture" in text
    assert "Source status: `fake-or-manual-note`" in text
    assert "Reading status: `needs-real-paper`" in text
    assert "Figures To Inspect" in text
    assert "Equations To Inspect" in text
    assert "Reproduction Blockers" in text
    assert "No equation is fabricated" in text
    assert "No final paper conclusion is generated" in text
    assert "D:/vggt" not in text
