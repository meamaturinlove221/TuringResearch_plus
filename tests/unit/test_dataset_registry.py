from __future__ import annotations

from turing_research_plus.compliance.dataset_registry import (
    dataset_asset,
    vggt_raw_dataset_placeholder,
)
from turing_research_plus.compliance.models import ComplianceAssetType, LicenseStatus


def test_dataset_asset_uses_conservative_defaults() -> None:
    asset = dataset_asset(asset_id="demo", name="Demo data")

    assert asset.asset_type == ComplianceAssetType.DATASET
    assert asset.license_status == LicenseStatus.UNKNOWN
    assert asset.bundled is False
    assert asset.requires_human_review is True


def test_vggt_raw_dataset_placeholder_is_not_public_safe() -> None:
    asset = vggt_raw_dataset_placeholder()

    assert asset.asset_id == "vggt_raw_dataset"
    assert asset.license_status == LicenseStatus.RESTRICTED
    assert asset.public_release_allowed is False
    assert any("do not bundle" in item for item in asset.usage_restrictions)
