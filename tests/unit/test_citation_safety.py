from __future__ import annotations

from pathlib import Path

import pytest

from turing_research_plus.paper_write.citation_safety import (
    RelatedWorkCitation,
    citation_from_digest_fixture,
    evaluate_citation_safety,
    render_citation_safety_report,
)

ROOT = Path(__file__).resolve().parents[2]
DIGESTS = ROOT / "examples" / "vggt-human-prior-survey" / "paper_digest"


def test_citation_from_digest_fixture_keeps_source_status() -> None:
    citation = citation_from_digest_fixture(DIGESTS / "neuralbody_digest.fixture.md")

    assert citation.citation_id == "neuralbody-fixture"
    assert citation.source_status == "fake-or-manual-note"
    assert citation.requires_human_review is True
    assert citation.citation_grade is False


def test_fixture_citation_cannot_be_citation_grade() -> None:
    with pytest.raises(ValueError, match="cannot be citation-grade"):
        RelatedWorkCitation(
            citation_id="fake-paper",
            title="Fake Paper",
            source_status="fake-or-manual-note",
            citation_grade=True,
        )


def test_citation_safety_report_flags_fixture_and_review_items() -> None:
    citations = [
        citation_from_digest_fixture(DIGESTS / "humanram_digest.fixture.md"),
        RelatedWorkCitation(
            citation_id="hart-review-needed",
            title="HART",
            source_status="requires-real-paper-review",
        ),
    ]

    report = evaluate_citation_safety(citations)
    markdown = render_citation_safety_report(report)

    assert len(report.unsafe_citations) == 2
    assert len(report.missing_review) == 2
    assert "Fake fixtures are not final citations." in markdown
    assert "No citation is fabricated." in markdown
