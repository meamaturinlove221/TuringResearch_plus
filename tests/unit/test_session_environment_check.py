from __future__ import annotations

from pathlib import Path

from turing_research_plus.pod_lifecycle import PodContextLifecycle
from turing_research_plus.session_runtime import (
    SessionPreflightRequest,
    SessionPreflightStatus,
    build_session_lookup_record,
    run_session_environment_checks,
)


def _lifecycle(route_id: str = "route") -> PodContextLifecycle:
    return PodContextLifecycle(
        context_package_id="ctx",
        source_machine_label="local",
        target_environment_label="pod",
        route_id=route_id,
    )


def _safe_request(tmp_path: Path) -> SessionPreflightRequest:
    context = tmp_path / "context"
    context.mkdir(exist_ok=True)
    for name in ["PROJECT_CONTEXT.md", "MEMORY.md", "ROUTE_SPEC.yaml"]:
        (context / name).write_text("demo\n", encoding="utf-8")
    return SessionPreflightRequest(
        session_id="session",
        project_root=tmp_path,
        context_source=Path("context"),
        output_dir=Path("out"),
        lifecycle=_lifecycle(),
    )


def test_environment_checks_pass_safe_fixture(tmp_path: Path) -> None:
    request = _safe_request(tmp_path)
    lookup = build_session_lookup_record(request)
    checks = run_session_environment_checks(request, lookup)

    assert not any(check.release_blocker for check in checks)
    assert {check.check_id for check in checks} >= {
        "project-root-exists",
        "context-source-exists",
        "output-directory-safe",
        "remote-execution-disabled",
    }


def test_environment_checks_block_missing_project_root(tmp_path: Path) -> None:
    request = SessionPreflightRequest(
        session_id="session",
        project_root=tmp_path / "missing",
        context_source=Path("context"),
        output_dir=Path("out"),
        lifecycle=_lifecycle(),
    )
    lookup = build_session_lookup_record(request)
    checks = run_session_environment_checks(request, lookup)

    assert any(check.check_id == "project-root-exists" for check in checks)
    assert any(check.status == SessionPreflightStatus.BLOCKED for check in checks)


def test_environment_checks_block_unsafe_context_paths(tmp_path: Path) -> None:
    request = _safe_request(tmp_path)
    request.candidate_paths.append("../secret.txt")
    lookup = build_session_lookup_record(request)
    checks = run_session_environment_checks(request, lookup)

    assert any(check.check_id == "context-file-safe" for check in checks)
    assert any(check.release_blocker for check in checks)


def test_environment_checks_allow_raw_data_only_when_explicit(tmp_path: Path) -> None:
    request = _safe_request(tmp_path)
    request.candidate_paths.append("raw_data/demo.txt")
    blocked = run_session_environment_checks(request, build_session_lookup_record(request))

    allowed_request = _safe_request(tmp_path)
    allowed_request.allow_raw_data = True
    allowed_request.candidate_paths.append("raw_data/demo.txt")
    allowed = run_session_environment_checks(
        allowed_request,
        build_session_lookup_record(allowed_request),
    )

    assert any(check.release_blocker for check in blocked)
    assert not any(check.release_blocker for check in allowed)
