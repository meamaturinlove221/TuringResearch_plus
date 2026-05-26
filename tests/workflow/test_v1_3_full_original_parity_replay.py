from __future__ import annotations

import json
from pathlib import Path

from turing_research_plus.artifacts.models import EvidenceRef
from turing_research_plus.campaigns import build_campaign_execution_trace
from turing_research_plus.convergence import (
    CandidateKind,
    ConvergenceCandidate,
    build_convergence_decision_report,
)
from turing_research_plus.scholar_tools import build_scholar_full_tool_surface
from turing_research_plus.session_runtime import (
    PodWorkflowReplayRequest,
    PodWorkflowReplayStatus,
    run_pod_workflow_replay,
)
from turing_research_plus.stress_test import build_stress_scenario_library
from turing_research_plus.web_tools import build_web_full_tool_surface

ROOT = Path(__file__).resolve().parents[2]
SESSION_FIXTURE = ROOT / "examples" / "session_runtime"


def evidence(source_id: str) -> EvidenceRef:
    return EvidenceRef(
        source_id=source_id,
        locator="section-1",
        quote="Fake evidence for v1.3 original parity replay.",
    )


def candidate(candidate_id: str, feasibility: float, novelty: float) -> ConvergenceCandidate:
    return ConvergenceCandidate(
        candidate_id=candidate_id,
        kind=CandidateKind.IMPLEMENTATION_VARIANT,
        title=f"Route {candidate_id}",
        mechanism="local full original parity replay",
        expected_gain="Improve v1.3 release readiness.",
        feasibility=feasibility,
        novelty=novelty,
        risk="medium",
        required_resources=["human review"],
        evidence_refs=[evidence(candidate_id)],
    )


def test_v1_3_full_original_parity_replay_fake_runtime(tmp_path: Path) -> None:
    replay = run_pod_workflow_replay(
        PodWorkflowReplayRequest(
            replay_id="v1-3-full-original-parity",
            session_id="v1-3-full-original-parity",
            package_id="ctx-v1-3-full-original-parity",
            route_id="route-v1-3-full-original-parity",
            project_root=SESSION_FIXTURE / "preflight_fixture",
            preflight_context_source=Path("context"),
            preflight_output_dir=Path("output"),
            context_pack_source_dir=SESSION_FIXTURE / "context_pack_fixture" / "source",
            replay_workspace=tmp_path / "full_original_parity_replay",
            fake_return_fixture_dir=SESSION_FIXTURE / "return_fixture",
        )
    )
    scholar_surface = build_scholar_full_tool_surface()
    web_surface = build_web_full_tool_surface()
    campaign_trace = build_campaign_execution_trace(
        "stress test unsupported route",
        provided_inputs=["candidate claim or release surface"],
    )
    stress_library = build_stress_scenario_library()
    convergence = build_convergence_decision_report(
        [
            candidate("session-runtime-first", 0.9, 0.76),
            candidate("dashboard-first", 0.72, 0.8),
        ],
        report_id="v1-3-full-original-parity",
    )

    assert replay.status == PodWorkflowReplayStatus.PASS_WITH_WARNINGS
    assert replay.live_ssh_enabled is False
    assert replay.remote_command_execution is False
    assert replay.automatic_ledger_write is False
    assert scholar_surface.release_blocker is False
    assert web_surface.release_blocker is False
    assert campaign_trace.fake_trace is True
    assert campaign_trace.ready_for_execution is False
    assert "missing_evidence" in stress_library.by_id()
    assert "advisor_report_overclaim" in stress_library.by_id()
    assert convergence.final_recommendation == "session-runtime-first"


def test_v1_3_full_original_parity_replay_mcp_and_skill_surfaces() -> None:
    config = json.loads((ROOT / ".mcp.example.json").read_text(encoding="utf-8"))
    surface = config["mcpServers"]["turingresearch-plus"]["tool_surface_v1_3"]
    tool_names = {tool["name"] for tool in surface["tools"]}
    routing = (ROOT / ".agents" / "ROUTING_TABLE.md").read_text(encoding="utf-8")

    assert surface["status"] == "documentation-contract-only"
    assert surface["starts_mcp_server"] is False
    assert all(tool["mcp_enabled_by_default"] is False for tool in surface["tools"])
    assert {
        "scholar.paper_searching",
        "web.web_fetching",
        "session.workflow_replay",
        "campaign.catalog",
        "vault.wiki_export",
        "stress.runner",
    } <= tool_names
    assert "master orchestrator" in routing
    assert "campaign catalog" in routing
    assert "scholar pipeline" in routing
    assert "pod workflow" in routing


def test_v1_3_full_original_parity_replay_docs_exist_and_cover_all_surfaces() -> None:
    required_paths = [
        ROOT / "docs" / "session-runtime-gate-report.md",
        ROOT / "docs" / "scholar-web-parity-gate-report.md",
        ROOT / "docs" / "mcp-tool-parity-v1.3.md",
        ROOT / "docs" / "skill-sop-parity.md",
        ROOT / "docs" / "campaign-execution-trace.md",
        ROOT / "docs" / "vault-wiki-export-demo.md",
        ROOT / "docs" / "ontology-runbook-demo.md",
        ROOT / "docs" / "stress-scenario-library.md",
        ROOT / "docs" / "convergence-decision-report.md",
        ROOT / "docs" / "v1.3.0-aris-deferral-reconfirm.md",
        ROOT / "docs" / "v1.3.0-full-original-parity-replay-report.md",
    ]
    for path in required_paths:
        assert path.exists(), path

    report = (ROOT / "docs" / "v1.3.0-full-original-parity-replay-report.md").read_text(
        encoding="utf-8"
    )
    for term in [
        "session runtime",
        "scholar tools",
        "web tools",
        "MCP parity",
        "skill SOP parity",
        "campaign trace",
        "vault wiki demo",
        "ontology demo",
        "stress library",
        "convergence report",
        "ARIS deferred",
    ]:
        assert term in report


def test_v1_3_full_original_parity_replay_keeps_aris_deferred() -> None:
    text = "\n".join(
        [
            (ROOT / "docs" / "v1.3.0-aris-deferral-reconfirm.md").read_text(
                encoding="utf-8"
            ),
            (ROOT / "docs" / "aris-implementation-blocklist-v1.3.md").read_text(
                encoding="utf-8"
            ),
            (ROOT / "docs" / "v1.3.0-full-original-parity-replay-report.md").read_text(
                encoding="utf-8"
            ),
        ]
    ).lower()

    assert "future reference" in text
    assert "deferred" in text
    assert "v1.3 does not implement" in text
    assert "cross-model review" in text
    assert "proof-checker" in text
    assert "meta-optimize" in text
    assert "paper-claim-audit" in text


def test_v1_3_full_original_parity_replay_public_safety() -> None:
    paths = [
        ROOT / "docs" / "v1.3.0-full-original-parity-replay-report.md",
        ROOT / "docs" / "session-runtime-gate-report.md",
        ROOT / "docs" / "scholar-web-parity-gate-report.md",
        ROOT / "docs" / "yogsoth-full-parity-gate-report.md",
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in paths)

    forbidden = ["D:/vggt", "D:\\vggt", "local_project_links.yaml", "ghp_", "sk-"]
    for marker in forbidden:
        assert marker not in combined

    assert "Tuling" + "Research" not in combined
    assert "no automatic Evidence Ledger mutation" in combined
    assert "no fake/demo result promotion" in combined
    assert "observed " + "success" not in combined.lower()
