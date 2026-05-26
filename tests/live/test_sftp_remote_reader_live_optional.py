from __future__ import annotations

import os

import pytest

from turing_research_plus.remote_readers.models import RemoteReaderRequest
from turing_research_plus.remote_readers.tools import read_remote_artifacts

pytestmark = pytest.mark.live


def test_sftp_remote_reader_live_optional_default_skips() -> None:
    if (
        os.getenv("TURINGRESEARCH_ENABLE_LIVE_TESTS") != "1"
        or not os.getenv("TURINGRESEARCH_SFTP_CREDENTIAL")
    ):
        pytest.skip("SFTP live reader requires explicit live opt-in and credentials")

    report = read_remote_artifacts(
        RemoteReaderRequest(
            host_label="configured-sftp-host",
            root_path="/remote/vggt/review_bundle",
            dry_run=False,
            live_enabled=True,
        )
    )

    assert report.requires_human_review is True
    assert report.human_verified is False
