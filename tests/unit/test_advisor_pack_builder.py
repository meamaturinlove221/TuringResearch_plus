from pathlib import Path

from turing_research_plus.advisor.models import (
    AdvisorPackBuildInput,
    AdvisorReadinessStatus,
)
from turing_research_plus.advisor.pack_builder import build_advisor_pack

ROOT = Path("examples") / "vggt-human-prior-survey"


def request_for_example(tmp_path: Path | None = None) -> AdvisorPackBuildInput:
    return AdvisorPackBuildInput(
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


def test_build_advisor_pack_blocks_visual_readiness() -> None:
    pack = build_advisor_pack(request_for_example())

    assert pack.visual_readiness == AdvisorReadinessStatus.BLOCKED
    assert any("SMPL-X feature encoding" in item for item in pack.what_changed_since_last_update)
    assert any("V260 is hard-blocked" in claim for claim in pack.not_ready_claims)
    assert any("SparseConv3D success is not complete" in claim for claim in pack.not_ready_claims)
    assert not any("local_scan_evidence_ledger.json" in item for item in pack.missing_inputs)
    assert any("Full body" in item for item in pack.blockers)
    assert "direct SMPL-X replacement" in pack.current_route_summary


def test_build_advisor_pack_does_not_write_planned_as_observed() -> None:
    pack = build_advisor_pack(request_for_example())
    text = pack.to_markdown()

    assert "Modal Real SparseConv3D is planned / next action" in text
    assert "SparseConv3D success is not complete" in text
    assert "V999 long-run route status is not final target achievement" in text
    assert "PPTX" in text
