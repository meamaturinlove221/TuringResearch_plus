from __future__ import annotations

from pathlib import Path

from turing_research_plus.paper_write.draft_assembly import assemble_paper_draft_beta
from turing_research_plus.paper_write.draft_package import export_paper_draft_package

ROOT = Path(__file__).resolve().parents[2]
SCAFFOLD = ROOT / "examples" / "vggt-human-prior-survey" / "paper_scaffold"
COMMITTED_DRAFT = SCAFFOLD / "draft_beta"


def test_vggt_paper_draft_beta_exports_review_package(tmp_path: Path) -> None:
    package = assemble_paper_draft_beta(SCAFFOLD)
    outputs = export_paper_draft_package(package, tmp_path)

    assert len(outputs) == 4
    draft = (tmp_path / "paper_draft_beta.md").read_text(encoding="utf-8")
    assert "Paper Draft Beta Package" in draft
    assert "Abstract placeholder only" in draft
    assert "Result tables allowed: `false`" in draft
    assert "This is not a final paper." in draft
    assert "SparseConv3D success is not established" in draft
    assert "No final result section is generated." in draft


def test_committed_vggt_paper_draft_beta_keeps_boundaries() -> None:
    draft = (COMMITTED_DRAFT / "paper_draft_beta.md").read_text(encoding="utf-8")
    missing = (COMMITTED_DRAFT / "missing_evidence_report.md").read_text(
        encoding="utf-8"
    )
    unsafe = (COMMITTED_DRAFT / "unsafe_claim_report.md").read_text(encoding="utf-8")
    citations = (COMMITTED_DRAFT / "citation_status_report.md").read_text(
        encoding="utf-8"
    )

    assert "This is not a final paper." in draft
    assert "No final result section is generated." in draft
    assert "Result tables allowed: `false`" in draft
    assert "`exp-real-sparse-backend`" in missing
    assert "Fake observed claim blocked: `true`" in unsafe
    assert "Fabricated citation blocked: `true`" in citations
    assert "SparseConv3D integration is already successful." in unsafe
    assert "risky unblocked" not in unsafe.lower()
