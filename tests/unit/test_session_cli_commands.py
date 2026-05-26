from __future__ import annotations

from pathlib import Path

import pytest

from turing_research_plus.session_runtime.cli_report import SessionCLIStatus
from turing_research_plus.session_runtime.commands import (
    render_cli_report,
    run_pack_command,
    run_preflight_command,
    run_replay_command,
    run_report_command,
    run_transfer_command,
    run_verify_return_command,
)

ROOT = Path(__file__).resolve().parents[2]
SESSION_FIXTURE = ROOT / "examples" / "session_runtime"


def test_session_cli_preflight_command_is_fake_default(tmp_path: Path) -> None:
    report = run_preflight_command(
        project_root=SESSION_FIXTURE / "preflight_fixture",
        context_source=Path("context"),
        output_dir=Path("output"),
        output=tmp_path / "preflight.md",
    )
    markdown = render_cli_report(report)

    assert report.status == SessionCLIStatus.PASS_WITH_WARNINGS
    assert report.live_ssh_enabled is False
    assert report.live_network_enabled is False
    assert report.remote_command_execution is False
    assert report.automatic_evidence_ledger_write is False
    assert (tmp_path / "preflight.md").exists()
    assert "Remote command execution: `false`" in markdown


def test_session_cli_pack_command_builds_safe_context_pack(tmp_path: Path) -> None:
    report = run_pack_command(
        source_dir=SESSION_FIXTURE / "context_pack_fixture" / "source",
        output_dir=tmp_path / "pack",
    )

    assert report.status == SessionCLIStatus.PASS_WITH_WARNINGS
    assert report.release_blocker is False
    assert (tmp_path / "pack" / "PROJECT_CONTEXT.md").exists()
    assert (tmp_path / "pack" / "SHA256SUMS.txt").exists()
    assert report.data["omitted_files"] != 0


def test_session_cli_transfer_requires_fake_mode(tmp_path: Path) -> None:
    pack_dir = tmp_path / "pack"
    pack_dir.mkdir()
    (pack_dir / "PROJECT_CONTEXT.md").write_text("context\n", encoding="utf-8")

    report = run_transfer_command(
        source_dir=pack_dir,
        target_dir=tmp_path / "target",
        fake=True,
    )

    assert report.status == SessionCLIStatus.PASS
    assert report.data["mode"] == "fake"
    assert report.data["selected_files"] == 1
    assert (tmp_path / "target" / "PROJECT_CONTEXT.md").exists()

    with pytest.raises(ValueError, match="only supports --fake"):
        run_transfer_command(
            source_dir=pack_dir,
            target_dir=tmp_path / "target2",
            fake=False,
        )


def test_session_cli_verify_return_command_proposed_only() -> None:
    report = run_verify_return_command(return_dir=SESSION_FIXTURE / "return_fixture")

    assert report.status == SessionCLIStatus.PASS
    assert report.automatic_evidence_ledger_write is False
    assert report.proposed_updates_only is True
    assert report.data["proposed_updates"] == 1


def test_session_cli_replay_command_runs_full_fake_chain(tmp_path: Path) -> None:
    report = run_replay_command(
        project_root=SESSION_FIXTURE / "preflight_fixture",
        preflight_context_source=Path("context"),
        preflight_output_dir=Path("output"),
        context_pack_source_dir=SESSION_FIXTURE / "context_pack_fixture" / "source",
        replay_workspace=tmp_path / "replay",
        fake_return_fixture_dir=SESSION_FIXTURE / "return_fixture",
    )
    markdown = render_cli_report(report)

    assert report.status == SessionCLIStatus.PASS_WITH_WARNINGS
    assert report.release_blocker is False
    assert report.data["chain_length"] == 6
    assert "Automatic Evidence Ledger write: `false`" in markdown


def test_session_cli_report_command_lists_surface() -> None:
    report = run_report_command()
    markdown = render_cli_report(report)

    assert report.status == SessionCLIStatus.PASS
    assert report.data["command_count"] == 6
    assert "`session transfer --fake`" in markdown
    assert "live SSH disabled by default" in markdown
