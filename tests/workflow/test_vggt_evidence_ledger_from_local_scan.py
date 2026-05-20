from pathlib import Path

from tuling_research_plus.vggt.evidence_ledger import build_vggt_evidence_ledger
from tuling_research_plus.vggt.evidence_models import (
    VGGTEvidenceLedgerBuildInput,
    VGGTEvidenceStatus,
)


def test_vggt_evidence_ledger_from_committed_local_scan() -> None:
    root = Path("examples") / "vggt-human-prior-survey"

    ledger = build_vggt_evidence_ledger(
        VGGTEvidenceLedgerBuildInput(
            run_id="round-38-fixture",
            local_scan_summary_path=root / "local_scan_summary.md",
            local_scan_artifact_index_path=root / "local_scan_artifact_index.md",
            local_scan_evidence_ledger_path=root / "local_scan_evidence_ledger.json",
        )
    )

    assert ledger.row_for("V770").status == VGGTEvidenceStatus.LOCAL_OBSERVED
    assert ledger.row_for("V129").status == VGGTEvidenceStatus.OBSERVED
    assert ledger.row_for("V260").status == VGGTEvidenceStatus.HARD_BLOCKED
    assert ledger.row_for("V900").status == VGGTEvidenceStatus.OBSERVED
    assert ledger.row_for("V930").status == VGGTEvidenceStatus.OBSERVED
    assert ledger.row_for("V999").status == VGGTEvidenceStatus.OBSERVED
    assert ledger.row_for("V999-SparseConv3D").status == VGGTEvidenceStatus.NOT_ENOUGH_EVIDENCE
    assert ledger.row_for("V120").status == VGGTEvidenceStatus.REQUIRES_HUMAN_REVIEW
    assert ledger.row_for("V121").status == VGGTEvidenceStatus.REQUIRES_HUMAN_REVIEW
    assert "V120" in ledger.to_markdown()

