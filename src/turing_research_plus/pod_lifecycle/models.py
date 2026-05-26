"""Models for pod context lifecycle safety planning."""

from __future__ import annotations

from enum import StrEnum
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class PodLifecycleStatus(StrEnum):
    """Review status for lifecycle safety reports."""

    PASS = "pass"
    PASS_WITH_WARNINGS = "pass-with-warnings"
    BLOCKED = "blocked"


class PodLifecycleFindingSeverity(StrEnum):
    """Finding severity levels."""

    INFO = "info"
    WARNING = "warning"
    BLOCKER = "blocker"


class PodPreflightCheck(BaseModel):
    """One preflight check result."""

    model_config = ConfigDict(extra="forbid")

    check_id: str = Field(min_length=1)
    status: PodLifecycleStatus
    message: str = Field(min_length=1)
    release_blocker: bool = False


class PodMemoryPolicy(BaseModel):
    """Review-only memory policy for a pod context package."""

    model_config = ConfigDict(extra="forbid")

    durable_context_files: list[str] = Field(
        default_factory=lambda: ["PROJECT_CONTEXT.md", "MEMORY.md", "ROUTE_SPEC.yaml"]
    )
    source_of_truth: str = (
        "Evidence Ledger, Artifact Audit, Run Ingest, Handoff Manifest, and Route Spec"
    )
    bidirectional_memory_sync: bool = False
    proposed_updates_only: bool = True
    review_required: bool = True

    @model_validator(mode="after")
    def enforce_review_only_memory(self) -> Self:
        if self.bidirectional_memory_sync:
            raise ValueError("pod memory lifecycle cannot enable bidirectional sync")
        if not self.proposed_updates_only:
            raise ValueError("pod memory lifecycle must emit proposed updates only")
        if not self.review_required:
            raise ValueError("pod memory lifecycle requires human review")
        if self.source_of_truth.strip().lower() == "memory.md":
            raise ValueError("MEMORY.md cannot be the only source of truth")
        return self


class PodTransferPolicy(BaseModel):
    """Transfer policy for durable pod context packages."""

    model_config = ConfigDict(extra="forbid")

    transport: str = "git_context_package"
    remote_execution_allowed: bool = False
    ssh_provision_allowed: bool = False
    modal_execution_allowed: bool = False
    git_push_allowed: bool = False
    shell_execution_allowed: bool = False
    dotfile_policy: str = "forbidden dotfiles blocked; generated package files only"
    archive_path_policy: str = "relative paths only; no traversal or absolute paths"
    compatibility_notes: list[str] = Field(
        default_factory=lambda: [
            "Windows archive creation and Linux unpack must preserve relative paths.",
            "Archive entries must be validated before unpack.",
        ]
    )

    @model_validator(mode="after")
    def enforce_no_execution_transport(self) -> Self:
        blocked = {
            "remote_execution_allowed": self.remote_execution_allowed,
            "ssh_provision_allowed": self.ssh_provision_allowed,
            "modal_execution_allowed": self.modal_execution_allowed,
            "git_push_allowed": self.git_push_allowed,
            "shell_execution_allowed": self.shell_execution_allowed,
        }
        enabled = [name for name, value in blocked.items() if value]
        if enabled:
            raise ValueError(f"pod transfer policy cannot enable: {', '.join(enabled)}")
        return self


class PodReturnVerification(BaseModel):
    """Required return artifacts and metadata checks."""

    model_config = ConfigDict(extra="forbid")

    required_files: list[str] = Field(
        default_factory=lambda: [
            "RETURN_MANIFEST.yaml",
            "RUN_STATUS.json",
            "FINAL_STATUS.json",
            "ARTIFACT_INDEX.md",
            "FAILURE_REPORT.md",
            "PROPOSED_EVIDENCE_UPDATES.json",
            "ADVISOR_SUMMARY_DRAFT.md",
            "SHA256SUMS.txt",
        ]
    )
    required_metadata_fields: list[str] = Field(
        default_factory=lambda: [
            "context_package_id",
            "route_id",
            "target_environment_label",
            "return_package_id",
            "sha256_manifest",
        ]
    )
    auto_apply_evidence_updates: bool = False
    validate_return_metadata: bool = True
    requires_human_review: bool = True

    @model_validator(mode="after")
    def enforce_return_review(self) -> Self:
        if self.auto_apply_evidence_updates:
            raise ValueError("pod return cannot auto-apply evidence updates")
        if not self.validate_return_metadata:
            raise ValueError("pod return metadata validation is required")
        if not self.requires_human_review:
            raise ValueError("pod return verification requires human review")
        return self


