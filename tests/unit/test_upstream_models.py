import pytest
from pydantic import ValidationError

from turing_research_plus.upstream.models import ChangeCategory, RepoBaseline, UpstreamBaselineSet


def test_repo_baseline_requires_commit_when_resolved() -> None:
    with pytest.raises(ValidationError):
        RepoBaseline(repository_full_name="org/repo", url="https://github.com/org/repo")


def test_unresolved_repo_baseline_is_allowed_without_commit() -> None:
    baseline = RepoBaseline(
        repository_full_name="org/repo",
        url="https://github.com/org/repo",
        unresolved_reason="404 not found",
    )

    assert not baseline.resolved


def test_baseline_set_indexes_by_repository_name() -> None:
    repo = RepoBaseline(
        repository_full_name="org/repo",
        url="https://github.com/org/repo",
        latest_commit_sha="abc",
    )
    baseline = UpstreamBaselineSet(
        baseline_id="baseline",
        generated_at="2026-05-20T00:00:00Z",
        repositories=[repo],
    )

    assert baseline.by_repo()["org/repo"] == repo
    assert ChangeCategory.NEW_FILE.value == "new_file"
