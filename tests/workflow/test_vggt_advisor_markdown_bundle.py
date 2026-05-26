from __future__ import annotations

from pathlib import Path

from turing_research_plus.advisor_export.markdown_bundle import (
    build_advisor_markdown_bundle,
)
from turing_research_plus.advisor_export.models import AdvisorMarkdownBundleRequest

ROOT = Path(__file__).resolve().parents[2]
EXAMPLE = ROOT / "examples" / "vggt-human-prior-survey" / "advisor_export"


def test_vggt_advisor_markdown_bundle_fixture_keeps_export_boundary() -> None:
    manifest = (EXAMPLE / "manifest.yaml").read_text(encoding="utf-8")
    report_source = (EXAMPLE / "advisor_report_source.md").read_text(encoding="utf-8")
    slides = (EXAMPLE / "slides_outline.md").read_text(encoding="utf-8")

    assert "generated_binary_exports: false" in manifest
    assert "no_pdf_generated" in manifest
    assert "no_pptx_generated" in manifest
    assert "SparseConv3D success is not claimed" in report_source
    assert "No PPTX file was generated" in slides


def test_vggt_advisor_markdown_bundle_runtime_matches_required_files(
    tmp_path: Path,
) -> None:
    bundle = build_advisor_markdown_bundle(
        AdvisorMarkdownBundleRequest(
            output_dir=tmp_path,
            advisor_pack_dir=ROOT
            / "examples"
            / "vggt-human-prior-survey"
            / "advisor_pack",
            knowledge_pack_dir=ROOT
            / "examples"
            / "vggt-human-prior-survey"
            / "research_knowledge_pack",
        )
    )

    assert len(bundle.files) == 8
    assert bundle.generated_pdf is False
    assert bundle.generated_pptx is False
    assert (tmp_path / "advisor_report_source.md").exists()
    assert "Planned work is not observed evidence" in (
        tmp_path / "advisor_report_source.md"
    ).read_text(encoding="utf-8")
