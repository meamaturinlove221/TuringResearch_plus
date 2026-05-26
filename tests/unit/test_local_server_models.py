from __future__ import annotations

from pathlib import Path

import pytest

from turing_research_plus.local_server.models import (
    LocalDashboardRequest,
    LocalDashboardRoute,
    LocalDashboardSafety,
)


def test_local_server_request_is_localhost_only() -> None:
    request = LocalDashboardRequest(
        repo_root=Path("."),
        public_demo_dir=Path("examples/public_demo"),
    )

    assert request.host == "127.0.0.1"
    assert request.safety.read_only is True


def test_local_server_rejects_public_host() -> None:
    with pytest.raises(ValueError, match="localhost"):
        LocalDashboardRequest(
            repo_root=Path("."),
            public_demo_dir=Path("examples/public_demo"),
            host="0.0.0.0",
        )


def test_local_server_safety_rejects_command_execution() -> None:
    with pytest.raises(ValueError, match="safety boundary"):
        LocalDashboardSafety(executes_commands=True)


def test_local_server_route_rejects_traversal() -> None:
    with pytest.raises(ValueError, match="normalized"):
        LocalDashboardRoute(path="/../secret", title="Bad", description="Bad route")
