"""Small local license registry helpers."""

from __future__ import annotations

from turing_research_plus.compliance.models import LicenseStatus

OPEN_LICENSES = {
    "mit",
    "apache-2.0",
    "bsd-2-clause",
    "bsd-3-clause",
    "cc-by-4.0",
}

RESTRICTED_LICENSE_HINTS = {
    "smpl-x": LicenseStatus.RESTRICTED,
    "smplx": LicenseStatus.RESTRICTED,
    "restricted-data": LicenseStatus.RESTRICTED,
    "proprietary": LicenseStatus.PROPRIETARY,
    "research-only": LicenseStatus.RESTRICTED,
    "non-commercial": LicenseStatus.RESTRICTED,
}


def normalize_license_name(name: str | None) -> str:
    """Normalize a license label for local matching."""

    if not name or not name.strip():
        return "unknown"
    return name.strip().lower().replace(" ", "-")


def classify_license(name: str | None) -> LicenseStatus:
    """Classify a license label without fetching external license text."""

    normalized = normalize_license_name(name)
    if normalized == "unknown":
        return LicenseStatus.UNKNOWN
    if normalized in OPEN_LICENSES:
        return LicenseStatus.KNOWN
    for hint, status in RESTRICTED_LICENSE_HINTS.items():
        if hint in normalized:
            return status
    return LicenseStatus.REVIEW_REQUIRED


def license_registry_summary() -> dict[str, list[str]]:
    """Return a small summary of known local license hints."""

    return {
        "open_license_hints": sorted(OPEN_LICENSES),
        "restricted_license_hints": sorted(RESTRICTED_LICENSE_HINTS),
        "boundary": [
            "No license text is downloaded.",
            "Unknown licenses require human review.",
            "This registry is not legal advice.",
        ],
    }
