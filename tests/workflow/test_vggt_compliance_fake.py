from __future__ import annotations

from pathlib import Path

from turing_research_plus.compliance.tools import compliance_build_vggt_fake_report

ROOT = Path(__file__).resolve().parents[2]
REPORT_PATH = (
    ROOT
    / "examples"
    / "vggt-human-prior-survey"
    / "compliance"
    / "compliance_report.md"
)


def test_vggt_compliance_fake_report_records_review_boundaries() -> None:
    report = compliance_build_vggt_fake_report()

    assert "SMPL-X body model files" in report
    assert "not bundled" in report
    assert "VGGT private/raw experiment data" in report
    assert "GitHub code license missing" in report
    assert "not legal advice" in report.lower()
    assert "D:/vggt" not in report


def test_committed_vggt_compliance_fixture_matches_boundaries() -> None:
    text = REPORT_PATH.read_text(encoding="utf-8")

    assert "Compliance Report: vggt_fake_compliance" in text
    assert "requires human review: `true`" in text
    assert "not legal advice" in text.lower()
    assert "SMPL-X body model files" in text
    assert "not bundled" in text
    assert "D:/vggt" not in text
