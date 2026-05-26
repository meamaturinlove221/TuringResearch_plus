from __future__ import annotations

from turing_research_plus.github_sync.fake_client import FakeGitHubArtifactClient
from turing_research_plus.github_sync.models import GitHubArtifactSourceType


def test_fake_github_client_returns_release_and_workflow_artifacts() -> None:
    client = FakeGitHubArtifactClient()

    release_assets = client.list_release_assets("example/repo", "v1")
    workflow_artifacts = client.list_workflow_artifacts("example/repo", "main")

    assert release_assets
    assert workflow_artifacts
    assert release_assets[0].source_type == GitHubArtifactSourceType.RELEASE_ASSET
    assert workflow_artifacts[0].source_type == GitHubArtifactSourceType.WORKFLOW_ARTIFACT
