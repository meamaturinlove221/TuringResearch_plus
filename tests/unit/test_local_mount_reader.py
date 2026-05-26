from __future__ import annotations

from pathlib import Path

from turing_research_plus.shared_store.local_mount_reader import scan_local_mount
from turing_research_plus.shared_store.models import (
    SharedStoreFileStatus,
    SharedStoreScanRequest,
    SharedStoreScanStatus,
)

FIXTURE = (
    Path(__file__).resolve().parents[2]
    / "examples"
    / "vggt-human-prior-survey"
    / "shared_store_fixture"
)


def test_local_mount_reader_indexes_fixture_without_mounting() -> None:
    report = scan_local_mount(
        SharedStoreScanRequest(
            mount_label="fake-shared-store",
            root_path=FIXTURE,
        )
    )

    assert report.scan_status == SharedStoreScanStatus.INDEXED
    assert any(item.relative_path == "review/final_status.json" for item in report.selected_files)
    assert any(item.relative_path == "review/failure_report.md" for item in report.selected_files)
    assert any(item.relative_path == ".env" for item in report.unsafe_files)
    assert any(item.relative_path == "private/SMPLX_model.pkl" for item in report.unsafe_files)
    assert any(item.relative_path == "large/predictions.npz" for item in report.large_files)
    assert report.manifest["review/final_status.json"]
    assert all(item["status"] == "requires-human-review" for item in report.proposed_imports)
    assert report.human_verified is False


def test_local_mount_reader_missing_root_is_graceful(tmp_path: Path) -> None:
    report = scan_local_mount(
        SharedStoreScanRequest(
            mount_label="missing-shared-store",
            root_path=tmp_path / "missing",
        )
    )

    assert report.scan_status == SharedStoreScanStatus.ROOT_MISSING
    assert report.selected_files == []


def test_local_mount_reader_marks_unsupported_as_omitted(tmp_path: Path) -> None:
    root = tmp_path / "store"
    root.mkdir()
    (root / "notes.bin").write_bytes(b"bin")

    report = scan_local_mount(
        SharedStoreScanRequest(
            mount_label="tmp-shared-store",
            root_path=root,
        )
    )

    assert report.omitted_files[0].status == SharedStoreFileStatus.OMITTED
