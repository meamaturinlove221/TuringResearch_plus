from __future__ import annotations

import json
from pathlib import Path

from turing_research_plus.campaigns import (
    build_campaign_execution_plan,
    build_campaign_strategy_book,
)
from turing_research_plus.experiment_execution import (
    build_experiment_execution_plan,
    render_experiment_execution_runbook,
)
from turing_research_plus.experiment_route.models import ExperimentRouteSpec
from turing_research_plus.pod_lifecycle import (
    PodContextLifecycle,
    build_session_context_pack_manifest,
    build_structured_return_manifest,
)
from turing_research_plus.scholar_pipeline import (
    build_scholar_fallback_policy,
    build_scholar_mcp_usage_guide,
    build_scholar_source_priority_plan,
    build_scholar_tool_list,
)
from turing_research_plus.stress_test import StressStatus, StressTestInput, run_stress_test
from turing_research_plus.vault_graph import (
    VaultGraph,
    build_wiki_vault_export,
    detect_ontology_gaps,
    run_ontology_sop_plan,
)
from turing_research_plus.vault_graph.edge_builder import build_edge
from turing_research_plus.vault_graph.models import VaultGraphEdgeType
from turing_research_plus.vault_graph.node_builder import build_concept_node
from turing_research_plus.web import (
    WebFetchingToolRequest,
    build_apify_usage_guide,
    run_web_fetching_tool,
    web_content_from_fetch_result,
)
from turing_research_plus.web.models import RetrievalStatus

ROOT = Path(__file__).resolve().parents[2]


def test_v1_2_full_fake_replay_reference_session_scholar_web_layers() -> None:
    lifecycle = PodContextLifecycle(
        context_package_id="ctx-v1-2-full-replay",
        source_machine_label="local-review-machine",
        target_environment_label="linux-review-pod",
        route_id="route-v1-2-full-replay",
    )
    session_pack = build_session_context_pack_manifest(
        lifecycle,
        ["PROJECT_CONTEXT.md", "MEMORY.md", "ROUTE_SPEC.yaml"],
    )
    return_manifest = build_structured_return_manifest(
        lifecycle,
        lifecycle.return_verification.required_files,
        return_package_id="return-v1-2-full-replay",
    )
    scholar_priority = build_scholar_source_priority_plan()
    scholar_tools = build_scholar_tool_list()
    scholar_mcp = build_scholar_mcp_usage_guide()
    scholar_fallback = build_scholar_fallback_policy()
    web_fetch = run_web_fetching_tool(
        WebFetchingToolRequest(url="https://example.com/public-demo")
    )
    web_content = web_content_from_fetch_result(web_fetch.fetch_result)
    apify = build_apify_usage_guide()
    mcp_config = json.loads((ROOT / ".mcp.example.json").read_text(encoding="utf-8"))
    mcp_env = mcp_config["mcpServers"]["turingresearch-plus"]["env"]

    assert session_pack.remote_execution_allowed is False
    assert session_pack.memory_bidirectional_sync is False
    assert return_manifest.auto_apply_evidence_updates is False
    assert return_manifest.requires_human_review is True
    assert scholar_priority.live_enabled_by_default is False
    assert scholar_tools.no_real_api_key_required is True
    assert scholar_mcp.live_tests_env == "TURINGRESEARCH_ENABLE_LIVE_TESTS=0"
    assert scholar_fallback.release_blocker is False
    assert web_fetch.fetch_result.retrieval_status == RetrievalStatus.DRY_RUN
    assert web_fetch.default_network is False
    assert web_content.requires_human_review is True
    assert apify.default_live_enabled is False
    assert mcp_env["TURINGRESEARCH_MODE"] == "fake"
    assert mcp_env["TURINGRESEARCH_ENABLE_LIVE_TESTS"] == "0"
    assert mcp_env["TURINGRESEARCH_ENABLE_WEB_LIVE"] == "0"
    assert mcp_env["TURINGRESEARCH_ENABLE_PLUGINS"] == "0"


