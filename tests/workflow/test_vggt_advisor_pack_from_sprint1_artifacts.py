from pathlib import Path

from turing_research_plus.advisor.models import (
    AdvisorPackBuildInput,
    AdvisorReadinessStatus,
)
from turing_research_plus.advisor.pack_builder import write_advisor_pack

ROOT = Path("examples") / "vggt-human-prior-survey"


def test_vggt_advisor_pack_from_sprint1_artifacts(tmp_path: Path) -> None:
    pack = write_advisor_pack(
        AdvisorPackBuildInput(
            output_dir=tmp_path,
            dogfooding_doc_path=Path("docs/dogfooding-vggt-smplx.md"),
            vggt_evidence_doc_path=Path("docs/vggt-evidence-ledger.md"),
            artifact_auditor_doc_path=Path("docs/artifact-auditor.md"),
            visual_evidence_doc_path=Path("docs/visual-evidence-auditor.md"),
            sprint_plan_path=Path("docs/v0.2.0-sprint-1-plan.md"),
            risk_register_path=Path("docs/v0.2.0-sprint-1-risk-register.md"),
            local_scan_summary_path=ROOT / "local_scan_summary.md",
            local_scan_artifact_index_path=ROOT / "local_scan_artifact_index.md",
            local_scan_evidence_ledger_path=ROOT / "local_scan_evidence_ledger.json",
            visual_evidence_audit_report_path=ROOT / "visual_evidence_audit_report.md",
            visual_evidence_missing_items_path=ROOT / "visual_evidence_missing_items.md",
            visual_evidence_scorecard_path=ROOT / "visual_evidence_scorecard.json",
        )
    )

    assert pack.visual_readiness == AdvisorReadinessStatus.BLOCKED
    assert (tmp_path / "advisor_summary.md").exists()
    assert (tmp_path / "current_status.md").exists()
    assert (tmp_path / "evidence_summary.md").exists()
    assert (tmp_path / "visual_readiness.md").exists()
    assert (tmp_path / "failure_analysis.md").exists()
    assert (tmp_path / "next_actions.md").exists()

    summary = (tmp_path / "advisor_summary.md").read_text(encoding="utf-8")

    assert "SMPL-X feature encoding" in summary
    assert "V260 is hard-blocked" in summary
    assert "SparseConv3D success is not complete" in summary
    assert "advisor-ready" in summary
    assert "PPTX" in summary
