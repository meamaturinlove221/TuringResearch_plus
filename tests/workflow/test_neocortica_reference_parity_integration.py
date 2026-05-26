from __future__ import annotations

import json
import re
from pathlib import Path

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
from turing_research_plus.web import (
    WebFetchingToolRequest,
    build_apify_usage_guide,
    run_web_fetching_tool,
    web_content_from_fetch_result,
)
from turing_research_plus.web.models import RetrievalStatus

ROOT = Path(__file__).resolve().parents[2]


def test_neocortica_reference_parity_layers_share_safe_defaults() -> None:
    lifecycle = PodContextLifecycle(
        context_package_id="ctx-reference-parity",
        source_machine_label="local-review-machine",
        target_environment_label="linux-review-pod",
        route_id="route-reference-parity",
    )
    context_files = ["PROJECT_CONTEXT.md", "MEMORY.md", "ROUTE_SPEC.yaml"]
    session_pack = build_session_context_pack_manifest(lifecycle, context_files)
    return_manifest = build_structured_return_manifest(
        lifecycle,
        lifecycle.return_verification.required_files,
        return_package_id="return-reference-parity",
    )
    scholar_priority = build_scholar_source_priority_plan()
    scholar_tools = build_scholar_tool_list()
    scholar_mcp = build_scholar_mcp_usage_guide()
    scholar_fallback = build_scholar_fallback_policy()
    web_fetch = run_web_fetching_tool(
        WebFetchingToolRequest(url="https://example.com/public-page")
    )
    web_content = web_content_from_fetch_result(web_fetch.fetch_result)
    apify = build_apify_usage_guide()

    assert session_pack.release_blocker is False
    assert session_pack.remote_execution_allowed is False
    assert session_pack.memory_bidirectional_sync is False
    assert return_manifest.auto_apply_evidence_updates is False
    assert return_manifest.requires_human_review is True
    assert scholar_priority.live_enabled_by_default is False
    assert scholar_priority.paywall_bypass_allowed is False
    assert scholar_tools.no_real_api_key_required is True
    assert scholar_mcp.live_tests_env == "TURINGRESEARCH_ENABLE_LIVE_TESTS=0"
    assert scholar_fallback.release_blocker is False
    assert web_fetch.fetch_result.retrieval_status == RetrievalStatus.DRY_RUN
    assert web_fetch.default_network is False
    assert web_content.human_verified is False
    assert web_content.requires_human_review is True
    assert apify.default_live_enabled is False
    assert apify.release_blocker is False


def test_mcp_and_skill_sop_parity_docs_are_integrated() -> None:
    config = json.loads((ROOT / ".mcp.example.json").read_text(encoding="utf-8"))
    env = config["mcpServers"]["turingresearch-plus"]["env"]
    entry = (ROOT / ".agents" / "ENTRY.md").read_text(encoding="utf-8")
    routing = (ROOT / ".agents" / "ROUTING_TABLE.md").read_text(encoding="utf-8")
    skill_doc = (ROOT / "docs" / "skill-sop-parity.md").read_text(encoding="utf-8")
    mcp_doc = (ROOT / "docs" / "mcp-config-parity.md").read_text(encoding="utf-8")

    assert env["TURINGRESEARCH_MODE"] == "fake"
    assert env["TURINGRESEARCH_ENABLE_LIVE_TESTS"] == "0"
    assert env["TURINGRESEARCH_ENABLE_WEB_LIVE"] == "0"
    assert env["TURINGRESEARCH_ENABLE_PLUGINS"] == "0"
    for workflow in [
        "upstream watch",
        "campaign catalog",
        "scholar pipeline",
        "web fetch",
        "pod workflow",
        "artifact audit",
        "advisor pack",
        "release gate",
    ]:
        assert workflow in entry or workflow in routing
        assert workflow in skill_doc
    assert "Semantic Scholar" in mcp_doc
    assert "Apify" in mcp_doc
    assert "Web fetch" in mcp_doc


def test_neocortica_reference_parity_reports_no_secret_or_old_name() -> None:
    paths = [
        ROOT / "docs" / ("neo" + "cortica-session-parity.md"),
        ROOT / "docs" / ("neo" + "cortica-scholar-parity.md"),
        ROOT / "docs" / ("neo" + "cortica-web-parity.md"),
        ROOT / "docs" / "mcp-config-parity.md",
        ROOT / "docs" / "skill-sop-parity.md",
        ROOT / ".mcp.example.json",
    ]
    text = "\n".join(path.read_text(encoding="utf-8") for path in paths)
    token_like = re.compile(
        r"(sk-[A-Za-z0-9_-]{8,}|ghp_[A-Za-z0-9_]{8,}|xox[baprs]-[A-Za-z0-9-]+)"
    )

    assert "Tuling" + "Research" not in text
    assert "D:" + "/vggt" not in text
    assert "D:\\vggt" not in text
    assert "SMPL" + "X_" not in text
    assert not token_like.search(text)
    assert "remote command execution" in text
    assert "disabled by default" in text
