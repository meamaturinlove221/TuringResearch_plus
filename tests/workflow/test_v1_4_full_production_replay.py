from __future__ import annotations

import json
import re
from pathlib import Path

from turing_research_plus.scholar_pipeline import build_heavy_pdf_backend_slot
from turing_research_plus.session_runtime import (
    PodWorkflowReplayRequest,
    PodWorkflowReplayStatus,
    run_pod_workflow_replay,
    run_report_command,
)
from turing_research_plus.web_tools import WebCacheLiveStatus, build_web_cache_manifest_entry

ROOT = Path(__file__).resolve().parents[2]
SESSION_FIXTURE = ROOT / "examples" / "session_runtime"


def _read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def test_v1_4_full_production_replay_required_reports_exist() -> None:
    required = [
        "docs/session-production-parity-gate-report.md",
        "docs/scholar-production-parity-gate-report.md",
        "docs/web-production-parity-gate-report.md",
        "docs/yogsoth-production-parity-gate-report.md",
        "docs/v1.4.0-aris-still-deferred.md",
        "docs/v1.4.0-full-production-replay-report.md",
        "docs/v1.4.0-yogsoth-production-summary.md",
    ]

    for relative in required:
        assert (ROOT / relative).exists(), relative


def test_v1_4_full_production_replay_session_runtime_is_fake_default(
    tmp_path: Path,
) -> None:
    cli_report = run_report_command()
    replay = run_pod_workflow_replay(
        PodWorkflowReplayRequest(
            replay_id="v1-4-full-production-replay",
            session_id="v1-4-full-production-replay",
            package_id="ctx-v1-4-full-production-replay",
            route_id="route-v1-4-full-production-replay",
            project_root=SESSION_FIXTURE / "preflight_fixture",
            preflight_context_source=Path("context"),
            preflight_output_dir=Path("output"),
            context_pack_source_dir=SESSION_FIXTURE / "context_pack_fixture" / "source",
            replay_workspace=tmp_path / "full_production_replay",
            fake_return_fixture_dir=SESSION_FIXTURE / "return_fixture",
        )
    )
    dashboard = json.loads(
        (
            ROOT
            / "examples"
            / "session_runtime"
            / "session_production_dashboard_v2.json"
        ).read_text(encoding="utf-8")
    )

    assert cli_report.data["command_count"] == 6
    assert replay.status == PodWorkflowReplayStatus.PASS_WITH_WARNINGS
    assert replay.live_ssh_enabled is False
    assert replay.remote_command_execution is False
    assert replay.automatic_ledger_write is False
    assert dashboard["production_parity"] is True
    assert dashboard["live_steps_disabled"] is True
    assert dashboard["no_remote_command_execution"] is True


def test_v1_4_full_production_replay_scholar_and_web_are_fake_default() -> None:
    scholar_text = "\n".join(
        [
            _read("docs/scholar-production-parity-gate-report.md"),
            _read("docs/scholar-production-parity-go-no-go.md"),
        ]
    )
    web_text = "\n".join(
        [
            _read("docs/web-production-parity-gate-report.md"),
            _read("docs/web-production-parity-go-no-go.md"),
        ]
    )
    heavy_slot = build_heavy_pdf_backend_slot()
    cache_entry = build_web_cache_manifest_entry(
        source_url="https://example.com/replay?utm_source=gate",
        content="fake web cache content for v1.4 production replay",
    )

    assert "GO for v1.4 fake/default Scholar production parity" in scholar_text
    assert "no MinerU implementation" in scholar_text
    assert "no fake citation is marked as verified" in scholar_text
    assert heavy_slot.implementation_present is False
    assert heavy_slot.ocr_enabled is False
    assert heavy_slot.large_pdf_processing is False

    assert "GO for v1.4 fake/default Web production parity" in web_text
    assert "NO-GO for default live network" in web_text
    assert "no private scraping" in web_text
    assert cache_entry.live_status == WebCacheLiveStatus.FAKE
    assert cache_entry.network_used is False
    assert cache_entry.human_verified is False


def test_v1_4_full_production_replay_yogsoth_gate_is_complete() -> None:
    report = _read("docs/yogsoth-production-parity-gate-report.md")
    summary = _read("docs/v1.4.0-yogsoth-production-summary.md")
    combined = report + "\n" + summary

    required = [
        "campaign trace E2E",
        "research catalog E2E",
        "vault wiki E2E",
        "ontology E2E",
        "stress/convergence E2E",
        "experiment runbook E2E",
        "No automatic experiment execution",
        "No fake result observed",
        "GO WITH REVIEW",
    ]
    for term in required:
        assert term in combined

    assert "autonomous research runtime" in combined
    assert "No default network" in combined
    assert "No Evidence Ledger mutation" in combined


def test_v1_4_full_production_replay_keeps_aris_deferred() -> None:
    aris = _read("docs/v1.4.0-aris-still-deferred.md").lower()
    replay = _read("docs/v1.4.0-full-production-replay-report.md").lower()
    combined = aris + "\n" + replay

    required = [
        "aris remains valuable as a future reference",
        "not part of the",
        "v1.4 implementation line",
        "cross-model review",
        "proof-checker",
        "meta-optimize",
        "paper-claim-audit",
        "aris deferred",
    ]
    for term in required:
        assert term in combined

    assert "aris runtime enabled" not in combined


def test_v1_4_full_production_replay_has_no_unsafe_live_default() -> None:
    combined = "\n".join(
        [
            _read("docs/v1.4.0-full-production-replay-report.md"),
            _read("docs/session-production-parity-gate-report.md"),
            _read("docs/scholar-production-parity-gate-report.md"),
            _read("docs/web-production-parity-gate-report.md"),
            _read("docs/yogsoth-production-parity-gate-report.md"),
            _read("docs/v1.4.0-aris-still-deferred.md"),
        ]
    )
    lowered = combined.lower()

    required_boundaries = [
        "no unsafe live default",
        "no default network",
        "no remote command execution",
        "no automatic experiment execution",
        "no evidence ledger mutation",
        "human review required",
    ]
    for boundary in required_boundaries:
        assert boundary in lowered

    blocked_enabled_phrases = [
        "live ssh enabled by default",
        "default network enabled",
        "remote execution enabled: `true`",
        "automatic experiment execution enabled",
        "aris runtime enabled",
        "automatic evidence ledger mutation enabled",
    ]
    for phrase in blocked_enabled_phrases:
        assert phrase not in lowered

    token_like = re.compile(
        r"(sk-[A-Za-z0-9_-]{8,}|ghp_[A-Za-z0-9_]{8,}|xox[baprs]-[A-Za-z0-9-]+)"
    )
    assert not token_like.search(combined)
    assert ("Tuling" + "Research") not in combined
    assert ("D:" + "/vggt") not in combined
    assert ("local_project_links" + ".yaml") not in combined
    assert ('"status": "' + 'observed"') not in combined
