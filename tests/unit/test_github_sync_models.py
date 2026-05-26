from __future__ import annotations

import pytest

from turing_research_plus.github_sync.models import (
    GitHubArtifactSourceType,
    GitHubArtifactStatus,
    GitHubArtifactSyncReport,
    GitHubSelectedFile,
)


def test_github_selected_file_cannot_be_verified() -> None:
    with pytest.raises(ValueError, match="never marks selected files verified"):
        GitHubSelectedFile(
            path="review/final_status.json",
            size=10,
            sha256="1" * 64,
            source_type=GitHubArtifactSourceType.WORKFLOW_ARTIFACT,
            verified=True,
        )


def test_github_sync_report_serializes_and_requires_review() -> None:
    report = GitHubArtifactSyncReport(
        source_repo="example/repo",
        source_ref="main",
        retrieval_status=GitHubArtifactStatus.INDEXED,
        selected_files=[
            GitHubSelectedFile(
                path="review/final_status.json",
                size=10,
                sha256="1" * 64,
                source_type=GitHubArtifactSourceType.WORKFLOW_ARTIFACT,
            )
        ],
    )

    payload = report.model_dump(mode="json")

    assert payload["requires_human_review"] is True
    assert payload["human_verified"] is False
    assert "final_status.json" in report.to_markdown()
