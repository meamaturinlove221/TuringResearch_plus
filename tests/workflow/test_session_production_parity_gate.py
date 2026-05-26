from __future__ import annotations

import json
from pathlib import Path

from turing_research_plus.session_runtime import (
    ArchiveMember,
    SessionScriptExportRequest,
    build_human_confirmation_packet,
    build_remote_dry_run_plan,
    export_session_scripts,
    run_report_command,
    validate_archive_members,
    verify_return_package,
)
from turing_research_plus.session_runtime.remote_dry_run_plan import (
    RemoteDryRunPlanRequest,
)

ROOT = Path(__file__).resolve().parents[2]
SESSION = ROOT / "examples" / "session_runtime"
CONTEXT_SOURCE = SESSION / "context_pack_fixture" / "source"
RETURN_FIXTURE = SESSION / "return_fixture"
DASHBOARD = SESSION / "session_production_dashboard_v2.json"


def test_session_production_gate_required_docs_exist() -> None:
    required = [
        "docs/session-cli-surface.md",
        "docs/session-shell-script-equivalent.md",
        "docs/cross-platform-archive-hardening.md",
        "docs/optional-remote-dry-run-plan.md",
        "docs/return-import-human-confirmation.md",
        "docs/session-production-parity-e2e.md",
        "docs/session-production-dashboard-v2.md",
        "docs/session-production-parity-gate-report.md",
        "docs/session-production-parity-go-no-go.md",
        "docs/session-production-parity-remaining-gaps.md",
    ]
    for path in required:
        assert (ROOT / path).is_file(), path


def test_session_production_gate_runtime_surfaces_pass(tmp_path: Path) -> None:
    cli = run_report_command()
    scripts = export_session_scripts(SessionScriptExportRequest(output_dir=tmp_path / "scripts"))
    archive = validate_archive_members(
        [
            ArchiveMember(path="PROJECT_CONTEXT.md"),
            ArchiveMember(path="../blocked.md"),
        ]
    )
    dry_run = build_remote_dry_run_plan(
        RemoteDryRunPlanRequest(
            plan_id="gate-dry-run",
            session_id="gate-session",
            package_id="gate-context-pack",
            route_id="gate-route",
            project_root=tmp_path,
            context_source=CONTEXT_SOURCE,
            output_dir=tmp_path / "out",
        )
    )
    verifier = verify_return_package(RETURN_FIXTURE, return_id="gate-return")
    confirmation = build_human_confirmation_packet(verifier)

    assert cli.data["command_count"] == 6
    assert cli.data["entrypoint"] == "turing_research_plus.session_runtime.cli:main"
    assert scripts.scripts_executed is False
    assert scripts.remote_execution_enabled is False
    assert archive.release_blocker is True
    assert "path-traversal" in {finding.finding_id for finding in archive.findings}
    assert dry_run.remote_execution_enabled is False
    assert dry_run.ssh_enabled is False
    assert dry_run.sftp_enabled is False
    assert dry_run.dry_run_only is True
    assert verifier.auto_write_evidence_ledger is False
    assert confirmation.auto_write_evidence_ledger is False
    assert confirmation.remote_claims_trusted is False


def test_session_production_gate_e2e_and_dashboard_v2_pass() -> None:
    e2e = (SESSION / "production_parity_e2e" / "SESSION_PRODUCTION_PARITY_E2E.md").read_text(
        encoding="utf-8"
    )
    dashboard = json.loads(DASHBOARD.read_text(encoding="utf-8"))

    assert "Live steps disabled: `true`" in e2e
    assert "Remote command execution: `false`" in e2e
    assert "Automatic Evidence Ledger write: `false`" in e2e
    assert dashboard["dashboard_id"] == "session-production-parity-v2"
    assert dashboard["production_parity"] is True
    assert dashboard["live_steps_disabled"] is True
    assert dashboard["no_remote_command_execution"] is True
    assert dashboard["no_automatic_observed_claim"] is True

    capabilities = {item["id"]: item for item in dashboard["capabilities"]}
    assert capabilities["preflight"]["production_status"] == "runnable"
    assert capabilities["script-export"]["production_status"] == "runnable"
    assert capabilities["return-verifier"]["production_status"] == "runnable"
    assert capabilities["human-confirmation"]["production_status"] == "runnable"
    assert capabilities["optional-live-transfer"]["production_status"] == "deferred-opt-in"
    assert capabilities["remote-execution"]["production_status"] == "disabled"


def test_session_production_gate_public_safety_boundaries() -> None:
    combined = "\n".join(
        [
            DASHBOARD.read_text(encoding="utf-8"),
            (ROOT / "docs" / "session-production-parity-gate-report.md").read_text(
                encoding="utf-8"
            ),
            (ROOT / "docs" / "session-production-parity-go-no-go.md").read_text(
                encoding="utf-8"
            ),
            (ROOT / "docs" / "session-production-parity-remaining-gaps.md").read_text(
                encoding="utf-8"
            ),
        ]
    )

    assert "no unsafe live default" in combined
    assert "remote execution disabled" in combined
    assert "automatic Evidence Ledger write" in combined
    forbidden = ["D:/vggt", "D:\\vggt", "local_project_links.yaml", "ghp_"]
    for marker in forbidden:
        assert marker not in combined
    assert "sk-" not in combined
    assert "observed " + "success" not in combined.lower()
