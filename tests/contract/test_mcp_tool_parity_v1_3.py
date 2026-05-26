from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / ".mcp.example.json"

REQUIRED_TOOL_GROUPS = {
    "scholar",
    "web",
    "session",
    "campaign",
    "vault",
    "stress",
}

REQUIRED_TOOLS = {
    "scholar.paper_searching",
    "scholar.paper_content",
    "scholar.paper_reference",
    "scholar.paper_reading",
    "web.web_fetching",
    "web.web_content",
    "web.cache",
    "web.source_metadata",
    "web.apify_optional",
    "session.preflight",
    "session.context_pack",
    "session.fake_transfer",
    "session.return_verifier",
    "session.workflow_replay",
    "campaign.catalog",
    "campaign.preconditions",
    "campaign.execution_plan",
    "vault.wiki_export",
    "vault.backlinks",
    "vault.edge_quality",
    "vault.ontology_sop",
    "stress.scenario_catalog",
    "stress.runner",
    "stress.report",
}


def _server() -> dict[str, object]:
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    return config["mcpServers"]["turingresearch-plus"]


def _surface() -> dict[str, object]:
    return _server()["tool_surface_v1_3"]  # type: ignore[index]


def _tools() -> list[dict[str, object]]:
    return _surface()["tools"]  # type: ignore[index]


def test_v1_3_mcp_tool_surface_is_documentation_contract_only() -> None:
    surface = _surface()

    assert surface["status"] == "documentation-contract-only"
    assert surface["default_mode"] == "fake"
    assert surface["starts_mcp_server"] is False
    assert surface["live_disabled_by_default"] is True


def test_v1_3_mcp_tool_surface_covers_required_groups_and_tools() -> None:
    tools = _tools()
    names = {str(tool["name"]) for tool in tools}
    groups = {str(tool["group"]) for tool in tools}

    assert REQUIRED_TOOL_GROUPS <= groups
    assert REQUIRED_TOOLS <= names


def test_v1_3_mcp_tool_surface_keeps_tools_disabled_by_default() -> None:
    for tool in _tools():
        assert tool["mcp_enabled_by_default"] is False

    apify = next(tool for tool in _tools() if tool["name"] == "web.apify_optional")
    assert apify["status"] == "optional-live-disabled-by-default"
    assert apify["requires_live"] is True


def test_v1_3_mcp_tool_surface_docs_match_config() -> None:
    text = "\n".join(
        [
            (ROOT / "docs" / "mcp-tool-parity-v1.3.md").read_text(encoding="utf-8"),
            (ROOT / "docs" / "mcp-tool-surface-v1.3.md").read_text(encoding="utf-8"),
        ]
    )

    for group in REQUIRED_TOOL_GROUPS:
        assert group.capitalize() in text or group in text
    for tool_name in REQUIRED_TOOLS:
        assert tool_name in text

    assert "documentation-contract-only" in text
    assert "mcp_enabled_by_default: false" in text
    assert "does not start" in text.lower()


def test_v1_3_mcp_tool_surface_has_no_secrets_or_old_name() -> None:
    text = "\n".join(
        [
            CONFIG_PATH.read_text(encoding="utf-8"),
            (ROOT / "docs" / "mcp-tool-parity-v1.3.md").read_text(encoding="utf-8"),
            (ROOT / "docs" / "mcp-tool-surface-v1.3.md").read_text(encoding="utf-8"),
        ]
    )

    token_like = re.compile(
        r"(sk-[A-Za-z0-9_-]{8,}|ghp_[A-Za-z0-9_]{8,}|xox[baprs]-[A-Za-z0-9-]+)"
    )
    assert not token_like.search(text)
    assert "Tuling" + "Research" not in text
    assert "D:" + "/vggt" not in text
    assert "local_project_links.yaml" not in text
