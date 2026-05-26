"""Local tool wrappers for compliance review."""

from __future__ import annotations

from turing_research_plus.compliance.dataset_registry import vggt_raw_dataset_placeholder
from turing_research_plus.compliance.model_registry import smplx_model_placeholder
from turing_research_plus.compliance.models import ComplianceAsset, ComplianceAssetType
from turing_research_plus.compliance.report import render_compliance_report_markdown
from turing_research_plus.compliance.risk_checker import build_compliance_report


def compliance_build_report(
    *,
    report_id: str,
    datasets: list[ComplianceAsset] | None = None,
    models: list[ComplianceAsset] | None = None,
    papers: list[ComplianceAsset] | None = None,
    code_repos: list[ComplianceAsset] | None = None,
) -> str:
    """Build a compliance report and return Markdown."""

    report = build_compliance_report(
        report_id=report_id,
        datasets=datasets,
        models=models,
        papers=papers,
        code_repos=code_repos,
    )
    return render_compliance_report_markdown(report)


def compliance_build_vggt_fake_report() -> str:
    """Build the VGGT review-only fake compliance report."""

    paper = ComplianceAsset(
        asset_id="third_party_paper_figures",
        name="Third-party paper figures used as related-work references",
        asset_type=ComplianceAssetType.PAPER,
        license_name="review-required",
        usage_restrictions=[
            "third-party paper figures require reuse rights review",
            "do not copy figures into public case study without permission",
        ],
        source="paper digest fixture placeholders",
        bundled=False,
        public_release_allowed=None,
    )
    code = ComplianceAsset(
        asset_id="github_code_dependency",
        name="GitHub code dependency with missing license metadata",
        asset_type=ComplianceAssetType.CODE_REPO,
        license_name="unknown",
        usage_restrictions=[
            "GitHub code license missing",
            "record license before redistribution",
        ],
        source="fake dependency placeholder",
        bundled=False,
        public_release_allowed=None,
    )
    return compliance_build_report(
        report_id="vggt_fake_compliance",
        datasets=[vggt_raw_dataset_placeholder()],
        models=[smplx_model_placeholder()],
        papers=[paper],
        code_repos=[code],
    )
