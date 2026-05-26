from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CASE_STUDY = ROOT / "examples" / "vggt-human-prior-survey" / "public_case_study"


def test_committed_vggt_public_case_study_is_sanitized() -> None:
    draft = (CASE_STUDY / "case_study_draft.md").read_text(encoding="utf-8")
    redaction = (CASE_STUDY / "redaction_report.md").read_text(encoding="utf-8")
    claim = (CASE_STUDY / "claim_safety_report.md").read_text(encoding="utf-8")

    assert "VGGT Human Prior Dogfooding Case Study Draft" in draft
    assert "What Not To Claim" in draft
    assert "Do not claim SparseConv3D success" in draft
    assert "It does not claim experiment success." in draft
    assert "D:/vggt" not in draft
    assert "SMPLX_model.pkl" not in draft
    assert "raw data" not in draft.lower()
    assert "private advisor feedback" not in draft.lower()
    assert "Sanitized: `true`" in redaction
    assert "Safe to publish: `true`" in claim


def test_public_case_study_reports_human_review_boundary() -> None:
    draft = (CASE_STUDY / "case_study_draft.md").read_text(encoding="utf-8")

    assert "requires human review" in draft.lower()
    assert "This case study is not a publication." in draft
    assert "It does not claim experiment success." in draft
