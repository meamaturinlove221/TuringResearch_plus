from __future__ import annotations

from pathlib import Path

from turing_research_plus.paper_write.markdown_export import (
    render_evidence_gap_report,
    render_paper_outline,
    render_section_status,
)
from turing_research_plus.paper_write.models import PaperSectionStatus
from turing_research_plus.paper_write.scaffold import build_vggt_paper_scaffold

ROOT = Path(__file__).resolve().parents[2]
KNOWLEDGE_PACK = (
    ROOT / "examples" / "vggt-human-prior-survey" / "research_knowledge_pack"
)


def test_build_vggt_paper_scaffold_keeps_results_unwritten() -> None:
    scaffold = build_vggt_paper_scaffold(KNOWLEDGE_PACK)

    assert scaffold.topic == "VGGT / SMPL-X Human Prior"
    assert scaffold.abstract_status == PaperSectionStatus.NEEDS_EVIDENCE
    assert scaffold.results_status == PaperSectionStatus.NEEDS_EVIDENCE
    assert scaffold.requires_human_review is True
    assert scaffold.generated_final_abstract is False
    assert scaffold.generated_final_results is False


def test_build_vggt_paper_scaffold_blocks_unsafe_vggt_claims() -> None:
    scaffold = build_vggt_paper_scaffold(KNOWLEDGE_PACK)

    unsafe = "\n".join(scaffold.unsafe_claims)

    assert "Do not claim SparseConv3D success." in unsafe
    assert "Do not claim full human completion." in unsafe
    assert "quantitative experiment numbers" in unsafe
    assert scaffold.experiment_plan.status == PaperSectionStatus.NEEDS_EVIDENCE


def test_paper_scaffold_markdown_exports_state_boundaries() -> None:
    scaffold = build_vggt_paper_scaffold(KNOWLEDGE_PACK)

    outline = render_paper_outline(scaffold)
    status = render_section_status(scaffold)
    gaps = render_evidence_gap_report(scaffold)

    assert "This is a scaffold, not final paper prose." in outline
    assert "No final abstract is generated." in outline
    assert "No final results are generated." in outline
    assert "Results status: `needs-evidence`" in status
    assert "Do not claim SparseConv3D success." in gaps
