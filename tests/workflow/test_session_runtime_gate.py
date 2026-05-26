from __future__ import annotations

import json
import os
from pathlib import Path

from turing_research_plus.pod_lifecycle import PodContextLifecycle
from turing_research_plus.session_runtime import (
    ContextPackBuildRequest,
    PodWorkflowReplayRequest,
    PodWorkflowReplayStatus,
    ReturnVerifierStatus,
    SessionPreflightRequest,
    TransferMode,
    TransferRunnerRequest,
    TransferStatus,
    build_context_pack,
    run_session_preflight,
    run_transfer,
    verify_return_package,
)

ROOT = Path(__file__).resolve().parents[2]
SESSION_FIXTURE = ROOT / "examples" / "session_runtime"
DASHBOARD = SESSION_FIXTURE / "session_parity_dashboard.json"


def test_session_runtime_gate_fake_surfaces_work(tmp_path: Path) -> None:
    lifecycle = PodContextLifecycle(
        context_package_id="ctx-session-runtime-gate",
        source_machine_label="local-gate-machine",
        target_environment_label="fake-gate-pod",
        route_id="route-session-runtime-gate",
    )
    preflight = run_session_preflight(
        SessionPreflightRequest(
            session_id="session-runtime-gate",
            project_root=SESSION_FIXTURE / "preflight_fixture",
            context_source=Path("context"),
            output_dir=Path("output"),
            lifecycle=lifecycle,
        )
    )
    assert preflight.release_blocker is False
    assert preflight.remote_execution_enabled is False

    pack_dir = tmp_path / "context_pack"
    context_pack = build_context_pack(
        ContextPackBuildRequest(
            package_id="ctx-session-runtime-gate",
            route_id="route-session-runtime-gate",
            source_dir=SESSION_FIXTURE / "context_pack_fixture" / "source",
            output_dir=pack_dir,
        )
    )
    assert context_pack.release_blocker is False
    assert context_pack.remote_execution_allowed is False
    assert context_pack.live_network_allowed is False

    transfer = run_transfer(
        TransferRunnerRequest(
            transfer_id="tx-session-runtime-gate",
            package_id="ctx-session-runtime-gate",
            source_dir=pack_dir,
            target=(tmp_path / "fake_transfer_target").as_posix(),
            mode=TransferMode.FAKE,
        )
    )
    assert transfer.status == TransferStatus.TRANSFERRED
    assert transfer.live_enabled is False
    assert transfer.remote_command_execution is False
    assert transfer.remote_delete is False

    return_verifier = verify_return_package(
        SESSION_FIXTURE / "return_fixture",
        return_id="return-session-runtime-gate",
    )
    assert return_verifier.status == ReturnVerifierStatus.PASS
    assert return_verifier.auto_write_evidence_ledger is False
    assert return_verifier.proposed_updates_only is True


def test_session_runtime_gate_live_transfer_skipped_by_default(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.mkdir()
    (source / "PROJECT_CONTEXT.md").write_text("project\n", encoding="utf-8")
    os.environ.pop("TURINGRESEARCH_ENABLE_LIVE_TESTS", None)

    report = run_transfer(
        TransferRunnerRequest(
            transfer_id="tx-session-runtime-live-skip",
            package_id="ctx-session-runtime-live-skip",
            source_dir=source,
            target="/safe/context-pack",
            mode=TransferMode.SFTP,
            live_enabled=True,
            allow_remote_write=True,
        )
    )

    assert report.status == TransferStatus.SKIPPED_LIVE_DISABLED
    assert report.remote_command_execution is False
    assert report.remote_delete is False


def test_session_runtime_gate_full_workflow_replay_and_dashboard(tmp_path: Path) -> None:
    replay = run_pod_workflow_replay_for_gate(tmp_path)
    dashboard = json.loads(DASHBOARD.read_text(encoding="utf-8"))

    assert replay.status == PodWorkflowReplayStatus.PASS_WITH_WARNINGS
    assert replay.release_blocker is False
    assert replay.live_ssh_enabled is False
    assert replay.remote_command_execution is False
    assert replay.automatic_ledger_write is False

    capabilities = {item["id"]: item for item in dashboard["capabilities"]}
    assert capabilities["preflight"]["status"] == "fake-runnable"
    assert capabilities["context-pack"]["status"] == "fake-runnable"
    assert capabilities["fake-transfer"]["status"] == "fake-runnable"
    assert capabilities["optional-live-transfer"]["status"] == "deferred-live-opt-in"
    assert capabilities["return-verifier"]["status"] == "fake-runnable"
    assert capabilities["workflow-replay"]["status"] == "fake-runnable"

    deferred = {item["id"]: item for item in dashboard["deferred"]}
    assert deferred["remote-execution"]["status"] == "deferred"


def test_session_runtime_gate_public_safety_boundaries() -> None:
    combined = "\n".join(
        [
            DASHBOARD.read_text(encoding="utf-8"),
            (ROOT / "docs" / "session-runtime-gate-report.md").read_text(
                encoding="utf-8"
            ),
            (ROOT / "docs" / "session-runtime-go-no-go.md").read_text(
                encoding="utf-8"
            ),
            (ROOT / "docs" / "session-runtime-known-limitations.md").read_text(
                encoding="utf-8"
            ),
        ]
    )
    assert "no remote command execution" in combined
    assert "no automatic Evidence Ledger write" in combined
    assert "raw data" in combined

    forbidden = ["D:/vggt", "D:\\vggt", "local_project_links.yaml", "ghp_"]
    for marker in forbidden:
        assert marker not in combined
    assert "sk-" not in combined
    assert "observed " + "success" not in combined.lower()


def run_pod_workflow_replay_for_gate(tmp_path: Path):
    from turing_research_plus.session_runtime import run_pod_workflow_replay

    return run_pod_workflow_replay(
        PodWorkflowReplayRequest(
            replay_id="session-runtime-gate-replay",
            session_id="session-runtime-gate-replay",
            package_id="ctx-session-runtime-gate-replay",
            route_id="route-session-runtime-gate-replay",
            project_root=SESSION_FIXTURE / "preflight_fixture",
            preflight_context_source=Path("context"),
            preflight_output_dir=Path("output"),
            context_pack_source_dir=SESSION_FIXTURE / "context_pack_fixture" / "source",
            replay_workspace=tmp_path / "session_runtime_gate_replay",
            fake_return_fixture_dir=SESSION_FIXTURE / "return_fixture",
        )
    )
