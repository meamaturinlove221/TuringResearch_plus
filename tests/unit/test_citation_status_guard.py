from __future__ import annotations

import pytest

from turing_research_plus.paper_write.citation_status_guard import (
    PaperCitationStatus,
    parse_citation_status_report,
    render_paper_citation_status_report,
)


def test_citation_status_guard_parses_fixture_citations() -> None:
    markdown = """# Citation Safety Report

| Citation | Source status | Citation grade | Requires review |
| --- | --- | --- | --- |
| `humanram-fixture` | `fake-or-manual-note` | `false` | `true` |
| `hart-review-needed` | `requires-real-paper-review` | `false` | `true` |
"""
    report = parse_citation_status_report(markdown)

    assert len(report.citations) == 2
    assert report.fabricated_citation_blocked is True
    assert all(not citation.citation_grade for citation in report.citations)
    assert len(report.blocked_citations) == 2


def test_citation_status_guard_rejects_fixture_as_citation_grade() -> None:
    with pytest.raises(ValueError):
        PaperCitationStatus(
            citation_id="fixture",
            source_status="fake-or-manual-note",
            citation_grade=True,
        )


def test_citation_status_guard_renders_review_boundary() -> None:
    report = parse_citation_status_report(
        "| Citation | Source status | Citation grade | Requires review |\n"
        "| --- | --- | --- | --- |\n"
        "| `x` | `requires-real-paper-review` | `false` | `true` |\n"
    )
    rendered = render_paper_citation_status_report(report)

    assert "Fixture citations are not final paper citations." in rendered
    assert "`x` remains `requires-real-paper-review`" in rendered
