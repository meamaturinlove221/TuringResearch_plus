from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_neocortica_split_repos_are_active_targets_only() -> None:
    text = (ROOT / "upstream_watch" / "targets.yaml").read_text(encoding="utf-8")

    assert "Pthahnix/Neocortica-Scholar" in text
    assert "Pthahnix/Neocortica-Web" in text
    assert "Pthahnix/Neocortica-Session" in text
    assert "legacy_alias_only" in text
    assert "Pthahnix/Neocortica is not an active required scan target" in text


def test_git_handoff_contracts_are_design_only_not_public_mcp() -> None:
    for name in ["git_context_handoff.yaml", "pod_workflow.yaml"]:
        text = (ROOT / "contracts" / name).read_text(encoding="utf-8")
        assert "design_only_not_public_mcp" in text
        assert "\ntools:" not in text


def test_web_fetch_contract_was_promoted_after_sprint1_planning() -> None:
    text = (ROOT / "contracts" / "web_fetch_adapter.yaml").read_text(encoding="utf-8")

    assert "status: implemented_minimal" in text
    assert "implementation_status: implemented_minimal" in text
    assert "network_behavior: fake_mode_default" in text


def test_scholar_pipeline_contract_is_public_paper_namespace() -> None:
    text = (ROOT / "contracts" / "scholar_pipeline.yaml").read_text(encoding="utf-8")

    assert "paper.search_pipeline" in text
    assert "paper.reference_pipeline" in text
    assert "paper.three_pass_reading_plan" in text
    assert "no_network_by_default_live_optional" in text


def test_web_adapter_plan_states_not_implemented() -> None:
    text = (ROOT / "docs" / "web-fetch-adapter-plan.md").read_text(encoding="utf-8")

    assert "No live adapter implementation in this round" in text
    assert "No Apify call in this round" in text
    assert "not part of the current public MCP" in text
