from __future__ import annotations

from pathlib import Path

import pytest

from turing_research_plus.pod_lifecycle import PodContextLifecycle
from turing_research_plus.session_runtime import (
    SessionLookupRecord,
    SessionPreflightReport,
    SessionPreflightRequest,
    SessionPreflightStatus,
)


def _lifecycle() -> PodContextLifecycle:
    return PodContextLifecycle(
        context_package_id="ctx-session-runtime",
        source_machine_label="local-review-machine",
        target_environment_label="linux-review-pod",
        route_id="route-session-runtime",
    )


def test_session_preflight_request_rejects_remote_execution() -> None:
    with pytest.raises(ValueError, match="remote execution"):
        SessionPreflightRequest(
            session_id="session",
            project_root=Path("."),
            context_source=Path("context"),
            output_dir=Path("out"),
            lifecycle=_lifecycle(),
            remote_execution_enabled=True,
        )


def test_session_preflight_request_rejects_live_networking() -> None:
    with pytest.raises(ValueError, match="live networking"):
        SessionPreflightRequest(
            session_id="session",
            project_root=Path("."),
            context_source=Path("context"),
            output_dir=Path("out"),
            lifecycle=_lifecycle(),
            live_network_enabled=True,
        )


def test_session_preflight_report_boundary_defaults() -> None:
    report = SessionPreflightReport(
        session_id="session",
        context_package_id="ctx",
        route_id="route",
        status=SessionPreflightStatus.PASS,
        lookup=SessionLookupRecord(
            session_id="session",
            project_root=".",
            context_source="context",
            output_dir="out",
        ),
    )

    assert report.release_blocker is False
    assert report.remote_execution_enabled is False
    assert report.live_network_enabled is False
    assert report.proposed_updates_only is True
    assert report.requires_human_review is True
