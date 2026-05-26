from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

BETA_CONTRACTS = [
    "live_adapters.yaml",
    "semantic_scholar_live.yaml",
    "citation_graph.yaml",
    "collision_risk.yaml",
    "run_ingest.yaml",
    "handoff_bundle.yaml",
]

BETA_TOOLS = {
    "graph.citation_graph_expand",
    "research.collision_risk_detect",
    "research.run_ingest",
    "research.handoff_bundle_export",
    "research.handoff_bundle_import",
}


def test_beta_contract_files_exist_and_use_project_identity() -> None:
    for name in BETA_CONTRACTS:
        text = (ROOT / "contracts" / name).read_text(encoding="utf-8")
        assert "project: TuringResearch Plus" in text
        assert "mcp_server: turingresearch-plus" in text


def test_beta_public_tool_contracts_are_documented() -> None:
    docs = (ROOT / "docs" / "mcp-tools.md").read_text(encoding="utf-8")
    contract_text = "\n".join(
        (ROOT / "contracts" / name).read_text(encoding="utf-8")
        for name in BETA_CONTRACTS
    )

    for tool in BETA_TOOLS:
        assert f"tool_name: {tool}" in contract_text
        assert f"`{tool}`" in docs


def test_live_adapters_are_disabled_by_default() -> None:
    text = (ROOT / "contracts" / "live_adapters.yaml").read_text(encoding="utf-8")
    assert "default_enabled: false" in text
    assert "Default tests must use fake adapters only" in text
    assert "Live tests must be marked live or manual" in text


def test_handoff_contract_rejects_sync_scope() -> None:
    text = (ROOT / "contracts" / "handoff_bundle.yaml").read_text(encoding="utf-8")

    assert "offline only" in text
    assert "does not overwrite Evidence Ledger" in text
    assert "not NAS, SSH, GitHub artifact sync, or cloud storage" in text
