"""Fake-first transfer runner for session runtime context packs."""

from __future__ import annotations

from pathlib import Path
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from turing_research_plus.session_runtime.fake_transfer import run_fake_transfer
from turing_research_plus.session_runtime.sftp_transfer_optional import (
    OptionalSFTPTransferRequest,
    run_optional_sftp_transfer,
    validate_remote_transfer_target,
)
from turing_research_plus.session_runtime.transfer_report import (
    TransferMode,
    TransferReport,
    TransferStatus,
)


class TransferRunnerRequest(BaseModel):
    """Request for fake-first context pack transfer."""

    model_config = ConfigDict(extra="forbid")

    transfer_id: str = Field(min_length=1)
    package_id: str = Field(min_length=1)
    source_dir: Path
    target: str = Field(min_length=1)
    mode: TransferMode = TransferMode.FAKE
    live_enabled: bool = False
    credential_env: str = "TURINGRESEARCH_SFTP_CREDENTIAL"
    allow_remote_write: bool = False
    remote_command_execution: bool = False
    remote_delete: bool = False
    requires_human_review: bool = True

    @model_validator(mode="after")
    def enforce_fake_first_boundary(self) -> Self:
        if self.remote_command_execution:
            raise ValueError("transfer runner cannot execute remote commands")
        if self.remote_delete:
            raise ValueError("transfer runner cannot delete remote files")
        if not self.requires_human_review:
            raise ValueError("transfer runner requires human review")
        if self.mode == TransferMode.FAKE and self.live_enabled:
            raise ValueError("fake transfer cannot enable live mode")
        if self.mode == TransferMode.SFTP and self.allow_remote_write and not self.live_enabled:
            raise ValueError("SFTP remote write requires explicit live mode")
        return self


def run_transfer(request: TransferRunnerRequest) -> TransferReport:
    """Run fake transfer by default or return guarded optional SFTP status."""

    if request.mode == TransferMode.FAKE:
        target_dir = Path(request.target)
        try:
            target_dir.relative_to(request.source_dir)
            return TransferReport(
                transfer_id=request.transfer_id,
                package_id=request.package_id,
                mode=TransferMode.FAKE,
                status=TransferStatus.BLOCKED,
                source_dir=request.source_dir.as_posix(),
                target=target_dir.as_posix(),
                errors=["fake transfer target must not be inside source directory"],
            )
        except ValueError:
            return run_fake_transfer(
                transfer_id=request.transfer_id,
                package_id=request.package_id,
                source_dir=request.source_dir,
                target_dir=target_dir,
            )

    warnings = validate_remote_transfer_target(request.target)
    if warnings:
        return TransferReport(
            transfer_id=request.transfer_id,
            package_id=request.package_id,
            mode=TransferMode.SFTP,
            status=TransferStatus.BLOCKED,
            source_dir=request.source_dir.as_posix(),
            target=request.target,
            errors=[f"unsafe remote target: {', '.join(warnings)}"],
            live_enabled=request.live_enabled,
            credential_env=request.credential_env,
        )

    return run_optional_sftp_transfer(
        OptionalSFTPTransferRequest(
            transfer_id=request.transfer_id,
            package_id=request.package_id,
            source_dir=request.source_dir.as_posix(),
            remote_target=request.target,
            live_enabled=request.live_enabled,
            credential_env=request.credential_env,
            allow_remote_write=request.allow_remote_write,
        )
    )
