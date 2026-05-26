from __future__ import annotations

from pathlib import Path

import pytest

from turing_research_plus.advisor_export.export_manifest import (
    build_advisor_export_manifest,
    render_export_manifest,
)
from turing_research_plus.advisor_export.models import (
    AdvisorBundleFile,
    AdvisorExportManifest,
    AdvisorMarkdownBundle,
)


def _bundle() -> AdvisorMarkdownBundle:
    return AdvisorMarkdownBundle(
        bundle_id="bundle-1",
        topic="VGGT",
        output_dir="out",
        files=[
            AdvisorBundleFile(path=f"out/{filename}", role=filename)
            for filename in [
                "advisor_report_source.md",
                "slides_outline.md",
                "figure_list.md",
                "table_list.md",
                "evidence_refs.md",
                "limitations.md",
                "next_actions.md",
                "manifest.yaml",
            ]
        ],
    )


def test_advisor_export_manifest_writes_plan_files(tmp_path: Path) -> None:
    manifest = build_advisor_export_manifest(_bundle(), tmp_path)
    rendered = render_export_manifest(manifest)

    assert manifest.generated_binary_exports is False
    assert manifest.external_converter_called is False
    assert (tmp_path / "advisor_pdf_export_plan.md").exists()
    assert (tmp_path / "advisor_pptx_outline.md").exists()
    assert (tmp_path / "export_manifest.yaml").exists()
    assert (tmp_path / "slide_section_mapping.md").exists()
    assert "generated_binary_exports: false" in rendered


def test_advisor_export_manifest_rejects_binary_claim(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="must not claim binary generation"):
        AdvisorExportManifest(
            manifest_id="manifest-1",
            source_bundle_id="bundle-1",
            output_dir=str(tmp_path),
            generated_files=[
                str(tmp_path / "advisor_pdf_export_plan.md"),
                str(tmp_path / "advisor_pptx_outline.md"),
                str(tmp_path / "export_manifest.yaml"),
                str(tmp_path / "slide_section_mapping.md"),
            ],
            generated_binary_exports=True,
        )


def test_advisor_export_manifest_requires_all_files(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="missing files"):
        AdvisorExportManifest(
            manifest_id="manifest-1",
            source_bundle_id="bundle-1",
            output_dir=str(tmp_path),
            generated_files=[str(tmp_path / "export_manifest.yaml")],
        )
