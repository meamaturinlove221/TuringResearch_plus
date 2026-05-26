from __future__ import annotations

from turing_research_plus.pod_lifecycle import build_platform_compatibility_report


def test_platform_compatibility_warns_for_windows_to_linux_archive() -> None:
    report = build_platform_compatibility_report(
        source_platform="Windows",
        target_platform="Linux pod",
    )

    assert report.release_blocker is False
    assert report.requires_pre_unpack_validation is True
    assert "windows-to-linux-unpack-requires-path-validation" in report.warnings
    assert "/" == report.normalized_separator


def test_platform_compatibility_warns_for_unreviewed_archive_format() -> None:
    report = build_platform_compatibility_report(
        source_platform="Linux",
        target_platform="Linux",
        archive_format="7z",
    )

    assert "unreviewed-archive-format" in report.warnings
