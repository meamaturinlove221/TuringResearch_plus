from __future__ import annotations

from pathlib import Path

from turing_research_plus.paper_write.tools import (
    related_work_draft_build_vggt,
    related_work_draft_export_markdown,
)

ROOT = Path(__file__).resolve().parents[2]
VGGT = ROOT / "examples" / "vggt-human-prior-survey"
COMMITTED_SCAFFOLD = VGGT / "paper_scaffold"


def test_vggt_related_work_draft_exports_markdown(tmp_path: Path) -> None:
    skeleton = related_work_draft_build_vggt(
        VGGT / "related_work",
        VGGT / "collision_risk",
        VGGT / "paper_digest",
    )
    outputs = related_work_draft_export_markdown(skeleton, tmp_path)

    assert {path.name for path in outputs} == {
        "related_work_skeleton.md",
        "citation_safety_report.md",
    }
    draft = (tmp_path / "related_work_skeleton.md").read_text(encoding="utf-8")
    safety = (tmp_path / "citation_safety_report.md").read_text(encoding="utf-8")

    assert "## Neural Body / Sparse Voxel" in draft
    assert "## Tri-plane / Rasterized Pose Feature" in draft
    assert "source_status=`requires-real-paper-review`" in draft
    assert "No final related-work paragraph is generated." in draft
    assert "Fake fixtures are not final citations." in safety


def test_committed_vggt_related_work_draft_examples_keep_boundaries() -> None:
    draft = (COMMITTED_SCAFFOLD / "related_work_skeleton.md").read_text(
        encoding="utf-8"
    )
    safety = (COMMITTED_SCAFFOLD / "citation_safety_report.md").read_text(
        encoding="utf-8"
    )

    assert "not camera-ready related-work text" in draft
    assert "source_status=`fake-or-manual-note`" in draft
    assert "The related work has been completely reviewed" in draft
    assert "No citation is fabricated." in safety
    assert "Human review is required before camera-ready paper text." in safety
