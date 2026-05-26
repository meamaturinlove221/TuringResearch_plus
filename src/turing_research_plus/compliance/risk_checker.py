"""Compliance risk checker."""

from __future__ import annotations

from turing_research_plus.compliance.models import (
    ComplianceAsset,
    ComplianceAssetType,
    ComplianceFinding,
    ComplianceReport,
    ComplianceRiskLevel,
    LicenseStatus,
)


def check_asset_risk(asset: ComplianceAsset) -> list[ComplianceFinding]:
    """Return conservative compliance findings for one asset."""

    findings: list[ComplianceFinding] = []
    if asset.license_status == LicenseStatus.UNKNOWN:
        findings.append(
            ComplianceFinding(
                asset_id=asset.asset_id,
                asset_type=asset.asset_type,
                risk_level=ComplianceRiskLevel.HIGH,
                message="License information is unknown.",
                recommended_action="Record license source before publication or redistribution.",
                release_blocker=True,
            )
        )
    if asset.license_status in {LicenseStatus.RESTRICTED, LicenseStatus.PROPRIETARY}:
        findings.append(
            ComplianceFinding(
                asset_id=asset.asset_id,
                asset_type=asset.asset_type,
                risk_level=ComplianceRiskLevel.BLOCKER,
                message="Asset has restricted or proprietary license status.",
                recommended_action="Do not bundle; require human license review.",
                release_blocker=True,
            )
        )
    if asset.license_status == LicenseStatus.REVIEW_REQUIRED:
        findings.append(
            ComplianceFinding(
                asset_id=asset.asset_id,
                asset_type=asset.asset_type,
                risk_level=ComplianceRiskLevel.MEDIUM,
                message="License status requires human review.",
                recommended_action="Confirm license terms before public reuse.",
                release_blocker=False,
            )
        )
    if asset.bundled and asset.public_release_allowed is not True:
        findings.append(
            ComplianceFinding(
                asset_id=asset.asset_id,
                asset_type=asset.asset_type,
                risk_level=ComplianceRiskLevel.BLOCKER,
                message="Asset appears bundled without public release approval.",
                recommended_action=(
                    "Remove from public package or document redistribution permission."
                ),
                release_blocker=True,
            )
        )
    if _looks_like_raw_dataset(asset):
        findings.append(
            ComplianceFinding(
                asset_id=asset.asset_id,
                asset_type=asset.asset_type,
                risk_level=ComplianceRiskLevel.BLOCKER,
                message="Raw dataset material is not public-release safe by default.",
                recommended_action="Keep raw data out of public examples and release packages.",
                release_blocker=True,
            )
        )
    if asset.asset_type == ComplianceAssetType.PAPER and _mentions_figures(asset):
        findings.append(
            ComplianceFinding(
                asset_id=asset.asset_id,
                asset_type=asset.asset_type,
                risk_level=ComplianceRiskLevel.MEDIUM,
                message="Third-party paper figures require reuse permission review.",
                recommended_action="Use citations or redraw only after confirming reuse rights.",
                release_blocker=False,
            )
        )
    return findings


def build_compliance_report(
    *,
    report_id: str,
    datasets: list[ComplianceAsset] | None = None,
    models: list[ComplianceAsset] | None = None,
    papers: list[ComplianceAsset] | None = None,
    code_repos: list[ComplianceAsset] | None = None,
) -> ComplianceReport:
    """Build a conservative compliance report."""

    dataset_items = datasets or []
    model_items = models or []
    paper_items = papers or []
    code_items = code_repos or []
    assets = [*dataset_items, *model_items, *paper_items, *code_items]
    findings = [finding for asset in assets for finding in check_asset_risk(asset)]
    missing_license_info = [
        asset.asset_id for asset in assets if asset.license_status == LicenseStatus.UNKNOWN
    ]
    usage_restrictions = sorted(
        {restriction for asset in assets for restriction in asset.usage_restrictions}
    )
    licenses = sorted({asset.license_name for asset in assets})
    redistribution_risk = _aggregate_risk(
        [finding for finding in findings if finding.release_blocker]
    )
    publication_risk = _aggregate_risk(findings)
    return ComplianceReport(
        report_id=report_id,
        datasets=dataset_items,
        models=model_items,
        papers=paper_items,
        code_repos=code_items,
        licenses=licenses,
        usage_restrictions=usage_restrictions,
        redistribution_risk=redistribution_risk,
        publication_risk=publication_risk,
        missing_license_info=missing_license_info,
        findings=findings,
    )


def _aggregate_risk(findings: list[ComplianceFinding]) -> ComplianceRiskLevel:
    if any(finding.risk_level == ComplianceRiskLevel.BLOCKER for finding in findings):
        return ComplianceRiskLevel.BLOCKER
    if any(finding.risk_level == ComplianceRiskLevel.HIGH for finding in findings):
        return ComplianceRiskLevel.HIGH
    if any(finding.risk_level == ComplianceRiskLevel.MEDIUM for finding in findings):
        return ComplianceRiskLevel.MEDIUM
    return ComplianceRiskLevel.LOW


def _looks_like_raw_dataset(asset: ComplianceAsset) -> bool:
    text = " ".join([asset.name, *asset.usage_restrictions]).lower()
    return asset.asset_type == ComplianceAssetType.DATASET and "raw" in text


def _mentions_figures(asset: ComplianceAsset) -> bool:
    text = " ".join([asset.name, *asset.usage_restrictions]).lower()
    return "figure" in text or "third-party" in text
