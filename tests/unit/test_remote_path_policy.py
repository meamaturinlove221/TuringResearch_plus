from __future__ import annotations

from turing_research_plus.remote_readers.path_policy import (
    normalize_remote_path,
    path_policy_warnings,
    remote_path_is_allowed,
)


def test_normalize_remote_path_uses_posix_form() -> None:
    assert normalize_remote_path("\\remote\\vggt//review_bundle/") == "/remote/vggt/review_bundle"


def test_remote_path_policy_blocks_traversal_and_outside_root() -> None:
    warnings = path_policy_warnings(
        "/remote/vggt/review_bundle/../secrets/key.txt",
        root_path="/remote/vggt/review_bundle",
    )

    assert "path-traversal" in warnings
    assert "forbidden-private-or-cache-path" in warnings
    assert remote_path_is_allowed(
        "/remote/vggt/review_bundle/review/final_status.json",
        root_path="/remote/vggt/review_bundle",
    )
    assert not remote_path_is_allowed("/etc", root_path="/remote/vggt/review_bundle")
