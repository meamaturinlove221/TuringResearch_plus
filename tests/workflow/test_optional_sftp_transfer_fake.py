from __future__ import annotations

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
FIXTURE = ROOT / "examples" / "session_runtime" / "context_pack_fixture" / "source"


def test_optional_sftp_transfer_fake_workflow(tmp_path: Path) -> None:
    pack_dir = tmp_path / "context_pack"
    build_context_pack(
        ContextPackBuildRequest(
            package_id="ctx-transfer-fake",
            route_id="route-transfer-fake",
            source_dir=FIXTURE,
            output_dir=pack_dir,
        )
    )

    report = run_transfer(
        TransferRunnerRequest(
            transfer_id="tx-transfer-fake",
            package_id="ctx-transfer-fake",
            source_dir=pack_dir,
            target=(tmp_path / "fake_target").as_posix(),
        )
    )

    assert report.status == TransferStatus.TRANSFERRED
    assert report.live_enabled is False
    assert report.remote_command_execution is False
    assert report.remote_delete is False
    assert report.secrets_logged is False
    assert report.requires_human_review is True
    assert any(item.path == "PROJECT_CONTEXT.md" for item in report.selected_files)
    combined = "\n".join(
        path.read_text(encoding="utf-8", errors="replace")
        for path in (tmp_path / "fake_target").iterdir()
        if path.is_file()
    )
    assert "not-for-pack" not in combined
    assert "observed " + "success" not in combined.lower()
