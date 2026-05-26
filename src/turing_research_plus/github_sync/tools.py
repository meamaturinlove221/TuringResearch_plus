"""Local tool wrappers for GitHub artifact sync."""

from __future__ import annotations

from turing_research_plus.github_sync.importer import build_github_artifact_sync_report
from turing_research_plus.github_sync.models import (
    GitHubArtifactSyncReport,
    GitHubArtifactSyncRequest,
)


def github_artifact_sync(request: GitHubArtifactSyncRequest) -> GitHubArtifactSyncReport:
    """Build a GitHub artifact sync report without default network access."""

    return build_github_artifact_sync_report(request)
