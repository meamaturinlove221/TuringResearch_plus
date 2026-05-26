from __future__ import annotations

from pathlib import Path

from turing_research_plus.session_runtime import (
    PodWorkflowReplayRequest,
    PodWorkflowReplayStatus,
    render_pod_workflow_replay_report,
    run_pod_workflow_replay,
)

ROOT = Path(__file__).resolve().parents[2]
SESSION_FIXTURE = ROOT / "examples" / "session_runtime"


def test_pod_workflow_replay_runtime_fake_chain(tmp_path: Path) -> None:
    report = run_pod_workflow_replay(
        PodWorkflowReplayRequest(
            replay_id="pod-workflow-replay-fake",
            session_id="session-runtime-replay-fake",
            package_id="ctx-runtime-replay-fake",
            route_id="route-runtime-replay-fake",
            project_root=SESSION_FIXTURE / "preflight_fixture",
            preflight_context_source=Path("context"),
            preflight_output_dir=Path("output"),
            context_pack_source_dir=SESSION_FIXTURE / "context_pack_fixture" / "source",
            replay_workspace=tmp_path / "replay_workspace",
            fake_return_fixture_dir=SESSION_FIXTURE / "return_fixture",
        )
    )
    markdown = render_pod_workflow_replay_report(report)

    assert report.status == PodWorkflowReplayStatus.PASS_WITH_WARNINGS
    assert report.release_blocker is False
    assert report.chain == [
        "SessionPreflightRunner",
        "ContextPackBuilder",
        "FakeTransferRunner",
        "FakePodReturnFixture",
        "RemoteReturnVerifier",
        "ProposedEvidenceUpdateReport",
    ]
    assert report.live_ssh_enabled is False
    assert report.live_network_enabled is False
    assert report.remote_command_execution is False
    assert report.automatic_ledger_write is False
    assert report.proposed_updates_only is True
    assert report.requires_human_review is True
    assert report.preflight.remote_execution_enabled is False
    assert report.context_pack.remote_execution_allowed is False
    assert report.context_pack.live_network_allowed is False
    assert report.transfer.live_enabled is False
    assert report.transfer.remote_command_execution is False
    assert report.transfer.remote_delete is False
    assert report.transfer.secrets_logged is False
    assert report.fake_return.live_ssh_enabled is False
    assert report.fake_return.remote_command_execution is False
    assert report.return_verifier.auto_write_evidence_ledger is False
    assert report.return_verifier.proposed_updates_only is True
    assert report.proposed_evidence_update_report.updates[0].status == "proposed"
    assert "Live SSH enabled: `false`" in markdown
    assert "Remote command execution: `false`" in markdown
    assert "Automatic Evidence Ledger write: `false`" in markdown


def test_pod_workflow_replay_runtime_outputs_stay_public_safe(tmp_path: Path) -> None:
    report = run_pod_workflow_replay(
        PodWorkflowReplayRequest(
            replay_id="pod-workflow-replay-safety",
            session_id="session-runtime-replay-safety",
            package_id="ctx-runtime-replay-safety",
            route_id="route-runtime-replay-safety",
            project_root=SESSION_FIXTURE / "preflight_fixture",
            preflight_context_source=Path("context"),
            preflight_output_dir=Path("output"),
            context_pack_source_dir=SESSION_FIXTURE / "context_pack_fixture" / "source",
            replay_workspace=tmp_path / "safe_replay_workspace",
            fake_return_fixture_dir=SESSION_FIXTURE / "return_fixture",
        )
    )

    replay_root = tmp_path / "safe_replay_workspace"
    combined = "\n".join(
        path.read_text(encoding="utf-8", errors="replace")
        for path in replay_root.rglob("*")
        if path.is_file()
    ).lower()
    assert ".env" not in {item.path for item in report.transfer.selected_files}
    assert "local_project_links.yaml" not in combined
    assert "not-for-pack" not in combined
    assert "smpl" + "x" not in combined
    assert "sk-" not in combined
    assert "ghp_" not in combined
    assert "observed " + "success" not in combined
