from __future__ import annotations

from pathlib import Path

from turing_research_plus.paper_write.tools import (
    method_section_build_vggt,
    method_section_export_markdown,
)

ROOT = Path(__file__).resolve().parents[2]
VGGT = ROOT / "examples" / "vggt-human-prior-survey"
COMMITTED_SCAFFOLD = VGGT / "paper_scaffold"


def test_vggt_method_section_skeleton_exports_markdown(tmp_path: Path) -> None:
    skeleton = method_section_build_vggt(
        VGGT / "paper_method_cards",
        VGGT / "architecture_diagrams",
        VGGT / "route_specs",
    )
    outputs = method_section_export_markdown(skeleton, tmp_path)

    assert {path.name for path in outputs} == {
        "method_section_skeleton.md",
        "method_figure_links.md",
    }
    section = (tmp_path / "method_section_skeleton.md").read_text(encoding="utf-8")
    figures = (tmp_path / "method_figure_links.md").read_text(encoding="utf-8")

    assert "## SMPL-X Feature Encoding" in section
    assert "## Hard Gates" in section
    assert "No method verification is claimed." in section
    assert "Do not claim SparseConv3D success." in section
    assert "not fabricated paper figures" in figures


def test_committed_vggt_method_section_examples_keep_boundaries() -> None:
    section = (COMMITTED_SCAFFOLD / "method_section_skeleton.md").read_text(
        encoding="utf-8"
    )
    figures = (COMMITTED_SCAFFOLD / "method_figure_links.md").read_text(
        encoding="utf-8"
    )

    assert "This is an evidence-linked skeleton, not a final method section." in section
    assert "requires-real-experiment" in section
    assert "SparseConv3D backend success is not established" in section
    assert "No final contribution claims are generated." in section
    assert "not fabricated paper figures" in figures
