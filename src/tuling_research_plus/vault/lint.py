"""Lint checks for Wiki Vault."""

from __future__ import annotations

from pathlib import Path

from tuling_research_plus.vault.graph import VaultGraph
from tuling_research_plus.vault.markdown_io import list_page_paths, read_page, split_frontmatter
from tuling_research_plus.vault.models import VaultLintIssue


def lint_vault(root: str | Path) -> list[VaultLintIssue]:
    """Lint vault pages and graph connectivity."""

    root_path = Path(root)
    issues: list[VaultLintIssue] = []
    for path in list_page_paths(root_path):
        text = path.read_text(encoding="utf-8")
        try:
            split_frontmatter(text)
        except ValueError as exc:
            issues.append(
                VaultLintIssue(
                    issue_type="missing_frontmatter",
                    path=path,
                    message=str(exc),
                )
            )
    issues.extend(orphan_issues(root_path))
    return issues


def orphan_issues(root: str | Path) -> list[VaultLintIssue]:
    """Return orphan page lint issues."""

    root_path = Path(root)
    graph = VaultGraph(root_path)
    connected = {edge.source_id for edge in graph.list_edges()} | {
        edge.target_id for edge in graph.list_edges()
    }
    issues: list[VaultLintIssue] = []
    for path in list_page_paths(root_path):
        try:
            page = read_page(path)
        except ValueError:
            continue
        if page.page_id not in connected:
            issues.append(
                VaultLintIssue(
                    issue_type="orphan_page",
                    path=path,
                    page_id=page.page_id,
                    message="page has no graph edges",
                )
            )
    return issues
