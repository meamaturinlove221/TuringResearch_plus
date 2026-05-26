from __future__ import annotations

from turing_research_plus.compliance.license_registry import (
    classify_license,
    license_registry_summary,
    normalize_license_name,
)
from turing_research_plus.compliance.models import LicenseStatus


def test_license_registry_classifies_open_and_unknown_licenses() -> None:
    assert normalize_license_name("Apache 2.0") == "apache-2.0"
    assert classify_license("MIT") == LicenseStatus.KNOWN
    assert classify_license("") == LicenseStatus.UNKNOWN


def test_license_registry_flags_restricted_hints() -> None:
    assert classify_license("SMPL-X restricted model license") == LicenseStatus.RESTRICTED
    assert classify_license("non-commercial research-only") == LicenseStatus.RESTRICTED
    assert classify_license("custom-lab-license") == LicenseStatus.REVIEW_REQUIRED


def test_license_registry_summary_is_local_only() -> None:
    summary = license_registry_summary()

    assert "No license text is downloaded." in summary["boundary"]
    assert "smpl-x" in summary["restricted_license_hints"]
