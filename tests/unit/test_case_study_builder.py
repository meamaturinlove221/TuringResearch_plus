from __future__ import annotations

from pathlib import Path

from turing_research_plus.case_study.builder import build_vggt_public_case_study
from turing_research_plus.case_study.markdown_export import render_case_study_draft_markdown

ROOT = Path(__file__).resolve().parents[2]


def test_vggt_public_case_study_builder_creates_required_sections() -> None:
    draft = build_vggt_public_case_study(ROOT)
    markdown = render_case_study_draft_markdown(draft)

    assert draft.case_study_id == "vggt_public_case_study_draft"
    assert len(draft.sections) == 8
    assert draft.published is False
    assert draft.requires_human_review is True
    assert "Problem Background" in markdown
    assert "Why TuringResearch Was Useful" in markdown
    assert "What Not To Claim" in markdown
    assert "does not claim SparseConv3D success" in markdown
    assert "D:/vggt" not in markdown


def test_vggt_public_case_study_keeps_claim_guard_clean() -> None:
    draft = build_vggt_public_case_study(ROOT)

    assert draft.claim_safety_report.safe_to_publish is True
    assert draft.claim_safety_report.unsupported_experiment_claims == []
    assert any(
        "Do not claim SparseConv3D success" in bullet
        for bullet in draft.what_not_to_claim.bullets
    )
