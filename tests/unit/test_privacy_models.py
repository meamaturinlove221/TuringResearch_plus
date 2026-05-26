from __future__ import annotations

import pytest

from turing_research_plus.privacy.models import (
    PrivacyFinding,
    PrivacyFindingType,
    PrivacyScanReport,
    PrivacySeverity,
    RedactionProposal,
    SafetyLevel,
)


def test_privacy_scan_report_summarizes_release_blocker() -> None:
    finding = PrivacyFinding(
        path=".env",
        finding_type=PrivacyFindingType.ENV_FILE,
        safety_level=SafetyLevel.SECRET_FORBIDDEN,
        severity=PrivacySeverity.CRITICAL,
        matched_rule="env-file",
        message="Environment file",
        recommended_action="Remove it.",
        release_blocker=True,
    )
    report = PrivacyScanReport(scanned_paths=[".env"], findings=[finding])

    assert report.severity == PrivacySeverity.CRITICAL
    assert report.release_blocker is True
    assert report.requires_human_review is True
    assert "Block release" in report.recommended_action


def test_privacy_report_requires_human_review() -> None:
    with pytest.raises(ValueError, match="require human review"):
        PrivacyScanReport(requires_human_review=False)


def test_redaction_proposal_cannot_be_destructive() -> None:
    with pytest.raises(ValueError, match="non-destructive"):
        RedactionProposal(
            path="notes.md",
            finding_type=PrivacyFindingType.TOKEN_PATTERN,
            destructive=True,
        )
