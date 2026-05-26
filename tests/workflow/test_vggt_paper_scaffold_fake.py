from __future__ import annotations

from pathlib import Path

from turing_research_plus.paper_write.scaffold import build_vggt_paper_scaffold
from turing_research_plus.paper_write.tools import paper_scaffold_export_markdown

ROOT = Path(__file__).resolve().parents[2]
KNOWLEDGE_PACK = (
    ROOT / "examples" / "vggt-human-prior-survey" / "research_knowledge_pack"
)
COMMITTED_SCAFFOLD = ROOT / "examples" / "vggt-human-prior-survey" / "paper_scaffold"


def test_vggt_paper_scaffold_exports_review_only_markdown(tmp_path: Path) -> None:
    scaffold = build_vggt_paper_scaffold(KNOWLEDGE_PACK)
    outputs = paper_scaffold_export_markdown(scaffold, tmp_path)

    assert {path.name for path in outputs} == {
        "paper_outline.md",
        "section_status.md",
        "evidence_gap_report.md",
    }
    outline = (tmp_path / "paper_outline.md").read_text(encoding="utf-8")
    status = (tmp_path / "section_status.md").read_text(encoding="utf-8")
    gaps = (tmp_path / "evidence_gap_report.md").read_text(encoding="utf-8")

    assert "This is a scaffold, not final paper prose." in outline
    assert "No final results are generated." in outline
    assert "Results status: `needs-evidence`" in status
    assert "`exp-real-sparse-backend`" in gaps
    assert "Do not claim SparseConv3D success." in gaps


def test_committed_vggt_paper_scaffold_examples_keep_boundaries() -> None:
    outline = (COMMITTED_SCAFFOLD / "paper_outline.md").read_text(encoding="utf-8")
    status = (COMMITTED_SCAFFOLD / "section_status.md").read_text(encoding="utf-8")
    gaps = (COMMITTED_SCAFFOLD / "evidence_gap_report.md").read_text(
        encoding="utf-8"
    )

    assert "No final abstract is generated." in outline
    assert "No final results are generated." in outline
    assert "Results status: `needs-evidence`" in status
    assert "Do not claim SparseConv3D success." in gaps
    assert "success claim" in gaps
