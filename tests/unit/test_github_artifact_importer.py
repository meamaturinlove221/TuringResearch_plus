from __future__ import annotations

from pathlib import Path

from turing_research_plus.github_sync.importer import build_github_artifact_sync_report
from turing_research_plus.github_sync.models import (
    GitHubArtifactStatus,
    GitHubArtifactSyncRequest,
)

FIXTURE = (
    Path(__file__).resolve().parents[2]
    / "examples"
    / "vggt-human-prior-survey"
    / "github_artifact_sync_fixture"
    / "artifact_index.json"
)


def test_github_artifact_importer_uses_fixture_without_network() -> None:
    report = build_github_artifact_sync_report(
        GitHubArtifactSyncRequest(
            source_repo="example/vggt-review-artifacts",
            source_ref="modal-sparseconv-review",
            fixture_index_path=FIXTURE,
        )
    )

    assert report.retrieval_status == GitHubArtifactStatus.INDEXED
    assert any(item.path == "review/final_status.json" for item in report.selected_files)
    assert any(item.path == "large/predictions.npz" for item in report.omitted_files)
    assert any(item.path == "private/SMPLX_model.pkl" for item in report.omitted_files)
    assert report.proposed_imports
    assert report.human_verified is False


def test_github_artifact_importer_live_missing_token_is_graceful(monkeypatch) -> None:
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)

    report = build_github_artifact_sync_report(
        GitHubArtifactSyncRequest(
            source_repo="example/private",
            source_ref="main",
            dry_run=False,
            live_enabled=True,
        )
    )

    assert report.retrieval_status == GitHubArtifactStatus.MISSING_TOKEN
    assert report.selected_files == []
    assert report.requires_human_review is True
