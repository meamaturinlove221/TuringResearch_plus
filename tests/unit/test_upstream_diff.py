from turing_research_plus.upstream.diff import diff_baselines
from turing_research_plus.upstream.models import ChangeCategory, RepoBaseline, UpstreamBaselineSet


def baseline_set(name: str, repos: list[RepoBaseline]) -> UpstreamBaselineSet:
    return UpstreamBaselineSet(
        baseline_id=name,
        generated_at="2026-05-20T00:00:00Z",
        repositories=repos,
    )


def repo(name: str, hashes: dict[str, str]) -> RepoBaseline:
    return RepoBaseline(
        repository_full_name=name,
        url=f"https://github.com/{name}",
        latest_commit_sha="abc",
        file_hashes=hashes,
    )


def test_initial_baseline_marks_initial_not_new_changes() -> None:
    report = diff_baselines(None, baseline_set("b1", [repo("org/repo", {"README.md": "a"})]))

    assert report.is_initial_baseline
    assert report.changes[0].category == ChangeCategory.NEW_REPO


def test_diff_detects_readme_and_skill_changes() -> None:
    old = baseline_set(
        "old",
        [repo("org/repo", {"README.md": "a", ".agents/skills/x/SKILL.md": "s1"})],
    )
    new = baseline_set(
        "new",
        [repo("org/repo", {"README.md": "b", ".agents/skills/x/SKILL.md": "s2"})],
    )

    report = diff_baselines(old, new)
    categories = {change.category for change in report.changes}

    assert ChangeCategory.README_CHANGE in categories
    assert ChangeCategory.SKILL_CHANGE in categories


def test_diff_detects_unresolved_repo() -> None:
    old = baseline_set("old", [repo("org/repo", {"README.md": "a"})])
    new = baseline_set(
        "new",
        [
            RepoBaseline(
                repository_full_name="org/repo",
                url="https://github.com/org/repo",
                unresolved_reason="404 not found",
            )
        ],
    )

    report = diff_baselines(old, new)

    assert report.changes[0].category == ChangeCategory.UNRESOLVED_REPO
