from __future__ import annotations

from pathlib import Path

from turing_research_plus.session_runtime.remote_dry_run_plan import (
    RemoteDryRunPlanRequest,
    RemoteDryRunStatus,
    build_remote_dry_run_plan,
    write_remote_dry_run_plan,
)


def test_optional_remote_dry_run_plan_fake_flow(tmp_path: Path) -> None:
    source = _write_context_source(tmp_path)
    (source / ".env").write_text("not exported\n", encoding="utf-8")

    plan = build_remote_dry_run_plan(
        RemoteDryRunPlanRequest(
            plan_id="dry-run-workflow",
            session_id="session-workflow",
            package_id="ctx-workflow",
            route_id="route-workflow",
            project_root=tmp_path,
            context_source=source,
            output_dir=tmp_path / "out",
            remote_target_placeholder="<manual-target-placeholder>",
        )
    )
    output = write_remote_dry_run_plan(plan, tmp_path / "REMOTE_DRY_RUN_PLAN.md")
    text = output.read_text(encoding="utf-8")

    assert plan.status == RemoteDryRunStatus.READY_WITH_WARNINGS
    assert "PROJECT_CONTEXT.md" in text
    assert "Forbidden Files Excluded" in text
    assert ".env" in text
    assert "SSH enabled: `false`" in text
    assert "SFTP enabled: `false`" in text
    assert "tmux enabled: `false`" in text
    assert "Modal enabled: `false`" in text
    assert "Automatic Evidence Ledger write: `false`" in text
    assert "MANUAL ONLY" in text


def test_checked_in_remote_dry_run_demo_is_public_safe() -> None:
    demo = Path("examples/session_runtime/remote_dry_run_plan")

    assert (demo / "README.md").is_file()
    assert (demo / "REMOTE_DRY_RUN_PLAN.md").is_file()

    text = "\n".join(path.read_text(encoding="utf-8") for path in demo.glob("*.md"))
    assert "fake/demo only" in text
    assert "SSH enabled: `false`" in text
    assert "SFTP enabled: `false`" in text
    assert "Remote execution enabled: `false`" in text
    assert "D:/vggt" not in text
    assert "API_KEY=" not in text
    assert "TOKEN=" not in text


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
