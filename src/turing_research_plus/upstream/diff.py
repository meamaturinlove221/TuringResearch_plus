"""Diff upstream watch baselines."""

from __future__ import annotations

from turing_research_plus.upstream.models import (
    ChangeCategory,
    RepoBaseline,
    UpstreamBaselineSet,
    UpstreamChange,
    UpstreamDiffReport,
)


def diff_baselines(
    old: UpstreamBaselineSet | None,
    new: UpstreamBaselineSet,
) -> UpstreamDiffReport:
    """Compare two upstream baselines."""

    if old is None:
        return UpstreamDiffReport(
            report_id=f"{new.baseline_id}-initial-report",
            new_baseline_id=new.baseline_id,
            is_initial_baseline=True,
            changes=[
                UpstreamChange(
                    repository_full_name=repo.repository_full_name,
                    category=ChangeCategory.UNRESOLVED_REPO
                    if repo.unresolved_reason
                    else ChangeCategory.NEW_REPO,
                    summary=repo.unresolved_reason or "Initial baseline captured.",
                )
                for repo in new.repositories
            ],
        )

    old_repos = old.by_repo()
    new_repos = new.by_repo()
    changes: list[UpstreamChange] = []

    for repo_name in sorted(set(new_repos) - set(old_repos)):
        repo = new_repos[repo_name]
        changes.append(
            UpstreamChange(
                repository_full_name=repo_name,
                category=ChangeCategory.UNRESOLVED_REPO
                if repo.unresolved_reason
                else ChangeCategory.NEW_REPO,
                summary=repo.unresolved_reason or "Repository appeared in new baseline.",
            )
        )
    for repo_name in sorted(set(old_repos) - set(new_repos)):
        changes.append(
            UpstreamChange(
                repository_full_name=repo_name,
                category=ChangeCategory.REMOVED_REPO,
                summary="Repository missing from new baseline.",
            )
        )
    for repo_name in sorted(set(old_repos) & set(new_repos)):
        changes.extend(_diff_repo(old_repos[repo_name], new_repos[repo_name]))

    return UpstreamDiffReport(
        report_id=f"{new.baseline_id}-diff-report",
        old_baseline_id=old.baseline_id,
        new_baseline_id=new.baseline_id,
        changes=changes,
    )


def _diff_repo(old: RepoBaseline, new: RepoBaseline) -> list[UpstreamChange]:
    if new.unresolved_reason:
        return [
            UpstreamChange(
                repository_full_name=new.repository_full_name,
                category=ChangeCategory.UNRESOLVED_REPO,
                summary=new.unresolved_reason,
            )
        ]
    if old.unresolved_reason and not new.unresolved_reason:
        return [
            UpstreamChange(
                repository_full_name=new.repository_full_name,
                category=ChangeCategory.NEW_REPO,
                summary="Repository resolved after prior unresolved baseline.",
            )
        ]

    changes: list[UpstreamChange] = []
    old_paths = set(old.file_hashes)
    new_paths = set(new.file_hashes)
    for path in sorted(new_paths - old_paths):
        changes.append(_file_change(new.repository_full_name, ChangeCategory.NEW_FILE, path))
    for path in sorted(old_paths - new_paths):
        changes.append(_file_change(new.repository_full_name, ChangeCategory.REMOVED_FILE, path))
    for path in sorted(old_paths & new_paths):
        if old.file_hashes[path] != new.file_hashes[path]:
            changes.append(_file_change(new.repository_full_name, _category_for_path(path), path))
    return changes


def _file_change(
    repo_name: str,
    category: ChangeCategory,
    path: str,
) -> UpstreamChange:
    return UpstreamChange(
        repository_full_name=repo_name,
        category=category,
        path=path,
        summary=f"{category.value}: {path}",
    )


def _category_for_path(path: str) -> ChangeCategory:
    lower = path.lower()
    basename = lower.rsplit("/", maxsplit=1)[-1]
    if basename == "readme.md":
        return ChangeCategory.README_CHANGE
    if basename == "entry.md":
        return ChangeCategory.ENTRY_CHANGE
    if lower.endswith("skill.md") or "skills/" in lower or ".agents/" in lower:
        return ChangeCategory.SKILL_CHANGE
    if "mcp" in lower:
        return ChangeCategory.MCP_TOOL_CHANGE
    if basename in {"package.json", "pyproject.toml", "setup.py", "setup.cfg"}:
        return ChangeCategory.PACKAGE_RELEASE_CHANGE
    if lower.startswith("docs/") or lower.endswith(".md"):
        return ChangeCategory.DOCS_CHANGE
    if lower.startswith("tests/"):
        return ChangeCategory.TEST_CHANGE
    if lower.startswith("src/"):
        return ChangeCategory.SOURCE_MODULE_CHANGE
    return ChangeCategory.CHANGED_FILE
