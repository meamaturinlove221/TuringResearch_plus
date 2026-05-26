from __future__ import annotations

from pathlib import Path

from turing_research_plus.remote_readers.models import (
    RemoteReaderRequest,
    RemoteReaderStatus,
)
from turing_research_plus.remote_readers.tools import read_remote_artifacts

FIXTURE = (
    Path(__file__).resolve().parents[2]
    / "examples"
    / "vggt-human-prior-survey"
    / "remote_reader_fixture"
    / "artifact_index.json"
)


def test_remote_reader_fake_vggt_fixture_preserves_boundaries() -> None:
    report = read_remote_artifacts(
        RemoteReaderRequest(
            host_label="fake-vggt-remote",
            root_path="/remote/vggt/review_bundle",
            fixture_index_path=FIXTURE,
            selected_patterns=["review/", "large/", "private/", ".env"],
        )
    )
    markdown = report.to_markdown()

    assert report.retrieval_status == RemoteReaderStatus.INDEXED
    assert any(item.path.endswith("review/final_status.json") for item in report.selected_files)
    assert any(item.path.endswith("review/failure_report.md") for item in report.selected_files)
    assert any(item.path.endswith("large/predictions.npz") for item in report.omitted_files)
    assert any(item.path.endswith("private/SMPLX_model.pkl") for item in report.omitted_files)
    assert any(item.path.endswith(".env") for item in report.omitted_files)
    assert any("symlink" in warning for warning in report.safety_warnings)
    assert all(item["status"] == "requires-human-review" for item in report.proposed_imports)
    assert report.human_verified is False
    assert "not human verified" in markdown
