from __future__ import annotations

import json
from pathlib import Path

from turing_research_plus.plugins.compat_report import PluginCompatibilityReport
from turing_research_plus.plugins.loading_report import PluginLoadingReport
from turing_research_plus.plugins.risk_report import PluginSandboxRiskReport

ROOT = Path(__file__).resolve().parents[2]


def test_v0_7_plugin_contract_files_exist_and_require_review() -> None:
    contracts = [
        ROOT / "contracts" / "trusted_local_plugin_loading.yaml",
        ROOT / "contracts" / "plugin_sandbox_policy.yaml",
        ROOT / "contracts" / "plugin_compatibility.yaml",
        ROOT / "contracts" / "mcp_plugin_registry.yaml",
        ROOT / "contracts" / "tool_capability_manifest.yaml",
    ]

    for path in contracts:
        text = path.read_text(encoding="utf-8")
        assert "requires_human_review: true" in text
        assert "network_behavior: no_network" in text or path.name in {
            "mcp_plugin_registry.yaml",
            "tool_capability_manifest.yaml",
        }


def test_v0_7_plugin_docs_state_runtime_boundaries() -> None:
    docs = "\n".join(
        [
            (ROOT / "docs" / "trusted-local-plugin-loading.md").read_text(encoding="utf-8"),
            (ROOT / "docs" / "plugin-sandbox-policy.md").read_text(encoding="utf-8"),
            (ROOT / "docs" / "plugin-compatibility-harness.md").read_text(
                encoding="utf-8"
            ),
            (ROOT / "docs" / "mcp-distribution-guide.md").read_text(encoding="utf-8"),
        ]
    )

    assert "No arbitrary third-party Python code execution" in docs
    assert "No OS-level sandbox is implemented" in docs
    assert "Compatibility does not enable plugins" in docs
    assert "plugin tools disabled by default" in docs
    assert "Tuling" + "Research" not in docs


def test_v0_7_plugin_report_models_are_review_only() -> None:
    loading_fields = set(PluginLoadingReport.model_fields)
    sandbox_fields = set(PluginSandboxRiskReport.model_fields)
    compatibility_fields = set(PluginCompatibilityReport.model_fields)

    assert "requires_human_review" in loading_fields
    assert "executes_code" in loading_fields
    assert "loads_entrypoint" in loading_fields
    assert "release_blocker" in sandbox_fields
    assert "requires_human_review" in sandbox_fields
    assert "executes_plugin_code" in compatibility_fields
    assert "starts_mcp_server" in compatibility_fields
    assert "enables_plugin" in compatibility_fields


def test_v0_7_mcp_config_is_safe_for_plugin_gate() -> None:
    config = json.loads((ROOT / ".mcp.example.json").read_text(encoding="utf-8"))
    server = config["mcpServers"]["turingresearch-plus"]
    env = server["env"]

    assert server["command"] == "turingresearch-plus-mcp"
    assert env["TURINGRESEARCH_MODE"] == "fake"
    assert env["TURINGRESEARCH_ENABLE_LIVE_TESTS"] == "0"
    assert env["TURINGRESEARCH_ENABLE_PLUGINS"] == "0"
    assert env["TURINGRESEARCH_ENABLE_PLUGIN_LIVE_MODE"] == "0"
    assert env["SEMANTIC_SCHOLAR_API_KEY"] == ""
    assert env["APIFY_TOKEN"] == ""
    assert env["OPENAI_API_KEY"] == ""
    assert env["GITHUB_TOKEN"] == ""
