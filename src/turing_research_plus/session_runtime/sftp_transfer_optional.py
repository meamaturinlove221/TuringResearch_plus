"""Optional SFTP transfer surface guarded by explicit live opt-in."""

from __future__ import annotations

import os
from pathlib import PurePosixPath
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from turing_research_plus.remote_readers.path_policy import path_policy_warnings
from turing_research_plus.session_runtime.transfer_report import (
    TransferMode,
    TransferReport,
    TransferStatus,
)

LIVE_TEST_ENV = "TURINGRESEARCH_ENABLE_LIVE_TESTS"
DEFAULT_CREDENTIAL_ENV = "TURINGRESEARCH_SFTP_CREDENTIAL"


class OptionalSFTPTransferRequest(BaseModel):
    """Input for optional live SFTP transfer checks."""

    model_config = ConfigDict(extra="forbid")

    transfer_id: str = Field(min_length=1)
    package_id: str = Field(min_length=1)
    source_dir: str = Field(min_length=1)
    remote_target: str = Field(min_length=1)
    live_enabled: bool = False
    credential_env: str = DEFAULT_CREDENTIAL_ENV
    allow_remote_write: bool = False

    @model_validator(mode="after")
    def enforce_explicit_remote_write(self) -> Self:
        if self.allow_remote_write and not self.live_enabled:
            raise ValueError("remote write requires live_enabled")
        return self


def live_sftp_is_enabled(
    *,
    live_enabled: bool,
    credential_env: str = DEFAULT_CREDENTIAL_ENV,
) -> tuple[bool, str | None]:
    """Return whether optional SFTP transfer may attempt live work."""

    if not live_enabled or os.getenv(LIVE_TEST_ENV) != "1":
        return False, "live tests are disabled"
    if not os.getenv(credential_env):
        return False, f"missing required credential env var: {credential_env}"
    return True, None


def validate_remote_transfer_target(remote_target: str) -> list[str]:
    """Validate explicit remote transfer target syntax without connecting."""

    warnings = path_policy_warnings(remote_target)
    normalized = remote_target.replace("\\", "/").strip()
    if ".." in PurePosixPath(normalized).parts:
        if "path-traversal" not in warnings:
            warnings.append("path-traversal")
    if normalized in {"/", ".", "~"}:
        warnings.append("remote-target-too-broad")
    return list(dict.fromkeys(warnings))


def run_optional_sftp_transfer(request: OptionalSFTPTransferRequest) -> TransferReport:
    """Return a guarded optional SFTP transfer report.

    The current implementation intentionally does not open a network
    connection. It validates opt-in, credential presence, and target path, then
    returns a review report. A project-specific live adapter must be added in a
    separately gated round before real transfer can occur.
    """

    target_warnings = validate_remote_transfer_target(request.remote_target)
    if target_warnings:
        return TransferReport(
            transfer_id=request.transfer_id,
            package_id=request.package_id,
            mode=TransferMode.SFTP,
            status=TransferStatus.BLOCKED,
            source_dir=request.source_dir,
            target=request.remote_target,
            errors=[f"unsafe remote target: {', '.join(target_warnings)}"],
            live_enabled=request.live_enabled,
            credential_env=request.credential_env,
        )

    enabled, reason = live_sftp_is_enabled(
        live_enabled=request.live_enabled,
        credential_env=request.credential_env,
    )
    if not enabled:
        status = (
            TransferStatus.SKIPPED_MISSING_CREDENTIAL
            if reason and reason.startswith("missing")
            else TransferStatus.SKIPPED_LIVE_DISABLED
        )
        return TransferReport(
            transfer_id=request.transfer_id,
            package_id=request.package_id,
            mode=TransferMode.SFTP,
            status=status,
            source_dir=request.source_dir,
            target=request.remote_target,
            errors=[reason or "live SFTP disabled"],
            live_enabled=False,
            credential_env=request.credential_env,
        )

    return TransferReport(
        transfer_id=request.transfer_id,
        package_id=request.package_id,
        mode=TransferMode.SFTP,
        status=TransferStatus.SKIPPED_LIVE_DISABLED,
        source_dir=request.source_dir,
        target=request.remote_target,
        errors=[
            "live SFTP transfer requires a separately reviewed project-specific adapter"
        ],
        live_enabled=True,
        credential_env=request.credential_env,
    )
