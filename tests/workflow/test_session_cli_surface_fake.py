from __future__ import annotations

from pathlib import Path

from turing_research_plus.session_runtime.cli import main

ROOT = Path(__file__).resolve().parents[2]
SESSION_FIXTURE = ROOT / "examples" / "session_runtime"


def test_session_cli_surface_fake_replay(tmp_path: Path, capsys) -> None:
    exit_code = main(
        [
            "session",
            "replay",
            "--project-root",
            str(SESSION_FIXTURE / "preflight_fixture"),
            "--preflight-context-source",
            "context",
            "--preflight-output-dir",
            "output",
            "--context-pack-source-dir",
            str(SESSION_FIXTURE / "context_pack_fixture" / "source"),
            "--replay-workspace",
            str(tmp_path / "replay"),
            "--fake-return-fixture-dir",
            str(SESSION_FIXTURE / "return_fixture"),
            "--output",
            str(tmp_path / "replay-report.md"),
        ]
    )
    captured = capsys.readouterr()
    written = (tmp_path / "replay-report.md").read_text(encoding="utf-8")

    assert exit_code == 0
    assert captured.err == ""
    assert "Session CLI Report: session replay" in captured.out
    assert "Remote command execution: `false`" in written
    assert "Automatic Evidence Ledger write: `false`" in written
    assert "ProposedEvidenceUpdateReport" in written


def test_session_cli_surface_report_command_has_boundaries(capsys) -> None:
    exit_code = main(["report"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "session preflight" in captured.out
    assert "session pack" in captured.out
    assert "session transfer --fake" in captured.out
    assert "live SSH disabled by default" in captured.out
    assert "no remote command execution" in captured.out
    assert "no automatic Evidence Ledger write" in captured.out
