from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTRACTS = {
    "experiment_route": ROOT / "contracts" / "experiment_route.yaml",
    "hard_gates": ROOT / "contracts" / "hard_gates.yaml",
    "failure_taxonomy": ROOT / "contracts" / "failure_taxonomy.yaml",
    "paper_method_card": ROOT / "contracts" / "paper_method_card.yaml",
    "architecture_diagram": ROOT / "contracts" / "architecture_diagram.yaml",
}


def test_sprint2_contracts_exist_and_are_capsule_local() -> None:
    for path in CONTRACTS.values():
        text = path.read_text(encoding="utf-8")
        assert "project: TuringResearch Plus" in text
        assert "mcp_server: turingresearch-plus" in text
        assert "implementation_status: implemented_minimal" in text
        assert "public_api: false" in text
        assert "status: proposed_not_public_api" in text


def test_sprint2_contracts_cover_expected_outputs() -> None:
    expected_outputs = {
        "experiment_route": "output_model: ExperimentRouteSpec",
        "hard_gates": "output_model: HardGateValidationReport",
        "failure_taxonomy": "output_model: FailureAttributionReport",
        "paper_method_card": "output_model: PaperMethodCard",
        "architecture_diagram": "output_model: ArchitectureDiagramSpec",
    }

    for name, expected in expected_outputs.items():
        assert expected in CONTRACTS[name].read_text(encoding="utf-8")


def test_sprint2_contracts_keep_no_live_boundaries() -> None:
    for path in CONTRACTS.values():
        text = path.read_text(encoding="utf-8").lower()
        assert "network_behavior: none" in text
        assert "public_api: false" in text
