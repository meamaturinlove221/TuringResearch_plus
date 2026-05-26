"""Platform compatibility notes for context archive handoff."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class PlatformCompatibilityReport(BaseModel):
    """Read-only compatibility guidance for archive handoff."""

    model_config = ConfigDict(extra="forbid")

    source_platform: str = Field(min_length=1)
    target_platform: str = Field(min_length=1)
    archive_format: str = "tar"
    normalized_separator: str = "/"
    requires_pre_unpack_validation: bool = True
    notes: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)

    @property
    def release_blocker(self) -> bool:
        """Return whether compatibility is unsafe."""

        return not self.requires_pre_unpack_validation


def build_platform_compatibility_report(
    *,
    source_platform: str,
    target_platform: str,
    archive_format: str = "tar",
) -> PlatformCompatibilityReport:
    """Build compatibility guidance for a context archive transfer."""

    source = source_platform.lower()
    target = target_platform.lower()
    notes = [
        "Use relative archive entries only.",
        "Normalize archive entries to forward slashes before validation.",
        "Validate paths before unpacking, regardless of platform.",
    ]
    warnings: list[str] = []
    if "windows" in source and ("linux" in target or "pod" in target):
        warnings.append("windows-to-linux-unpack-requires-path-validation")
        notes.append("Do not preserve drive letters or backslash-only paths in the archive.")
    if archive_format not in {"tar", "zip"}:
        warnings.append("unreviewed-archive-format")

    return PlatformCompatibilityReport(
        source_platform=source_platform,
        target_platform=target_platform,
        archive_format=archive_format,
        notes=notes,
        warnings=warnings,
    )
