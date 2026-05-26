"""Artifact audit models for local VGGT dogfooding evidence."""

from __future__ import annotations

from enum import StrEnum
from pathlib import Path
from typing import Any, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ArtifactFileType(StrEnum):
    """File categories recognized by the minimal artifact auditor."""

    ZIP = "zip"
    JSON = "json"
    CSV = "csv"
    PNG = "png"
    JPG = "jpg"
    NPZ = "npz"
    MD = "md"
    UNKNOWN = "unknown"


class ArtifactSafetyFlag(StrEnum):
    """Safety flags that prevent unsafe local artifact handling."""

    LOCAL_ONLY = "local-only"
    EXTERNAL_PATH_REFERENCE = "external-path-reference"
    PRIVATE_PATH_NOT_READ = "private-path-not-read"
    HASH_SKIPPED = "hash-skipped"
    NPZ_SUMMARY_PLACEHOLDER = "npz-summary-placeholder"


class NPZArraySummary(BaseModel):
    """Small metadata summary for one array inside an NPZ file."""

    model_config = ConfigDict(extra="forbid")

    key: str = Field(min_length=1)
    shape: list[int] = Field(default_factory=list)
    dtype: str = ""
    file_size: int = Field(ge=0)
    summary_status: str = Field(min_length=1)


class ArtifactRecord(BaseModel):
    """One audited artifact record."""

    model_config = ConfigDict(extra="forbid")

    path: str = Field(min_length=1)
    file_type: ArtifactFileType = ArtifactFileType.UNKNOWN
    file_size: int | None = Field(default=None, ge=0)
    sha256: str | None = None
    included: bool = True
    omitted_reason: str | None = None
    safety_flags: list[ArtifactSafetyFlag] = Field(default_factory=list)
    npz_summary: list[NPZArraySummary] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def require_omitted_reason(self) -> Self:
        if not self.included and not self.omitted_reason:
            raise ValueError("omitted artifact requires omitted_reason")
        return self


class ArtifactBundleManifest(BaseModel):
    """Manifest-like collection of artifact records."""

    model_config = ConfigDict(extra="forbid")

    manifest_id: str = Field(min_length=1)
    source: str = Field(min_length=1)
    records: list[ArtifactRecord] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class ArtifactAuditInput(BaseModel):
    """Input for local artifact auditing."""

    model_config = ConfigDict(extra="forbid")

    source_path: Path
    base_dir: Path | None = None
    compute_sha256: bool = False
    summarize_npz: bool = True


class ArtifactAuditReport(BaseModel):
    """Output from the minimal artifact auditor."""

    model_config = ConfigDict(extra="forbid")

    report_id: str = Field(min_length=1)
    source_path: str = Field(min_length=1)
    records: list[ArtifactRecord] = Field(default_factory=list)
    included_count: int = Field(ge=0)
    omitted_count: int = Field(ge=0)
    warnings: list[str] = Field(default_factory=list)
    safety_flags: list[ArtifactSafetyFlag] = Field(default_factory=list)

    @model_validator(mode="after")
    def counts_match_records(self) -> Self:
        included = sum(1 for record in self.records if record.included)
        omitted = sum(1 for record in self.records if not record.included)
        if included != self.included_count or omitted != self.omitted_count:
            raise ValueError("ArtifactAuditReport counts must match records")
        return self

    def to_markdown(self) -> str:
        """Serialize the audit report as Markdown."""

        lines = [
            f"# TuringResearch Plus Artifact Audit: {self.report_id}",
            "",
            "| Path | Type | Included | Size | Safety flags | Omitted reason |",
            "| --- | --- | --- | ---: | --- | --- |",
        ]
        for record in self.records:
            lines.append(
                "| "
                + " | ".join(
                    [
                        record.path.replace("|", "/"),
                        record.file_type.value,
                        str(record.included).lower(),
                        "" if record.file_size is None else str(record.file_size),
                        ", ".join(flag.value for flag in record.safety_flags),
                        record.omitted_reason or "",
                    ]
                )
                + " |"
            )
        if self.warnings:
            lines.extend(["", "## Warnings"])
            lines.extend(f"- {warning}" for warning in self.warnings)
        return "\n".join(lines) + "\n"
