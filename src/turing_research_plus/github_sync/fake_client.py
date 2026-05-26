"""Fake GitHub artifact client used by default tests."""

from __future__ import annotations

from turing_research_plus.github_sync.models import (
    GitHubArtifactRecord,
    GitHubArtifactSourceType,
)


class FakeGitHubArtifactClient:
    """Return deterministic GitHub artifact metadata without network access."""

    def list_release_assets(self, source_repo: str, source_ref: str) -> list[GitHubArtifactRecord]:
        """Return fake release assets."""

        return [
            GitHubArtifactRecord(
                name="final_status.json",
                path="release/final_status.json",
                source_type=GitHubArtifactSourceType.RELEASE_ASSET,
                size=512,
                sha256="a" * 64,
                metadata={"source_repo": source_repo, "source_ref": source_ref},
            ),
            GitHubArtifactRecord(
                name="predictions.npz",
                path="release/predictions.npz",
                source_type=GitHubArtifactSourceType.RELEASE_ASSET,
                size=50_000_000,
                sha256="b" * 64,
                metadata={"source_repo": source_repo, "source_ref": source_ref},
            ),
        ]

    def list_workflow_artifacts(
        self,
        source_repo: str,
        source_ref: str,
    ) -> list[GitHubArtifactRecord]:
        """Return fake workflow artifacts."""

        return [
            GitHubArtifactRecord(
                name="failure_report.md",
                path="workflow/failure_report.md",
                source_type=GitHubArtifactSourceType.WORKFLOW_ARTIFACT,
                size=2048,
                sha256="c" * 64,
                metadata={"source_repo": source_repo, "source_ref": source_ref},
            ),
            GitHubArtifactRecord(
                name="SMPLX_model.pkl",
                path="workflow/SMPLX_model.pkl",
                source_type=GitHubArtifactSourceType.WORKFLOW_ARTIFACT,
                size=100_000_000,
                sha256="d" * 64,
                metadata={"source_repo": source_repo, "source_ref": source_ref},
            ),
        ]
