from __future__ import annotations

import pytest

from turing_research_plus.remote_readers.models import (
    RemoteReaderReport,
    RemoteReaderSourceType,
    RemoteReaderStatus,
    RemoteSelectedFile,
)


def test_remote_reader_report_serializes_and_exports_markdown() -> None:
    report = RemoteReaderReport(
        host_label="fake-vggt-remote",
        root_path="/remote/vggt/review_bundle",
        retrieval_status=RemoteReaderStatus.INDEXED,
        scanned_paths=["/remote/vggt/review_bundle/review/final_status.json"],
        selected_files=[
            RemoteSelectedFile(
                path="/remote/vggt/review_bundle/review/final_status.json",
                size=512,
                source_type=RemoteReaderSourceType.LOCAL_FIXTURE,
            )
        ],
    )

    payload = report.model_dump(mode="json")
    markdown = report.to_markdown()

    assert payload["requires_human_review"] is True
    assert payload["human_verified"] is False
    assert "not human verified" in markdown


def test_remote_selected_file_cannot_be_verified() -> None:
    with pytest.raises(ValueError, match="never marks selected files verified"):
        RemoteSelectedFile(
            path="/remote/vggt/review_bundle/review/final_status.json",
            size=512,
            source_type=RemoteReaderSourceType.LOCAL_FIXTURE,
            verified=True,
        )
