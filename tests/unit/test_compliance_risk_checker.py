from __future__ import annotations

from turing_research_plus.compliance.dataset_registry import vggt_raw_dataset_placeholder
from turing_research_plus.compliance.model_registry import smplx_model_placeholder
from turing_research_plus.compliance.models import ComplianceAsset, ComplianceAssetType
from turing_research_plus.compliance.risk_checker import (
    build_compliance_report,
    check_asset_risk,
)


def test_risk_checker_blocks_restricted_assets() -> None:
    findings = check_asset_risk(smplx_model_placeholder())

    assert any(finding.release_blocker for finding in findings)
    assert any("restricted" in finding.message.lower() for finding in findings)


def test_risk_checker_blocks_raw_dataset_public_packaging() -> None:
    findings = check_asset_risk(vggt_raw_dataset_placeholder())

    assert any("raw dataset" in finding.message.lower() for finding in findings)
    assert any(finding.release_blocker for finding in findings)


def test_compliance_report_collects_unknown_license_and_paper_figure_review() -> None:
    paper = ComplianceAsset(
        asset_id="paper_figures",
        name="Third-party paper figures",
        asset_type=ComplianceAssetType.PAPER,
        license_name="review-required",
        usage_restrictions=["third-party figure reuse requires permission"],
    )
    code = ComplianceAsset(
        asset_id="github_repo",
        name="GitHub repo with no license file",
        asset_type=ComplianceAssetType.CODE_REPO,
        license_name="unknown",
    )

    report = build_compliance_report(
        report_id="demo",
        papers=[paper],
        code_repos=[code],
    )

    assert "github_repo" in report.missing_license_info
    assert report.publication_risk in {"high", "blocker"}
    assert any("figures require reuse" in finding.message for finding in report.findings)
    assert report.requires_human_review is True
