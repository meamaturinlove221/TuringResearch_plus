from __future__ import annotations

import base64
import json
from pathlib import Path

import pytest

from turing_research.pdf.asset_report import extract_pdf_assets
from turing_research_plus.advisor.models import AdvisorPackBuildInput, AdvisorReadinessStatus
from turing_research_plus.advisor.pack_builder import build_advisor_pack
from turing_research_plus.artifact_audit.auditor import audit_artifacts
from turing_research_plus.artifact_audit.models import ArtifactAuditInput, ArtifactSafetyFlag
from turing_research_plus.paper.figure_registry import FigureAssetStatus
from turing_research_plus.paper.pdf_asset_import import register_pdf_assets
from turing_research_plus.vggt.edge_audit import audit_vggt_evidence_edges
from turing_research_plus.vggt.evidence_ledger import build_vggt_evidence_ledger
from turing_research_plus.vggt.evidence_models import (
    VGGTEvidenceLedgerBuildInput,
    VGGTEvidenceStatus,
)
from turing_research_plus.vggt.markdown_export import export_vggt_evidence_markdown

ROOT = Path("examples") / "vggt-human-prior-survey"
PNG_1X1 = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+/p9sAAAAASUVORK5CYII="
)


def test_vggt_sprint1_end_to_end_fake_flow(tmp_path: Path) -> None:
    ledger = build_vggt_evidence_ledger(
        VGGTEvidenceLedgerBuildInput(
            run_id="sprint1-integration",
            local_scan_summary_path=ROOT / "local_scan_summary.md",
            local_scan_artifact_index_path=ROOT / "local_scan_artifact_index.md",
            local_scan_evidence_ledger_path=ROOT / "local_scan_evidence_ledger.json",
        )
    )
    edge_audit = audit_vggt_evidence_edges(ledger)
    ledger_markdown = export_vggt_evidence_markdown(ledger)

    assert edge_audit.passed
    assert "V999-SparseConv3D" in ledger_markdown
    assert ledger.row_for("V260").status == VGGTEvidenceStatus.HARD_BLOCKED
    assert ledger.row_for("V999-SparseConv3D").status == VGGTEvidenceStatus.NOT_ENOUGH_EVIDENCE
    assert ledger.model_dump(mode="json")
    assert edge_audit.model_dump(mode="json")

    artifact_report = audit_artifacts(
        ArtifactAuditInput(source_path=ROOT / "local_scan_artifact_index.md")
    )
    assert artifact_report.records == []
    assert "No artifacts were scanned" in " ".join(artifact_report.warnings)

    manifest = tmp_path / "manifest.json"
    manifest.write_text(
        '{"records":[{"path":"D:/vggt/private.npz","file_type":"npz","included":true}]}',
        encoding="utf-8",
    )
    safety_report = audit_artifacts(ArtifactAuditInput(source_path=manifest))
    assert ArtifactSafetyFlag.PRIVATE_PATH_NOT_READ in safety_report.records[0].safety_flags

    scorecard = json.loads((ROOT / "visual_evidence_scorecard.json").read_text())
    assert scorecard["advisor_ready_visual_proof"] is False
    assert scorecard["required_visual_evidence"]["full_body"] == "missing"

    advisor_pack = build_advisor_pack(
        AdvisorPackBuildInput(
            output_dir=tmp_path / "advisor",
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
    assert advisor_pack.visual_readiness == AdvisorReadinessStatus.BLOCKED
    assert "SparseConv3D success is not complete" in advisor_pack.to_markdown()
    assert advisor_pack.model_dump(mode="json")

    pdf_path = _create_fixture_pdf(tmp_path)
    pdf_report = extract_pdf_assets(pdf_path, tmp_path / "pdf_assets")
    registry, outputs = register_pdf_assets(pdf_report, used_in_blocks=["related_work"])

    assert pdf_report.extracted_figures
    assert pdf_report.extracted_tables
    assert pdf_report.to_markdown()
    assert pdf_report.model_dump(mode="json")
    assert outputs
    assert all(asset.status == FigureAssetStatus.READY for asset in registry.assets)


def _create_fixture_pdf(tmp_path: Path) -> Path:
    fitz = pytest.importorskip("fitz")
    pdf_path = tmp_path / "sprint1.pdf"
    document = fitz.open()
    page = document.new_page()
    page.insert_text((72, 72), "Introduction\n| Item | Status |\n| Phase B | local |")
    page.insert_image(fitz.Rect(72, 140, 92, 160), stream=PNG_1X1)
    document.save(str(pdf_path))
    document.close()
    return pdf_path
