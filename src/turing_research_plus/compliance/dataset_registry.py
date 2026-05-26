"""Dataset registry helpers for compliance review."""

from __future__ import annotations

from turing_research_plus.compliance.license_registry import classify_license
from turing_research_plus.compliance.models import ComplianceAsset, ComplianceAssetType


def dataset_asset(
    *,
    asset_id: str,
    name: str,
    license_name: str = "unknown",
    usage_restrictions: list[str] | None = None,
    source: str | None = None,
    bundled: bool = False,
    public_release_allowed: bool | None = None,
) -> ComplianceAsset:
    """Create a dataset asset with conservative defaults."""

    return ComplianceAsset(
        asset_id=asset_id,
        name=name,
        asset_type=ComplianceAssetType.DATASET,
        license_name=license_name,
        license_status=classify_license(license_name),
        usage_restrictions=usage_restrictions or [],
        source=source,
        bundled=bundled,
        public_release_allowed=public_release_allowed,
    )


def vggt_raw_dataset_placeholder() -> ComplianceAsset:
    """Return the VGGT raw dataset placeholder for fake compliance checks."""

    return dataset_asset(
        asset_id="vggt_raw_dataset",
        name="VGGT private/raw experiment data",
        license_name="restricted-data",
        usage_restrictions=[
            "raw dataset is not public-demo safe",
            "do not bundle in public release",
            "requires project owner review",
        ],
        source="local research workflow placeholder",
        bundled=False,
        public_release_allowed=False,
    )
