"""Import selected GitHub artifact metadata and small files."""

from __future__ import annotations

from turing_research_plus.github_sync.artifact_index import (
    filter_selected_artifacts,
    load_artifact_index,
)
from turing_research_plus.github_sync.fake_client import FakeGitHubArtifactClient
from turing_research_plus.github_sync.live_client import GitHubLiveClient
from turing_research_plus.github_sync.models import (
    GitHubArtifactRecord,
    GitHubArtifactStatus,
    GitHubArtifactSyncReport,
    GitHubArtifactSyncRequest,
    GitHubOmittedFile,
    GitHubSelectedFile,
)
from turing_research_plus.github_sync.safety import (
    omitted_reason_for_artifact,
    safety_warnings_for_artifact_path,
)


def build_github_artifact_sync_report(
    request: GitHubArtifactSyncRequest,
    *,
    fake_client: FakeGitHubArtifactClient | None = None,
    live_client: GitHubLiveClient | None = None,
) -> GitHubArtifactSyncReport:
    """Build a fake/default GitHub artifact sync report."""

    artifacts, status, warnings, live_result = _load_artifacts(
        request,
        fake_client=fake_client,
        live_client=live_client,
    )
    selected_candidates = filter_selected_artifacts(artifacts, request.selected_patterns)
    selected_files: list[GitHubSelectedFile] = []
    omitted_files: list[GitHubOmittedFile] = []
    all_warnings = list(warnings)

    for artifact in selected_candidates:
        safety_warnings = safety_warnings_for_artifact_path(
            artifact.path,
            size=artifact.size,
            max_size=request.max_file_size_bytes,
        )
        if safety_warnings:
            omitted_files.append(
                GitHubOmittedFile(
                    path=artifact.path,
                    size=artifact.size,
                    reason=omitted_reason_for_artifact(safety_warnings),
                    safety_warnings=safety_warnings,
                )
            )
            all_warnings.extend(safety_warnings)
            continue
        selected_files.append(
            GitHubSelectedFile(
                path=artifact.path,
                size=artifact.size,
                sha256=artifact.sha256,
                source_type=artifact.source_type,
                retrieval_status=GitHubArtifactStatus.RETRIEVED
                if request.allow_download and live_result
                else GitHubArtifactStatus.SELECTED,
                verified=False,
                warnings=["retrieved/indexed GitHub artifact is not human verified"],
            )
        )

    sha256 = {item.path: item.sha256 for item in selected_files if item.sha256}
    size = {artifact.path: artifact.size for artifact in artifacts}
    proposed_imports = [
        {
            "path": item.path,
            "status": "requires-human-review",
            "source_repo": request.source_repo,
            "source_ref": request.source_ref,
        }
        for item in selected_files
    ]
    return GitHubArtifactSyncReport(
        source_repo=request.source_repo,
        source_ref=request.source_ref,
        retrieval_status=status,
        artifact_list=artifacts,
        selected_files=selected_files,
        omitted_files=omitted_files,
        sha256=sha256,
        size=size,
        safety_warnings=sorted(set(all_warnings)),
        proposed_imports=proposed_imports,
        requires_human_review=True,
        live_result=live_result,
        human_verified=False,
        limitations=[
            "GitHub artifact sync imports selected metadata and small review files only.",
            "Remote artifacts are retrieved or indexed, not human verified.",
            "Evidence Ledger is not overwritten automatically.",
        ],
    )


def _load_artifacts(
    request: GitHubArtifactSyncRequest,
    *,
    fake_client: FakeGitHubArtifactClient | None,
    live_client: GitHubLiveClient | None,
) -> tuple[list[GitHubArtifactRecord], GitHubArtifactStatus, list[str], bool]:
    if request.fixture_index_path is not None:
        return (
            load_artifact_index(request.fixture_index_path),
            GitHubArtifactStatus.INDEXED,
            ["local fixture index; no network access performed"],
            False,
        )
    if request.dry_run:
        fake = fake_client or FakeGitHubArtifactClient()
        artifacts = [
            *fake.list_release_assets(request.source_repo, request.source_ref),
            *fake.list_workflow_artifacts(request.source_repo, request.source_ref),
        ]
        return artifacts, GitHubArtifactStatus.INDEXED, ["fake client; no network access"], False
    if not request.live_enabled:
        return [], GitHubArtifactStatus.LIVE_DISABLED, ["GitHub live sync is disabled"], False
    live = live_client or GitHubLiveClient(token_env=request.token_env)
    if not live.has_token():
        return [], GitHubArtifactStatus.MISSING_TOKEN, [live.missing_token_error().message], False
    try:
        artifacts = [
            *live.list_release_assets(request.source_repo, request.source_ref),
            *live.list_workflow_artifacts(request.source_repo, request.source_ref),
        ]
    except Exception as exc:  # pragma: no cover - live path guarded by optional tests
        return [], GitHubArtifactStatus.ERROR, [f"GitHub live sync failed: {exc}"], True
    return (
        artifacts,
        GitHubArtifactStatus.RETRIEVED,
        ["live result is retrieved, not verified"],
        True,
    )
