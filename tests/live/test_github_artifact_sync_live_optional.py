from __future__ import annotations

import os

import pytest

from turing_research_plus.github_sync.importer import build_github_artifact_sync_report
from turing_research_plus.github_sync.models import GitHubArtifactSyncRequest

pytestmark = pytest.mark.live


def test_github_artifact_sync_live_optional_default_skips() -> None:
    if os.getenv("TURINGRESEARCH_ENABLE_LIVE_TESTS") != "1" or not os.getenv("GITHUB_TOKEN"):
        pytest.skip("GitHub live artifact sync requires explicit live opt-in and GITHUB_TOKEN")

    report = build_github_artifact_sync_report(
        GitHubArtifactSyncRequest(
            source_repo="octocat/Hello-World",
            source_ref="main",
            dry_run=False,
            live_enabled=True,
        )
    )

    assert report.requires_human_review is True
    assert report.human_verified is False
