from __future__ import annotations

from pathlib import Path

from turing_research_plus.advisor_export.export_manifest import (
    build_advisor_export_manifest,
)
from turing_research_plus.advisor_export.models import (
    AdvisorBundleFile,
    AdvisorMarkdownBundle,
)

ROOT = Path(__file__).resolve().parents[2]
EXAMPLE = ROOT / "examples" / "vggt-human-prior-survey" / "advisor_export"
EXPORT_PLAN = EXAMPLE / "export_plan"


def _fixture_bundle() -> AdvisorMarkdownBundle:
    required = [
        "advisor_report_source.md",
        "slides_outline.md",
        "figure_list.md",
        "table_list.md",
        "evidence_refs.md",
        "limitations.md",
        "next_actions.md",
        "manifest.yaml",
    ]
    return AdvisorMarkdownBundle(
        bundle_id="vggt_advisor_markdown_bundle",
        topic="VGGT / SMPL-X Human Prior",
        output_dir=str(EXAMPLE),
        files=[
            AdvisorBundleFile(path=str(EXAMPLE / filename), role=filename)
            for filename in required
        ],
    )


def test_vggt_advisor_export_plan_fixture_is_plan_only() -> None:
    manifest = (EXPORT_PLAN / "export_manifest.yaml").read_text(encoding="utf-8")
    pdf_plan = (EXPORT_PLAN / "advisor_pdf_export_plan.md").read_text(encoding="utf-8")
    pptx_outline = (EXPORT_PLAN / "advisor_pptx_outline.md").read_text(encoding="utf-8")
    mapping = (EXPORT_PLAN / "slide_section_mapping.md").read_text(encoding="utf-8")

    assert "generated_binary_exports: false" in manifest
    assert "external_converter_called: false" in manifest
    assert "No real PDF was generated." in manifest
    assert "No real PPTX was generated." in manifest
    assert "Generated PDF: `false`" in pdf_plan
    assert "Generated PPTX: `false`" in pptx_outline
    assert "No PPTX file was generated" in mapping


def test_vggt_advisor_export_plan_runtime_matches_fixture_shape(tmp_path: Path) -> None:
    manifest = build_advisor_export_manifest(_fixture_bundle(), tmp_path)

    assert manifest.requires_human_review is True
    assert manifest.generated_binary_exports is False
    assert len(manifest.generated_files) == 4
    assert (tmp_path / "advisor_pdf_export_plan.md").exists()
    assert "Do not fabricate figures" in (
        tmp_path / "advisor_pdf_export_plan.md"
    ).read_text(encoding="utf-8")
