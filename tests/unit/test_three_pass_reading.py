from __future__ import annotations

from turing_research_plus.paper_digest.three_pass import build_three_pass_notes


def test_three_pass_notes_are_review_scaffold() -> None:
    notes = build_three_pass_notes(
        "# HumanRAM\nSMPL-X tri-plane token geometry note for review."
    )

    assert "Bird's-eye scan" in notes.pass1_summary
    assert any("SMPL-X" in item for item in notes.pass2_notes)
    assert any("VGGT mapping" in item for item in notes.pass3_deep_notes)
    assert notes.requires_real_paper_review is True
