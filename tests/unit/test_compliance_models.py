from __future__ import annotations

import pytest

from turing_research_plus.compliance.models import (
    ComplianceAsset,
    ComplianceAssetType,
    ComplianceReport,
    ComplianceRiskLevel,
    LicenseStatus,
)


def test_compliance_report_serializes_required_fields() -> None:
    report = ComplianceReport(
        report_id="demo",
        datasets=[
            ComplianceAsset(
                asset_id="dataset",
                name="Demo dataset",
                asset_type=ComplianceAssetType.DATASET,
                license_name="MIT",
                license_status=LicenseStatus.KNOWN,
                requires_human_review=True,
            )
        ],
        redistribution_risk=ComplianceRiskLevel.LOW,
        publication_risk=ComplianceRiskLevel.LOW,
    )

    payload = report.model_dump(mode="json")

    assert payload["report_id"] == "demo"
    assert payload["datasets"][0]["asset_type"] == "dataset"
    assert payload["requires_human_review"] is True
    assert "not legal advice" in payload["disclaimer"].lower()


def test_unknown_asset_requires_human_review() -> None:
    with pytest.raises(ValueError, match="require human review"):
        ComplianceAsset(
            asset_id="unknown",
            name="Unknown",
            asset_type=ComplianceAssetType.CODE_REPO,
            license_status=LicenseStatus.UNKNOWN,
            requires_human_review=False,
        )


def test_compliance_report_cannot_claim_legal_advice() -> None:
    with pytest.raises(ValueError, match="not legal advice"):
        ComplianceReport(
            report_id="bad",
            disclaimer="This is legal advice.",
        )
