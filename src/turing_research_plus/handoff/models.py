"""Models for controlled handoff bundles."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from pathlib import Path
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class HandoffBundleType(StrEnum):
    """Supported handoff bundle types."""

    VGGT_DOGFOOD = "vggt_dogfood"
    RUN_REVIEW = "run_review"
    ADVISOR_REVIEW = "advisor_review"
    MANUAL = "manual"


class HandoffStatusLabel(StrEnum):
    """Allowed status labels mirrored from the evidence ledger."""

    OBSERVED = "observed"
    PLANNED = "planned"
    FAKE_DATA = "fake-data"
    FAILED = "failed"
    HARD_BLOCKED = "hard-blocked"
    REQUIRES_REAL_PAPER = "requires-real-paper"
    REQUIRES_REAL_EXPERIMENT = "requires-real-experiment"
    REQUIRES_HUMAN_REVIEW = "requires-human-review"
    LOCAL_OBSERVED = "local-observed"
    NOT_ENOUGH_EVIDENCE = "not-enough-evidence"


class HandoffFileRecord(BaseModel):
    """One file in or omitted from a handoff bundle."""

    model_config = ConfigDict(extra="forbid")

    relative_path: str = Field(min_length=1)
    included: bool = True
    sha256: str | None = None
    file_size: int | None = Field(default=None, ge=0)
    omitted_reason: str | None = None
    safety_warnings: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def omitted_files_need_reason(self) -> Self:
        if not self.included and not self.omitted_reason:
            raise ValueError("omitted handoff file requires omitted_reason")
        return self


class HandoffBundleManifest(BaseModel):
    """Manifest for a controlled handoff bundle."""

    model_config = ConfigDict(extra="forbid")

    bundle_id: str = Field(min_length=1)
    project_name: str = "TuringResearch Plus"
    source_machine_label: str = Field(min_length=1)
    export_time: datetime = Field(default_factory=lambda: datetime.now(UTC))
    bundle_type: HandoffBundleType
    included_files: list[HandoffFileRecord] = Field(default_factory=list)
    omitted_files: list[HandoffFileRecord] = Field(default_factory=list)
    sha256: str | None = None
    evidence_tags: list[str] = Field(default_factory=list)
    status_labels: list[HandoffStatusLabel] = Field(default_factory=list)
    safety_warnings: list[str] = Field(default_factory=list)
    manual_review_required: bool = True

    @model_validator(mode="after")
    def manual_review_required_for_handoff(self) -> Self:
        if not self.manual_review_required:
            raise ValueError("handoff bundles require manual review")
        return self


class HandoffExportRequest(BaseModel):
    """Input for local handoff export."""

    model_config = ConfigDict(extra="forbid")

    bundle_id: str = Field(min_length=1)
    source_root: Path
    output_dir: Path
    file_paths: list[Path] = Field(default_factory=list)
    source_machine_label: str = "unknown-machine"
    bundle_type: HandoffBundleType = HandoffBundleType.VGGT_DOGFOOD
    evidence_tags: list[str] = Field(default_factory=list)
    status_labels: list[HandoffStatusLabel] = Field(default_factory=list)
    max_file_size_bytes: int = Field(default=2_000_000, ge=1)


class HandoffImportRequest(BaseModel):
    """Input for handoff import validation."""

    model_config = ConfigDict(extra="forbid")

    bundle_dir: Path
    verify_sha256: bool = True


class HandoffBundleImportReport(BaseModel):
    """Import validation report; does not overwrite local ledgers."""

    model_config = ConfigDict(extra="forbid")

    bundle_id: str = Field(min_length=1)
    valid_manifest: bool
    verified_files: list[str] = Field(default_factory=list)
    missing_files: list[str] = Field(default_factory=list)
    unsafe_files: list[str] = Field(default_factory=list)
    sha256_mismatches: list[str] = Field(default_factory=list)
    proposed_updates: list[dict[str, object]] = Field(default_factory=list)
    safety_warnings: list[str] = Field(default_factory=list)
    manual_review_required: bool = True

    @property
    def is_usable_for_review(self) -> bool:
        """Return whether the bundle can be reviewed after validation."""

        return (
            self.valid_manifest
            and not self.missing_files
            and not self.unsafe_files
            and not self.sha256_mismatches
        )

    def to_markdown(self) -> str:
        """Render import report Markdown."""

        lines = [
            f"# Handoff Import Report: {self.bundle_id}",
            "",
            f"- Valid manifest: `{str(self.valid_manifest).lower()}`",
            f"- Manual review required: `{str(self.manual_review_required).lower()}`",
            "",
            "## Missing Files",
            "",
            *[f"- {item}" for item in self.missing_files],
            "",
            "## Unsafe Files",
            "",
            *[f"- {item}" for item in self.unsafe_files],
            "",
            "## SHA256 Mismatches",
            "",
            *[f"- {item}" for item in self.sha256_mismatches],
            "",
            "## Proposed Updates",
            "",
            *[f"- {item}" for item in self.proposed_updates],
        ]
        return "\n".join(lines) + "\n"
