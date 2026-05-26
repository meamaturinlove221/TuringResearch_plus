from __future__ import annotations

from pathlib import Path

from turing_research_plus.session_runtime import (
    ContextPackBuildRequest,
    SessionScriptExportRequest,
    TransferMode,
    TransferRunnerRequest,
    build_context_pack,
    build_human_confirmation_packet,
    copy_fake_pod_return_fixture,
    export_session_scripts,
    render_human_confirmation_packet,
    render_pod_workflow_replay_report,
    run_pod_workflow_replay,
    run_preflight_command,
    run_transfer,
    verify_return_package,
    write_human_confirmation_packet,
)
from turing_research_plus.session_runtime.workflow_replay import (
    PodWorkflowReplayRequest,
    PodWorkflowReplayStatus,
)

ROOT = Path(__file__).resolve().parents[2]
CONTEXT_SOURCE = ROOT / "examples" / "session_runtime" / "context_pack_fixture" / "source"
RETURN_FIXTURE = ROOT / "examples" / "session_runtime" / "return_fixture"


def test_session_production_parity_e2e_fake_chain(tmp_path: Path) -> None:
    cli_report = run_preflight_command(
        project_root=tmp_path,
        context_source=CONTEXT_SOURCE,
        output_dir=tmp_path / "preflight",
        session_id="e2e-session",
        package_id="e2e-context-pack",
        route_id="e2e-route",
    )
    context_pack = build_context_pack(
        ContextPackBuildRequest(
            package_id="e2e-context-pack",
            route_id="e2e-route",
            source_dir=CONTEXT_SOURCE,
            output_dir=tmp_path / "context_pack",
        )
    )
    scripts = export_session_scripts(
        SessionScriptExportRequest(output_dir=tmp_path / "scripts")
    )
    transfer = run_transfer(
        TransferRunnerRequest(
            transfer_id="e2e-fake-transfer",
            package_id="e2e-context-pack",
            source_dir=tmp_path / "context_pack",
            target=(tmp_path / "fake_transfer_target").as_posix(),
            mode=TransferMode.FAKE,
        )
    )
    fake_return = copy_fake_pod_return_fixture(
        return_id="e2e-fake-return",
        source_dir=RETURN_FIXTURE,
        target_dir=tmp_path / "fake_return",
    )
    verifier = verify_return_package(tmp_path / "fake_return", return_id="e2e-return")
    confirmation = build_human_confirmation_packet(
        verifier,
        confirmation_id="e2e-human-confirmation",
    )
    confirmation_path = write_human_confirmation_packet(
        confirmation,
        tmp_path / "CONFIRMATION_PACKET.md",
    )
    replay = run_pod_workflow_replay(
        PodWorkflowReplayRequest(
            replay_id="e2e-replay",
            session_id="e2e-session",
            package_id="e2e-context-pack",
            route_id="e2e-route",
            project_root=tmp_path,
            preflight_context_source=CONTEXT_SOURCE,
            preflight_output_dir=tmp_path / "preflight-replay",
            context_pack_source_dir=CONTEXT_SOURCE,
            replay_workspace=tmp_path / "replay",
            fake_return_fixture_dir=RETURN_FIXTURE,
        )
    )
    report_text = "\n".join(
        [
            "# Session Production Parity E2E Report",
            "",
            f"- CLI preflight command: `{cli_report.command}`",
            f"- Context pack files: `{len(context_pack.files)}`",
            f"- Script export status: `{scripts.status}`",
            f"- Fake transfer files: `{len(transfer.selected_files)}`",
            f"- Fake return copied files: `{len(fake_return.copied_files)}`",
            f"- Return verifier status: `{verifier.status}`",
            f"- Human confirmation decision: `{confirmation.decision.status}`",
            "",
            render_pod_workflow_replay_report(replay),
            render_human_confirmation_packet(confirmation),
        ]
    )

    assert cli_report.data["remote_execution_enabled"] is False
    assert cli_report.data["live_network_enabled"] is False
    assert context_pack.remote_execution_allowed is False
    assert context_pack.live_network_allowed is False
    assert scripts.scripts_executed is False
    assert transfer.remote_command_execution is False
    assert transfer.live_enabled is False
    assert fake_return.remote_command_execution is False
    assert verifier.auto_write_evidence_ledger is False
    assert confirmation.auto_write_evidence_ledger is False
    assert confirmation.remote_claims_trusted is False
    assert replay.status in {
        PodWorkflowReplayStatus.PASS,
        PodWorkflowReplayStatus.PASS_WITH_WARNINGS,
    }
    assert replay.release_blocker is False
    assert replay.live_ssh_enabled is False
    assert replay.remote_command_execution is False
    assert replay.automatic_ledger_write is False
    assert "Auto-write Evidence Ledger: `false`" in confirmation_path.read_text(
        encoding="utf-8"
    )
    assert "observed success" not in report_text.lower()


def test_checked_in_session_production_parity_e2e_demo_is_public_safe() -> None:
    demo = Path("examples/session_runtime/production_parity_e2e")

    assert (demo / "README.md").is_file()
    assert (demo / "SESSION_PRODUCTION_PARITY_E2E.md").is_file()

    text = "\n".join(path.read_text(encoding="utf-8") for path in demo.glob("*.md"))
    assert "fake/demo only" in text
    assert "Live steps disabled: `true`" in text
    assert "Remote command execution: `false`" in text
    assert "Automatic Evidence Ledger write: `false`" in text
    assert "D:/vggt" not in text
    assert "API_KEY=" not in text
    assert "TOKEN=" not in text
    assert "observed success" not in text.lower()