def test_v1_2_full_fake_replay_yogsoth_layers() -> None:
    campaign_book = build_campaign_strategy_book()
    campaign_plan = build_campaign_execution_plan(
        "Stress-test a public demo route before release",
        provided_inputs=["claim list", "artifact list", "privacy boundary"],
    )
    graph = VaultGraph(
        graph_id="v1-2-full-replay-graph",
        nodes=[
            build_concept_node("north-star", "North Star", source_refs=["demo"]),
            build_concept_node("hypothesis", "Hypothesis", source_refs=["demo"]),
            build_concept_node("artifact", "Artifact", source_refs=["demo"]),
        ],
        edges=[
            build_edge("north-star", "hypothesis", VaultGraphEdgeType.BELONGS_TO),
            build_edge(
                "hypothesis",
                "artifact",
                VaultGraphEdgeType.SUPPORTS,
                source_refs=["demo"],
            ),
        ],
    )
    wiki_export = build_wiki_vault_export(graph)
    ontology_gaps = detect_ontology_gaps(graph)
    ontology_plan = run_ontology_sop_plan(
        graph,
        sop_names=["alias-resolution", "gap-detection", "ontology-export"],
        aliases=["North Star"],
    )
    stress_report = run_stress_test(
        StressTestInput(
            target_id="v1-2-full-replay",
            task_summary="demo only public replay with review boundary",
            evidence_refs=["evidence:demo"],
            artifact_refs=["artifact:index"],
            related_work_refs=["paper:a", "paper:b"],
            route_hard_gates=["claim experiment completion forbidden"],
            route_forbidden_actions=["claim experiment completion forbidden"],
            route_claims=["planned route only"],
            advisor_claims=["advisor note linked to evidence"],
            plugin_permissions=["read_manifest"],
        )
    )
    route = ExperimentRouteSpec(
        route_id="v1-2-full-replay-route",
        goal="Plan fake replay experiment handoff.",
        context="fake/demo route only; not executed",
        forbidden_actions=["claim experiment completion", "write observed result"],
        hard_gates=["no_promotion"],
        artifact_requirements=["run manifest", "artifact index"],
        stages=[
            {
                "id": "plan",
                "name": "Plan",
                "purpose": "Plan human-reviewed handoff.",
                "outputs": ["runbook"],
                "hard_gates": ["no_promotion"],
            }
        ],
    )
    execution_plan = build_experiment_execution_plan(route)
    runbook = render_experiment_execution_runbook(execution_plan)

    assert campaign_book.does_not_execute is True
    assert campaign_plan.does_not_execute is True
    assert campaign_plan.replaces_master_orchestrator is False
    assert wiki_export.requires_human_review is True
    assert wiki_export.graph_summary["nodes"] == 3
    assert ontology_gaps.requires_human_review is True
    assert ontology_plan.final_knowledge_graph_generated is False
    assert stress_report.status == StressStatus.PASS
    assert stress_report.multi_agent_runtime is False
    assert stress_report.network_required is False
    assert execution_plan.automatically_executes is False
    assert execution_plan.remote_execution is False
    assert execution_plan.modal_call is False
    assert execution_plan.gpu_call is False
    assert execution_plan.writes_observed_result is False
    assert "Writes observed result: `false`" in runbook


def test_v1_2_full_fake_replay_docs_catalog_and_aris_deferral() -> None:
    required_docs = [
        "docs/" + "neo" + "cortica-reference-parity-integration-report.md",
        "docs/" + "neo" + "cortica-parity-gate-report.md",
        "docs/yogsoth-parity-gate-report.md",
        "docs/turingresearch-research-catalog.md",
        "docs/aris-deferral-decision.md",
    ]
    for relative in required_docs:
        assert (ROOT / relative).exists(), relative

    catalog = (ROOT / "docs" / "turingresearch-research-catalog.md").read_text(
        encoding="utf-8"
    )
    aris = (ROOT / "docs" / "aris-deferral-decision.md").read_text(encoding="utf-8")
    gate = (ROOT / "docs" / "yogsoth-parity-gate-report.md").read_text(
        encoding="utf-8"
    )

    assert "Campaigns" in catalog
    assert "Vault graph" in catalog
    assert "Stress tests" in catalog
    assert "Experiment runbooks" in catalog
    assert "Advisor pack" in catalog
    assert "Public release" in catalog
    assert "not v1.2" in aris.lower()
    assert "v1.3" in aris
    assert "GO WITH REVIEW" in gate
    assert "No automatic experiment execution" in gate
