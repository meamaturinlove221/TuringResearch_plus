from __future__ import annotations

from turing_research_plus.privacy.models import (
    PrivacyFinding,
    PrivacyFindingType,
    PrivacyScanReport,
    PrivacySeverity,
    SafetyLevel,
)
from turing_research_plus.privacy.report import render_privacy_scan_report_markdown


def test_privacy_report_markdown_lists_findings_and_boundary() -> None:
    report = PrivacyScanReport(
        scanned_paths=["notes.md"],
        findings=[
            PrivacyFinding(
                path="notes.md",
                finding_type=PrivacyFindingType.PRIVATE_ADVISOR_FEEDBACK,
                safety_level=SafetyLevel.PRIVATE_RESEARCH,
                severity=PrivacySeverity.MEDIUM,
                matched_rule="private-advisor-feedback",
                message="private feedback",
                recommended_action="Review before public release.",
                redaction_possible=True,
            )
        ],
    )
    markdown = render_privacy_scan_report_markdown(report)

    assert "# Privacy Scan Report" in markdown
    assert "`medium`" in markdown
    assert "Review before public release" in markdown
    assert "Human review" in markdown or "human review" in markdown
