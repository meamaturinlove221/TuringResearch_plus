from __future__ import annotations

from turing_research_plus.pod_lifecycle import (
    normalize_archive_entry,
    validate_archive_entry,
    validate_context_archive_entries,
)


def test_normalize_archive_entry_uses_relative_posix_paths() -> None:
    assert normalize_archive_entry(".\\PROJECT_CONTEXT.md") == "PROJECT_CONTEXT.md"
    assert normalize_archive_entry("notes\\MEMORY.md") == "notes/MEMORY.md"


def test_archive_safety_blocks_dotfiles_and_path_traversal() -> None:
    report = validate_context_archive_entries(["PROJECT_CONTEXT.md", ".env", "../secret.txt"])

    assert report.release_blocker is True
    assert ".env" in report.blocked_paths
    assert "../secret.txt" in report.blocked_paths


def test_archive_safety_blocks_shell_metacharacter_risk() -> None:
    entry = validate_archive_entry("safe;rm.txt")

    assert entry.safe is False
    assert "shell-metacharacter-risk" in entry.warnings


def test_archive_safety_blocks_windows_absolute_paths() -> None:
    entry = validate_archive_entry("C:/Users/private/PROJECT_CONTEXT.md")

    assert entry.safe is False
    assert "unsafe-archive-absolute-path" in entry.warnings
