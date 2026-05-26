from __future__ import annotations

from turing_research_plus.compliance.model_registry import model_asset, smplx_model_placeholder
from turing_research_plus.compliance.models import ComplianceAssetType, LicenseStatus


def test_model_asset_classifies_license() -> None:
    asset = model_asset(
        asset_id="model",
        name="Open model",
        license_name="Apache-2.0",
    )

    assert asset.asset_type == ComplianceAssetType.MODEL
    assert asset.license_status == LicenseStatus.KNOWN


def test_smplx_model_placeholder_is_restricted_and_not_bundled() -> None:
    asset = smplx_model_placeholder()

    assert asset.asset_id == "smplx_body_model_files"
    assert asset.license_status == LicenseStatus.RESTRICTED
    assert asset.bundled is False
    assert asset.public_release_allowed is False
    assert "not bundled" in asset.usage_restrictions
