"""Export manifest builder for plan-only advisor PDF / PPTX outputs."""

from __future__ import annotations

from pathlib import Path

from turing_research_plus.advisor_export.models import (
    AdvisorExportFormat,
    AdvisorExportManifest,
    AdvisorMarkdownBundle,
)
from turing_research_plus.advisor_export.pdf_plan import (
    build_pdf_export_plan,
    render_pdf_export_plan,
)
from turing_research_plus.advisor_export.pptx_plan import (
    build_pptx_export_plan,
    render_pptx_outline,
    render_slide_section_mapping,
)

EXPORT_PLAN_FILES = [
    "advisor_pdf_export_plan.md",
    "advisor_pptx_outline.md",
    "export_manifest.yaml",
    "slide_section_mapping.md",
]


def build_advisor_export_manifest(
    bundle: AdvisorMarkdownBundle,
    output_dir: Path,
    *,
    write_files: bool = True,
) -> AdvisorExportManifest:
    """Build and optionally write the plan-only advisor export package."""

    pdf_plan = build_pdf_export_plan(bundle)
    pptx_plan = build_pptx_export_plan(bundle)
    contents = {
        "advisor_pdf_export_plan.md": render_pdf_export_plan(pdf_plan),
        "advisor_pptx_outline.md": render_pptx_outline(pptx_plan),
        "slide_section_mapping.md": render_slide_section_mapping(pptx_plan),
    }

    manifest = AdvisorExportManifest(
        manifest_id=f"{bundle.bundle_id}_pdf_pptx_export_manifest",
        source_bundle_id=bundle.bundle_id,
        output_dir=str(output_dir),
        generated_files=[str(output_dir / filename) for filename in EXPORT_PLAN_FILES],
        planned_formats=[AdvisorExportFormat.PDF, AdvisorExportFormat.PPTX],
        optional_adapters=[
            "future markdown-to-pdf adapter",
            "future markdown-to-pptx adapter",
        ],
        safety_warnings=[
            "No real PDF was generated.",
            "No real PPTX was generated.",
            "No external converter or office tool was called.",
            "No fabricated charts, figures, or experiment results are included.",
            "Planned work remains planned and is not observed evidence.",
        ],
        limitations=[
            "This package is an export plan and template package only.",
            "Human review is required before advisor delivery.",
            "Future binary adapters must preserve this manifest boundary.",
        ],
    )
    contents["export_manifest.yaml"] = render_export_manifest(manifest)

    if write_files:
        output_dir.mkdir(parents=True, exist_ok=True)
        for filename, content in contents.items():
            (output_dir / filename).write_text(content, encoding="utf-8")

    return manifest


def render_export_manifest(manifest: AdvisorExportManifest) -> str:
    """Render the export manifest as small YAML."""

    lines = [
        f"manifest_id: {manifest.manifest_id}",
        f"source_bundle_id: {manifest.source_bundle_id}",
        f"output_dir: {manifest.output_dir}",
        "generated_binary_exports: false",
        "external_converter_called: false",
        "requires_human_review: true",
        "planned_formats:",
    ]
    lines.extend([f"  - {item.value}" for item in manifest.planned_formats])
    lines.append("generated_files:")
    lines.extend([f"  - {Path(item).name}" for item in manifest.generated_files])
    lines.append("optional_adapters:")
    lines.extend([f"  - {item}" for item in manifest.optional_adapters])
    lines.append("safety_warnings:")
    lines.extend([f"  - {item}" for item in manifest.safety_warnings])
    lines.append("limitations:")
    lines.extend([f"  - {item}" for item in manifest.limitations])
    lines.append("")
    return "\n".join(lines)
