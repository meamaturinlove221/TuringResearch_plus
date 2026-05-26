from __future__ import annotations

from pathlib import Path

import pytest

from turing_research_plus.repo_split.models import (
    RepoSplitDryRunRequest,
    RepoSplitFileRecord,
    RepoSplitManifest,
    RepoSplitSafetyReport,
)


def test_repo_split_models_require_dry_run_and_review(tmp_path: Path) -> None:
    request = RepoSplitDryRunRequest(
        candidate_id="turingresearch-vggt-case",
        source_root=tmp_path / "source",
        output_root=tmp_path / "out",
    )

    assert request.candidate_id == "turingresearch-vggt-case"
    assert ".md" in request.allowed_suffixes

    manifest = RepoSplitManifest(
        candidate_id="turingresearch-vggt-case",
        source_root="examples/split_repos/turingresearch-vggt-case",
    )
    assert manifest.dry_run_only is True
    assert manifest.creates_github_repo is False
    assert manifest.pushes_git is False
    assert manifest.requires_human_review is True


def test_repo_split_manifest_rejects_push_semantics() -> None:
    with pytest.raises(ValueError, match="must not create GitHub repos or push git"):
        RepoSplitManifest(
            candidate_id="bad",
            source_root="source",
            pushes_git=True,
        )


def test_omitted_file_record_requires_reason() -> None:
    with pytest.raises(ValueError, match="requires omitted_reason"):
        RepoSplitFileRecord(relative_path="secret.env", included=False)


def test_safety_report_summarizes_release_blockers() -> None:
    report = RepoSplitSafetyReport(candidate_id="candidate")

    assert report.safe_to_export is True
    assert report.release_blocker is False
    assert report.requires_human_review is True
