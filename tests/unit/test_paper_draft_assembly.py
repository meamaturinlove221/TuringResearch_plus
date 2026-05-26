from __future__ import annotations

from pathlib import Path

import pytest

from turing_research_plus.paper_write.draft_assembly import assemble_paper_draft_beta
from turing_research_plus.paper_write.draft_package import (
    PaperDraftPackage,
    export_paper_draft_package,
    render_paper_draft_package,
)

ROOT = Path(__file__).resolve().parents[2]
SCAFFOLD = ROOT / "examples" / "vggt-human-prior-survey" / "paper_scaffold"


def test_assemble_paper_draft_beta_keeps_results_blocked() -> None:
    package = assemble_paper_draft_beta(SCAFFOLD)

    assert package.package_id == "vggt_paper_draft_beta"
    assert package.title_candidates
    assert "placeholder" in package.abstract_placeholder.lower()
    assert "Result tables allowed: `false`" in package.results_blocked_section
    assert package.generated_final_paper is False
    assert package.generated_final_abstract is False
    assert package.generated_final_results is False
    assert package.camera_ready_text is False


def test_paper_draft_package_rejects_final_outputs() -> None:
    with pytest.raises(ValueError):
        PaperDraftPackage(
            package_id="bad",
            topic="Bad",
            title_candidates=["Bad"],
            abstract_placeholder="Final abstract",
            introduction_skeleton="Intro",
            related_work_skeleton="Related",
            method_skeleton="Method",
            experiment_skeleton="Experiment",
            results_blocked_section="Result tables allowed: `true`",
            limitations="Limitations",
            missing_evidence_report="Missing",
            unsafe_claim_report="Unsafe",
            citation_status_report="Citations",
            generated_final_paper=True,
        )


def test_export_paper_draft_package_writes_review_files(tmp_path: Path) -> None:
    package = assemble_paper_draft_beta(SCAFFOLD)
    outputs = export_paper_draft_package(package, tmp_path)

    assert {path.name for path in outputs} == {
        "paper_draft_beta.md",
        "missing_evidence_report.md",
        "unsafe_claim_report.md",
        "citation_status_report.md",
    }
    draft = render_paper_draft_package(package)
    assert "This is not a final paper." in draft
    assert "No final result section is generated." in draft
    assert (tmp_path / "paper_draft_beta.md").exists()
