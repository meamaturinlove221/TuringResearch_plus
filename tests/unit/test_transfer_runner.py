from __future__ import annotations

from pathlib import Path

import pytest
from pydantic import ValidationError

from turing_research_plus.session_runtime.transfer_report import TransferMode, TransferStatus
from turing_research_plus.session_runtime.transfer_runner import (
    TransferRunnerRequest,
    run_transfer,
)


def _source(tmp_path: Path) -> Path:
    source = tmp_path / "source"
    source.mkdir(exist_ok=True)
    (source / "PROJECT_CONTEXT.md").write_text("project\n", encoding="utf-8")
    return source


def test_transfer_runner_defaults_to_fake_mode(tmp_path: Path) -> None:
    source = _source(tmp_path)
    report = run_transfer(
        TransferRunnerRequest(
            transfer_id="tx",
            package_id="ctx",
            source_dir=source,
            target=(tmp_path / "target").as_posix(),
        )
    )

    assert report.mode == TransferMode.FAKE
    assert report.status == TransferStatus.TRANSFERRED
    assert report.live_enabled is False


def test_transfer_runner_blocks_unsafe_remote_target(tmp_path: Path) -> None:
    report = run_transfer(
        TransferRunnerRequest(
            transfer_id="tx",
            package_id="ctx",
            source_dir=_source(tmp_path),
            target="../escape",
            mode=TransferMode.SFTP,
            live_enabled=True,
            allow_remote_write=True,
        )
    )

    assert report.status == TransferStatus.BLOCKED
    assert "unsafe remote target" in report.errors[0]


def test_transfer_runner_rejects_remote_command_and_delete_flags(tmp_path: Path) -> None:
    with pytest.raises(ValidationError):
        TransferRunnerRequest(
            transfer_id="tx",
            package_id="ctx",
            source_dir=_source(tmp_path),
            target="target",
            remote_command_execution=True,
        )
    with pytest.raises(ValidationError):
        TransferRunnerRequest(
            transfer_id="tx",
            package_id="ctx",
            source_dir=_source(tmp_path),
            target="target",
            remote_delete=True,
        )


def test_transfer_runner_sftp_skips_when_live_disabled(tmp_path: Path) -> None:
    report = run_transfer(
        TransferRunnerRequest(
            transfer_id="tx",
            package_id="ctx",
            source_dir=_source(tmp_path),
            target="/safe/context-pack",
            mode=TransferMode.SFTP,
        )
    )

    assert report.status == TransferStatus.SKIPPED_LIVE_DISABLED
    assert report.live_enabled is False
