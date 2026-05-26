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
def test_sftp_live_smoke_skipped_by_default(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv(LIVE_TEST_ENV, raising=False)
    monkeypatch.delenv(DEFAULT_CREDENTIAL_ENV, raising=False)
    monkeypatch.delenv("TURINGRESEARCH_ENABLE_SFTP_LIVE", raising=False)
    monkeypatch.delenv("TURINGRESEARCH_SFTP_KEY_PATH", raising=False)

    source = tmp_path / "context-pack"
    source.mkdir()

    report = run_optional_sftp_transfer(
        OptionalSFTPTransferRequest(
            transfer_id="sftp-live-smoke-skip",
            package_id="ctx-sftp-live-smoke",
            source_dir=str(source),
            remote_target="/explicit/reviewed/target",
            live_enabled=True,
            allow_remote_write=True,
        )
    )

    if report.status == TransferStatus.SKIPPED_LIVE_DISABLED:
        pytest.skip(report.errors[0])

    pytest.fail("SFTP live smoke should skip without explicit live opt-in")
