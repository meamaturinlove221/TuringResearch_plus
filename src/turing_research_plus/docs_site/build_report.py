"""Build hardening report for local docs-site exports."""

from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from turing_research_plus.docs_site.link_checker import (
    DocsSiteLinkCheckReport,
    check_docs_site_links,
)
from turing_research_plus.docs_site.static_export import (
    DocsSiteStaticExportManifest,
    export_static_docs_site,
)

BuildHardeningStatus = Literal["pass", "pass_with_warnings", "blocked"]


class DocsSiteBuildHardeningReport(BaseModel):
    """Combined docs-site build hardening report."""

    model_config = ConfigDict(extra="forbid")

    site_id: str = Field(min_length=1)
    status: BuildHardeningStatus
    link_report: DocsSiteLinkCheckReport
    export_manifest: DocsSiteStaticExportManifest
    deployment_performed: bool = False
    requires_human_review: bool = True

    @model_validator(mode="after")
    def build_report_must_not_deploy(self) -> DocsSiteBuildHardeningReport:
        if self.deployment_performed:
            raise ValueError("docs-site build hardening report must not deploy")
        if not self.requires_human_review:
            raise ValueError("docs-site build hardening report requires human review")
        return self


def build_docs_site_hardening_report(
    repo_root: Path,
    *,
    output_root: Path | None = None,
) -> DocsSiteBuildHardeningReport:
    """Run link checks and local static export, returning a deployment-ready report."""

    link_report = check_docs_site_links(repo_root)
    export_manifest = export_static_docs_site(
        repo_root,
        output_root=output_root,
        write_manifest=False,
    )
    status = _status(link_report, export_manifest)
    return DocsSiteBuildHardeningReport(
        site_id=export_manifest.site_id,
        status=status,
        link_report=link_report,
        export_manifest=export_manifest,
    )


def render_build_hardening_markdown(report: DocsSiteBuildHardeningReport) -> str:
    """Render a human-readable docs-site build hardening report."""

    lines = [
        "# Docs Site Build Report",
        "",
        f"Status: {report.status}.",
        "",
        f"Site ID: `{report.site_id}`",
        f"Deployment performed: `{str(report.deployment_performed).lower()}`",
        f"Requires human review: `{str(report.requires_human_review).lower()}`",
        "",
        "## Summary",
        "",
        f"- Checked pages: {len(report.link_report.checked_pages)}",
        f"- Checked source docs: {len(report.link_report.checked_source_docs)}",
        f"- Generated files: {len(report.export_manifest.files)}",
        f"- Nav validation warnings: {len(report.link_report.nav_validation_warnings)}",
        f"- Missing pages: {len(report.link_report.missing_pages)}",
        f"- Broken links: {len(report.link_report.broken_links)}",
        f"- Missing source docs: {len(report.link_report.missing_source_docs)}",
        f"- Orphan pages: {len(report.link_report.orphan_pages)}",
        f"- Private path hits: {len(report.link_report.private_path_hits)}",
        "",
        "## Build Boundaries",
        "",
        "- no deployment",
        "- no live network",
        "- no analytics",
        "- no private data required",
        "- human review required before publication",
        "",
        "## Generated Files",
        "",
    ]
    for file in report.export_manifest.files:
        lines.append(f"- `{file.path}` ({file.kind}, `{file.sha256}`)")
    if not report.export_manifest.files:
        lines.append("- none")
    lines.extend(["", "## Findings", ""])
    finding_groups = [
        ("Nav validation", report.link_report.nav_validation_warnings),
        ("Missing pages", [item.message for item in report.link_report.missing_pages]),
        ("Broken links", [item.message for item in report.link_report.broken_links]),
        (
            "Missing source docs",
            [item.message for item in report.link_report.missing_source_docs],
        ),
        ("Orphan pages", [item.message for item in report.link_report.orphan_pages]),
        ("Private path hits", [item.message for item in report.link_report.private_path_hits]),
    ]
    for title, items in finding_groups:
        lines.extend([f"### {title}", ""])
        if items:
            lines.extend(f"- {item}" for item in items)
        else:
            lines.append("- none")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _status(
    link_report: DocsSiteLinkCheckReport,
    export_manifest: DocsSiteStaticExportManifest,
) -> BuildHardeningStatus:
    if link_report.has_blockers:
        return "blocked"
    if link_report.nav_validation_warnings or link_report.orphan_pages or export_manifest.warnings:
        return "pass_with_warnings"
    return "pass"
