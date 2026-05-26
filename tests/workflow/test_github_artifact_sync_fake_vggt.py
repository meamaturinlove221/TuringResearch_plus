from __future__ import annotations

from pathlib import Path

from turing_research_plus.github_sync.importer import build_github_artifact_sync_report
from turing_research_plus.github_sync.models import GitHubArtifactSyncRequest

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = (
    ROOT
    / "examples"
    / "vggt-human-prior-survey"
    / "github_artifact_sync_fixture"
    / "artifact_index.json"
)


def test_github_artifact_sync_fake_vggt_fixture_preserves_boundaries() -> None:
    report = build_github_artifact_sync_report(
        GitHubArtifactSyncRequest(
            source_repo="example/vggt-review-artifacts",
            source_ref="modal-sparseconv-review",
            fixture_index_path=FIXTURE,
            selected_patterns=["review/", "large/", "private/"],
        )
    )
    markdown = report.to_markdown()

    assert any(item.path == "review/final_status.json" for item in report.selected_files)
    assert any(item.path == "review/failure_report.md" for item in report.selected_files)
    assert any(item.path == "large/predictions.npz" for item in report.omitted_files)
    assert any(item.path == "private/SMPLX_model.pkl" for item in report.omitted_files)
    assert all(item["status"] == "requires-human-review" for item in report.proposed_imports)
    assert report.human_verified is False
    assert "not human verified" in markdown
