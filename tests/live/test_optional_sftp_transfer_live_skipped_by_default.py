from __future__ import annotations

import os
from pathlib import Path

import pytest

from turing_research_plus.session_runtime.sftp_transfer_optional import (
    DEFAULT_CREDENTIAL_ENV,
)
from turing_research_plus.session_runtime.transfer_report import TransferMode, TransferStatus
from turing_research_plus.session_runtime.transfer_runner import (
    TransferRunnerRequest,
    run_transfer,
)

pytestmark = pytest.mark.live


def test_optional_sftp_transfer_live_skipped_by_default(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.mkdir()
    (source / "PROJECT_CONTEXT.md").write_text("project\n", encoding="utf-8")

    if (
        os.getenv("TURINGRESEARCH_ENABLE_LIVE_TESTS") == "1"
        and os.getenv(DEFAULT_CREDENTIAL_ENV)
    ):
        pytest.skip("live SFTP transfer requires a project-specific adapter in a later gate")

    report = run_transfer(
        TransferRunnerRequest(
            transfer_id="tx-live-skip",
            package_id="ctx-live-skip",
            source_dir=source,
            target="/safe/context-pack",
            mode=TransferMode.SFTP,
            live_enabled=True,
            allow_remote_write=True,
        )
    )

    assert report.status in {
        TransferStatus.SKIPPED_LIVE_DISABLED,
        TransferStatus.SKIPPED_MISSING_CREDENTIAL,
    }
    assert report.remote_command_execution is False
    assert report.remote_delete is False
