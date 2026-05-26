from __future__ import annotations

import pytest

from turing_research_plus.git_handoff.models import (
    ContextFile,
    ContextPackage,
    GitTransportPolicy,
    MemoryPolicy,
)


def test_context_package_requires_human_review() -> None:
    package = ContextPackage(
        package_id="pkg",
        route_id="route",
        context_files=[ContextFile(relative_path="README.md", sha256="a" * 64)],
    )

    assert package.project_name == "TuringResearch Plus"
    assert package.requires_human_review is True
    assert "not executed by TuringResearch" in package.to_markdown()


def test_context_package_rejects_remote_execution_policy() -> None:
    with pytest.raises(ValueError, match="remote execution"):
        ContextPackage(
            package_id="pkg",
            route_id="route",
            context_files=[ContextFile(relative_path="README.md", sha256="a" * 64)],
            git_transport_policy=GitTransportPolicy(remote_execution_allowed=True),
        )


def test_memory_policy_rejects_memory_as_only_truth() -> None:
    with pytest.raises(ValueError, match="cannot be the only source"):
        MemoryPolicy(source_of_truth="memory")
