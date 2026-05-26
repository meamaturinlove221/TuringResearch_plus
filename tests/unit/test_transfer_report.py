from __future__ import annotations

import pytest
from pydantic import ValidationError

from turing_research_plus.session_runtime.transfer_report import (
    TransferReport,
    TransferStatus,
    render_transfer_report,
)


def test_transfer_report_requires_review_and_blocks_remote_command_flags() -> None:
    with pytest.raises(ValidationError):
        TransferReport(
            transfer_id="tx",
            package_id="ctx",
            status=TransferStatus.TRANSFERRED,
            source_dir="source",
            target="target",
            remote_command_execution=True,
        )

    with pytest.raises(ValidationError):
        TransferReport(
            transfer_id="tx",
            package_id="ctx",
            status=TransferStatus.TRANSFERRED,
            source_dir="source",
            target="target",
            remote_delete=True,
        )


def test_render_transfer_report_shows_no_secret_logging_boundary() -> None:
    report = TransferReport(
        transfer_id="tx",
        package_id="ctx",
        status=TransferStatus.TRANSFERRED,
        source_dir="source",
        target="target",
    )

    text = render_transfer_report(report)

    assert "Remote command execution: `false`" in text
    assert "Remote delete: `false`" in text
    assert "Secrets logged: `false`" in text
    assert "Requires human review: `true`" in text


def test_transfer_report_release_blocker_for_errors() -> None:
    report = TransferReport(
        transfer_id="tx",
        package_id="ctx",
        status=TransferStatus.BLOCKED,
        source_dir="source",
        target="target",
        errors=["blocked"],
    )

    assert report.release_blocker is True
