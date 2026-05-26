from __future__ import annotations

from pathlib import Path

import pytest
from pydantic import ValidationError

from turing_research_plus.session_runtime.remote_dry_run_plan import (
    RemoteDryRunPlanRequest,
    RemoteDryRunStatus,
    build_remote_dry_run_plan,
    render_remote_dry_run_plan,
)


def test_remote_dry_run_plan_lists_transfer_and_exclusions(tmp_path: Path) -> None:
    source = _write_context_source(tmp_path)
    (source / ".env").write_text("not exported\n", encoding="utf-8")

    plan = build_remote_dry_run_plan(
        RemoteDryRunPlanRequest(
            plan_id="dry-run-demo",
            session_id="session-demo",
            package_id="ctx-demo",
            route_id="route-demo",
            project_root=tmp_path,
            context_source=source,
            output_dir=tmp_path / "out",
        )
    )

    assert plan.status == RemoteDryRunStatus.READY_WITH_WARNINGS
    assert "PROJECT_CONTEXT.md" in {item.path for item in plan.files_to_transfer}
    assert ".env" in {item.path for item in plan.forbidden_files_excluded}
    assert plan.remote_target_placeholder == "<user>@<host>:/reviewed/target/path"
    assert plan.return_artifact_requirements
    assert plan.ssh_enabled is False
    assert plan.sftp_enabled is False
    assert plan.remote_execution_enabled is False
    assert plan.dry_run_only is True


def test_remote_dry_run_plan_blocks_remote_execution_flags(tmp_path: Path) -> None:
    with pytest.raises(ValidationError):
        RemoteDryRunPlanRequest(
            plan_id="bad",
            session_id="session-demo",
            package_id="ctx-demo",
            route_id="route-demo",
            project_root=tmp_path,
            context_source=tmp_path,
            output_dir=tmp_path / "out",
            remote_execution_enabled=True,
        )


def test_render_remote_dry_run_plan_keeps_manual_boundaries(tmp_path: Path) -> None:
    source = _write_context_source(tmp_path)
    plan = build_remote_dry_run_plan(
        RemoteDryRunPlanRequest(
            plan_id="dry-run-demo",
            session_id="session-demo",
            package_id="ctx-demo",
            route_id="route-demo",
            project_root=tmp_path,
            context_source=source,
            output_dir=tmp_path / "out",
        )
    )

    text = render_remote_dry_run_plan(plan)

    assert "Optional Remote Dry-run Plan" in text
    assert "SSH enabled: `false`" in text
    assert "SFTP enabled: `false`" in text
    assert "Remote execution enabled: `false`" in text
    assert "MANUAL ONLY" in text


def _write_context_source(root: Path) -> Path:
    source = root / "source"
    source.mkdir()
    for name in [
        "PROJECT_CONTEXT.md",
        "MEMORY.md",
        "ROUTE_SPEC.yaml",
        "HARD_GATES.md",
        "ARTIFACT_REQUIREMENTS.md",
        "FAILURE_TAXONOMY.md",
    ]:
        (source / name).write_text(f"{name}\n", encoding="utf-8")
    return source
