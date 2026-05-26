"""Models for Advisor Export planning and Markdown bundles."""

from __future__ import annotations

from enum import StrEnum
from pathlib import Path
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class AdvisorExportFormat(StrEnum):
    """Future export formats."""

    PDF = "pdf"
    PPTX = "pptx"
    DOCX = "docx"
    HTML = "html"
    MARKDOWN_BUNDLE = "markdown-bundle"


class AdvisorBundleFile(BaseModel):
    """One file in an advisor Markdown bundle."""

    model_config = ConfigDict(extra="forbid")

    path: str = Field(min_length=1)
    role: str = Field(min_length=1)
    source_refs: list[str] = Field(default_factory=list)
    generated: bool = True


class AdvisorMarkdownBundle(BaseModel):
    """Markdown source package for future advisor exports."""

    model_config = ConfigDict(extra="forbid")

    bundle_id: str = Field(min_length=1)
    topic: str = Field(min_length=1)
    output_dir: str = Field(min_length=1)
    files: list[AdvisorBundleFile]
    future_exports: list[AdvisorExportFormat] = Field(
        default_factory=lambda: [
            AdvisorExportFormat.PDF,
            AdvisorExportFormat.PPTX,
            AdvisorExportFormat.DOCX,
            AdvisorExportFormat.HTML,
        ]
    )
    source_paths: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    requires_human_review: bool = True
    generated_pdf: bool = False
    generated_pptx: bool = False

    @model_validator(mode="after")
    def markdown_bundle_does_not_claim_binary_export(self) -> Self:
        if self.generated_pdf or self.generated_pptx:
            raise ValueError("Markdown bundle must not claim PDF/PPTX generation")
        required = {
            "advisor_report_source.md",
            "slides_outline.md",
            "figure_list.md",
            "table_list.md",
            "evidence_refs.md",
            "limitations.md",
            "next_actions.md",
            "manifest.yaml",
        }
        present = {Path(item.path).name for item in self.files}
        missing = required - present
        if missing:
            raise ValueError(f"advisor markdown bundle missing files: {sorted(missing)}")
        return self


class AdvisorExportPlan(BaseModel):
    """Plan for future advisor export formats."""

    model_config = ConfigDict(extra="forbid")

    plan_id: str = Field(min_length=1)
    source_bundle_id: str = Field(min_length=1)
    target_formats: list[AdvisorExportFormat]
    conversion_tools: list[str] = Field(default_factory=list)
    safety_requirements: list[str] = Field(default_factory=list)
    non_goals: list[str] = Field(default_factory=list)
    implementation_status: str = Field(default="planned", min_length=1)
    requires_human_review: bool = True

    @model_validator(mode="after")
    def export_plan_is_not_generation(self) -> Self:
        if self.implementation_status not in {"planned", "design", "markdown-source-ready"}:
            raise ValueError("export plan cannot claim binary export implementation")
        return self


class AdvisorPdfExportPlan(BaseModel):
    """Plan-only PDF export specification."""

    model_config = ConfigDict(extra="forbid")

    plan_id: str = Field(min_length=1)
    source_bundle_id: str = Field(min_length=1)
    output_filename: str = Field(default="advisor_pdf_export_plan.md", min_length=1)
    document_title: str = Field(min_length=1)
    source_files: list[str] = Field(default_factory=list)
    section_order: list[str] = Field(default_factory=list)
    template_name: str = Field(default="advisor_pdf_review_template", min_length=1)
    adapter_status: str = Field(default="optional_not_run", min_length=1)
    generated_pdf: bool = False
    external_converter_called: bool = False
    safety_warnings: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    requires_human_review: bool = True

    @model_validator(mode="after")
    def pdf_plan_is_not_binary_generation(self) -> Self:
        if self.generated_pdf:
            raise ValueError("PDF export plan must not claim generated PDF output")
        if self.external_converter_called:
            raise ValueError("PDF export plan must not call external converters")
        if not self.requires_human_review:
            raise ValueError("PDF export plan requires human review")
        return self


class AdvisorPptxSlidePlan(BaseModel):
    """One planned slide in a PPTX outline."""

    model_config = ConfigDict(extra="forbid")

    slide_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    source_sections: list[str] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)
    requires_human_review: bool = True


class AdvisorPptxExportPlan(BaseModel):
    """Plan-only PPTX export specification."""

    model_config = ConfigDict(extra="forbid")

    plan_id: str = Field(min_length=1)
    source_bundle_id: str = Field(min_length=1)
    output_filename: str = Field(default="advisor_pptx_outline.md", min_length=1)
    slide_mapping_filename: str = Field(default="slide_section_mapping.md", min_length=1)
    deck_title: str = Field(min_length=1)
    slides: list[AdvisorPptxSlidePlan] = Field(default_factory=list)
    template_name: str = Field(default="advisor_pptx_review_outline", min_length=1)
    adapter_status: str = Field(default="optional_not_run", min_length=1)
    generated_pptx: bool = False
    external_converter_called: bool = False
    safety_warnings: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    requires_human_review: bool = True

    @model_validator(mode="after")
    def pptx_plan_is_not_binary_generation(self) -> Self:
        if self.generated_pptx:
            raise ValueError("PPTX export plan must not claim generated PPTX output")
        if self.external_converter_called:
            raise ValueError("PPTX export plan must not call external converters")
        if not self.requires_human_review:
            raise ValueError("PPTX export plan requires human review")
        if not self.slides:
            raise ValueError("PPTX export plan requires at least one slide")
        return self


class AdvisorExportManifest(BaseModel):
    """Manifest for a plan-only advisor PDF/PPTX export package."""

    model_config = ConfigDict(extra="forbid")

    manifest_id: str = Field(min_length=1)
    source_bundle_id: str = Field(min_length=1)
    output_dir: str = Field(min_length=1)
    generated_files: list[str] = Field(default_factory=list)
    planned_formats: list[AdvisorExportFormat] = Field(default_factory=list)
    generated_binary_exports: bool = False
    external_converter_called: bool = False
    optional_adapters: list[str] = Field(default_factory=list)
    safety_warnings: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    requires_human_review: bool = True

    @model_validator(mode="after")
    def manifest_preserves_plan_only_boundary(self) -> Self:
        if self.generated_binary_exports:
            raise ValueError("advisor export manifest must not claim binary generation")
        if self.external_converter_called:
            raise ValueError("advisor export manifest must not call external converters")
        required = {
            "advisor_pdf_export_plan.md",
            "advisor_pptx_outline.md",
            "export_manifest.yaml",
            "slide_section_mapping.md",
        }
        present = {Path(item).name for item in self.generated_files}
        missing = required - present
        if missing:
            raise ValueError(f"advisor export manifest missing files: {sorted(missing)}")
        if not self.requires_human_review:
            raise ValueError("advisor export manifest requires human review")
        return self


class AdvisorMarkdownBundleRequest(BaseModel):
    """Input for building a local advisor Markdown bundle."""

    model_config = ConfigDict(extra="forbid")

    bundle_id: str = Field(default="vggt_advisor_markdown_bundle", min_length=1)
    topic: str = Field(default="VGGT / SMPL-X Human Prior", min_length=1)
    output_dir: Path
    advisor_pack_dir: Path
    knowledge_pack_dir: Path
