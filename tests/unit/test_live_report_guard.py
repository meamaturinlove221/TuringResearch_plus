from __future__ import annotations

from turing_research_plus.live_safety import guard_live_report, render_live_report_guard


def test_live_report_guard_blocks_and_renders_sanitized_output() -> None:
    result = guard_live_report(
        report_id="live-report-001",
        source="apify",
        live_output=(
            "token" + "=secret-token-123456789 "
            "private_content=private scraped body "
            "C:/Users/researcher/raw.txt"
        ),
    )
    rendered = render_live_report_guard(result)

    assert result.blocked is True
    assert result.raw_output_retained is False
    assert result.automatic_evidence_write is False
    assert result.requires_human_review is True
    assert result.redactions
    assert "secret-token-123456789" not in result.sanitized_text
    assert "private scraped body" not in result.sanitized_text
    assert "C:/Users/researcher" not in result.sanitized_text
    assert "Raw output retained: `false`" in rendered
    assert "Automatic evidence write: `false`" in rendered
    assert "[REDACTED_TOKEN]" in rendered
    assert "[REDACTED_RAW_PRIVATE_CONTENT]" in rendered


def test_live_report_guard_allows_clean_summary_but_requires_review() -> None:
    result = guard_live_report(
        report_id="live-report-clean",
        source="scholar",
        live_output="retrieved title only; no raw private content retained",
    )

    assert result.blocked is False
    assert result.redactions == []
    assert result.raw_output_retained is False
    assert result.automatic_evidence_write is False
    assert result.requires_human_review is True
    assert result.warnings == ["no sensitive live output detected; human review still required"]
