from __future__ import annotations

from pathlib import Path

from turing_research_plus.paper_write.tools import (
    experiment_section_build_vggt,
    experiment_section_export_markdown,
)

ROOT = Path(__file__).resolve().parents[2]
VGGT = ROOT / "examples" / "vggt-human-prior-survey"
COMMITTED_SCAFFOLD = VGGT / "paper_scaffold"


def test_vggt_experiment_section_skeleton_exports_markdown(tmp_path: Path) -> None:
    skeleton = experiment_section_build_vggt(
        VGGT / "run_ingest_report.md",
        VGGT / "dashboard",
        VGGT / "route_specs" / "modal_sparseconv_v0.yaml",
    )
    outputs = experiment_section_export_markdown(skeleton, tmp_path)

    assert {path.name for path in outputs} == {
        "experiment_section_skeleton.md",
        "result_table_missing_items.md",
    }
    section = (tmp_path / "experiment_section_skeleton.md").read_text(
        encoding="utf-8"
    )
    missing = (tmp_path / "result_table_missing_items.md").read_text(
        encoding="utf-8"
    )

    assert "Route status: `requires-real-experiment`" in section
    assert "Run status: `ROUTE_EXHAUSTED_WITH_FAILURE_ANALYSIS`" in section
    assert "Dashboard is not a paper result." in section
    assert "No figure or table is fabricated." in section
    assert "Result tables allowed: `false`" in missing


def test_committed_vggt_experiment_section_examples_keep_boundaries() -> None:
    section = (COMMITTED_SCAFFOLD / "experiment_section_skeleton.md").read_text(
        encoding="utf-8"
    )
    missing = (COMMITTED_SCAFFOLD / "result_table_missing_items.md").read_text(
        encoding="utf-8"
    )

    assert "not a paper results section" in section
    assert "SparseConv3D success is not established." in section
    assert "No result value is generated." in section
    assert "`predictions.npz`" in missing
    assert "Do not claim SparseConv3D success without backend evidence." in missing
