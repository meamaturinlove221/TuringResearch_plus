from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_v0_7_export_contracts_exist_and_require_review() -> None:
    contract_names = [
        "dashboard_refinement.yaml",
        "advisor_pdf_export.yaml",
        "advisor_pptx_export.yaml",
        "export_quality_gate.yaml",
    ]

    for name in contract_names:
        text = (ROOT / "contracts" / name).read_text(encoding="utf-8")
        assert "status: implemented_minimal" in text
        assert "network_behavior: no_network" in text
        assert (
            "human_review_required: true" in text
            or "requires_human_review: true" in text
        )


def test_v0_7_export_docs_and_fixtures_exist() -> None:
    paths = [
        "docs/dashboard-refinement.md",
        "docs/advisor-real-pdf-export.md",
        "docs/advisor-real-pptx-export.md",
        "docs/export-quality-gate.md",
        "examples/vggt-human-prior-survey/dashboard_html/refined_dashboard.html",
        "examples/vggt-human-prior-survey/advisor_export/pdf_export/pdf_export_report.md",
        "examples/vggt-human-prior-survey/advisor_export/pptx_export/pptx_export_report.md",
        "examples/vggt-human-prior-survey/advisor_export/export_quality_report.md",
    ]

    for path in paths:
        assert (ROOT / path).exists(), path


def test_v0_7_export_fixtures_keep_optional_backend_boundary() -> None:
    pdf = (
        ROOT
        / "examples"
        / "vggt-human-prior-survey"
        / "advisor_export"
        / "pdf_export"
        / "pdf_export_report.md"
    ).read_text(encoding="utf-8")
    pptx = (
        ROOT
        / "examples"
        / "vggt-human-prior-survey"
        / "advisor_export"
        / "pptx_export"
        / "pptx_export_report.md"
    ).read_text(encoding="utf-8")

    assert "status: skipped" in pdf
    assert "PDF backend intentionally skipped" in pdf
    assert "status: skipped" in pptx
    assert "PPTX backend intentionally skipped" in pptx
    assert "Planned work remains planned and is not observed evidence" in pdf
    assert "Planned work remains planned and is not observed evidence" in pptx
