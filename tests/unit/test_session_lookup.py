from __future__ import annotations

from pathlib import Path

from turing_research_plus.pod_lifecycle import PodContextLifecycle
from turing_research_plus.session_runtime import (
    SessionPreflightRequest,
    build_session_lookup_record,
    discover_context_files,
)


def _request(tmp_path: Path) -> SessionPreflightRequest:
    context = tmp_path / "context"
    context.mkdir()
    (context / "PROJECT_CONTEXT.md").write_text("project\n", encoding="utf-8")
    (context / "MEMORY.md").write_text("memory\n", encoding="utf-8")
    (context / "ROUTE_SPEC.yaml").write_text("route: demo\n", encoding="utf-8")
    return SessionPreflightRequest(
        session_id="session",
        project_root=tmp_path,
        context_source=Path("context"),
        output_dir=Path("out"),
        lifecycle=PodContextLifecycle(
            context_package_id="ctx",
            source_machine_label="local",
            target_environment_label="pod",
            route_id="route",
        ),
    )


def test_discover_context_files_from_directory(tmp_path: Path) -> None:
    request = _request(tmp_path)
    files = discover_context_files(tmp_path / "context")

    assert files == ["MEMORY.md", "PROJECT_CONTEXT.md", "ROUTE_SPEC.yaml"]
    assert request.candidate_paths == []


def test_build_session_lookup_record_resolves_paths(tmp_path: Path) -> None:
    request = _request(tmp_path)
    lookup = build_session_lookup_record(request)

    assert lookup.session_id == "session"
    assert lookup.project_root == tmp_path.resolve().as_posix()
    assert lookup.context_source.endswith("/context")
    assert lookup.output_dir.endswith("/out")
    assert "PROJECT_CONTEXT.md" in lookup.context_files
