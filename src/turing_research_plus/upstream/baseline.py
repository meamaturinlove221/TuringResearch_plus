"""Build upstream baselines from public repository metadata."""

from __future__ import annotations

from collections.abc import Mapping

from turing_research_plus.upstream.models import RepoBaseline

PACKAGE_FILENAMES = {
    "package.json",
    "package-lock.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "pyproject.toml",
    "setup.py",
    "setup.cfg",
}
MCP_FILENAMES = {
    ".mcp.example.json",
    "mcp.json",
    "mcp.config.json",
}


def build_repo_baseline(
    *,
    repository_full_name: str,
    url: str,
    default_branch: str,
    latest_commit_sha: str,
    latest_commit_message: str,
    latest_commit_time: str,
    paths: list[str],
    file_hashes: Mapping[str, str],
) -> RepoBaseline:
    """Build a normalized repository baseline from public metadata."""

    classified = classify_repo_paths(paths)
    focused_hashes = {
        path: digest
        for path, digest in sorted(file_hashes.items())
        if _is_focus_path(path)
    }
    return RepoBaseline(
        repository_full_name=repository_full_name,
        url=url,
        default_branch=default_branch,
        latest_commit_sha=latest_commit_sha,
        latest_commit_message=latest_commit_message,
        latest_commit_time=latest_commit_time,
        file_hashes=focused_hashes,
        **classified,
    )


def build_unresolved_repo_baseline(
    *,
    repository_full_name: str,
    url: str,
    unresolved_reason: str,
) -> RepoBaseline:
    """Build an unresolved repository baseline without failing the scan."""

    return RepoBaseline(
        repository_full_name=repository_full_name,
        url=url,
        unresolved_reason=unresolved_reason,
    )


def classify_repo_paths(paths: list[str]) -> dict[str, list[str]]:
    """Classify paths into upstream watch baseline buckets."""

    normalized = sorted(dict.fromkeys(path.strip("/") for path in paths if path))
    return {
        "root_files": [path for path in normalized if "/" not in path],
        "markdown_files": [path for path in normalized if path.lower().endswith(".md")],
        "skill_files": [
            path
            for path in normalized
            if path.startswith(".agents/")
            or path.startswith("skills/")
            or "/skills/" in path
            or path.endswith("SKILL.md")
        ],
        "docs_files": [path for path in normalized if path.startswith("docs/")],
        "package_files": [
            path for path in normalized if path.rsplit("/", maxsplit=1)[-1] in PACKAGE_FILENAMES
        ],
        "mcp_config_files": [
            path
            for path in normalized
            if path.rsplit("/", maxsplit=1)[-1] in MCP_FILENAMES or "mcp" in path.lower()
        ],
        "src_files": [path for path in normalized if path.startswith("src/")],
        "test_files": [path for path in normalized if path.startswith("tests/")],
    }


def _is_focus_path(path: str) -> bool:
    lower = path.lower()
    basename = lower.rsplit("/", maxsplit=1)[-1]
    return (
        basename in {"readme.md", "entry.md"}
        or basename in PACKAGE_FILENAMES
        or basename in MCP_FILENAMES
        or lower.startswith(
            (".codex/", ".agents/", "skills/", "src/", "docs/", "tests/", "examples/")
        )
        or lower.endswith((".md", ".yaml", ".yml"))
    )
