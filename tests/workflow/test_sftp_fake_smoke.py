from __future__ import annotations

import json
from pathlib import Path

from turing_research_plus.session_runtime.context_pack_builder import (
    ContextPackBuildRequest,
    build_context_pack,
)
from turing_research_plus.session_runtime.transfer_report import TransferStatus
from turing_research_plus.session_runtime.transfer_runner import (
    TransferRunnerRequest,
    run_transfer,
)

ROOT = Path(__file__).resolve().parents[2]
SMOKE = ROOT / "examples" / "session_runtime" / "sftp_live_smoke"
DOC = ROOT / "docs" / "sftp-optional-live-smoke.md"


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_sftp_fake_smoke_files_are_public_safe() -> None:
    data = json.loads(_text(SMOKE / "fake_sftp_smoke.json"))
    combined = "\n".join(
        _text(path)
        for path in [
            DOC,
            SMOKE / "README.md",
            SMOKE / "fake_sftp_smoke.json",
            SMOKE / "expected_fake_smoke_report.md",
            SMOKE / "live_skip_report.md",
        ]
    )

    assert data["mode"] == "fake"
    assert data["live_enabled"] is False
    assert data["requires_password"] is False
    assert data["requires_key_path"] is False
    assert data["remote_command_execution"] is False
    assert data["remote_delete"] is False
    assert data["transfer_target_explicit"] is True
    assert data["requires_human_review"] is True
    assert "no password" in combined
    assert "no key path" in combined
    assert "no remote command" in combined
    assert "no remote delete" in combined
    assert "transfer target explicit" in combined
    assert "password" + "=" not in combined.lower()
    assert "BEGIN OPENSSH " + "PRIVATE KEY" not in combined
    assert "D:" + "/vggt" not in combined
    assert "D:" + "\\vggt" not in combined
    assert "sk-" not in combined
    assert "ghp_" not in combined


def test_sftp_fake_smoke_runs_without_remote_connection(tmp_path: Path) -> None:
    data = json.loads(_text(SMOKE / "fake_sftp_smoke.json"))
    source = ROOT / data["source_dir"]
    pack_dir = tmp_path / "context_pack"
    target = tmp_path / "fake_target"

    build_context_pack(
        ContextPackBuildRequest(
            package_id=data["package_id"],
            route_id="route-sftp-fake-smoke",
            source_dir=source,
            output_dir=pack_dir,
        )
    )

    report = run_transfer(
        TransferRunnerRequest(
            transfer_id=data["transfer_id"],
            package_id=data["package_id"],
            source_dir=pack_dir,
            target=target.as_posix(),
        )
    )

    assert report.status == TransferStatus.TRANSFERRED
    assert report.live_enabled is False
    assert report.remote_command_execution is False
    assert report.remote_delete is False
    assert report.secrets_logged is False
    assert report.remote_write_scope == "explicit_transfer_target_only"
    assert report.requires_human_review is True
    assert target.exists()
    assert any(item.path == "PROJECT_CONTEXT.md" for item in report.selected_files)


def test_sftp_fake_smoke_docs_define_live_skip_policy() -> None:
    combined = "\n".join(
        [
            _text(DOC),
            _text(ROOT / "docs" / "sftp-live-optional-guide.md"),
            _text(ROOT / "docs" / "optional-live-safety-policy.md"),
            _text(SMOKE / "live_skip_report.md"),
        ]
    )

    assert "live skipped by default" in combined
    assert "TURINGRESEARCH_ENABLE_LIVE_TESTS=0" in combined
    assert "TURINGRESEARCH_ENABLE_SFTP_LIVE=0" in combined
    assert "TURINGRESEARCH_SFTP_CREDENTIAL=" in combined
    assert "TURINGRESEARCH_SFTP_TARGET=/explicit/reviewed/target" in combined
    assert "no remote command" in combined
    assert "no remote delete" in combined
    assert "transfer target explicit" in combined
    assert "no automatic Evidence Ledger write" in combined
