"""Local helper wrappers for advisor export planning."""

from __future__ import annotations

from pathlib import Path

from turing_research_plus.advisor_export.export_manifest import (
    build_advisor_export_manifest,
)
from turing_research_plus.advisor_export.export_plan import build_advisor_export_plan
from turing_research_plus.advisor_export.markdown_bundle import (
    build_advisor_markdown_bundle,
)
from turing_research_plus.advisor_export.models import (
    AdvisorExportManifest,
    AdvisorExportPlan,
    AdvisorMarkdownBundle,
    AdvisorMarkdownBundleRequest,
    AdvisorPdfExportPlan,
    AdvisorPptxExportPlan,
)
from turing_research_plus.advisor_export.pdf_exporter import (
    build_advisor_pdf_export_plan,
    export_advisor_pdf_optional,
)
from turing_research_plus.advisor_export.pdf_models import (
    AdvisorPdfExportResult,
    AdvisorRealPdfExportPlan,
)
from turing_research_plus.advisor_export.pdf_plan import build_pdf_export_plan
from turing_research_plus.advisor_export.pptx_exporter import (
    build_advisor_pptx_export_plan,
    export_advisor_pptx_optional,
)
from turing_research_plus.advisor_export.pptx_models import (
    AdvisorPptxExportResult,
    AdvisorRealPptxExportPlan,
)
from turing_research_plus.advisor_export.pptx_plan import build_pptx_export_plan


def advisor_markdown_bundle_build(
    request: AdvisorMarkdownBundleRequest,
) -> AdvisorMarkdownBundle:
    """Build a Markdown-only advisor bundle."""

    return build_advisor_markdown_bundle(request)


def advisor_export_plan_build(bundle: AdvisorMarkdownBundle) -> AdvisorExportPlan:
    """Build a future export plan from a Markdown bundle."""

    return build_advisor_export_plan(bundle)


def advisor_pdf_export_plan_build(bundle: AdvisorMarkdownBundle) -> AdvisorPdfExportPlan:
    """Build a plan-only PDF export specification."""

    return build_pdf_export_plan(bundle)


def advisor_pptx_export_plan_build(bundle: AdvisorMarkdownBundle) -> AdvisorPptxExportPlan:
    """Build a plan-only PPTX export specification."""

    return build_pptx_export_plan(bundle)


def advisor_pdf_pptx_manifest_build(
    bundle: AdvisorMarkdownBundle,
    output_dir: Path,
) -> AdvisorExportManifest:
    """Build a plan-only PDF/PPTX export package manifest."""

    return build_advisor_export_manifest(bundle, output_dir)


def advisor_real_pdf_export_plan_build(
    bundle: AdvisorMarkdownBundle,
    output_dir: Path,
) -> AdvisorRealPdfExportPlan:
    """Build a concrete optional PDF export plan."""

    return build_advisor_pdf_export_plan(bundle, output_dir)


def advisor_real_pdf_export_optional(
    bundle: AdvisorMarkdownBundle,
    output_dir: Path,
    *,
    force_skip: bool = False,
) -> AdvisorPdfExportResult:
    """Optionally export an advisor PDF, gracefully skipping missing backends."""

    return export_advisor_pdf_optional(bundle, output_dir, force_skip=force_skip)


def advisor_real_pptx_export_plan_build(
    bundle: AdvisorMarkdownBundle,
    output_dir: Path,
) -> AdvisorRealPptxExportPlan:
    """Build a concrete optional PPTX export plan."""

    return build_advisor_pptx_export_plan(bundle, output_dir)


def advisor_real_pptx_export_optional(
    bundle: AdvisorMarkdownBundle,
    output_dir: Path,
    *,
    force_skip: bool = False,
) -> AdvisorPptxExportResult:
    """Optionally export an advisor PPTX, gracefully skipping missing backends."""

    return export_advisor_pptx_optional(bundle, output_dir, force_skip=force_skip)
