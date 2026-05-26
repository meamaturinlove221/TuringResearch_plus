from __future__ import annotations

from pathlib import Path

from turing_research_plus.session_runtime.fake_transfer import run_fake_transfer
from turing_research_plus.session_runtime.transfer_report import TransferStatus


def test_fake_transfer_copies_safe_files_and_omits_unsafe(tmp_path: Path) -> None:
    source = tmp_path / "source"
    target = tmp_path / "target"
    source.mkdir()
    (source / "PROJECT_CONTEXT.md").write_text("project\n", encoding="utf-8")
    (source / "SHA256SUMS.txt").write_text("placeholder\n", encoding="utf-8")
    (source / ".env").write_text("PLACEHOLDER=secret\n", encoding="utf-8")

    report = run_fake_transfer(
        transfer_id="tx-fake",
        package_id="ctx-fake",
        source_dir=source,
        target_dir=target,
    )

    assert report.status == TransferStatus.TRANSFERRED
    assert (target / "PROJECT_CONTEXT.md").exists()
    assert not (target / ".env").exists()
    assert any(item.path == ".env" for item in report.omitted_files)
    assert report.live_enabled is False
    assert report.remote_command_execution is False


def test_fake_transfer_blocks_missing_source(tmp_path: Path) -> None:
    report = run_fake_transfer(
        transfer_id="tx-missing",
        package_id="ctx",
        source_dir=tmp_path / "missing",
        target_dir=tmp_path / "target",
    )

    assert report.status == TransferStatus.BLOCKED
    assert "source directory is missing" in report.errors
