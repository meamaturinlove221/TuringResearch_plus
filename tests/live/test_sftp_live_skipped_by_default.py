from __future__ import annotations

from pathlib import Path

import pytest

from turing_research_plus.session_runtime.sftp_transfer_optional import (
    DEFAULT_CREDENTIAL_ENV,
    LIVE_TEST_ENV,
    OptionalSFTPTransferRequest,
    run_optional_sftp_transfer,
)
from turing_research_plus.session_runtime.transfer_report import TransferStatus


@pytest.mark.live
def test_sftp_live_is_skipped_by_default(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv(LIVE_TEST_ENV, raising=False)
    monkeypatch.delenv(DEFAULT_CREDENTIAL_ENV, raising=False)
    monkeypatch.delenv("TURINGRESEARCH_ENABLE_SFTP_LIVE", raising=False)

    source = tmp_path / "context-pack"
    source.mkdir()

    report = run_optional_sftp_transfer(
        OptionalSFTPTransferRequest(
            transfer_id="sftp-live-skip",
            package_id="ctx-live-skip",
            source_dir=str(source),
            remote_target="/explicit/reviewed/target",
            live_enabled=True,
            allow_remote_write=True,
        )
    )

    assert report.status == TransferStatus.SKIPPED_LIVE_DISABLED
    assert report.remote_command_execution is False
    assert report.remote_delete is False
    assert report.target == "/explicit/reviewed/target"
