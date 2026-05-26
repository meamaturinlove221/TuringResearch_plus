from pathlib import Path

from turing_research_plus.vggt.evidence_ledger import build_vggt_evidence_ledger
from turing_research_plus.vggt.evidence_models import (
    VGGTEvidenceLedgerBuildInput,
    VGGTEvidenceStatus,
)


def fixture_path(*parts: str) -> Path:
    return Path("examples", "vggt-human-prior-survey", *parts)


def test_build_default_ledger_keeps_v120_v121_human_review() -> None:
    ledger = build_vggt_evidence_ledger(
        VGGTEvidenceLedgerBuildInput(
            local_scan_summary_path=fixture_path("local_scan_summary.md"),
            local_scan_artifact_index_path=fixture_path("local_scan_artifact_index.md"),
            local_scan_evidence_ledger_path=fixture_path("local_scan_evidence_ledger.json"),
        )
    )

    assert ledger.row_for("V120").status == VGGTEvidenceStatus.REQUIRES_HUMAN_REVIEW
    assert ledger.row_for("V121").status == VGGTEvidenceStatus.REQUIRES_HUMAN_REVIEW
    assert "local_scan_evidence_ledger.json" not in " ".join(ledger.missing_inputs)
    assert ledger.row_for("V120").blockers


def test_v999_sparseconv3d_success_is_not_enough_evidence() -> None:
    ledger = build_vggt_evidence_ledger(
        VGGTEvidenceLedgerBuildInput(
            local_scan_summary_path=fixture_path("local_scan_summary.md"),
            local_scan_artifact_index_path=fixture_path("local_scan_artifact_index.md"),
        )
    )

    sparse_row = ledger.row_for("V999-SparseConv3D")

    assert sparse_row.status == VGGTEvidenceStatus.NOT_ENOUGH_EVIDENCE
    assert sparse_row.blockers


def test_expected_vggt_versions_are_present() -> None:
    ledger = build_vggt_evidence_ledger(
        VGGTEvidenceLedgerBuildInput(
            local_scan_summary_path=fixture_path("local_scan_summary.md"),
            local_scan_artifact_index_path=fixture_path("local_scan_artifact_index.md"),
        )
    )

    labels = {row.version_label for row in ledger.rows}

    assert {"V770", "V129", "V260", "V900", "V930", "V999", "V120", "V121"} <= labels
