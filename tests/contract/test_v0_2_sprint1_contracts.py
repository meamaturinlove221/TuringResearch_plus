from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_sprint1_contract_files_exist_and_declare_boundaries() -> None:
    required = [
        "contracts/vggt_evidence.yaml",
        "contracts/artifact_audit.yaml",
        "contracts/visual_evidence.yaml",
        "contracts/advisor_pack.yaml",
        "contracts/pdf_markdown.yaml",
        "contracts/paper_pipeline.yaml",
    ]

    for path in required:
        assert (ROOT / path).exists(), path

    assert "not-enough-evidence" in read("contracts/vggt_evidence.yaml")
    assert "private" in read("contracts/artifact_audit.yaml").lower()
    assert "dry-run artifact surface" in read("contracts/visual_evidence.yaml")
    assert "Do not generate PPTX or PDF" in read("contracts/advisor_pack.yaml")
    assert "PDFAssetExtractionReport" in read("contracts/pdf_markdown.yaml")
    assert "original_pdf_source" in read("contracts/paper_pipeline.yaml")


def test_sprint1_docs_record_non_goals_and_limitations() -> None:
    report = read("docs/v0.2.0-sprint-1-integration-report.md")
    limitations = read("docs/v0.2.0-sprint-1-known-limitations.md")

    assert "Future Sync Adapters remain non-goal" in report
    assert "Visual Evidence Auditor is currently a dry-run artifact surface" in limitations
    assert "SparseConv3D success is not claimed" in limitations
    assert "No OCR" in limitations


def test_sprint1_mcp_statuses_are_aligned_for_pdf_phase_b() -> None:
    contracts = read("contracts/pdf_markdown.yaml")
    docs = read("docs/mcp-tools.md")

    for tool in ["pdf.extract_figures", "pdf.extract_tables", "pdf.sectionize"]:
        assert tool in contracts
        assert tool in docs
    assert "PDFAssetExtractionReport" in docs
    assert "implementation_status: implemented_minimal" in contracts