class PodConflictPolicy(BaseModel):
    """Policy for resolving returned context and memory changes."""

    model_config = ConfigDict(extra="forbid")

    no_bidirectional_memory_sync: bool = True
    reviewer_resolves_conflicts: bool = True
    proposed_updates_only: bool = True
    evidence_ledger_auto_write: bool = False
    conflict_resolution_surface: str = "proposed updates plus human review"

    @model_validator(mode="after")
    def enforce_conflict_review(self) -> Self:
        if not self.no_bidirectional_memory_sync:
            raise ValueError("pod lifecycle cannot enable bidirectional memory sync")
        if not self.reviewer_resolves_conflicts:
            raise ValueError("pod lifecycle conflicts require reviewer resolution")
        if not self.proposed_updates_only:
            raise ValueError("pod lifecycle must keep updates proposed-only")
        if self.evidence_ledger_auto_write:
            raise ValueError("pod lifecycle cannot auto-write the Evidence Ledger")
        return self


class PodContextLifecycle(BaseModel):
    """Review-only lifecycle model for a pod context package."""

    model_config = ConfigDict(extra="forbid")

    context_package_id: str = Field(min_length=1)
    source_machine_label: str = Field(min_length=1)
    target_environment_label: str = Field(min_length=1)
    route_id: str = Field(min_length=1)
    memory_policy: PodMemoryPolicy = Field(default_factory=PodMemoryPolicy)
    transfer_policy: PodTransferPolicy = Field(default_factory=PodTransferPolicy)
    preflight_checks: list[PodPreflightCheck] = Field(default_factory=list)
    forbidden_files: list[str] = Field(
        default_factory=lambda: [
            ".env",
            ".git",
            ".ssh",
            ".codex",
            "local_project_links.yaml",
            "private_data",
            "raw_data",
            "raw_dataset",
            "secrets",
            "SMPL" + "X_*.npz",
            "SMPL" + "X_*.pkl",
            "predictions.npz",
        ]
    )
    structured_output_requirements: list[str] = Field(
        default_factory=lambda: PodReturnVerification().required_files
    )
    return_verification: PodReturnVerification = Field(default_factory=PodReturnVerification)
    conflict_policy: PodConflictPolicy = Field(default_factory=PodConflictPolicy)
    requires_human_review: bool = True

    @model_validator(mode="after")
    def enforce_review_only_lifecycle(self) -> Self:
        if not self.requires_human_review:
            raise ValueError("pod context lifecycle requires human review")
        return self


class PodLifecycleFinding(BaseModel):
    """One safety or verification finding."""

    model_config = ConfigDict(extra="forbid")

    finding_id: str = Field(min_length=1)
    severity: PodLifecycleFindingSeverity
    message: str = Field(min_length=1)
    path: str | None = None
    release_blocker: bool = False


class PodLifecycleSafetyReport(BaseModel):
    """Safety report for pod context lifecycle checks."""

    model_config = ConfigDict(extra="forbid")

    context_package_id: str = Field(min_length=1)
    route_id: str = Field(min_length=1)
    status: PodLifecycleStatus
    findings: list[PodLifecycleFinding] = Field(default_factory=list)
    checked_paths: list[str] = Field(default_factory=list)
    missing_return_files: list[str] = Field(default_factory=list)
    missing_metadata_fields: list[str] = Field(default_factory=list)
    proposed_updates_only: bool = True
    requires_human_review: bool = True

    @property
    def release_blocker(self) -> bool:
        """Return whether any finding blocks release."""

        return any(finding.release_blocker for finding in self.findings)

    def to_markdown(self) -> str:
        """Render the report to Markdown."""

        lines = [
            f"# Pod Lifecycle Safety Report: {self.context_package_id}",
            "",
            f"- Route: `{self.route_id}`",
            f"- Status: `{self.status}`",
            f"- Release blocker: `{str(self.release_blocker).lower()}`",
            f"- Proposed updates only: `{str(self.proposed_updates_only).lower()}`",
            f"- Requires human review: `{str(self.requires_human_review).lower()}`",
            "",
            "## Findings",
            "",
        ]
        lines.extend(
            [
                f"- `{finding.severity}` `{finding.finding_id}`: {finding.message}"
                + (f" (`{finding.path}`)" if finding.path else "")
                for finding in self.findings
            ]
            or ["- None."]
        )
        lines.extend(["", "## Missing Return Files", ""])
        lines.extend([f"- `{item}`" for item in self.missing_return_files] or ["- None."])
        lines.extend(["", "## Missing Metadata Fields", ""])
        lines.extend([f"- `{item}`" for item in self.missing_metadata_fields] or ["- None."])
        return "\n".join(lines) + "\n"
