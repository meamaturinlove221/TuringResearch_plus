from __future__ import annotations

from turing_research_plus.remote_readers.safety import (
    omitted_reason_for_remote_file,
    safety_warnings_for_remote_path,
    should_select_remote_file,
)


def test_remote_reader_safety_omits_smplx_and_large_files() -> None:
    warnings = safety_warnings_for_remote_path(
        "/remote/vggt/review_bundle/private/SMPLX_model.pkl",
        root_path="/remote/vggt/review_bundle",
        size=100_000_000,
    )

    assert "summary-only-required" in warnings
    assert "forbidden-secret-or-body-model-pattern" in warnings
    assert "file-too-large" in warnings
    assert not should_select_remote_file(
        "/remote/vggt/review_bundle/private/SMPLX_model.pkl",
        root_path="/remote/vggt/review_bundle",
        size=100_000_000,
    )


def test_remote_reader_safety_marks_symlink_for_review() -> None:
    warnings = safety_warnings_for_remote_path(
        "/remote/vggt/review_bundle/review/current_failure_link.md",
        root_path="/remote/vggt/review_bundle",
        is_symlink=True,
    )

    assert warnings == ["symlink-requires-review"]
    assert omitted_reason_for_remote_file(warnings) == "remote symlink requires manual review"
