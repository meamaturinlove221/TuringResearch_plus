"""Safe unpack validation for context and return archive members."""

from __future__ import annotations

from pathlib import Path
from typing import Literal, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from turing_research_plus.pod_lifecycle.transfer_policy import transfer_warnings_for_path
from turing_research_plus.session_runtime.archive_platform import (
    NO_SAME_OWNER_NOTE,
    SYMLINK_POLICY_NOTE,
)
from turing_research_plus.session_runtime.archive_writer import sha256_file
from turing_research_plus.session_runtime.dotfile_policy import evaluate_dotfile_policy
from turing_research_plus.session_runtime.path_normalization import (
    normalize_archive_member_path,
)
from turing_research_plus.session_runtime.return_manifest import (
    REQUIRED_RETURN_FILES,
    load_sha256sums,
)

ArchiveMemberType = Literal["file", "directory", "symlink"]


class ArchiveMember(BaseModel):
    """One archive member candidate for safe unpack review."""

    model_config = ConfigDict(extra="forbid")

    path: str = Field(min_length=1)
    member_type: ArchiveMemberType = "file"
    size_bytes: int = 0
    link_target: str | None = None
    expected_sha256: str | None = Field(default=None, min_length=64, max_length=64)
    actual_sha256: str | None = Field(default=None, min_length=64, max_length=64)

    @model_validator(mode="after")
    def validate_symlink_target(self) -> Self:
        if self.member_type == "symlink" and not self.link_target:
            raise ValueError("symlink archive members require link_target")
        return self


class UnpackSafetyFinding(BaseModel):
    """One safe-unpack finding."""

    model_config = ConfigDict(extra="forbid")

    finding_id: str = Field(min_length=1)
    path: str = Field(min_length=1)
    message: str = Field(min_length=1)
    release_blocker: bool = True


class UnpackSafetyReport(BaseModel):
    """Report for archive member validation before unpack or ingest review."""

    model_config = ConfigDict(extra="forbid")

    members: list[ArchiveMember] = Field(default_factory=list)
    findings: list[UnpackSafetyFinding] = Field(default_factory=list)
    no_same_owner_note: str = NO_SAME_OWNER_NOTE
    symlink_policy: str = SYMLINK_POLICY_NOTE
    checksum_policy: str = "checksum validation must pass before ingest review"
    return_archive_validation: bool = False
    remote_execution_allowed: bool = False
    requires_human_review: bool = True

    @property
    def release_blocker(self) -> bool:
        """Return whether any finding blocks safe unpack or ingest review."""

        return any(finding.release_blocker for finding in self.findings)

    @property
    def safe_paths(self) -> list[str]:
        """Return normalized safe file paths."""

        blocked = {finding.path for finding in self.findings if finding.release_blocker}
        paths: list[str] = []
        for member in self.members:
            normalized = normalize_archive_member_path(member.path).normalized_path
            if normalized not in blocked and member.member_type == "file":
                paths.append(normalized)
        return paths


