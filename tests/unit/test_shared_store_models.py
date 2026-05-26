from __future__ import annotations

from pathlib import Path

import pytest

from turing_research_plus.shared_store.models import (
    SharedStoreFileRef,
    SharedStoreFileStatus,
    SharedStoreReport,
    SharedStoreScanStatus,
)


def test_shared_store_report_serializes_and_exports_markdown() -> None:
    report = SharedStoreReport(
        mount_label="fake-shared-store",
        root_path=Path("examples/vggt-human-prior-survey/shared_store_fixture"),
        scan_status=SharedStoreScanStatus.INDEXED,
        selected_files=[
            SharedStoreFileRef(
                relative_path="review/final_status.json",
                size=128,
                status=SharedStoreFileStatus.SELECTED,
            )
        ],
    )

    payload = report.model_dump(mode="json")
    markdown = report.to_markdown()

    assert payload["requires_human_review"] is True
    assert payload["human_verified"] is False
    assert "review/final_status.json" in markdown


def test_shared_store_report_cannot_be_human_verified() -> None:
    with pytest.raises(ValueError, match="indexed, not verified"):
        SharedStoreReport(
            mount_label="fake-shared-store",
            root_path=Path("examples/vggt-human-prior-survey/shared_store_fixture"),
            scan_status=SharedStoreScanStatus.INDEXED,
            human_verified=True,
        )
