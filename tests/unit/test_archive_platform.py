from __future__ import annotations

from turing_research_plus.session_runtime.archive_platform import (
    build_archive_platform_notes,
    normalize_platform_archive_path,
    render_archive_platform_notes,
)


def test_archive_platform_notes_cover_cross_platform_policies() -> None:
    notes = build_archive_platform_notes()

    assert "POSIX" in notes.windows_path_policy
    assert "same-owner" in notes.no_same_owner_note
    assert "Symlink" in notes.symlink_policy
    assert "checksums" in notes.checksum_policy
    assert "Return archives" in notes.return_archive_policy


def test_normalize_platform_archive_path_converts_windows_separator() -> None:
    assert normalize_platform_archive_path(r"returns\FINAL_STATUS.json") == (
        "returns/FINAL_STATUS.json"
    )


def test_render_archive_platform_notes_mentions_manual_unpack_policy() -> None:
    text = render_archive_platform_notes()

    assert "Cross-platform Archive Notes" in text
    assert "--same-owner" in text
    assert "Symlink policy" in text
