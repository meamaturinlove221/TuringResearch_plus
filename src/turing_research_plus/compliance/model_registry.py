"""Model registry helpers for compliance review."""

from __future__ import annotations

from turing_research_plus.compliance.license_registry import classify_license
from turing_research_plus.compliance.models import ComplianceAsset, ComplianceAssetType


def model_asset(
    *,
    asset_id: str,
    name: str,
    license_name: str = "unknown",
    usage_restrictions: list[str] | None = None,
    source: str | None = None,
    bundled: bool = False,
    public_release_allowed: bool | None = None,
) -> ComplianceAsset:
    """Create a model asset with conservative defaults."""

    return ComplianceAsset(
        asset_id=asset_id,
        name=name,
        asset_type=ComplianceAssetType.MODEL,
        license_name=license_name,
        license_status=classify_license(license_name),
        usage_restrictions=usage_restrictions or [],
        source=source,
        bundled=bundled,
        public_release_allowed=public_release_allowed,
    )


def smplx_model_placeholder() -> ComplianceAsset:
    """Return the SMPL-X model placeholder for fake compliance checks."""

    return model_asset(
        asset_id="smplx_body_model_files",
        name="SMPL-X body model files",
        license_name="SMPL-X restricted model license",
        usage_restrictions=[
            "license restricted",
            "not bundled",
            "requires user-provided licensed copy",
        ],
        source="third-party licensed model placeholder",
        bundled=False,
        public_release_allowed=False,
    )
