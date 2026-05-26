from __future__ import annotations

from pathlib import Path

from turing_research_plus.shared_store.models import SharedStoreScanRequest
from turing_research_plus.shared_store.tools import artifact_shared_store_index

FIXTURE = (
    Path(__file__).resolve().parents[2]
    / "examples"
    / "vggt-human-prior-survey"
    / "shared_store_fixture"
)


def test_shared_store_fake_artifacts_preserve_evidence_boundaries() -> None:
    report = artifact_shared_store_index(
        SharedStoreScanRequest(
            mount_label="fake-shared-store",
            root_path=FIXTURE,
            selected_patterns=["review/", "large/", "private/", ".env"],
        )
    )
    markdown = report.to_markdown()

    assert any(item.relative_path == "review/final_status.json" for item in report.selected_files)
    assert any(item.relative_path == "large/predictions.npz" for item in report.large_files)
    assert any(item.relative_path == "private/SMPLX_model.pkl" for item in report.unsafe_files)
    assert any(item.relative_path == ".env" for item in report.unsafe_files)
    assert all(item["status"] == "requires-human-review" for item in report.proposed_imports)
    assert report.human_verified is False
    assert "Shared Store Report" in markdown
    assert "SparseConv3D" not in markdown
