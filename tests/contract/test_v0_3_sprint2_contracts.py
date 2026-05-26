from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


CONTRACTS = [
    ROOT / "contracts" / "web_fetch_adapter.yaml",
    ROOT / "contracts" / "apify_adapter.yaml",
    ROOT / "contracts" / "related_work_positioning.yaml",
    ROOT / "contracts" / "skill_routing.yaml",
    ROOT / "contracts" / "vault_graph.yaml",
    ROOT / "contracts" / "ontology_sops.yaml",
]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_v0_3_sprint2_contracts_exist_and_are_minimal_implemented() -> None:
    missing = [path for path in CONTRACTS if not path.exists()]

    assert missing == []
    for path in CONTRACTS:
        text = _read(path)
        assert "project: TuringResearch Plus" in text
        assert "mcp_server: turingresearch-plus" in text
        assert "implementation_status: implemented_minimal" in text


def test_v0_3_sprint2_live_web_contracts_are_fake_default() -> None:
    web_contract = _read(ROOT / "contracts" / "web_fetch_adapter.yaml")
    apify_contract = _read(ROOT / "contracts" / "apify_adapter.yaml")

    assert "default_enabled: false" in web_contract
    assert "network_behavior: fake_mode_default" in web_contract
    assert "Do not bypass login or paywall." in web_contract
    assert "default_enabled: false" in apify_contract
    assert "APIFY_TOKEN is optional outside explicit live mode." in apify_contract


def test_v0_3_sprint2_review_contracts_require_conservative_outputs() -> None:
    related_contract = _read(ROOT / "contracts" / "related_work_positioning.yaml")
    vault_contract = _read(ROOT / "contracts" / "vault_graph.yaml")
    ontology_contract = _read(ROOT / "contracts" / "ontology_sops.yaml")
    skill_contract = _read(ROOT / "contracts" / "skill_routing.yaml")

    assert "Do not claim definitive novelty or no collision." in related_contract
    assert "Do not treat graph output as final truth." in vault_contract
    assert "Ontology exports require human review." in ontology_contract
    assert "Routing recommendations must not execute skills." in skill_contract
