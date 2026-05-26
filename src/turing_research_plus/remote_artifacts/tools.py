"""Local tool wrappers for remote artifact integration."""

from __future__ import annotations

from turing_research_plus.github_sync.models import GitHubArtifactSyncReport
from turing_research_plus.object_store.models import ObjectArtifactIndex
from turing_research_plus.remote_artifacts.models import UnifiedRemoteArtifactReport
from turing_research_plus.remote_artifacts.unified_report import (
    build_unified_remote_artifact_report,
)
from turing_research_plus.remote_readers.models import RemoteReaderReport
from turing_research_plus.shared_store.models import SharedStoreReport


def remote_artifact_unify(
    *,
    github_reports: list[GitHubArtifactSyncReport] | None = None,
    remote_reader_reports: list[RemoteReaderReport] | None = None,
    shared_store_reports: list[SharedStoreReport] | None = None,
    object_indexes: list[ObjectArtifactIndex] | None = None,
) -> UnifiedRemoteArtifactReport:
    """Build a unified remote artifact report."""

    return build_unified_remote_artifact_report(
        github_reports=github_reports,
        remote_reader_reports=remote_reader_reports,
        shared_store_reports=shared_store_reports,
        object_indexes=object_indexes,
    )
