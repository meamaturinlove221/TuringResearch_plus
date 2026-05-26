from __future__ import annotations

from pathlib import Path

from turing_research_plus.pod_lifecycle import PodContextLifecycle
from turing_research_plus.session_runtime import (
    SessionPreflightRequest,
    SessionPreflightStatus,
    render_session_preflight_report,
    run_session_preflight,
)


def _lifecycle(route_id: str = "route-session") -> PodContextLifecycle:
    return PodContextLifecycle(
        context_package_id="ctx-session",
        source_machine_label="local-review-machine",
        target_environment_label="linux-review-pod",
        route_id=route_id,
    )


def _safe_context(tmp_path: Path) -> Path:
    context = tmp_path / "context"
    context.mkdir()
    (context / "PROJECT_CONTEXT.md").write_text("Project context\n", encoding="utf-8")
    (context / "MEMORY.md").write_text("Memory summary\n", encoding="utf-8")
    (context / "ROUTE_SPEC.yaml").write_text("route: demo\n", encoding="utf-8")
    return context


def test_session_preflight_passes_with_platform_warning(tmp_path: Path) -> None:
    _safe_context(tmp_path)
    request = SessionPreflightRequest(
        session_id="session-demo",
        project_root=tmp_path,
        context_source=Path("context"),
        output_dir=Path("out"),
        lifecycle=_lifecycle(),
    )
    report = run_session_preflight(request)

    assert report.release_blocker is False
    assert report.status == SessionPreflightStatus.PASS_WITH_WARNINGS
    assert "windows-to-linux-unpack-requires-path-validation" in report.platform_warnings
    assert report.remote_execution_enabled is False
    assert report.checked_paths == ["MEMORY.md", "PROJECT_CONTEXT.md", "ROUTE_SPEC.yaml"]


def test_session_preflight_blocks_secret_like_context(tmp_path: Path) -> None:
    context = _safe_context(tmp_path)
    (context / "PROJECT_CONTEXT.md").write_text(
        "API_KEY=notarealbutlongsecret\n",
        encoding="utf-8",
    )
    request = SessionPreflightRequest(
        session_id="session-demo",
        project_root=tmp_path,
        context_source=Path("context"),
        output_dir=Path("out"),
        lifecycle=_lifecycle(),
    )
    report = run_session_preflight(request)

    assert report.status == SessionPreflightStatus.BLOCKED
    assert "possible-secret-value" in {finding.finding_id for finding in report.findings}


def test_session_preflight_blocks_shell_metacharacter_identifier(tmp_path: Path) -> None:
    _safe_context(tmp_path)
    request = SessionPreflightRequest(
        session_id="session-demo",
        project_root=tmp_path,
        context_source=Path("context"),
        output_dir=Path("out"),
        lifecycle=_lifecycle(route_id="route;rm"),
    )
    report = run_session_preflight(request)

    assert report.status == SessionPreflightStatus.BLOCKED
    assert any(check.check_id == "shell-metacharacter-risk" for check in report.environment_checks)


def test_render_session_preflight_report_contains_boundaries(tmp_path: Path) -> None:
    _safe_context(tmp_path)
    request = SessionPreflightRequest(
        session_id="session-demo",
        project_root=tmp_path,
        context_source=Path("context"),
        output_dir=Path("out"),
        lifecycle=_lifecycle(),
    )
    markdown = render_session_preflight_report(run_session_preflight(request))

    assert "Remote execution enabled: `false`" in markdown
    assert "Live network enabled: `false`" in markdown
    assert "Requires human review: `true`" in markdown
