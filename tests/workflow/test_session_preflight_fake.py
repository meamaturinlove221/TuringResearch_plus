from __future__ import annotations

from pathlib import Path

from turing_research_plus.pod_lifecycle import PodContextLifecycle
from turing_research_plus.session_runtime import (
    SessionPreflightRequest,
    SessionPreflightStatus,
    render_session_preflight_report,
    run_session_preflight,
)

ROOT = Path(__file__).resolve().parents[2]


def test_session_preflight_fake_fixture_is_local_review_only() -> None:
    fixture = ROOT / "examples" / "session_runtime" / "preflight_fixture"
    request = SessionPreflightRequest(
        session_id="session-preflight-fixture",
        project_root=fixture,
        context_source=Path("context"),
        output_dir=Path("output"),
        lifecycle=PodContextLifecycle(
            context_package_id="ctx-preflight-fixture",
            source_machine_label="local-review-machine",
            target_environment_label="linux-review-pod",
            route_id="route-preflight-fixture",
        ),
    )

    report = run_session_preflight(request)
    markdown = render_session_preflight_report(report)

    assert report.release_blocker is False
    assert report.status == SessionPreflightStatus.PASS_WITH_WARNINGS
    assert report.remote_execution_enabled is False
    assert report.live_network_enabled is False
    assert report.proposed_updates_only is True
    assert "PROJECT_CONTEXT.md" in report.checked_paths
    assert "Remote execution enabled: `false`" in markdown
