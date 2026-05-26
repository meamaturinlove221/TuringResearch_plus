from __future__ import annotations

import pytest

from turing_research_plus.session_runtime.path_normalization import (
    normalize_archive_member_path,
    require_safe_archive_member_path,
    windows_path_to_posix,
)


def test_windows_path_to_posix_preserves_archive_intent() -> None:
    assert windows_path_to_posix(r"nested\PROJECT_CONTEXT.md") == "nested/PROJECT_CONTEXT.md"


def test_normalize_archive_member_path_blocks_traversal() -> None:
    report = normalize_archive_member_path(r"..\secrets\.env")

    assert report.release_blocker is True
    assert "path-traversal" in report.blocked_reasons
    assert report.normalized_path == "secrets/.env"


def test_normalize_archive_member_path_blocks_windows_drive() -> None:
    report = normalize_archive_member_path(r"C:\Users\demo\file.md")

    assert "windows-drive-path" in report.blocked_reasons


def test_require_safe_archive_member_path_returns_posix_path() -> None:
    assert require_safe_archive_member_path(r"docs\README.md") == "docs/README.md"


def test_require_safe_archive_member_path_raises_for_unsafe_path() -> None:
    with pytest.raises(ValueError, match="unsafe archive member path"):
        require_safe_archive_member_path("/tmp/file.md")
