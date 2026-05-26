from __future__ import annotations

import importlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "contracts" / "v1_public_api.yaml"

MODULES = {
    "core": ("turing_research_core", "beta"),
    "paper": ("turing_research_paper", "experimental"),
    "artifact": ("turing_research_artifact", "experimental"),
    "experiment": ("turing_research_experiment", "beta"),
    "dashboard": ("turing_research_dashboard", "experimental"),
    "plugins": ("turing_research_plugins", "experimental"),
    "cases": ("turing_research_cases", "experimental"),
}

ALLOWED_STABILITY = {"stable", "beta", "experimental", "internal", "deprecated"}

REQUIRED_DOCS = [
    ROOT / "docs" / "v1.0.0-public-api.md",
    ROOT / "docs" / "v1.0.0-api-stability-matrix.md",
    ROOT / "docs" / "v1.0.0-internal-api-list.md",
    ROOT / "docs" / "v1.0.0-deprecated-api-list.md",
]


def _contract_text() -> str:
    return CONTRACT.read_text(encoding="utf-8")


def _module_block(text: str, module_id: str) -> str:
    match = re.search(
        rf"  - id: {module_id}\n(?P<body>.*?)(?=\n  - id:|\ndeprecated_apis:)",
        text,
        re.DOTALL,
    )
    assert match, f"missing module block for {module_id}"
    return match.group("body")


def test_v1_public_api_contract_exists_and_lists_all_modules() -> None:
    text = _contract_text()

    assert "compatibility_namespace: turing_research_plus" in text
    for module_id, (namespace, stability) in MODULES.items():
        block = _module_block(text, module_id)
        assert f"namespace: {namespace}" in block
        assert f"stability: {stability}" in block
        assert "compatibility_namespace: turing_research_plus" in block
        assert "public_models:" in block
        assert "public_functions_tools:" in block
        assert "internal_only_modules:" in block


def test_v1_public_api_stability_values_are_known() -> None:
    text = _contract_text()
    values = re.findall(r"^\s+stability:\s+([a-z_]+)\s*$", text, re.MULTILINE)

    assert values
    assert set(values) <= ALLOWED_STABILITY


def test_no_experimental_module_is_marked_stable() -> None:
    text = _contract_text()

    for module_id in ["paper", "artifact", "dashboard", "plugins", "cases"]:
        block = _module_block(text, module_id)
        assert "stability: stable" not in block


def test_deprecated_apis_have_replacement_paths() -> None:
    text = _contract_text()

    assert "deprecated_apis:" in text
    assert "replacement:" in text
    assert "removal_before_v1: false" in text


def test_documented_public_api_namespaces_import() -> None:
    for namespace, expected_stability in MODULES.values():
        package = importlib.import_module(namespace)
        public_api = importlib.import_module(f"{namespace}.public_api")

        assert package.NAMESPACE == namespace
        assert public_api.NAMESPACE == namespace
        assert public_api.COMPATIBILITY_NAMESPACE == "turing_research_plus"
        assert public_api.STABILITY == expected_stability
        assert isinstance(public_api.__all__, list)


def test_v1_public_api_docs_exist() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_DOCS if not path.exists()]

    assert missing == []