def validate_archive_members(
    members: list[ArchiveMember],
    *,
    require_checksums: bool = False,
    allow_symlinks: bool = False,
    return_archive_validation: bool = False,
) -> UnpackSafetyReport:
    """Validate archive members before unpacking or ingest review."""

    findings: list[UnpackSafetyFinding] = []
    normalized_members: list[ArchiveMember] = []
    seen_paths: set[str] = set()

    for member in members:
        path_report = normalize_archive_member_path(member.path)
        normalized_path = path_report.normalized_path
        normalized_members.append(member.model_copy(update={"path": normalized_path}))

        for reason in path_report.blocked_reasons:
            findings.append(
                UnpackSafetyFinding(
                    finding_id=reason,
                    path=normalized_path,
                    message=f"archive member path is unsafe: {reason}",
                )
            )

        if normalized_path in seen_paths:
            findings.append(
                UnpackSafetyFinding(
                    finding_id="duplicate-archive-member",
                    path=normalized_path,
                    message="archive member path appears more than once",
                )
            )
        seen_paths.add(normalized_path)

        dotfile = evaluate_dotfile_policy(normalized_path)
        for reason in dotfile.reasons:
            findings.append(
                UnpackSafetyFinding(
                    finding_id=reason,
                    path=normalized_path,
                    message=f"archive member violates dotfile policy: {reason}",
                )
            )

        for warning in transfer_warnings_for_path(
            normalized_path,
            file_size=member.size_bytes,
        ):
            findings.append(
                UnpackSafetyFinding(
                    finding_id=warning,
                    path=normalized_path,
                    message=f"archive member violates transfer safety: {warning}",
                )
            )

        if member.member_type == "symlink":
            if not allow_symlinks:
                findings.append(
                    UnpackSafetyFinding(
                        finding_id="symlink-blocked",
                        path=normalized_path,
                        message="symlink members are blocked by default",
                    )
                )
            if member.link_target:
                target_report = normalize_archive_member_path(member.link_target)
                for reason in target_report.blocked_reasons:
                    findings.append(
                        UnpackSafetyFinding(
                            finding_id="unsafe-symlink-target",
                            path=normalized_path,
                            message=f"symlink target is unsafe: {reason}",
                        )
                    )

        if (
            require_checksums
            and member.member_type == "file"
            and normalized_path != "SHA256SUMS.txt"
        ):
            if not member.expected_sha256 or not member.actual_sha256:
                findings.append(
                    UnpackSafetyFinding(
                        finding_id="missing-checksum",
                        path=normalized_path,
                        message="archive member requires expected and actual checksum",
                    )
                )
            elif member.expected_sha256 != member.actual_sha256:
                findings.append(
                    UnpackSafetyFinding(
                        finding_id="checksum-mismatch",
                        path=normalized_path,
                        message="archive member checksum mismatch",
                    )
                )

    if return_archive_validation:
        present = {member.path for member in normalized_members}
        for required_path in REQUIRED_RETURN_FILES:
            if required_path not in present:
                findings.append(
                    UnpackSafetyFinding(
                        finding_id="missing-return-file",
                        path=required_path,
                        message=f"return archive is missing required file: {required_path}",
                    )
                )

    return UnpackSafetyReport(
        members=normalized_members,
        findings=list(_dedupe_findings(findings)),
        return_archive_validation=return_archive_validation,
    )


def archive_members_from_directory(root: Path) -> list[ArchiveMember]:
    """Build archive member records from a local directory without unpacking."""

    if not root.exists():
        return []
    members: list[ArchiveMember] = []
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        if path.is_symlink():
            members.append(
                ArchiveMember(
                    path=relative,
                    member_type="symlink",
                    link_target=str(path.readlink()),
                )
            )
        elif path.is_dir():
            members.append(ArchiveMember(path=relative, member_type="directory"))
        elif path.is_file():
            members.append(
                ArchiveMember(
                    path=relative,
                    member_type="file",
                    size_bytes=path.stat().st_size,
                )
            )
    return members


def validate_return_archive_directory(return_dir: Path) -> UnpackSafetyReport:
    """Validate a structured return archive directory before ingest review."""

    checksums = load_sha256sums(return_dir / "SHA256SUMS.txt")
    members: list[ArchiveMember] = []
    for member in archive_members_from_directory(return_dir):
        if member.member_type == "file":
            file_path = return_dir / member.path
            member = member.model_copy(
                update={
                    "expected_sha256": checksums.get(member.path),
                    "actual_sha256": sha256_file(file_path),
                }
            )
        members.append(member)
    return validate_archive_members(
        members,
        require_checksums=True,
        allow_symlinks=False,
        return_archive_validation=True,
    )


def _dedupe_findings(
    findings: list[UnpackSafetyFinding],
) -> list[UnpackSafetyFinding]:
    seen: set[tuple[str, str, str]] = set()
    deduped: list[UnpackSafetyFinding] = []
    for finding in findings:
        key = (finding.finding_id, finding.path, finding.message)
        if key in seen:
            continue
        seen.add(key)
        deduped.append(finding)
    return deduped
